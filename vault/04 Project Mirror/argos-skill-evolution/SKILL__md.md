---
argos_import: project_file
source_path: argos-skill-evolution/SKILL.md
source_abs: F:\debug\argoss\argos-skill-evolution\SKILL.md
source_ext: .md
source_sha256: eea0a4bef99b9b6bc197682a2e1be82e6c988e70c2103c9132879a9e952fb6f6
text_sha256: eea0a4bef99b9b6bc197682a2e1be82e6c988e70c2103c9132879a9e952fb6f6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:42
---

# SKILL.md

- Source: `argos-skill-evolution/SKILL.md`
- Extract: `text`
- SHA256: `eea0a4bef99b9b6bc197682a2e1be82e6c988e70c2103c9132879a9e952fb6f6`

## Content

---
name: argos-skill-evolution
description: "Create, inject, test, and manage ARGOS skills (modules) through the built-in evolution system. Use this skill when the user wants to add a new capability to ARGOS, inject code via Telegram (TGCodeInjector), auto-generate a skill using AI (ArgosEvolution), roll back a bad patch, or view the skill list. Trigger on phrases like 'создай скил', 'добавь скил', 'напиши скил', 'inject skill', 'горячая загрузка', 'запусти инжектор', 'ArgosEvolution', 'new ARGOS module', 'добавь возможность в ARGOS', 'патч ARGOS', 'rollback скил'."
---

# ARGOS Skill Evolution

ARGOS has two ways to add new skills at runtime — no restart needed.

## Method 1: TGCodeInjector — Manual Code Patch

Best when: you have specific Python code to inject, want full control, or are patching an existing skill.

### Start the injector

```
запусти инжектор
```

This starts the `TGCodeInjector` Telegram bot.

### Inject a new skill

```
/code my_skill.py         → begin code input (send this command, then paste code)
# paste your code here
/end                      → save + inject (triggers ast.parse check + hot reload)
```

### Manage skills

```
/inject my_skill          → hot-load skill into core (if not already loaded)
/rollback my_skill        → revert to previous backup version
/skills                   → list all loaded skills
/status                   → injector status
/history                  → patch history log
```

### How it works internally

1. You send code to the Telegram bot
2. ARGOS validates syntax (`ast.parse`)
3. Backs up the existing file (if any) to `src/skills/backups/`
4. Saves new skill to `src/skills/`
5. Hot-reloads via `importlib.reload` — no restart needed

### Skill file structure

New skills go in `src/skills/`. They should be a Python module with a class. Example skeleton:

```python
class MySkill:
    """Brief description of what this skill does."""

    def __init__(self, core=None):
        self.core = core

    async def handle(self, message: str) -> str:
        # Process the incoming Telegram message
        return f"MySkill response to: {message}"

    # Add trigger keywords ARGOS should route to this skill
    TRIGGERS = ["my keyword", "другое слово"]
```

---

## Method 2: ArgosEvolution — AI-Generated Skills

Best when: you want ARGOS to write the skill for you from a description.

### Generate a skill

```
создай скил [описание]           → via AICoder (fast, uses Ollama locally)
напиши скил мониторинг YouTube   → AI generates + tests + saves
```

### How it works

1. ARGOS sends your description to Ollama (local) or cloud AI
2. AI writes Python code for the skill
3. ARGOS validates syntax → runs unit tests
4. If tests pass → skill is saved and loaded
5. If tests fail → AI retries with error context

### Module location

`src/skills/evolution/skill.py` → class `ArgosEvolution`

---

## Method 3: ArgosAutoUpdater — GitHub Sync

For pulling code updates from GitHub:

```
# In .env:
GITHUB_TOKEN=your_token

# ARGOS monitors its own repo
# On new commits → auto git pull + restart
```

Module: `src/argoss_evolver.py`

---

## Tips

**Naming:** Skill filenames should be `snake_case.py`. Class name should be `PascalCase`.

**Debugging:** If hot-reload fails, check `/history` — the injector logs what went wrong.

**Rollback is automatic:** Before any `/inject`, ARGOS backs up the current version. You can always run `/rollback skill_name` to undo.

**Combine methods:** Use ArgosEvolution to generate a draft, then use TGCodeInjector to refine it manually.

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
