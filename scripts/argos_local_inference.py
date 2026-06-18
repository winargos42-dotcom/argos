#!/usr/bin/env python3
"""
ARGOS Local Inference — обёртка над BM25 моделью.

Использование:
    from argos_local_inference import ask_argos_local
    answer = ask_argos_local("Что делать если Брейн недоступен?")
    print(answer)
"""
import pickle
import re
import math
from collections import Counter
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path("/home/ava/Projects/argoss")
RETRAIN_DIR = PROJECT_ROOT / "data/retrain"


class ArgosLocal:
    """Локальная модель ARGOS — BM25 retrieval."""
    
    def __init__(self, model_path: Optional[Path] = None):
        if model_path is None:
            # Use latest BM25 model
            models = sorted(RETRAIN_DIR.glob("argos_local_model_bm25_*.pkl"))
            if not models:
                # Fallback to TF-IDF
                models = sorted(RETRAIN_DIR.glob("argos_local_model_*.pkl"))
                models = [m for m in models if "bm25" not in m.name]
            if not models:
                raise FileNotFoundError("No model found. Run argos_local_train.py first.")
            model_path = models[-1]
        with open(model_path, 'rb') as f:
            d = pickle.load(f)
        self.vocab = d['vocab']
        self.idf = d['idf']
        self.docs = d['docs']
        self.avg_dl = d.get('avg_dl', 1)
        self.N = d.get('N', len(self.docs))
        self.k1 = d.get('k1', 1.5)
        self.b = d.get('b', 0.75)
        self.model_path = model_path
    
    def tokenize(self, text: str) -> list:
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return [w for w in text.split() if len(w) > 2]
    
    def score(self, query_tokens, doc_tokens):
        score = 0.0
        doc_len = max(len(doc_tokens), 1)
        tf_q = Counter(query_tokens)
        for w, qf in tf_q.items():
            if w not in self.idf:
                continue
            doc_tf = doc_tokens.count(w)
            if doc_tf == 0:
                continue
            numerator = doc_tf * (self.k1 + 1)
            denominator = doc_tf + self.k1 * (1 - self.b + self.b * doc_len / max(self.avg_dl, 1))
            score += self.idf[w] * (numerator / denominator)
        return score
    
    def ask(self, query: str, top_k: int = 1) -> str:
        """Найти лучший ответ на вопрос."""
        q_tokens = self.tokenize(query)
        scores = []
        for user, asst, ut, at in self.docs:
            s = self.score(q_tokens, ut) + self.score(q_tokens, at) * 0.5
            if s > 0:
                scores.append((s, asst, user))
        scores.sort(reverse=True)
        if not scores:
            return ""
        return scores[0][1]
    
    def ask_multi(self, query: str, top_k: int = 3) -> list:
        """Топ-K ответов."""
        q_tokens = self.tokenize(query)
        scores = []
        for user, asst, ut, at in self.docs:
            s = self.score(q_tokens, ut) + self.score(q_tokens, at) * 0.5
            if s > 0:
                scores.append((s, asst))
        scores.sort(reverse=True)
        return [asst for _, asst in scores[:top_k]]


# Singleton
_MODEL = None

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = ArgosLocal()
    return _MODEL


def ask_argos_local(query: str, top_k: int = 1) -> str:
    """Быстрый helper."""
    return get_model().ask(query, top_k=top_k)


if __name__ == "__main__":
    queries = [
        "Брейн недоступен что делать?",
        "VetoEvidence пример",
        "ARGOS persona status",
        "Evolution insights",
        "Как обучить локальную модель?",
    ]
    model = ArgosLocal()
    print(f"Model: {model.model_path.name}")
    print(f"Vocab: {len(model.vocab)}, Docs: {model.N}")
    print()
    for q in queries:
        ans = model.ask(q)
        print(f"Q: {q}")
        print(f"  → {ans[:200]}")
        print()
