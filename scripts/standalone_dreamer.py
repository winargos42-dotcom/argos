#!/usr/bin/env python3
"""Standalone Dreamer runner — генерирует инсайты без полного core.py"""
import sys, os, time, json
PROJECT_ROOT = os.path.expanduser("~/Projects/argoss")
sys.path.insert(0, PROJECT_ROOT)

from pathlib import Path
from src.mind.dreamer import Dreamer

class MinimalCore:
    def __init__(self):
        self.memory = {"thoughts": [], "facts": []}
    def recall(self, q, k=5): return []
    def think(self, q): return {"text": "[minimal think stub]"}

# Создаём минимальный core и Dreamer
core = MinimalCore()
dreamer = Dreamer(core)
dreamer.start()
print(f"[DREAMER] Started | interval={getattr(dreamer, '_interval', '?')}s")

try:
    while True:
        time.sleep(60)
        print(f"[DREAMER] tick | running={getattr(dreamer, '_running', '?')}")
except KeyboardInterrupt:
    print("[DREAMER] Stopped by user")
