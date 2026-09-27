"""arc3/perception.py — объектный encoder кадра.

Не подаём 64×64 «мухе» сырым. Извлекаем:
  colors_present, changed_cells, connected_components, component_positions,
  frame_delta (diff с прошлым кадром), previous_action, levels_completed.
"""
from collections import deque

BLOCK = '█'


def color_of(token):
    """'38;5;196m:█' → '38;5;196m'; '█' → '0'; '.' → None."""
    if token == '.':
        return None
    if ':' in token:
        return token.split(':', 1)[0]
    return '0'


def connected_components(grid):
    """BFS по непустым клеткам с учётом цвета (цвет — часть компоненты)."""
    h = len(grid)
    comps = []
    seen = set()
    for y in range(h):
        for x in range(len(grid[y])):
            if (x, y) in seen:
                continue
            color = color_of(grid[y][x])
            if color is None:
                continue
            q = deque([(x, y)])
            cells = []
            seen.add((x, y))
            while q:
                cx, cy = q.popleft()
                cells.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if (nx, ny) in seen:
                        continue
                    if 0 <= ny < h and 0 <= nx < len(grid[ny]) \
                            and color_of(grid[ny][nx]) == color:
                        seen.add((nx, ny))
                        q.append((nx, ny))
            comps.append({'color': color, 'cells': cells,
                          'size': len(cells),
                          'cx': sum(c[0] for c in cells) / len(cells),
                          'cy': sum(c[1] for c in cells) / len(cells)})
    return comps


def extract_features(grid, prev_grid=None, previous_action=None,
                     levels_completed=0, available_actions=None):
    h = len(grid)
    w = max((len(r) for r in grid), default=0)
    colors = {color_of(c) for r in grid for c in r}
    colors.discard(None)
    colors = {str(c) for c in colors}
    comps = connected_components(grid)
    changed = []
    if prev_grid is not None:
        ph = len(prev_grid)
        for y in range(max(h, ph)):
            pw = len(prev_grid[y]) if y < ph else 0
            for x in range(max(w, pw)):
                cur = grid[y][x] if y < h and x < len(grid[y]) else '.'
                old = prev_grid[y][x] if y < ph and x < pw else '.'
                if cur != old:
                    changed.append((x, y, old, cur))
    return {
        'colors_present': sorted(colors),
        'n_colors': len(colors),
        'components': comps,
        'n_components': len(comps),
        'component_sizes': sorted((c['size'] for c in comps), reverse=True),
        'changed_cells': changed,
        'n_changed': len(changed),
        'previous_action': previous_action,
        'levels_completed': levels_completed,
        'available_actions': list(available_actions or []),
        'grid_w': w, 'grid_h': h,
    }


def feature_vector(features, max_comp=12, max_changed=64):
    """Плоский числовой вектор фиксированной длины для входа адаптера."""
    vec = []
    vec.append(features['n_colors'])
    vec.append(features['n_components'])
    vec.append(features['n_changed'])
    vec.append(features['grid_w'])
    vec.append(features['grid_h'])
    for c in sorted(set(features['colors_present']))[:8]:
        try:
            vec.append(int(c.split(';')[-1].rstrip('m')))
        except ValueError:
            vec.append(-1)
    vec += [0.0] * (8 - len(vec) + 5)
    sizes = features['component_sizes'][:max_comp]
    vec += sizes + [0] * (max_comp - len(sizes))
    for (x, y, _old, _new) in features['changed_cells'][:max_changed]:
        vec += [x / 64.0, y / 64.0]
    vec += [0.0] * (2 * max_changed - 2 * min(len(
        features['changed_cells']), max_changed))
    prev = features['previous_action']
    action = str(prev).split(':', 1)[0] if prev is not None else ''
    action_id = int(action[1:]) if action.startswith('A') and action[1:].isdigit() else 0
    vec.append(float(action_id) / 8.0)
    vec.append(float(features['levels_completed']) / 100.0)
    return vec
