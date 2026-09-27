"""arc3/world_memory.py — граф состояний: S0 --ACTION--> S1.

visit_count, actions_tried, level_progress, dead_end, novelty.
Запрещает бессмысленные повторы известных бесполезных переходов.
"""


class WorldMemory:
    def __init__(self):
        self.states = {}        # hash -> {visit_count, first_seen, last_seen}
        self.transitions = {}   # (hash, action_key) -> next_hash, new_state
        self.action_counts = {}  # action_key -> tried
        self.dead_ends = set()  # (hash, action_key), приведшие в тупик

    def observe(self, state_id, action_key, next_state_id,
                new_state, progress=0.0):
        s = self.states.setdefault(
            state_id,
            {'visit_count': 0, 'first_seen': None, 'last_seen': None,
             'best_progress': 0.0})
        s['visit_count'] += 1
        s['best_progress'] = max(s['best_progress'], progress)
        self.transitions[(state_id, action_key)] = (next_state_id, new_state)
        self.action_counts[action_key] = self.action_counts.get(
            action_key, 0) + 1
        return next_state_id

    def mark_dead_end(self, state_id, action_key):
        self.dead_ends.add((state_id, action_key))

    def is_dead_end(self, state_id, action_key):
        return (state_id, action_key) in self.dead_ends

    def novelty(self, state_id):
        """0.0 — знакомое до дыр, 1.0 — никогда не видели."""
        s = self.states.get(state_id)
        if s is None:
            return 1.0
        return max(0.0, 1.0 - 0.2 * s['visit_count'])

    def stats(self):
        return {'states': len(self.states),
                'transitions': len(self.transitions),
                'actions_tried': len(self.action_counts),
                'dead_ends': len(self.dead_ends)}
