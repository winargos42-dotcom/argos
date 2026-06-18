---
argos_import: sharedmemory_mirror
source_path: claude/project_argos_deps.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_argos_deps.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_argos_deps.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_argos_deps.md`
- Category: [[Claude Hub]]

## Content

---
name: ARGOS зависимости и установка на ноутбуке
description: Python venv, pip пакеты, системные зависимости для ARGOS на X230
type: project
originSessionId: 81a638d4-f034-4bbb-8b6c-d15b46bb4b71
---
## venv
- Путь: `~/Projects/argoss/.venv`
- Python: 3.14.4
- Активация: `source ~/Projects/argoss/.venv/bin/activate`

## Системные пакеты (установлены через pacman)
```
nmap, ffmpeg, tk, portaudio, sunxi-tools
```

## Python пакеты — установлено (~251 шт, 2026-05-02/03)
### Ядро
python-dotenv, aiohttp, httpx, pydantic, SQLAlchemy, argon2-cffi, aiofiles, tenacity

### AI провайдеры
google-genai, ollama, openai, huggingface_hub, ibm-watsonx-ai==1.1.16

### Telegram
python-telegram-bot

### Голос TTS/STT
gTTS, pyttsx3, pydub, SpeechRecognition, faster-whisper, PyAudio

### Vision
Pillow, opencv-python-headless

### ML / Векторная память
scikit-learn, numpy, scipy, chromadb, sentence-transformers, skl2onnx, mempalace

### Квантовые вычисления
qiskit, qiskit-aer, qiskit-ibm-runtime

### Управление ПК
pyautogui, pynput, pyperclip, mss

### Web / API / Дашборды
fastapi, uvicorn, flask, flask-cors, websockets, streamlit, redis

### Веб-скрапинг
beautifulsoup4, lxml, ddgs, duckduckgo-search

### IoT / Serial / Сеть
paho-mqtt, pyserial, smbus2, python-nmap, bleak, pymodbus, xknx, asyncua

### Аналитика
google-analytics-data

### Git
GitPython

### ESP32 / MCU
esptool, mpremote, platformio, rshell

### UI
customtkinter

### Прочее
gradio_client, arc-agi

## Несовместимо с Python 3.14
- `ibm-watsonx-ai>=1.4.2` — установлена 1.1.16 (последняя совместимая)
- `pygost` (ГОСТ crypto) — сервер pypi.cypherpunks.su недоступен

## Статус health_check (2026-05-02 22:23)
- TTS: ✅ OK
- Ollama: ✅ запущен (localhost:11434)
- Kimi: ✅ ключ найден
- Память (SQLite): ✅ OK
- Homeostasis: ✅ OK
- Curiosity: ✅ OK
- Планировщик: ✅ OK
- Алерты: ✅ OK
- Vision: ✅ OK
- Навыки: weather, evolution, firmware_manager — загружены

## Запуск ARGOS на ноутбуке
```bash
cd ~/Projects/argoss
source .venv/bin/activate
python main.py --no-gui --dashboard   # headless + вебпанель :8080
python main.py --shell                # REPL
```

**Why:** запуск ARGOS на ноутбуке для локальной разработки и P2P кластера.
**How to apply:** health_check проходит (exit 0). Всё готово к запуску.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_argos_deps.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
