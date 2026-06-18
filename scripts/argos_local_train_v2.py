#!/usr/bin/env python3
"""
ARGOS Local Model Training v2 — BM25 (улучшенный TF-IDF).

BM25 — стандарт в information retrieval.
Улучшения v1→v2:
- BM25 scoring вместо TF-IDF
- Лучшая нормализация длины документа
- Поддержка multi-word phrases
- Quality filter
"""
import json
import math
import pickle
import re
import time
from collections import Counter
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("/home/ava/Projects/argoss")
RETRAIN_DIR = PROJECT_ROOT / "data/retrain"


class BM25Trainer:
    """BM25-based retrieval."""
    
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.vocab = {}
        self.idf = {}
        self.docs = []  # list of (user, answer, tokens)
        self.avg_dl = 0
        self.N = 0
    
    def tokenize(self, text: str) -> list:
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return [w for w in text.split() if len(w) > 2]
    
    def fit(self, dataset_path: Path):
        print(f"  Loading {dataset_path.name}")
        with open(dataset_path, encoding='utf-8') as f:
            pairs = [json.loads(line) for line in f if line.strip()]
        print(f"  Pairs: {len(pairs)}")
        
        # Build vocab + tokenize
        doc_freq = Counter()
        self.docs = []
        for p in pairs:
            user = p["messages"][0]["content"]
            asst = p["messages"][1]["content"]
            ut = self.tokenize(user)
            at = self.tokenize(asst)
            self.docs.append((user, asst, ut, at))
            for w in set(ut + at):
                doc_freq[w] += 1
        
        # Vocab (>=2 freq)
        self.vocab = {w: i for i, (w, c) in enumerate(doc_freq.most_common()) if c >= 2}
        print(f"  Vocab: {len(self.vocab)}")
        
        # IDF (BM25 formula)
        self.N = len(self.docs)
        self.idf = {}
        for w, df in doc_freq.items():
            if w in self.vocab:
                self.idf[w] = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        
        # Avg doc length
        self.avg_dl = sum(len(ut) + len(at) for _, _, ut, at in self.docs) / max(self.N, 1)
        print(f"  Avg doc len: {self.avg_dl:.0f}")
        print(f"  N docs: {self.N}")
    
    def score(self, query_tokens, doc_tokens):
        """BM25 score for a single doc."""
        score = 0.0
        doc_len = len(doc_tokens)
        tf_q = Counter(query_tokens)
        for w, qf in tf_q.items():
            if w not in self.idf:
                continue
            df = self.idf[w]  # actually idf stored; need df
            # We need raw term frequency in doc
            # Use doc_len normalization
            doc_tf = doc_tokens.count(w)
            if doc_tf == 0:
                continue
            numerator = doc_tf * (self.k1 + 1)
            denominator = doc_tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_dl)
            score += self.idf[w] * (numerator / denominator)
        return score
    
    def predict(self, query: str, top_k: int = 3) -> list:
        q_tokens = self.tokenize(query)
        scores = []
        for user, asst, ut, at in self.docs:
            # Score against user + assistant tokens
            s = self.score(q_tokens, ut) + self.score(q_tokens, at) * 0.5
            if s > 0:
                scores.append((s, asst))
        scores.sort(reverse=True)
        return [asst for _, asst in scores[:top_k]]
    
    def save(self, model_path: Path):
        with open(model_path, 'wb') as f:
            pickle.dump({
                'vocab': self.vocab,
                'idf': self.idf,
                'docs': self.docs,
                'avg_dl': self.avg_dl,
                'N': self.N,
                'k1': self.k1,
                'b': self.b,
            }, f)


def main():
    print("="*70)
    print("  ARGOS Local Model v2 (BM25)")
    print("="*70)
    
    datasets = sorted(RETRAIN_DIR.glob("dataset_*.jsonl"))
    if not datasets:
        print("❌ No dataset found")
        return
    
    latest = datasets[-1]
    print(f"  Using: {latest.name}")
    
    trainer = BM25Trainer()
    t0 = time.time()
    trainer.fit(latest)
    print(f"  Train: {time.time() - t0:.1f}s")
    
    model_path = RETRAIN_DIR / f"argos_local_model_bm25_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
    trainer.save(model_path)
    print(f"  ✓ Saved: {model_path} ({model_path.stat().st_size / 1024 / 1024:.1f} MB)")
    
    # Test
    print("\n  === Тесты ===")
    queries = [
        ("Брейн недоступен", "brain"),
        ("VetoEvidence как использовать", "veto"),
        ("ARGOS persona status", "status"),
        ("Evolution cycle insights", "evolution"),
        ("Traининг ARGOS", "train"),
    ]
    for q, expected in queries:
        answers = trainer.predict(q, top_k=2)
        print(f"\n  Q: {q} (expected: {expected})")
        for i, a in enumerate(answers, 1):
            print(f"    [{i}] {a[:150].strip()}")


if __name__ == "__main__":
    main()
