"""arc3/mukhtar/action_head.py — обучаемая голова (единственное, что
обучается в v0.1; ядро заморожено).

scores(candidate_embeds, candidate_tags) -> [0..1]
Обучается на teacher-траекториях: argmax(head) = teacher_action.
"""
import numpy as np


class ActionHead:
    """Минимальная линейная голова (numpy, чтобы не зависеть от torch
    на X230). Если понадобится нелинейность — обновить при обучении."""

    def __init__(self, embed_dim=64, n_tags=8, seed=7):
        rng = np.random.default_rng(seed)
        self.w_emb = rng.normal(0, 0.05, (embed_dim,))
        self.w_tag = rng.normal(0, 0.05, (n_tags,))
        self.b = 0.0

    def tag_onehot(self, tags, n_tags=8):
        m = np.zeros((len(tags), n_tags), dtype=float)
        for i, t in enumerate(tags):
            action = t.split(':', 1)[0]
            if not (action.startswith('A') and action[1:].isdigit()):
                raise ValueError(f'Unknown action tag: {t}')
            j = int(action[1:]) - 1
            if not 0 <= j < n_tags:
                raise ValueError(f'Action tag out of range: {t}')
            m[i, j] = 1.0
        return m

    def scores(self, embeds, tags):
        e = np.asarray(embeds, dtype=float)
        t = self.tag_onehot(tags)
        return e @ self.w_emb + t @ self.w_tag + self.b

    def train_step(self, embeds, tags, teacher_idx, lr=0.01):
        """Один шаг: подтягиваем score учителя к 1, остальных к 0
        (softmax-кросс-энтропия, numpy-реализация)."""
        logits = self.scores(embeds, tags)
        logits -= logits.max()
        p = np.exp(logits) / np.exp(logits).sum()
        grad = p.copy()
        grad[teacher_idx] -= 1.0
        e = np.asarray(embeds, dtype=float)
        t = self.tag_onehot(tags)
        self.w_emb -= lr * (grad @ e)
        self.w_tag -= lr * (grad @ t)
        self.b -= lr * grad.sum()
        return float(-np.log(p[teacher_idx] + 1e-12))

    def save(self, path):
        np.savez(path, w_emb=self.w_emb, w_tag=self.w_tag, b=self.b)

    def load(self, path):
        d = np.load(path)
        self.w_emb = d['w_emb']
        self.w_tag = d['w_tag']
        self.b = float(d['b'])
