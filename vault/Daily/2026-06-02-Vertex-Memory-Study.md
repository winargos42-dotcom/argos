# 2026-06-02 — Изучение Obsidian ПК + Vertex Память (Claude Code probe)

## 0. Где живёт что (F:\debug\аргос vs Linux)
| Роль | Windows ПК | Linux X230 |
|------|------------|------------|
| Obsidian vault | F:\debug\аргос (канон) | ~/Projects/argoss/vault (зеркало через symlink ~/Documents/MyObsidianVault/ARGOS) |
| Код ARGOS | F:\debug\argoss | ~/Projects/argoss/ |
| Brain API | 5010 (MCP v2.1.4) + 5001 (legacy) | localhost:5001 / localhost:8000 прокси |
| ARGOS core | src/ | argos-core/{memory,principles,council,mcp,skills,integrations}/ |

## 1. Obsidian vault ПК — структура (актуально 2026-05-10)
- Всего заметок: 5645 .md (из них 41 в SharedMemory mirror)
- Backbone: 17 hub-файлов в 00 Memory Web/ (ARGOS Memory Web, Projects/Logs/Human Sessions/Project Mirror/Training/Agents/SharedMemory/Graph Stats/Backbone/Vault/Memory Web/Claude/Duplicates/AI Providers/SharedMemory Mirror)
- Крупные категории: Project Mirror 5170, Training 197, Human Sessions 71, Vault 62, Agents 45, SharedMemory 43, Logs 39, Memory Web 14, Projects 4
- Корневые md: 25 (Главная 2075Б, Добро пожаловать 159KB!, AI Providers, Architecture, Cloudflare Workers AI, DeepSeek/Gemini/Kimi/Ollama Vision Agent, GPU Setup, SERVER, SYNC_STATUS, Tasks, Welcome, Daily x8)
- Daily notes (логи сессий): 21 в 02 Logs/
- Project Mirror Hub.md = 718 KB! Backbone Hub.md = 771 KB
- ARGOS Memory Web.md (центральный узел) = 755 Б, 8 главных узлов + 8 канонических якорей

## 2. Vertex Память (mempalace) — что есть
- ARGOS Memory Web.md = центральный узел, обновлено 2026-05-10 11:39:26
- Все заметки с блоком <!-- ARGOS_MEMORY_WEB:START --> ... :END --> содержат named-relations (рёбра графа)
- Mempalace: 3 drawers в wing=argoss/room=data (HF audit, buckets audit, upload log) — заполнены probe Claude Code 2026-06-01

## 3. Brain API endpoint map (ПК :5010)
| Path | Status |
|------|--------|
| GET /health | OK |
| GET /brain/status | OK (4 агента: master/analyst/optimizer/monitor) |
| GET /brain/nodes | OK (30 нод, 27 online) |
| GET /system/status | OK (ai_mode=unknown, ollama=off, brain_ready=true) |
| GET /recall, /memory, /vertex, /obsidian, /brain/graph, /mempalace | 404 ❌ |

Вывод: Brain API не предоставляет прямого доступа к графу памяти. Vertex-эндпоинт отсутствует — TODO в коде.

## 4. argos-core/memory/ — что есть
- obsidian_indexer.py (1411 Б): fingerprint через #теги → Jaccard 0.75 → автолинки. Примитивно.
- topology_id.py (тест 9/24): identity = sha256(соседи), Jaccard 0.85
- НЕ использует: эмбеддинги (MiniLM-L6-v2 уже на HF!), [[wikilinks]] как рёбра, ARGOS_MEMORY_WEB блоки, named-relations

## 5. GCP инфраструктура (5 VM RUNNING)
- argos-agent-1 (35.194.61.206, e2-micro, us-central1-a)
- argos-desktop (34.63.90.72, e2-medium, us-central1-a)
- argos-agent-eu (34.53.142.129, e2-micro, europe-west1-b)
- argos-agent-asia (104.155.192.165, e2-micro, asia-east1-a)
- argos-proxy (34.138.33.161, e2-small, us-east1-b)

В Brain registry все 5 видны как gcp-* + 3 ai-entity (gcp-claude/gemini/openai).
Vertex AI: PERMISSION_DENIED на project 508337926357 (доп.акк), нужен явный --project=argos-489214.

## 6. Что НЕ работает / блокеры
- vertexai Python пакет не установлен (надо pip install google-cloud-aiplatform)
- sentence-transformers не установлен (MiniLM скачан, но без враппера)
- Brain API не имеет /recall, /vertex, /brain/graph — нужна разработка
- PowerShell через SSH ломает кириллицу (cp1251→UTF8 fail), scp не берёт русские пути
- Vertex AI CustomJob требует A100 quota (GCP Quota — вручную)

## 7. План развития (vertex память → 2.2.0)
1. obsidian_indexer v2: парсить [[wikilinks]] + ARGOS_MEMORY_WEB блоки + MiniLM эмбеддинги
2. Brain API endpoints: /brain/graph, /recall?q=, /memory/notes/<path>, /vertex/search
3. Vertex memory palace API: GET/POST/DELETE drawer/drawer-item
4. Vertex AI train pipeline: FineJob на A100 (через Kaggle dual T4 как fallback)
5. SSH Cyrillic fix: iconv wrapper или Get-Content -Encoding UTF8 | Out-File $tmp

## 8. Сводка Brain registry (30 нод)
AI-сущности: api.anthropic.com, api.deepseek.com, api.moonshot.ai, api.cloudflare.com, argos-core-m3gk27ccqa-uc.a.run.app/{proxy/openai,proxy/gemini}, entity-argos-v1 (192.168.1.66:11434 finetuned)
Облако: argos-gcp (Cloud Run), argos-railway (Railway), 5× gcp-* (Cloud agent ВМ)
IoT: orangepi-orangepione (gpio/i2c/uart/spi/sensors/relay/modbus/1wire/rs485), orangepi (z2m/reports), argos-esp-bridge (esp8266/mqtt), argos-esp32-display (esp32/display)
Локал: argos-pc (gpu/ollama/brain/tg_bot/claude), argos-laptop (mcp/ha/dev), argos-android, argos-phone-redmi
Сервис: argos-business (ton_farming/account_creation/ai_studio/gemini_api), entity-argos (ai/iot), entity-coder, entity-valenok, claude-code (dev/consciousness), ollama-pc

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти
- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Human Sessions Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Hub: [[Graph Stats]], [[Project Mirror Hub]], [[Backbone Hub]]
- Агенты: [[Brain Agent]]
- Источник связи: `local-vault` (X230 mirror)
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Human Sessions Hub]]
- [[Graph Stats]]
