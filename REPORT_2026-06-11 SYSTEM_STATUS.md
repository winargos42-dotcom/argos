# ARGOS System Status Report
**Дата:** 2026-06-11 17:55 UTC+10  
**Ноутбук:** archlinux (192.168.1.53)  
**PC Brain:** Orion (192.168.1.72:5001)  

---

## 📊 Текущее состояние системы

### ARGOS Brain (PC Orion - Master)
- **URL:** http://192.168.1.72:5001
- **Версия:** ARGOS AI Brain API v2.0.0
- **Статус:** ✅ Работает
- **Узлы:** 25 online из 26 (P2P сеть: 26 online из 26)
- **Агенты:** 4 зарегистрировано
- **ОПЕРАЦИОННАЯ СИСТЕМА:** Работает, brain_ready: true

### P2P Network Status
```
Total nodes: 26
Online: 26
Offline: 0
```

### Основные узлы
| Node ID | Address | Status | Type | Capabilities |
|---------|---------|--------|------|--------------|
| argos-pc | 192.168.1.72:5001 | online | brain | gpu, ollama, brain, tg_bot, claude |
| argos-laptop | 192.168.1.53:8000 | online | mcp | ha, dev |
| orangepi | 192.168.2.168:7777 | online | iot | z2m, reports |
| argos-railway | argos-v2-production.up.railway.app | online | cloud | |
| argos-gcp | argos-core-m3gk27ccqa-uc.a.run.app | online | cloud | openai, gemini |
| argos-esp-bridge | 192.168.1.181 | online | device | esp8266, mqtt |
| argos-esp32-display | 192.168.1.211 | online | device | esp32, display |
| argos-phone-redmi | - | online | mobile | |
| ollama-pc | - | online | ai | local |
| entity-claude | api.anthropic.com | online | ai | claude |
| entity-deepseek | api.deepseek.com | online | ai | ai |
| entity-kimi | api.moonshot.ai | online | ai | ai |
| entity-openai | argos-core-m3gk27ccqa-uc.a.run.app/proxy/openai | online | ai | ai |
| entity-gemini | argos-core-m3gk27ccqa-uc.a.run.app/proxy/gemini | online | ai | ai |
| entity-cloudflare | api.cloudflare.com | online | ai | ai |
| entity-argos | 192.168.1.72:5001 | online | ai | iot |

---

## 🌐 Network Infrastructure

### Tailscale Status
- **Ноутбук (archlinux):** ✅ Подключен (100.122.48.115)
- **Redmi Note 13:** ⚠️ Offline (100.70.169.37, last seen 19h ago)
- **PC Orion (Windows):** ❌ Не подключен к Tailscale
- **Action:** Установить Tailscale на Windows PC с https://tailscale.com/download/windows

