"""Offline tests for ARGOS Telegram menu restoration."""

import asyncio
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from src.connectivity.telegram_menu import COMMAND_MENU, configure_command_menu
except ModuleNotFoundError:
    from telegram_menu import COMMAND_MENU, configure_command_menu


class FakeBot:
    def __init__(self, fail_default=False):
        self.commands = None
        self.menu_calls = []
        self.fail_default = fail_default

    async def set_my_commands(self, commands):
        self.commands = list(commands)

    async def set_chat_menu_button(self, **kwargs):
        self.menu_calls.append(kwargs)
        if self.fail_default and "chat_id" not in kwargs:
            raise RuntimeError("default menu failed")


class TelegramMenuTests(unittest.IsolatedAsyncioTestCase):
    async def test_restores_global_and_individual_menus(self):
        bot = FakeBot()
        button = object()
        errors = await configure_command_menu(bot, {"123", "123", "456", "invalid"}, button)
        self.assertEqual(errors, [])
        self.assertIn(("help", "Справка по командам"), bot.commands)
        self.assertEqual(bot.menu_calls, [
            {"menu_button": button},
            {"chat_id": 123, "menu_button": button},
            {"chat_id": 456, "menu_button": button},
        ])

    async def test_default_failure_does_not_block_private_menu(self):
        bot = FakeBot(fail_default=True)
        errors = await configure_command_menu(bot, ["123"], object())
        self.assertEqual(len(errors), 1)
        self.assertEqual(bot.menu_calls[1]["chat_id"], 123)


if __name__ == "__main__":
    unittest.main()
