"""arc3/candidate_generator.py — какие ходы вообще разумно рассматривать.

Переиспользует проверенную логику arc_agent.py (непустые клетки + сетка
шага 4, максимум ~48 координат на кликовое действие; центр при пустом
кадре). Поиск сужает пространство, муха только ранжирует.
"""


from arcengine import GameAction

ACT_ID = {a.value: a for a in GameAction if hasattr(a, 'value')}

BLOCK = '█'
MAX_COORD = 48
STEP = 4


def coord_candidates(grid, step=STEP, max_n=MAX_COORD):
    cands = []
    seen = set()
    h = len(grid)
    w = max((len(r) for r in grid), default=0)
    for y in range(0, h, step):
        for x in range(0, w, step):
            cell = grid[y][x] if y < h and x < len(grid[y]) else BLOCK
            if cell not in (BLOCK, '.') and (x, y) not in seen:
                cands.append((x, y))
                seen.add((x, y))
                if len(cands) >= max_n:
                    return cands
    return cands


def candidate_list(available, grid):
    """available: список значений GameAction (или None → все)."""
    cands = []
    for a in (available if available else [x.value for x in ACT_ID.values()]):
        act = ACT_ID.get(a)
        if act is None:
            continue
        if act in (GameAction.ACTION6, GameAction.ACTION7):
            for (x, y) in coord_candidates(grid):
                cands.append((f'A{act.value}:{x},{y}', act, {'x': x, 'y': y}))
        else:
            cands.append((f'A{act.value}', act, None))
    if not cands and available:
        for a in available:
            act = ACT_ID.get(a)
            if act in (GameAction.ACTION6, GameAction.ACTION7):
                cands.append((f'A{act.value}:32,32', act,
                              {'x': 32, 'y': 32}))
    return cands
