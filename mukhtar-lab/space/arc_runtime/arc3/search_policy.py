"""arc3/search_policy.py — вариант A (контроль): обычное правило
ранжирования. Новизна состояния + табу на точные повторы (кадр, действие).

Тот же ControlRanker, что в arc_agent.py — сюда вынесен для честного A/B:
варианты A и B получают ОДИНАКОВЫЕ кандидаты, различается только rank().
"""


class SearchRanker:
    def __init__(self, memory):
        self.memory = memory
        self.tabu = set()          # (frame_hash, action_key) — точные повторы
        self.action_novelty = {}   # action_key -> сколько раз дал новое

    def rank(self, frame_hash, candidates, features=None):
        def key(c):
            ak = c[0]
            tabu = (frame_hash, ak) in self.tabu \
                or self.memory.is_dead_end(frame_hash, ak)
            novel = self.action_novelty.get(ak, 0)
            return (tabu, -novel)
        return sorted(candidates, key=key)

    def record(self, frame_hash, action_key, new_state):
        if new_state:
            self.action_novelty[action_key] = \
                self.action_novelty.get(action_key, 0) + 1
        self.tabu.add((frame_hash, action_key))
