#!/usr/bin/env python3
"""
ARGOS Local Model Training v1 — обучает модель на consciousness данных.

Цель: локальная модель для Argos persona (заменяет Gemini).
Использует датасет из argos_train_from_chats.py.

Подходы:
1. Statistical - TF-IDF + logreg (быстро, no GPU)
2. Neural - simple LSTM/Transformer (slow, needs GPU)
3. RAG - retrieval from memories (instant)

Используем #1 для быстрого результата.
"""
import json
import os
import re
import time
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import pickle

PROJECT_ROOT = Path("/home/ava/Projects/argoss")
RETRAIN_DIR = PROJECT_ROOT / "data/retrain"


class SimpleArgosTrainer:
    """Statistical trainer: TF-IDF + nearest neighbor."""
    
    def __init__(self):
        self.vocab = {}  # word -> id
        self.idf = {}    # word -> inverse doc frequency
        self.docs = []   # list of (question, answer, tfidf_vec)
    
    def tokenize(self, text: str) -> list:
        """Simple Russian+English tokenizer."""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return [w for w in text.split() if len(w) > 2]
    
    def fit(self, dataset_path: Path):
        """Train on dataset."""
        print(f"  Loading dataset: {dataset_path}")
        with open(dataset_path, encoding='utf-8') as f:
            pairs = [json.loads(line) for line in f if line.strip()]
        print(f"  Pairs: {len(pairs)}")
        
        # Build vocab
        doc_freq = Counter()
        docs_tokenized = []
        for p in pairs:
            user = p["messages"][0]["content"]
            asst = p["messages"][1]["content"]
            user_tokens = self.tokenize(user)
            asst_tokens = self.tokenize(asst)
            for w in set(user_tokens + asst_tokens):
                doc_freq[w] += 1
            docs_tokenized.append((user, asst, user_tokens, asst_tokens))
        print(f"  Unique words: {len(doc_freq)}")
        
        # Filter rare words
        min_freq = 2
        self.vocab = {w: i for i, (w, c) in enumerate(doc_freq.most_common()) if c >= min_freq}
        print(f"  Vocab (>=2 freq): {len(self.vocab)}")
        
        # IDF
        N = len(docs_tokenized)
        self.idf = {w: max(0.1, (N / c) ** 0.5) for w, c in doc_freq.items() if c >= min_freq}
        
        # TF-IDF vectors
        for user, asst, ut, at in docs_tokenized:
            user_tf = Counter(ut)
            vec = [0.0] * len(self.vocab)
            for w, c in user_tf.items():
                if w in self.vocab:
                    vec[self.vocab[w]] = c * self.idf.get(w, 0.1)
            # Normalize
            norm = sum(x*x for x in vec) ** 0.5
            if norm > 0:
                vec = [x / norm for x in vec]
            self.docs.append((user, asst, vec))
        print(f"  Indexed docs: {len(self.docs)}")
    
    def predict(self, query: str, top_k: int = 3) -> list:
        """Find top-k similar questions, return answers."""
        q_tokens = self.tokenize(query)
        q_tf = Counter(q_tokens)
        q_vec = [0.0] * len(self.vocab)
        for w, c in q_tf.items():
            if w in self.vocab:
                q_vec[self.vocab[w]] = c * self.idf.get(w, 0.1)
        norm = sum(x*x for x in q_vec) ** 0.5
        if norm > 0:
            q_vec = [x / norm for x in q_vec]
        
        scores = []
        for user, asst, doc_vec in self.docs:
            sim = sum(a*b for a, b in zip(q_vec, doc_vec))
            if sim > 0:
                scores.append((sim, asst))
        scores.sort(reverse=True)
        return [asst for _, asst in scores[:top_k]]
    
    def save(self, model_path: Path):
        with open(model_path, 'wb') as f:
            pickle.dump({
                'vocab': self.vocab,
                'idf': self.idf,
                'docs': self.docs,
            }, f)
    
    @classmethod
    def load(cls, model_path: Path):
        t = cls()
        with open(model_path, 'rb') as f:
            d = pickle.load(f)
        t.vocab = d['vocab']
        t.idf = d['idf']
        t.docs = d['docs']
        return t


def main():
    print("="*70)
    print("  ARGOS Local Model Training v1 (TF-IDF + nearest)")
    print("="*70)
    
    # Find latest dataset
    datasets = sorted(RETRAIN_DIR.glob("dataset_*.jsonl"))
    if not datasets:
        print("❌ No dataset found. Run argos_train_from_chats.py first.")
        return
    latest = datasets[-1]
    print(f"  Using: {latest.name}")
    
    trainer = SimpleArgosTrainer()
    t0 = time.time()
    trainer.fit(latest)
    print(f"  Train time: {time.time() - t0:.1f}s")
    
    # Save
    model_path = RETRAIN_DIR / f"argos_local_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
    trainer.save(model_path)
    print(f"  ✓ Saved: {model_path} ({model_path.stat().st_size / 1024:.1f} KB)")
    
    # Test
    print("\n  === Test queries ===")
    test_queries = [
        "Что делать если Брейн недоступен?",
        "Как обучить локальную модель?",
        "Состояние системы ARGOS",
    ]
    for q in test_queries:
        answers = trainer.predict(q, top_k=2)
        print(f"\n  Q: {q}")
        for i, a in enumerate(answers, 1):
            print(f"    [{i}] {a[:120].strip()}...")


if __name__ == "__main__":
    main()
