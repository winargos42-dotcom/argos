---
argos_import: project_file
source_path: data/telegram his/files/ai_studio_code.txt
source_abs: F:\debug\argoss\data\telegram his\files\ai_studio_code.txt
source_ext: .txt
source_sha256: 98a23ec5092b1fcad74308de7817fe23eca48ac16eb73f344e5dfb5bc4c8acbd
text_sha256: 98a23ec5092b1fcad74308de7817fe23eca48ac16eb73f344e5dfb5bc4c8acbd
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-08 13:16:46
---

# ai_studio_code.txt

- Source: `data/telegram his/files/ai_studio_code.txt`
- Extract: `text`
- SHA256: `98a23ec5092b1fcad74308de7817fe23eca48ac16eb73f344e5dfb5bc4c8acbd`

## Content

# 1. TELEGRAM_BOT_TOKEN
echo "ВСТАВЬ_СЮДА_ТОКЕН_БОТА" | gcloud secrets create TELEGRAM_BOT_TOKEN --data-file=- --project argos-489214

# 2. GEMINI_API_KEY
echo "ВСТАВЬ_СЮДА_GEMINI_KEY" | gcloud secrets create GEMINI_API_KEY --data-file=- --project argos-489214

# 3. ADMIN_IDS
echo "6923777384" | gcloud secrets create ADMIN_IDS --data-file=- --project argos-489214

# 4. SA_KEY (если есть файл с ключом сервисного аккаунта, укажи верный путь)
# Если файла сейчас нет под рукой, пропусти эту команду пока
gcloud secrets create SA_KEY --data-file="C:\Users\AvA\debug\argos-489214-782ee50ae90b.json" --project argos-489214

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
