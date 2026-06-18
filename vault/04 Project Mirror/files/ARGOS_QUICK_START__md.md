---
argos_import: project_file
source_path: files/ARGOS_QUICK_START.md
source_abs: F:\debug\argoss\files\ARGOS_QUICK_START.md
source_ext: .md
source_sha256: 2acbbba12ad2ec8aaa8f0ee2c0434153bf96f296b39c9c838ea1dc6406ccabe2
text_sha256: 2acbbba12ad2ec8aaa8f0ee2c0434153bf96f296b39c9c838ea1dc6406ccabe2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# ARGOS_QUICK_START.md

- Source: `files/ARGOS_QUICK_START.md`
- Extract: `text`
- SHA256: `2acbbba12ad2ec8aaa8f0ee2c0434153bf96f296b39c9c838ea1dc6406ccabe2`

## Content

# ⚡ ARGOS QUICK START GUIDE - ФИНАЛЬНЫЙ РЕЛИЗ

## 🎯 ТРИ ШАГА К ЗАПУСКУ

### ШАГИ ЧТОБЫ ПОЛУЧИТЬ ПОЛНОСТЬЮ РАБОЧУЮ СЕТЬ

---

## 1️⃣ ЗАПУСК JAPAN VM 2

**⏱️ Время: 2-3 минуты**

```powershell
# PowerShell / Terminal
az vm run-command invoke `
  --resource-group rg-argos `
  --name argos-vm-jp_079c3df3 `
  --command-id RunShellScript `
  --scripts "cd /home/ava/argoss && unzip -o src.zip && nohup python3 main.py --no-gui > argos.log 2>&1 &"
```

**Проверка статуса:**
```bash
# Проверить логи
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_079c3df3 \
  --command-id RunShellScript --scripts "tail -20 argos.log"
```

✅ **Готово когда:** Вы увидите в логах `[ARGOS] Started successfully`

---

## 2️⃣ НАСТРОЙКА P2P СОЕДИНЕНИЙ

**⏱️ Время: 3-5 минут**

Откройте **ARGOS консоль на локальном ПК**:

```bash
# Если ARGOS не запущен:
python main.py

# Если запущен, откройте консоль:
# Нажмите Enter в окне ARGOS
```

Выполните команды:

```
# Добавить все Azure узлы
p2p add 20.53.240.36:8000
p2p add 40.81.208.101:8000
p2p add 172.207.209.134:8000

# Проверить соединение
p2p list
```

✅ **Готово когда:**
```
Connected Peers: 3/3
├─ 20.53.240.36:8000 → ONLINE
├─ 40.81.208.101:8000 → ONLINE
└─ 172.207.209.134:8000 → ONLINE
```

---

## 3️⃣ ПРОВЕРКА ВСЕЙ СЕТИ

**⏱️ Время: 2-3 минуты**

### В ARGOS консоли:

```
# Полный статус
p2p status

# Информация о сети
network info

# Статистика
stats
```

### В PowerShell/Terminal:

```bash
# Google Cloud
curl https://argos-core-508337926357.us-central1.run.app/health

# Australia VM
curl http://20.53.240.36:8000/health

# Japan VM 1
curl http://40.81.208.101:8000/health

# Japan VM 2
curl http://172.207.209.134:8000/health
```

✅ **Готово когда:** Все запросы возвращают `{"status": "online"}`

---

## 📊 ТЕКУЩЕЕ СОСТОЯНИЕ

| Компонент | IP/URL | Статус |
|-----------|--------|--------|
| 🖥️ Локальный ПК | 127.0.0.1:5000 | ✅ РАБОТАЕТ |
| ☁️ Google Cloud | argos-core-....run.app | ✅ РАБОТАЕТ |
| 🇦🇺 Australia | 20.53.240.36:8000 | ✅ РАБОТАЕТ |
| 🇯🇵 Japan 1 | 40.81.208.101:8000 | ✅ РАБОТАЕТ |
| 🇯🇵 Japan 2 | 172.207.209.134:8000 | 🚧 ЗАПУСКАЕТСЯ |

---

## 🚨 ВОЗМОЖНЫЕ ПРОБЛЕМЫ & РЕШЕНИЯ

### Проблема: "ModuleNotFoundError: No module named 'db_init'"
**Решение:**
```bash
# Убедитесь что вы в правильной директории
cd /path/to/argoss

# Установите зависимости
pip install -r requirements.txt

# Запустите с флагом --full
python main.py --full
```

### Проблема: P2P узлы не подключаются
**Решение:**
```
# В ARGOS консоли:
p2p debug on

# Попробуйте добавить с явным timeout
p2p add 20.53.240.36:8000 --timeout 30

# Проверьте firewall правила
```

### Проблема: Google Cloud недоступен
**Решение:**
```bash
# Проверьте статус сервиса
gcloud run services describe argos-core --region us-central1

# Посмотрите логи
gcloud run services logs read argos-core --region us-central1
```

### Проблема: "Connection refused" для Azure VMs
**Решение:**
```bash
# Проверьте Network Security Groups
az network nsg list --resource-group rg-argos

# Убедитесь что порт 8000 открыт
az network nsg rule list --resource-group rg-argos --nsg-name argos-nsg
```

---

## 📋 ЧЕКЛИСТ ПЕРЕД ПРОИЗВОДСТВОМ

- [ ] ✅ Все 3 шага выше выполнены
- [ ] ✅ P2P статус показывает все узлы ONLINE
- [ ] ✅ `network info` показывает корректное состояние
- [ ] ✅ Тестовый запрос через API успешен
- [ ] ✅ Логи не содержат ошибок
- [ ] ✅ Резервные копии базы данных сделаны
- [ ] ✅ Мониторинг включен
- [ ] ✅ Команда в курсе о деплое

---

## 🎮 ОСНОВНЫЕ КОМАНДЫ ARGOS

```
# Статус и информация
p2p status              # P2P сетевой статус
p2p list               # Список подключённых узлов
network info           # Информация о сети
stats                  # Статистика системы

# Управление
p2p add IP:PORT        # Добавить узел
p2p remove IP:PORT     # Удалить узел
p2p connect IP:PORT    # Явно подключиться
shutdown --clean       # Чистое завершение

# Отладка
p2p debug on/off       # Включить отладку
p2p ping IP:PORT       # Проверить задержку
network test           # Тест сети
```

---

## 📞 КОНТАКТЫ И ПОДДЕРЖКА

- **Документация:** `/mnt/skills/public/*`
- **Логи:** `~/.argos/logs/`
- **Конфиг:** `~/.argos/config.json`
- **Скрипты:** `argos_final_setup.sh`, `argos_release_checklist.sh`

---

## 🎉 ФИНАЛЬНОЕ СОСТОЯНИЕ

После выполнения всех 3 шагов у вас будет:

```
✅ 5 АКТИВНЫХ УЗЛОВ:
   • Локальный мастер-узел (Windows)
   • Google Cloud Run (Public API)
   • Azure Australia (Восточная Австралия)
   • Azure Japan 1 (Восток Японии)
   • Azure Japan 2 (Запад Японии)

✅ ПОЛНОСТЬЮ РАБОТАЮЩАЯ P2P СЕТЬ
✅ РАСПРЕДЕЛЁННАЯ АРХИТЕКТУРА
✅ ГОТОВНОСТЬ К МАСШТАБИРОВАНИЮ
✅ PRODUCTION-READY
```

---

**Время на запуск:** ~10-15 минут  
**Сложность:** ⭐⭐ (Простой)  
**Статус:** 🟢 ГОТОВ К РЕЛИЗУ

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
