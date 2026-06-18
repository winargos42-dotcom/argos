# Модуль collections в Python — чит-код для алгоритмов

> Источник: [Habr — enamored_poc](https://habr.com/ru/articles/1034858/)
> Теги: #python #алгоритмы #collections #leetcode #собеседование

## Краткое резюме

Стандартные `list.pop(0)` и ручной подсчёт в словарях — причина TLE. Модуль `collections` решает это из коробки, на C-уровне.

## 1. deque — двусторонняя очередь

**Замена:** `list.pop(0)` → `deque.popleft()`

| Операция | list | deque |
|----------|------|-------|
| Удаление первого | O(n) | **O(1)** |
| Добавление в начало | O(n) | **O(1)** |
| Добавление в конец | O(1) | O(1) |

**Юзкейсы:** BFS, скользящее окно, Sliding Window Maximum

```python
from collections import deque

def good_bfs(graph, start_node):
    queue = deque([start_node])
    visited = set([start_node])
    while queue:
        node = queue.popleft()  # O(1) вместо O(n) у list.pop(0)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

## 2. Counter — подсчёт частот

**Замена:** ручной цикл `for + dict.get()` → `Counter(итерабельный)`

Фичи:
- `Counter(s) == Counter(t)` — проверка анаграмм
- `.most_common(k)` — топ-k элементов (через heapq, O(n·log k))
- Арифметика: `+`, `-`, `&` (пересечение), `|` (объединение)

```python
from collections import Counter

# Анаграмма — одна строка
is_anagram = lambda s, t: Counter(s) == Counter(t)

# Ransom Note — вычитание
can_construct = lambda ransom, mag: len(Counter(ransom) - Counter(mag)) == 0
```

## 3. defaultdict — забудь про KeyError

**Замена:** `if k not in dict: dict[k] = []` → `defaultdict(list)`

```python
from collections import defaultdict

# Граф из списка рёбер — без единой проверки
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

# Группировка анаграмм
groups = defaultdict(list)
for word in strs:
    key = ''.join(sorted(word))
    groups[key].append(word)
```

Фабрики: `list`, `int` (дефолт 0), `set` (уникальные элементы)

## 4. namedtuple — самодокументируемый код

```python
from collections import namedtuple
State = namedtuple('State', ['x', 'y', 'distance', 'has_key'])
node = State(x=5, y=10, distance=3, has_key=True)
node.distance  # вместо node[2]
```

## 5. OrderedDict — LRU Cache в 2 строки

```python
from collections import OrderedDict
cache = OrderedDict()
cache['a'] = 1
cache.move_to_end('a')  # обновили → в конец
oldest = next(iter(cache))  # кандидат на удаление
```

## Шпаргалка Big-O

| Задача | Наивно | collections | Ускорение |
|--------|--------|-------------|-----------|
| Удалить первый | list.pop(0) O(n) | deque.popleft() **O(1)** | ×n |
| Вставить в начало | list.insert(0,v) O(n) | deque.appendleft(v) **O(1)** | ×n |
| Подсчёт частот | for+dict.get O(n) | Counter O(n) | C-скорость |
| Топ-K элементов | sorted()[:k] O(n·log n) | most_common(k) **O(n·log k)** | ×log n |
| Группировка | if k not in dict O(1) | defaultdict(list) O(1) | чище код |

## Практика (LeetCode)

- **Counter**: [242. Valid Anagram](https://leetcode.com/problems/valid-anagram/) — 1 строка
- **defaultdict**: [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) — без if
- **deque**: [239. Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) — Hard

---

*Сохранено: 2026-05-14 | Связи: [[ARGOS]], [[Контекст работы]]*