---
argos_import: project_file
source_path: simple_install.txt
source_abs: F:\debug\argoss\simple_install.txt
source_ext: .txt
source_sha256: 9824c63ba60a9bb5714e4d1de253afb075a1b4d7923f172a53782c335318497b
text_sha256: 9824c63ba60a9bb5714e4d1de253afb075a1b4d7923f172a53782c335318497b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# simple_install.txt

- Source: `simple_install.txt`
- Extract: `text`
- SHA256: `9824c63ba60a9bb5714e4d1de253afb075a1b4d7923f172a53782c335318497b`

## Content

Команды для Japan VM 2:

1. Распаковать ARGOS:
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_079c3df3 --command-id RunShellScript --scripts "cd /home/ava/argoss && unzip -o src.zip"

2. Проверить файлы:
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_079c3df3 --command-id RunShellScript --scripts "cd /home/ava/argoss && ls -la"

3. Запустить ARGOS:
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_079c3df3 --command-id RunShellScript --scripts "cd /home/ava/argoss && nohup python3 main.py --no-gui > argos.log 2>&1 &"

4. Проверить запуск:
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_079c3df3 --command-id RunShellScript --scripts "ps aux | grep python | grep -v grep"

5. Проверить порт:
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_079c3df3 --command-id RunShellScript --scripts "curl -s http://localhost:8000/health 2>/dev/null || echo 'Жди 30 секунд'"

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
