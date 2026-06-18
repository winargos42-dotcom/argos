---
argos_import: project_file
source_path: requirements-brain.txt
source_abs: F:\debug\argoss\requirements-brain.txt
source_ext: .txt
source_sha256: fa465be9ad508116df6a6b1ddf63944deb0da96b84aafdeeaa7e8679e7b9995f
text_sha256: fa465be9ad508116df6a6b1ddf63944deb0da96b84aafdeeaa7e8679e7b9995f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# requirements-brain.txt

- Source: `requirements-brain.txt`
- Extract: `text`
- SHA256: `fa465be9ad508116df6a6b1ddf63944deb0da96b84aafdeeaa7e8679e7b9995f`

## Content

# ARGOS AI Brain — dependencies
# Установка:  pip install -r requirements-brain.txt
#
# Пакет `azure-ai-openai` НЕ существует на PyPI. Класс AzureOpenAI лежит
# в пакете `openai` (>=1.0). Это совместимо с Azure OpenAI endpoints.

openai>=1.0.0
flask>=2.2
flask-cors>=4.0
aiohttp>=3.9
python-dotenv>=1.0
requests>=2.31

# Опциональные — используются в argos_brain_examples и для аналитики.
# Если проект уже ставит их через requirements.txt, можно оставить как есть.
pandas>=2.0
numpy>=1.24

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
