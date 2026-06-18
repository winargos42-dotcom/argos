---
argos_import: project_file
source_path: CLAUDE_INTEGRATION.md
source_abs: F:\debug\argoss\CLAUDE_INTEGRATION.md
source_ext: .md
source_sha256: 1a3a9c7862798d95aae8ceb2c41880b0160c2d9fe1cadf8871584f54ff5c338a
text_sha256: 1a3a9c7862798d95aae8ceb2c41880b0160c2d9fe1cadf8871584f54ff5c338a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# CLAUDE_INTEGRATION.md

- Source: `CLAUDE_INTEGRATION.md`
- Extract: `text`
- SHA256: `1a3a9c7862798d95aae8ceb2c41880b0160c2d9fe1cadf8871584f54ff5c338a`

## Content

# ARGOS + Claude Code Templates Integration

## Обзор

Успешно интегрировано **695 компонентов** из `claude-code-templates` в экосистему ARGOS.

## Статистика

| Тип компонента | Количество |
|----------------|------------|
| 🤖 Agents      | 417        |
| ⌨️ Commands    | 276        |
| 🪝 Hooks       | 0          |
| 🔗 MCPs        | 0          |
| ⚙️ Settings    | 0          |
| 🧠 Skills      | 2          |
| **ИТОГО**      | **695**    |

## Топ категории агентов

| Категория | Агентов |
|-----------|---------|
| expert-advisors | 52 |
| programming-languages | 50 |
| data-ai | 40 |
| devops-infrastructure | 39 |
| development-tools | 34 |
| business-marketing | 21 |
| security | 21 |
| development-team | 17 |
| deep-research-team | 16 |
| web-tools | 16 |

## Созданные файлы

### Новые модули интеграции:

1. **`src/claude_templates_integrator.py`** (15KB)
   - `ClaudeTemplatesLoader` — загрузчик компонентов
   - `ArgosClaudeAdapter` — адаптер компонентов → ARGOS
   - `ClaudeTemplatesIntegrator` — унифицированный интегратор

2. **`argos-claude.py`** (5KB)
   - CLI-инструмент для работы с Claude агентами
   - Команды: `search`, `list`, `agent`, `use`

### Модифицированные файлы:

- `src/argos_integrator.py` — добавлена интеграция Claude Templates
- `src/event_bus.py` — добавлено событие `COMPONENT_LOADED`

## Использование

### Поиск агентов:
```bash
python argos-claude.py search "python"
python argos-claude.py search "security"
python argos-claude.py search "frontend"
```

### Просмотр деталей агента:
```bash
python argos-claude.py agent "python-pro"
```

### Автоматический выбор агента для задачи:
```python
from src.argos_integrator import ArgosIntegrator

integrator = ArgosIntegrator(core)
registry = integrator.integrate_all()

# Получить Claude интегратор
claude = integrator.get("claude.agents")
```

### Прямой доступ к загрузчику:
```python
from src.claude_templates_integrator import ClaudeTemplatesLoader

loader = ClaudeTemplatesLoader()
loader.discover()

# Поиск
results = loader.search("backend")
for agent in results:
    print(f"{agent.name}: {agent.description}")
```

## Примеры популярных агентов

### Разработка:
- `python-pro` — Python эксперт с типизацией и async
- `frontend-developer` — React/Next.js специалист  
- `api-designer` — Проектирование API
- `database-architect` — Архитектура БД

### DevOps:
- `docker-specialist` — Docker контейнеризация
- `kubernetes-expert` — K8s оркестрация
- `cicd-pipeline-architect` — CI/CD пайплайны
- `infrastructure-designer` — Облачная инфраструктура

### Безопасность:
- `security-auditor` — Аудит безопасности
- `penetration-tester` — Пентесты
- `dependency-vulnerability-analyzer` — Анализ уязвимостей

### AI/ML:
- `llm-architect` — Архитектура LLM
- `prompt-engineer` — Инженерия промптов
- `ml-model-evaluator` — Оценка моделей
- `ai-ethics-advisor` — Этика AI

## Интеграция с ядром ARGOS

При запуске ArgosCore:
```
[INTEGRATOR] CLAUDE TEMPLATES v3.0
📦 Обнаружено компонентов: 695
  └─ agents: 417
  └─ commands: 276
  └─ skills: 2
🤖 Адаптация агентов: 417
⌨️ Адаптация команд: 276
══════════════ ИНТЕГРАЦИЯ ШАБЛОНОВ ЗАВЕРШЕНА ═══════════════
🤖 Агенты:    417
⌨️ Команды:   276
🪝 Хуки:      0
🔗 MCP:       0
════════════════════════════════════════════════════════════
```

## Архитектура интеграции

```
┌─────────────────────────────────────────────────────────────┐
│                    ARGOS Universal OS                        │
├─────────────────────────────────────────────────────────────┤
│  ArgosIntegrator                                            │
│    ├─ Security (4)                                          │
│    ├─ Connectivity (16)                                     │
│    ├─ Knowledge (1)                                         │
│    ├─ Factory (3)                                           │
│    ├─ Mind (0)                                              │
│    ├─ Quantum (4)                                           │
│    ├─ Vision (2)                                            │
│    ├─ Skills (7)                                            │
│    ├─ Modules (3)                                           │
│    ├─ Interfaces (6)                                        │
│    └─ Claude Templates (3) ← NEW!                           │
│         ├─ 417 Agents (adapted)                             │
│         ├─ 276 Commands                                     │
│         └─ 2 Skills                                         │
└─────────────────────────────────────────────────────────────┘
```

## Будущие улучшения

- [ ] Интеграция с SkillLoader для регистрации как навыков ARGOS
- [ ] Автоматический выбор агента на основе Intent Classification
- [ ] Поддержка MCP (Model Context Protocol) серверов
- [ ] Создание агентов ARGOS из Claude шаблонов
- [ ] P2P синхронизация шаблонов между нодами

## Лицензия

Claude Code Templates интегрированы в соответствии с лицензией исходного проекта.

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
