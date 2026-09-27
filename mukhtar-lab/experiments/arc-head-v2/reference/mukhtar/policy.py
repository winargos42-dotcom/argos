"""arc3/mukhtar/policy.py — вариант B: Search + Mukhtar.

Те же кандидаты, та же память, тот же бюджет — другой rank().
frame + history → encoder → замороженное ядро → head → scores →
порядок кандидатов. Ноги и ARC не смешиваются: этот ранжировщик не
знает ничего про суставы.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, '/home/argos-data/improve')
sys.path.insert(0, '/home/argos-data/improve/arc3')

from arc3.perception import extract_features  # noqa: E402
from arc3.mukhtar.encoder import feature_vector  # noqa: E402
from arc3.mukhtar.action_head import ActionHead  # noqa: E402


class MukhtarRanker:
    def __init__(self, backend, head=None, memory=None, head_path=None):
        self.backend = backend
        self.head = head or ActionHead()
        if head_path and Path(head_path).exists():
            self.head.load(head_path)
        self.memory = memory
        self.tabu = set()
        self.calls = 0

    def _embeds(self, features, candidates):
        """Один вектор фич на состояние + тег действия на кандидата."""
        base = feature_vector(features)
        return [base for _ in candidates]

    def rank(self, frame_hash, candidates, features=None, prev_grid=None,
             previous_action=None, levels_completed=0):
        if features is None:
            features = extract_features(
                [], prev_grid or [], previous_action, levels_completed)
        embeds = self._embeds(features, candidates)
        self.calls += 1
        if self.backend is not None:
            embeds = self.backend.embed(embeds)
        tags = [c[0] for c in candidates]
        scores = self.head.scores(embeds, tags)

        def key(c_i):
            i, c = c_i
            tabu = (frame_hash, c[0]) in self.tabu
            if self.memory is not None:
                tabu = tabu or self.memory.is_dead_end(frame_hash, c[0])
            return (tabu, -float(scores[i]))
        return [candidates[i] for i, _ in
                sorted(enumerate(candidates), key=key)]

    def node_scores(self, nodes):
        """Оценка узлов BFS-фронтира: head-score состояния минус
        лёгкий штраф глубины (чтобы не зацикливаться на корне)."""
        t0 = time.monotonic()
        embeds = self.backend.embed(
            [feature_vector(n['feats']) for n in nodes]) \
            if self.backend is not None else None
        tags = ['state'] * len(nodes)
        if embeds is None:
            embeds = self._embeds(nodes[0]['feats'], tags)
        scores = self.head.scores(embeds, tags)
        out = [float(scores[i]) - 0.02 * nodes[i]['depth']
               for i in range(len(nodes))]
        self.calls += 1
        return out

    def record(self, frame_hash, action_key, new_state):
        self.tabu.add((frame_hash, action_key))
