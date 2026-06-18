---
argos_import: project_file
source_path: C2_SETUP.md
source_abs: F:\debug\argoss\C2_SETUP.md
source_ext: .md
source_sha256: 4ca97444728cdb9ede95799b1c3fb7e19901762155a25cf65366f229ed5fc133
text_sha256: 4ca97444728cdb9ede95799b1c3fb7e19901762155a25cf65366f229ed5fc133
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# C2_SETUP.md

- Source: `C2_SETUP.md`
- Extract: `text`
- SHA256: `4ca97444728cdb9ede95799b1c3fb7e19901762155a25cf65366f229ed5fc133`

## Content

# C2/Ghost Command Setup
Настройка командования для Argos Swarm

## Быстрый старт

### 1. Создай GitHub Gist (бесплатный C2 сервер)
1. Открой https://gist.github.com
2. Создай новый gist (можно пустой)
3. Скопируй Gist ID из URL
4. Создай GitHub Token: https://github.com/settings/tokens
   - Разрешения: gist

### 2. Настрой .env

Добавь в .env на ВСЕХ узлах:
```env
ARGOS_GIST_ID=your_gist_id
ARGOS_GITHUB_TOKEN=your_token
GHOST_C2_ENABLED=true
```

### 3. Команды Ghost

Через Telegram бота:
```
ghost status          # статус всех узлов
ghost cmd ls -la      # выполнить команду на всех узлах
ghost deploy          # деплой на все узлы
ghost backup          # бэкап со всех узлов
```

### 4. Проверка связи

```bash
curl https://api.github.com/gists/YOUR_GIST_ID
```

## Архитектура

```
[ПК] ←→ [GitHub Gist] ←→ [Azure VM]
  ↑                        ↓
[Telegram] ←────────── [Phone]
```

## Безопасность

- Все команды подписываются ключом
- Шифрование через GPG
- Fallback каналы: P2P прямое соединение

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