### MQTT Broker
- **Брокер:** mosquitto на ноутбуке (192.168.1.53:1883)
- **Статус:** ✅ Работает
- **ESP Bridge:** Подключен к MQTT (argos-esp-bridge/#)
- **ESP Display:** Подключен к MQTT (argos/esp-display/#)

### Local Network
- **Gateway:** 192.168.1.111
- **Ноутбук IP:** 192.168.1.53
- **PC IP:** 192.168.1.72
- **ESP Bridge IP:** 192.168.1.181
- **ESP Display IP:** 192.168.1.211
- **Orange Pi:** 192.168.2.168 (другая подсеть)

---

## 📦 Установленное ПО

### На ноутбуке (archlinux)
- ✅ Python 3.14
- ✅ ARGOS Brain API
- ✅ Mosquitto MQTT Broker
- ✅ ESP Display Manager
- ✅ MQTT Publishers (unified, ha)
- ✅ Tailscale
- ✅ agent-squad (v1.0.2)
- ❌ OpenCV (не установлен - externall-managed environment)

### На PC Orion (Windows)
- ✅ ARGOS Brain Master
- ✅ Ollama
- ✅ Docker
- ❌ Tailscale (нужно установить)

---

## 🎯 Интеграции для выполнения

### 1. Tailscale Integration ✅ PARTIAL
- [x] Установлен на ноутбуке
- [ ] Установить на Windows PC
- [ ] Проверить подключение всех устройств
- [ ] Настроить P2P через Tailscale для удаленного доступа

### 2. Cubbit Workspace Integration ⏳ TODO
- **Workspace ID:** be544a2c-4f35-466e-a4be-b05b53ab7bda
- **URL:** https://console.trial.cubbit.eu/workspace/projects/
- **Action:** 
  - Создать Cubbit client для ARGOS
  - Интегрировать с ARGOS Brain как cloud storage
  - Настроить синхронизацию файлов

### 3. Bubble.io Projects Integration ⏳ TODO
- **URL:** https://bubble.io/home/projects
- **Action:**
  - Изучить текущие Bubble.io проекты
  - Создать API интеграцию с ARGOS Brain
  - Настроить вебхуки для событий

### 4. OpenCV Integration ⏳ TODO
- **Status:** Не установлен
- **Action:**
  - Установить opencv-python-headless через pip с --break-system-packages
  - Или настроить venv для ARGOS
  - Интегрировать с agent-squad для компьютерного зрения

### 5. ESP Dongle Integration ✅ WORKING
- **argos-esp-bridge (ESP8266):** ✅ Online, MQTT работа
- **argos-esp32-display (ESP32):** ✅ Online, дисплей работа
- **MQTT Broker:** ✅ Работает на ноутбуке
- **ESP Display Manager:** ✅ Скрипт есть, нужно запустить

---

## 🔧 Выявленные проблемы из чатов Telegram

### Из ChatExport_2026-06-11:

1. **Knowledge Base Explosion** (02.05 → 03.05)
   - Факты: 35 → 7916
   - Заметки: 0 → 912
   - Рёбра: 86 → 15143
   - **Status:** ✅ Восстановление памяти выполнено

2. **Infrastructure Scale**
   - Ноды: 22 (16 ПК + 6 ноут) → упало до 18 к 03.06
   - **Current:** 25 узлов online (улучшилось!)
   
3. **System Load Issues**
   - **Ноутбук X230:** RAM 94-100%, CPU 100% ⚠️ **БУТЫЛОЧНОЕ ГОРЛЫШКО!**
   - **ПК Орион:** CPU 12-67%, RAM ~40% ✅ Стабильно
   
4. **Council Activity (июнь)**
   - 1844 сообщения за 8 дней
   - 32% сообщений с ошибкой Brain:❌ (593 шт)
   - **Action:** Исследовать почему 32% ошибок

5. **FPGA Integration**
   - Репозиторий: m2-artix7-accelerator-card
   - Целевая плата: XC7A35T-CSG325
   - **Action:** Адаптировать constraints под SPR2801/XC7A35T

6. **Railway Deployment**
   - ARGOS deployed: argos-v2-production.up.railway.app
   - **Problem:** Токен project-scoped, account shows 0 проектов
   - **Action:** Использовать правильные токены

---

## 📚 API Ключи (из .env на Orion)

| Сервис | Статус | Примечания |
|--------|--------|------------|
| Railway | ✅ | Account-wide, но 0 проектов на winargos42-dotcom |
| HuggingFace | ✅ | 2 токена, read+write |
| OpenAI | ✅ | GPT-4, GPT-4o |
| Anthropic | ✅ | Claude |
| DeepSeek | ✅ | Работает |
| Gemini | ✅ | 8 ключей, ротация |
| Azure OpenAI | ✅ | Endpoint + key |
| xAI/Grok | ✅ | Работает |
| Kimi/Moonshot | ✅ | Работает |
| IBM Watsonx | ✅ | Ключ есть |
| IBM Quantum | ✅ | Ключ есть, но только 3 джобы в quantum_seed.json |
| Cloudflare | ✅ | Ключ есть |
| Shodan | ✅ | Ключ есть |
| SerpAPI | ✅ | Ключ есть |
| TonCenter | ✅ | Ключ есть |
| Telegram | ✅ | Ключ есть |

**Отсутствующие:**
- Groq
- Together AI
- Fireworks
- Mistral
- OpenRouter
- Replicate
- Cohere

---

## 🎯 План действий (Priorities)

### P0 - Критические задачи
1. **Нагрузка на ноутбук**
   - Ноутбук X230: RAM 94-100%, CPU 100%
   - **Action:** Перенести часть нагрузки на PC Orion или ESP устройства
   
2. **32% ошибок Brain**
   - Исследовать почему 593 сообщения из 1844 с ошибкой
   - **Action:** Проверить логи Brain API на PC Orion

### P1 - Интеграции
1. **Tailscale на Windows PC**
   - Скачать: https://tailscale.com/download/windows
   - Установить и авторизоваться
   - Проверить подключение к Tailnet
   
2. **OpenCV установка**
   ```bash
   python -m pip install --break-system-packages opencv-python-headless
   # или
   sudo pacman -S python-opencv
   ```

3. **Cubbit Integration**
   - Изучить API Cubbit
   - Создать клиент для ARGOS
   - Интегрировать как cloud storage в Brain
   
4. **Bubble.io Integration**
   - Получить доступ к проектам
   - Изучить API
   - Создать вебхуки для ARGOS событий

### P2 - Улучшения
1. **FPGA Адаптация**
   - Адаптировать m2-artix7-accelerator-card под XC7A35T-CSG325
   - Создать constraints файлы для CSG325
   
2. **ESP Display Manager**
   - Запустить скрипт esp_display_manager.py
   - Проверить отображение на OLED
   
3. **MQTT Monitor**
   - Настроить мониторинг MQTT топиков
   - Логировать сообщения от ESP устройств

### P3 - Документация
1. **Обновить Obsidian Vault**
   - Добавить информацию о текущем состоянии
   - Зафиксировать интеграции
   - Документировать API ключи

---

## 📈 Метрики производительности (из отчетов)

### Knowledge Growth
- **02.05:** 35 фактов, 0 заметок, 86 рёбер
- **03.05:** 7916 фактов (+225x), 912 заметок, 15143 рёбер (+175x)
- **Рост:** Экспоненциальный рост после восстановления памяти

### Council Statistics (июнь, 8 дней)
- **Всего сообщений:** 1844
- **Пик:** 276 сообщений (06.06)
- **Минимум:** 127 сообщений (08.06)
- **Среднее:** ~230 сообщений/день
- **Ошибки:** 593 (32%)

### System Load
- **Ноутбук:** RAM 94-100%, CPU 100% (критично!)
- **ПК:** CPU 12-67%, RAM ~40% (нормально)

---

## 🔗 Ссылки и ресурсы

### ARGOS
- Brain API: http://192.168.1.72:5001
- Railway Deployment: https://argos-v2-production.up.railway.app
- GCP Endpoint: https://argos-core-m3gk27ccqa-uc.a.run.app

### Облачные сервисы
- Tailscale: https://tailscale.com/download/windows
- Cubbit Console: https://console.trial.cubbit.eu/workspace/projects/be544a2c-4f35-466e-a4be-b05b53ab7bda
- Bubble.io: https://bubble.io/home/projects
- OpenCV: https://github.com/opencv/opencv

### Документация
- Obsidian Vault: /home/ava/Projects/argoss/vault/
- Telegram Chat Export: /home/ava/Downloads/Telegram Desktop/ChatExport_2026-06-11/
- ESP Configs: /home/ava/Projects/argoss/vault/configs/
- ESPHome Config: /home/ava/Projects/argoss/esphome/argos-esp32-display.yaml

---

## ✅ Выполненные задачи (из предыдущей сессии)

- [x] PC Brain как master (192.168.1.72:5001)
- [x] Ноутбук использует PC Brain (localhost:5001 отключен)
- [x] Исправлены интервалы heartbeat: 900s→30s
- [x] Заменены localhost:5001 на 192.168.1.72:5001 на ноутбуке
- [x] Заменены 192.168.1.66→192.168.1.72 на PC
- [x] argos-entity-valenok.service: перезапущен с 30s heartbeat
- [x] argos-business.service: перезапущен с background heartbeat thread

---

## 📌 Следующие шаги (Immediate Actions)

1. **Установить Tailscale на Windows PC**
   - Скачать и установить: https://tailscale.com/download/windows
   - Авторизоваться с тем же аккаунтом (winargos42@gmail.com)
   
2. **Запустить ESP Display Manager**
   ```bash
   cd /home/ava/Projects/argoss
   python scripts/esp_display_manager.py
   ```
   
3. **Установить OpenCV**
   ```bash
   python -m pip install --break-system-packages opencv-python-headless
   ```

4. **Исследовать 32% ошибок Brain**
   - Проверить логи на PC Orion
   - Проверить, какие модели/провайдеры дают ошибки

5. **Создать интеграцию Cubbit**
   - Изучить API
   - Создать модуль для ARGOS Brain

---

**Отчет создан:** 2026-06-11 18:00 UTC+10  
**Следующий отчет:** После выполнения P0 и P1 задач
