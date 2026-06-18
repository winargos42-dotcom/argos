---
argos_import: project_file
source_path: docs/skills.md
source_abs: F:\debug\argoss\docs\skills.md
source_ext: .md
source_sha256: eb82eef92de58d8e94238c327ea0fa459f9e82c6ea023162292b48165fbb96b9
text_sha256: eb82eef92de58d8e94238c327ea0fa459f9e82c6ea023162292b48165fbb96b9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:59
---

# skills.md

- Source: `docs/skills.md`
- Extract: `text`
- SHA256: `eb82eef92de58d8e94238c327ea0fa459f9e82c6ea023162292b48165fbb96b9`

## Content

# Developer Guide: Как писать новые навыки (плагины)

ARGOS поддерживает два формата навыков:

1) Legacy: `src/skills/<name>.py`
2) Plugin v2: `src/skills/<name>/manifest.json` + `skill.py`

Рекомендуется использовать Plugin v2.

## Структура навыка v2

```text
src/skills/my_skill/
  manifest.json
  skill.py
  README.md
```

Пример `manifest.json`:

```json
{
  "name": "my_skill",
  "version": "1.0.0",
  "entry": "skill.py",
  "author": "you",
  "description": "Мой навык",
  "category": "custom",
  "dependencies": [],
  "permissions": ["network"]
}
```

Пример `skill.py`:

```python
TRIGGERS = ["мой навык", "my skill"]

def setup(core=None):
    pass

def handle(text: str, core=None) -> str | None:
    t = text.lower()
    if not any(tr in t for tr in TRIGGERS):
        return None
    return "✅ Навык сработал"

def teardown():
    pass
```

## Подключение навыка

- Автозагрузка: через `SkillLoader` при старте.
- Ручное управление:
  - `загрузи навык my_skill`
  - `перезагрузи навык my_skill`
  - `выгрузи навык my_skill`

## Рекомендации

- Возвращай `None`, если команда не относится к навыку.
- Не выполняй опасные действия без явного подтверждения пользователя.
- Держи логику навыка независимой и тестируемой.

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
