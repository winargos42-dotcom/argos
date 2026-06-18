#!/usr/bin/env python3
"""
ARGOS Telegram Bot Startup Script
=================================
Запускает Telegram-бота с:
  • загрузкой .env
  • настройкой логирования
  • авто-рестартом при падении
  • standalone-режимом (если ArgosCore недоступен — бот работает через Brain API)

Usage:
    python scripts/run_argos_telegram_bot.py
"""
from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path

# ── Пути ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
VENV_SITE = PROJECT_ROOT / ".venv" / "lib" / "python3.14" / "site-packages"

sys.path.insert(0, str(PROJECT_ROOT))
if VENV_SITE.exists():
    sys.path.insert(0, str(VENV_SITE))

# ── .env ────────────────────────────────────────────────────────────────────
ENV_PATH = PROJECT_ROOT / ".env"
if ENV_PATH.exists():
    try:
        from dotenv import load_dotenv

        load_dotenv(dotenv_path=str(ENV_PATH), override=False)
        print(f"[STARTUP] .env загружен: {ENV_PATH}")
    except Exception as e:
        print(f"[STARTUP] Ошибка загрузки .env: {e}")
else:
    print(f"[STARTUP] ⚠️ .env не найден: {ENV_PATH}")

# ── Логирование ───────────────────────────────────────────────────────────
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_LEVEL = os.getenv("ARGOS_LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO), format=LOG_FORMAT)
logger = logging.getLogger("argos-tg")

# ── Проверка токена ───────────────────────────────────────────────────────
TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()
if not TOKEN or ":" not in TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN не задан или невалиден. Запуск невозможен.")
    sys.exit(1)

# ── Импорт бота ──────────────────────────────────────────────────────────
try:
    from src.connectivity.telegram_bot import ArgosTelegram
except Exception as e:
    logger.error("Не удалось импортировать ArgosTelegram: %s", e)
    sys.exit(1)


# ── Минимальный stub Core для standalone-режима ───────────────────────────
class _MinimalCore:
    """Stub ядра, если ArgosCore недоступен. Бот будет работать через Brain API."""

    def __init__(self):
        self.ai_mode = "brain"
        self.sensors = _SensorsStub()
        self.quantum = _QuantumStub()
        self.voice_on = False
        self.p2p = None
        self.skill_loader = None
        self.memory = None
        self.alerts = None
        self.smart_sys = None
        self.iot_bridge = None
        self.db = None
        self.vision = None
        self.web_explorer = None
        self.replicator = _ReplicatorStub()

    def ai_mode_label(self) -> str:
        return "brain-standalone"

    def process_logic_async(self, text, admin, flasher):
        import asyncio
        from src.connectivity.telegram_bot import _BRAIN_CLIENT
        answer = _BRAIN_CLIENT.ask(text)
        return {"answer": answer or "⚡ Brain API и llama-server недоступны.", "state": "Brain"}

    def transcribe_audio_path(self, path: str) -> str:
        return ""


class _SensorsStub:
    def get_full_report(self) -> str:
        return "Сенсоры недоступны (standalone mode)"


class _QuantumStub:
    def generate_state(self):
        return {"name": "standalone"}


class _ReplicatorStub:
    def create_replica(self):
        return "Репликация недоступна (standalone mode)"


# ── Инициализация ─────────────────────────────────────────────────────────
def _build_core():
    try:
        from src.core import ArgosCore
        return ArgosCore()
    except Exception as e:
        logger.warning("ArgosCore недоступен, переключение в standalone-режим: %s", e)
        return _MinimalCore()


def main():
    retry_delay = max(3, int(os.getenv("TG_RETRY_DELAY_SEC", "8") or "8"))
    retries = 0

    while True:
        try:
            core = _build_core()
            bot = ArgosTelegram(core=core, admin=None, flasher=None)
            ok, reason = bot.can_start()
            if not ok:
                logger.error("Бот не может стартовать: %s", reason)
                sys.exit(1)

            logger.info("Запуск ArgosTelegram...")
            bot.run()
            # run() возвращает только при остановке (InvalidToken) или webhook stop
            logger.info("Бот остановлен. Перезапуск через %s сек...", retry_delay)
        except KeyboardInterrupt:
            logger.info("Прервано пользователем. Выход.")
            sys.exit(0)
        except Exception as e:
            retries += 1
            logger.exception("Критическая ошибка (retry=%s): %s", retries, e)

        time.sleep(retry_delay)


if __name__ == "__main__":
    main()
