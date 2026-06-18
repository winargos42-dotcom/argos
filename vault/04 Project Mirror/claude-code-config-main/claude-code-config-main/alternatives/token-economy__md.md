---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/alternatives/token-economy.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\alternatives\token-economy.md
source_ext: .md
source_sha256: 21c00af4499d1cf0952cfc6ad818a461f3a45474faafdf05dd8fc4201a744803
text_sha256: 21c00af4499d1cf0952cfc6ad818a461f3a45474faafdf05dd8fc4201a744803
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:26
---

# token-economy.md

- Source: `claude-code-config-main/claude-code-config-main/alternatives/token-economy.md`
- Extract: `text`
- SHA256: `21c00af4499d1cf0952cfc6ad818a461f3a45474faafdf05dd8fc4201a744803`

## Content

# Token Economy - экономия токенов в AI-агентах

## Проблема

Токены = деньги. Claude Code может тратить 180 токенов на "I'd be happy to help you with that. Let me search the web for you." когда достаточно 2 токена: "Tool work".

## Caveman Prompting

Источник: 16-летний SaaS-разработчик, Derp Learning (апрель 2026)

**Идея:** научить агента говорить минимально, как пещерный человек.

| Обычный Claude | Caveman Claude |
|----------------|----------------|
| "I executed the web search tool and found relevant results" (8 tok) | "Tool work" (2 tok) |
| "Let me analyze the codebase to understand the architecture" (10 tok) | "Read code" (2 tok) |
| "I'd be happy to help you with that request" (9 tok) | (ничего, сразу делает) |

**Результат: 75% экономия токенов** (180 → 45 на задачу).

## Где применять

### 1. Sub-agents (Agent tool)

При запуске субагентов через Agent tool - добавить в промпт:
```
Respond minimally. No preamble, no summaries. 
Action → result. Skip "I'll", "Let me", "I found".
```

Субагенты не видны пользователю - красивый текст не нужен.

### 2. Internal reasoning

В системных промптах для внутренних операций:
```
Output: facts only. No explanations. No transitions.
Format: bullet points, no prose.
```

### 3. Batch operations

При обработке 10+ файлов, не писать "Processing file X..." для каждого.

## Где НЕ применять

- Ответы пользователю (нужна понятность)
- Обучающие объяснения (нужна детальность)
- Первый ответ в сессии (нужен контекст)
- Debugging output (нужна полнота)

## Количественные ориентиры

| Операция | Обычно | Caveman | Экономия |
|----------|--------|---------|----------|
| Web search + отчёт | ~180 tok | ~45 tok | 75% |
| File analysis | ~300 tok | ~80 tok | 73% |
| Multi-file refactor (10 files) | ~2000 tok | ~500 tok | 75% |
| Sub-agent research task | ~1500 tok | ~400 tok | 73% |

## Реализация в Claude Code

### Через prompt для субагентов
```python
Agent(prompt="""
[CAVEMAN MODE] Terse output. No preamble. Facts only.
Task: {task}
""")
```

### Через CLAUDE.md секцию
```markdown
## Token Economy
- Sub-agents: minimal output, no preamble
- Batch ops: no per-item status messages
- Internal: bullet points, no prose
```

## Связь с другими практиками

- **Layered memory loading** - загружать только нужное = меньше input токенов
- **JIT context** - не загружать весь проект, а только релевантные файлы
- **Context Engineering** - pruning + re-inject вместо полного контекста

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
