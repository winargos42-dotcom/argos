import sys, os, time, json, re
# Add project root to path BEFORE other imports
PROJECT_ROOT = os.path.expanduser("~/Projects/argoss")
sys.path.insert(0, PROJECT_ROOT)

from pathlib import Path

class MinimalCore:
    """Минимальный mock-core для EvolutionEngine"""
    def __init__(self):
        self.memory = {"facts": [], "errors": []}
        self.db = None
        self.config = {}
    def recall(self, query: str, k: int = 5):
        return []
    def learn(self, fact: str):
        self.memory["facts"].append(fact)

# Создаём минимальный core
from src.mind.evolution_engine import EvolutionEngine
core = MinimalCore()
engine = EvolutionEngine(core)

# Запускаем авто-эволюцию
msg = engine.start_auto()
print(f"[EVOLUTION] {msg}")

# Если авто отключена (interval=0), делаем один ручной цикл
if not engine._running:
    print("[EVOLUTION] Running manual cycle...")
    result = engine.evolve()
    print(f"[EVOLUTION] Manual result: {result}")
else:
    print("[EVOLUTION] Auto-cycle active. Waiting forever (Ctrl+C to stop)...")
    try:
        import time
        while True:
            time.sleep(60)
            print(f"[EVOLUTION] tick | history={len(engine._history)} | running={engine._running}")
    except KeyboardInterrupt:
        print("[EVOLUTION] Stopped by user")
