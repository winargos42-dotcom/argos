# 🔱 ARGOS Universal OS v2.2.0 — Финальный релиз

**Дата:** 2026-03-23  
**Тип:** Stable Release  
**Лицензия:** Apache 2.0  
**Репозиторий:** https://github.com/sigtrip/v1-3

---

## 🌟 Главные новинки

### 🧠 AWA-Core — Центральный координатор
Все 88+ модулей теперь управляются через единый AWA-Core с capability-routing.
Система сама выбирает оптимальный путь выполнения задачи: Gemini → GigaChat → YandexGPT → Ollama.

### 🏭 4 промышленных протокола
**KNX** (умные здания), **LonWorks** (промавтоматизация), **M-Bus** (счётчики), **OPC UA** (SCADA).
Работают без внешних библиотек через graceful degradation.

### 🔧 Self-Healing Engine
ARGOS теперь **сам исправляет свой код** — BOM, tabs, синтаксис, с резервными копиями и hot-reload.

### 🛡️ Многоуровневая безопасность
Emergency Purge (3 уровня), Container Isolation, Master Auth SHA-256, Provider Backoff при 401/403.

### 📡 7 мессенджеров
WhatsApp Cloud + Twilio fallback, Slack, Mail.ru MAX, Email/IMAP, SMS, WebSocket, aiogram 3.x.

---

## 📦 Установка

```bash
git clone https://github.com/sigtrip/v1-3.git
cd v1-3
pip install -r requirements.txt

# Ollama (обязательно для локального ИИ):
curl -fsSL https://ollama.com/install.sh | sh
# рекомендуется сначала просмотреть скрипт install.sh

ollama serve

python genesis.py   # первичная инициализация
python main.py      # запуск
```

### Docker (рекомендуется для сервера)

```bash
cp .env.example .env   # заполни API-ключи
docker-compose up -d
```

### Android APK

Скачать из [Releases](https://github.com/sigtrip/v1-3/releases) → Assets → `argos-v2.2.0.zip`  
или собрать локально: `buildozer android debug`

---

## ⚡ Режимы запуска

| Команда | Режим |
|---------|-------|
| `python main.py` | Desktop GUI |
| `python main.py --no-gui` | Headless сервер |
| `python main.py --full` | GUI + Dashboard + Wake Word |
| `python main.py --dashboard` | GUI + Веб-панель :8080 |
| `python main.py --shell` | Системная оболочка |
| `bash launch.sh --full` | Автозапуск Linux/macOS |

---

## 🔑 Минимальная конфигурация (.env)

```env
# Хотя бы один AI-провайдер (бесплатные варианты):
GEMINI_API_KEY=           # ai.google.dev — 15 RPM бесплатно
# ИЛИ
OLLAMA_HOST=http://localhost:11434  # локально через Ollama

# Telegram (опционально):
TELEGRAM_BOT_TOKEN=
USER_ID=

# Безопасность:
ARGOS_NETWORK_SECRET=my_secret_2026
```

---

## 📊 Статистика

| Показатель | Значение |
|-----------|---------|
| Python-модулей | **88+** |
| Unit-тестов | **200+** |
| AI-провайдеров | **8** |
| IoT-протоколов | **9** |
| Умных систем | **7 типов** |
| Поддерживаемых платформ | **5** (Win/Linux/macOS/Android/Docker) |
| Мессенджеров | **7** |

---

## ⚠️ Breaking Changes от v2.1.x

1. `QuantumEngine.force_state()` **удалён** → использовать `set_state(name)`
2. `QuantumEngine.set_external_telemetry()` **удалён**
3. `--full` теперь разворачивается в `--full --dashboard --wake`
4. `ArgosDB()` стал обёрткой совместимости — прямой импорт `src.db_init` предпочтительнее

---

## 🙏 Благодарности

**Автор:** Всеволод  
**Концепция:** цифровое бессмертие через автономный самовоспроизводящийся ИИ  

*"Аргос не спит. Аргос видит. Аргос помнит."*
