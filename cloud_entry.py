#!/usr/bin/env python3
"""
cloud_entry.py — точка входа ARGOS для облака (Railway / Cloud Run / App Engine).

Файл утрачен при пожаре 03.08.2026 и не сохранился ни в одном репозитории.
Написан заново по спецификации из `GEMINI_DEPLOY_PROMPT.md`:

    cloud_entry.py — точка входа для Cloud Run (запускает ArgosOrchestrator + MCP API)

На него ссылаются `app.yaml` (`uvicorn cloud_entry:app`), `railway.full.json`
и `Dockerfile` (`if ARGOS_ENV=cloud → python3 cloud_entry.py`).

Что делает
----------
Облачные платформы дают ровно один порт в `$PORT` и ждут на нём healthcheck.
ARGOS же поднимает MCP-эндпоинт на `ARGOS_MCP_PORT`. Поэтому здесь порт из
окружения платформы прокидывается в конфигурацию оркестратора, после чего
запускается штатный `argos_main.py` в headless-режиме: MCP API оказывается
на `$PORT` и сам обслуживает `/health`, который проверяет платформа.

Запуск
------
    python3 cloud_entry.py          # как в Dockerfile и railway.full.json
    uvicorn cloud_entry:app         # как в app.yaml — отдаёт ASGI-приложение MCP

Переменные окружения
--------------------
    PORT                 порт платформы (Railway/Cloud Run задают сами)
    ARGOS_ENV=cloud      облачный режим
    ARGOS_MCP_HOST       по умолчанию 0.0.0.0
    ARGOS_DASHBOARD_PORT дашборд; в облаке отключён, если не задан явно
    TELEGRAM_BOT_TOKEN   бот стартует только если токен задан
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _configure_cloud_env() -> int:
    """Прокидывает порт платформы в конфигурацию ARGOS. Возвращает порт."""
    port = int(os.getenv("PORT") or os.getenv("ARGOS_MCP_PORT") or "8080")

    os.environ.setdefault("ARGOS_ENV", "cloud")
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    # MCP слушает именно тот порт, который платформа проверяет healthcheck-ом.
    os.environ["ARGOS_MCP_PORT"] = str(port)
    os.environ.setdefault("ARGOS_MCP_HOST", "0.0.0.0")

    # Дашборды и веб-мастер в облаке заняли бы порты, которых платформа не даёт;
    # включаются только явным указанием портов.
    os.environ.setdefault("ARGOS_DASHBOARD_PORT", "0")
    os.environ.setdefault("ARGOS_WEB_PORT", "0")

    # Роутер моделей по умолчанию смотрит на 192.168.1.72 — сгоревший ПК.
    # В облаке этих адресов нет, поэтому без явной настройки не ходим никуда.
    os.environ.setdefault("ARGOS_MODEL_ROUTER", "")

    return port


def build_app():
    """ASGI-приложение MCP API — для `uvicorn cloud_entry:app` из app.yaml."""
    _configure_cloud_env()
    from src.mcp_api_standalone import app as mcp_app

    return mcp_app


def main() -> int:
    port = _configure_cloud_env()
    print(f"[cloud_entry] ARGOS_ENV={os.environ['ARGOS_ENV']} порт MCP: {port}")

    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        print("[cloud_entry] TELEGRAM_BOT_TOKEN не задан — Telegram-бот не поднимается")

    import argos_main

    # server-режим: без GUI, MCP + P2P + агенты.
    if "--no-gui" not in sys.argv:
        sys.argv.append("--no-gui")
    return argos_main.main() or 0


# app доступен для `uvicorn cloud_entry:app`; при прямом запуске не создаётся,
# чтобы не поднимать второй экземпляр MCP рядом с оркестратором.
if os.getenv("ARGOS_CLOUD_ASGI", "").strip() == "1":
    app = build_app()

if __name__ == "__main__":
    raise SystemExit(main())
