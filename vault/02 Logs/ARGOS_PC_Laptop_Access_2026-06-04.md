# ARGOS — доступ ПК→ноутбук настроен + интеграция систем — 2026-06-04

## Задача
Настроить доступ с ПК Orion на ноутбук X230 и интегрировать в работу всех систем
(чтобы снять блокеры "не мой доступ" — Hermes на ноутбуке и т.д.).

## Что сделано
### SSH доступ Orion→ноутбук — НАСТРОЕН
- Ноутбук: X230 Arch Linux, 192.168.1.53, юзер **ava** (не AvA — был неверный регистр!)
- Ключ `~/.ssh/id_ed25519` (PC-to-laptop-20260603) уже авторизован на ноутбуке.
- Создан `~/.ssh/config` с alias: **argos-laptop** (он же laptop, x230):
  ```
  Host argos-laptop laptop x230
      HostName 192.168.1.53
      User ava
      IdentityFile ~/.ssh/id_ed25519
  ```
- Проверка: `ssh argos-laptop` → archlinux, работает.

### Системы ноутбука (видны через доступ)
- Hermes config: `~/.hermes/config.yaml`
- OSINT skill (Hermes начал): `~/.hermes/skills/osint-recon/` (SKILL.md, osint_tools.py, mcp_tools_spec.yaml)
- ARGOS brain :5001 — работает (ноды: orangepi)
- Ollama модели: minimax-m3:cloud, argos-v2, argos-v1, qwen2.5:0.5b, llama3.1:8b

### Блокер #3 РЕШЁН (Hermes compression)
Причина постоянной ошибки "Auxiliary compression model ... 32768 < 64000":
- было `model: qwen2.5:0.5b` (реальный контекст 32K) — Hermes детектит 32K < 64K и падает,
  несмотря на `context_length: 64000` override.
ФИКС (применён через SSH, с коррекцией):
- Сначала `qwen2.5:0.5b` → `llama3.1:8b` (128K). Но llama3.1 ЛОКАЛЬНАЯ — грузит слабый X230.
- КОРРЕКЦИЯ (Hermes работает на Ollama Cloud + Nemo ARGOS): compression →
  **`kimi-k2.6:cloud`** (256K, Ollama Cloud) — не грузит X230, та же модель что основная.
- Проверены контексты: argos-v2(Nemo)=32K (НЕ годится!), kimi-k2.6:cloud=256K,
  minimax-m3:cloud=512K, llama3.1:8b=128K.
- Бэкапы: config.yaml.bak_20260604_201921, .bak_20260604_202947.
- НАДО: перезапустить Hermes (/reset в Telegram) чтобы подхватил.

## V100 Nemo модель → Hermes (туннель/доступ)
Hermes должен иметь доступ к модели на V100 (Tesla V100 на Orion).
- V100 :8085 на Orion жив: модель `mistral-nemo-instruct-2407.Q4_K_M.gguf` (Nemo ARGOS).
- Ноутбук видит V100 по ПРЯМОМУ LAN (192.168.1.66:8085) — Cloudflare-туннель не нужен в LAN.
- Добавлен провайдер в Hermes config (`providers.v100-nemo`):
  ```
  v100-nemo:
      api: http://192.168.1.66:8085/v1
      default_model: mistral-nemo-instruct-2407.Q4_K_M.gguf
      name: V100 Nemo ARGOS (Orion)
  ```
- Живой тест: V100 chat ответил → endpoint рабочий.
- Hermes может /model на mistral-nemo (провайдер v100-nemo).
- Если нужен ВНЕШНИЙ доступ (вне LAN) — отдельно поднять Cloudflare туннель v100-pc.argosssss.win.

## Статус
- [x] SSH доступ Orion→ноутбук (alias argos-laptop, юзер ava)
- [x] Интеграция: все системы ноутбука видны через SSH
- [x] Блокер #3 (Hermes compression) → kimi-k2.6:cloud (Ollama Cloud, 256K)
- [x] V100 Nemo добавлена в Hermes как провайдер v100-nemo (LAN endpoint, тест прошёл)
- [ ] Перезапустить Hermes (пользователь — /reset в Telegram)
- [ ] OSINT (#2): osint_tools.py на ноутбуке — интегрировать в ARGOS
- [ ] GPU-кластер (#5): OLLAMA_GPU_MODE=on

## Заметка
Доступ argos-laptop теперь рабочий — можно править/проверять ноутбук с Orion напрямую.
Снимает все блокеры "на ноутбуке, не мой доступ".
