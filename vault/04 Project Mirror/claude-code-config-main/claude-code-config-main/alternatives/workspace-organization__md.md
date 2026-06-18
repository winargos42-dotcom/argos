---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/alternatives/workspace-organization.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\alternatives\workspace-organization.md
source_ext: .md
source_sha256: 72fd4cabdb90f4cdbe4a9e08823645c0ca5902f3e53bca8e68f6fddc5ad08d5b
text_sha256: 72fd4cabdb90f4cdbe4a9e08823645c0ca5902f3e53bca8e68f6fddc5ad08d5b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:26
---

# workspace-organization.md

- Source: `claude-code-config-main/claude-code-config-main/alternatives/workspace-organization.md`
- Extract: `text`
- SHA256: `72fd4cabdb90f4cdbe4a9e08823645c0ca5902f3e53bca8e68f6fddc5ad08d5b`

## Content

# Workspace Organization - предотвращение хаоса в проектах

## Проблема

При долгой работе с Claude Code:
- Папки плодятся бесконтрольно (каждая сессия может создать новую)
- Ресерч разбросан по корню и подпапкам
- Агент не знает что уже есть и делает дубликаты
- Нет единого места чтобы понять "где что"

## Решение: 3 навигационных файла в корне

### 1. WORKSPACE.md - карта территории

```markdown
# Workspace Navigation

## Структура
- research/           ← централизованный ресерч
  - _inbox/           ← сырое
  - agentic/          ← агенты, memory
  - ml/               ← нейросети
  - infrastructure/   ← серверы, deploy
  - security/         ← безопасность
  - product/          ← конкуренты, UX
  - _distributed/     ← лог раскидки
- knowledge-vault/    ← переработанная knowledge base
- learning-hub/       ← обучение
- [проекты]           ← см. PROJECTS.md

## Потоки данных
сырой ресерч → research/{тема}/ → incoming-research/ → knowledge-vault
                                 → конкретный проект

## Ключевые файлы
| Файл | Когда |
|------|-------|
| WORKSPACE.md | Старт сессии |
| PROJECTS.md | Работа с проектами |
| .claude/HANDOFF.md | Продолжение работы |
| research/ | Перед ресерчем |
```

### 2. PROJECTS.md - реестр проектов

```markdown
# Project Registry

| Папка | Что | Статус |
|-------|-----|--------|
| project-a/ | Описание | Активный |
| project-b/ | Описание | Поддержка |
| project-c/ | Описание | Пауза |
| project-d/ | Описание | Архив (→ D:\archive\) |

## Правила
1. Перед созданием нового - проверить этот файл
2. При создании - добавить запись
3. При архивации - перенести в секцию "Архив"
4. Статусы: Активный → Поддержка → Пауза → Архив
```

### 3. .claude/rules/session-handoff.md - автоматическое чтение

```markdown
## При старте сессии
1. Прочитать WORKSPACE.md - понять структуру
2. Проверить .claude/HANDOFF.md - продолжить прошлую сессию
3. При работе с проектами - сверяться с PROJECTS.md
4. При ресерче - проверить research/ (нет ли готового)
```

## Research Hub - структура для ресерчей

Отдельная папка `research/` с тематическими подпапками:

```
research/
├── _inbox/          ← сырые результаты, ещё не разобранные
├── agentic/         ← агенты, orchestration, memory, tools
├── ml/              ← нейросети, training, inference
├── infrastructure/  ← серверы, deploy, storage
├── security/        ← безопасность, licensing
├── product/         ← конкуренты, рынок, UX
└── _distributed/    ← лог: что куда ушло
```

**Поток:** сырое → `_inbox/` → разбор → тематическая папка → проект (если нужно) + запись в `_distributed/`

**Именование файлов:** `{subtopic}-{описание}.md`, дата обязательна в начале файла.

## Зачем это работает

1. **JIT context** - агент при старте знает структуру, не исследует заново
2. **Предотвращение дублей** - PROJECTS.md = source of truth по проектам
3. **Ресерч не теряется** - research/ = единое место, не раскидано по корню
4. **Session continuity** - HANDOFF.md передаёт контекст между сессиями
5. **Масштабируется** - тематические подпапки в research/ растут независимо

## Связь с другими подходами

- **Karpathy LLM Wiki** (gist, Apr 2026): raw/ → wiki/ ≈ research/ → knowledge-vault/
- **MemPalace** (Jovovich): hierarchical memory ≈ WORKSPACE.md → PROJECTS.md → project docs
- **CORAL** (MIT/Meta): shared knowledge layer ≈ research/ as shared artifacts
- **Session Handoff** (см. `session-handoff.md`): дополняет WORKSPACE.md передачей контекста

## Anti-patterns

- Создавать папку для каждого маленького скрипта
- Оставлять ресерч-файлы в корне проекта
- Не обновлять PROJECTS.md при создании/архивации
- Полагаться на memory без навигационных файлов

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
