#!/usr/bin/env python3
"""ARGOS Telegram Bot launcher — uses real ArgosCore."""
import os, sys, asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set env vars if not already set
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "8651650695:AAFKp_UyRq0cRorzV-Boouwwkf7kHB3xYw8")
os.environ.setdefault("ADMIN_IDS", "6923777384")

from src.telegram_bot import ArgosTelegram
from src.core import ArgosCore

def main():
    print("[TG-LAUNCHER] Initializing ArgosCore...")
    core = ArgosCore()
    print("[TG-LAUNCHER] ArgosCore ready. Starting Telegram bot...")
    bot = ArgosTelegram(core=core, admin=None, flasher=None)
    bot.run()

if __name__ == "__main__":
    main()
