#!/usr/bin/env python3
"""Brain heartbeat daemon — keeps all nodes alive in Brain registry."""
import os, time, requests, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("heartbeat")

BRAIN = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.53:5001")
INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", "60"))

NODES = [
    {"node_id": "argos-pc",            "address": "192.168.1.53:5001",                          "capabilities": ["gpu","ollama","brain","tg_bot","claude"]},
    {"node_id": "argos-laptop",        "address": "192.168.1.53:8000",                          "capabilities": ["mcp","ha","dev"]},
    {"node_id": "orangepi",            "address": "192.168.2.168:7777",                         "capabilities": ["iot","z2m","reports"]},
    {"node_id": "argos-railway",       "address": "argos-v2-production.up.railway.app",         "capabilities": ["cloud"]},
    {"node_id": "argos-gcp",           "address": "argos-core-m3gk27ccqa-uc.a.run.app",        "capabilities": ["cloud","openai","gemini"]},
    {"node_id": "claude-code",         "address": "192.168.1.53",                               "capabilities": ["dev","consciousness"]},
    {"node_id": "argos-esp-bridge",    "address": "192.168.1.181",                              "capabilities": ["esp8266","mqtt"]},
    {"node_id": "argos-esp32-display", "address": "192.168.1.211",                              "capabilities": ["esp32","display"]},
    {"node_id": "entity-argos-v1",     "address": "192.168.1.53:11434",                         "capabilities": ["ai","local","finetuned"], "meta": {"name": "argos-v1"}},
    {"node_id": "entity-claude",       "address": "api.anthropic.com",                          "capabilities": ["ai","claude"],            "meta": {"name": "Клод"}},
    {"node_id": "entity-deepseek",     "address": "api.deepseek.com",                           "capabilities": ["ai"],                     "meta": {"name": "Дипсик"}},
    {"node_id": "entity-kimi",         "address": "api.moonshot.ai",                            "capabilities": ["ai"],                     "meta": {"name": "Кими"}},
    {"node_id": "entity-openai",       "address": "argos-core-m3gk27ccqa-uc.a.run.app/proxy/openai",  "capabilities": ["ai"],             "meta": {"name": "OpenAI"}},
    {"node_id": "entity-gemini",       "address": "argos-core-m3gk27ccqa-uc.a.run.app/proxy/gemini",  "capabilities": ["ai"],             "meta": {"name": "Джемини"}},
    {"node_id": "entity-cloudflare",   "address": "api.cloudflare.com",                         "capabilities": ["ai"],                     "meta": {"name": "Клауд"}},
    {"node_id": "entity-argos",        "address": "192.168.1.53:5001",                          "capabilities": ["ai","iot"],               "meta": {"name": "ARGOS"}},
]


def register_all():
    ok = 0
    for node in NODES:
        try:
            requests.post(f"{BRAIN}/brain/register", json=node, timeout=3)
            ok += 1
        except Exception:
            pass
    return ok


def heartbeat_all():
    ok = 0
    for node in NODES:
        try:
            requests.post(f"{BRAIN}/brain/heartbeat",
                          json={"node_id": node["node_id"]}, timeout=3)
            ok += 1
        except Exception:
            pass
    return ok


def sync_nodes_from_master():
    """Disabled: Using PC Brain as single source of truth. All nodes register directly to PC Brain."""
    pass


def main():
    log.info(f"Brain heartbeat daemon started → {BRAIN} interval={INTERVAL}s")
    # Начальная регистрация всех нод в PC Brain
    n = register_all()
    log.info(f"Registered {n}/{len(NODES)} nodes to PC Brain")

    cycle = 0
    while True:
        time.sleep(INTERVAL)
        cycle += 1
        ok = heartbeat_all()
        # Каждые 10 циклов переregister чтобы обновить capabilities
        if cycle % 10 == 0:
            register_all()
        try:
            r = requests.get(f"{BRAIN}/brain/nodes", timeout=5).json()
            log.info(f"Heartbeat {ok}/{len(NODES)} ok — Brain: {r['online']}/{r['total']} online")
        except Exception as e:
            log.warning(f"Brain unreachable: {e}")


if __name__ == "__main__":
    main()
