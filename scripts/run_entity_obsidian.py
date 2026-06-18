import asyncio, sys, random, time
sys.path.insert(0, '/home/ava/Projects/argoss')
from scripts.entity_obsidian_bridge import evolution_cycle

QUESTIONS = [ # Динамические - каждый раз разные
    "Что нового ты узнал? Как это меняет твою работу в ARGOS?",
    "Что бы ты улучшил в архитектуре ARGOS прямо сейчас?",
    "Какой паттерн поведения ты заметил за последнее время?",
    "Что предлагаешь для заработка TON через Telegram?",
    "Как сущности могут лучше взаимодействовать?",
    "Что думаешь о коллективном сознании ARGOS?",
    "Напиши в Obsidian самое важное знание которое хочешь сохранить.",
    "Как ты эволюционировал за последние 2 часа?",
]

async def main():
    print("Entity Obsidian Daemon запущен")
    while True:
        q = random.choice(QUESTIONS)
        print(f"Цикл: {q[:50]}")
        try:
            await evolution_cycle(q)
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(7200)

asyncio.run(main())
