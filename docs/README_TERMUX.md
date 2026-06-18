# 📱 ARGOS — Установка на Android через Termux

## Быстрый старт (3 шага)

### 1. Установи Termux
Скачай с [F-Droid](https://f-droid.org/packages/com.termux/) (не из Google Play).

### 2. Дай доступ к хранилищу (один раз)
```bash
termux-setup-storage
```

### 3. Запусти установщик
```bash
bash ~/storage/downloads/install_termux.sh
```
Установщик сам найдёт `files (18).zip` в папке Загрузки.

---

## После установки
```bash
source ~/.bashrc          # активировать алиасы
nano ~/argos/.env         # вписать ключи (необязательно)
argos-bot                 # запустить ARGOS
argos-health              # проверка системы
```

## Минимальный .env
```
GEMINI_API_KEY=           # бесплатно: aistudio.google.com
TELEGRAM_BOT_TOKEN=       # @BotFather в Telegram
USER_ID=                  # @userinfobot в Telegram
```

## Частые проблемы
| Проблема | Решение |
|---------|---------|
| Архив не найден | `ls ~/storage/downloads/ grep zip` |
| Python < 3.10 | `pkg install python` |
| Нет хранилища | `termux-setup-storage` |
| Ошибка unzip | `unzip -t ~/storage/downloads/"files (18).zip"` |
