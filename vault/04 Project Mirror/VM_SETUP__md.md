---
argos_import: project_file
source_path: VM_SETUP.md
source_abs: F:\debug\argoss\VM_SETUP.md
source_ext: .md
source_sha256: 0317ef1f29e6bdb4922c85018b58f78762ae987f742eac10dc7f46afb5901e28
text_sha256: 0317ef1f29e6bdb4922c85018b58f78762ae987f742eac10dc7f46afb5901e28
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# VM_SETUP.md

- Source: `VM_SETUP.md`
- Extract: `text`
- SHA256: `0317ef1f29e6bdb4922c85018b58f78762ae987f742eac10dc7f46afb5901e28`

## Content

# Проверка и настройка Ollama на VM

## Australia VM (argos@argos-vm)

```bash
# 1. Проверить статус (warning нормально)
sudo systemctl status ollama

# 2. Если не запущена:
sudo systemctl start ollama

# 3. Настроить на всех интерфейсах:
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo tee /etc/systemd/system/ollama.service.d/override.conf << 'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
EOF

sudo systemctl daemon-reload
sudo systemctl restart ollama

# 4. Открыть порт (если ufw не работает, используй iptables)
sudo iptables -I INPUT -p tcp --dport 11434 -j ACCEPT

# 5. Проверить локально:
curl http://localhost:11434/api/tags
```

## Japan VMs

Аналогично для:
- `argos@argos-vm-B2FSB9` (40.81.208.101)
- `argos@argos-vm-jp_079c3df3` (172.207.209.134)

## Исправление warning sudo

```bash
# Добавить hostname в /etc/hosts
echo "127.0.0.1 $(hostname)" | sudo tee -a /etc/hosts
```

После настройки все 4 VM должны отвечать на порту 11434.

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
