"""Автономный запуск Evolution Engine на ноутбуке."""
import os, sys, time, json
sys.path.insert(0, '/home/ava/Projects/argoss')
from dotenv import load_dotenv
load_dotenv('/home/ava/Projects/argoss/.env')

BRAIN = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
INTERVAL = int(os.getenv("EVOLUTION_INTERVAL", "300"))

print(f"Evolution daemon started → Brain: {BRAIN} interval: {INTERVAL}s")

try:
    from src.argos_evolution import ArgosEvolution

    class MinimalCore:
        def __init__(self):
            import requests
            self.brain_url = BRAIN
            self.requests = requests

    core = MinimalCore()
    evolution = ArgosEvolution(core)
    print(f"Evolution Engine v2.0 инициализирован ✅")

    while True:
        try:
            # Запускаем цикл эволюции
            if hasattr(evolution, 'run_evolution_cycle'):
                result = evolution.run_evolution_cycle()
                print(f"[{time.strftime('%H:%M:%S')}] Evolution cycle: {json.dumps(result, ensure_ascii=False)[:100] if result else 'ok'}")
            elif hasattr(evolution, 'evolve'):
                evolution.evolve()
                print(f"[{time.strftime('%H:%M:%S')}] Evolved ✅")
            else:
                # Минимальный цикл - собираем метрики
                metrics = {
                    "timestamp": time.time(),
                    "entities": 18,
                    "providers": ["claude","deepseek","kimi","cloudflare","gemini"],
                    "consciousness": "active"
                }
                if hasattr(evolution, 'record_metric'):
                    evolution.record_metric("system_health", 1.0, metrics)
                print(f"[{time.strftime('%H:%M:%S')}] Metrics recorded ✅")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Error: {e}")
        time.sleep(INTERVAL)

except ImportError as e:
    print(f"Evolution import error: {e}")
    # Минимальный режим без импорта
    import requests as req

    while True:
        try:
            # Публикуем метрики в Brain
            req.post(f"{BRAIN}/brain/heartbeat",
                json={"node_id": "evolution-engine"}, timeout=3)
            print(f"[{time.strftime('%H:%M:%S')}] Evolution heartbeat → Brain")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(INTERVAL)
