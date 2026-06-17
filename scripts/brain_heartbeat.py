#!/usr/bin/env python3
"""Brain heartbeat daemon — keeps all nodes alive in Brain registry."""
import os, time, requests, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("heartbeat")

BRAIN = os.getenv("ARGOS_BRAIN_API_URL", "http://192.168.1.66:5010")
INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", "60"))

NODES = [
    {"node_id": "argos-pc",            "address": "192.168.1.66:5010",                          "capabilities": ["gpu","ollama","brain","tg_bot","claude"]},
    {"node_id": "argos-laptop",        "address": "192.168.1.53:8000",                          "capabilities": ["mcp","ha","dev"]},
    {"node_id": "orangepi",            "address": "192.168.2.168:7777",                         "capabilities": ["iot","z2m","reports"]},
    {"node_id": "argos-railway",       "address": "argos-v2-production.up.railway.app",         "capabilities": ["cloud"]},
    {"node_id": "argos-gcp",           "address": "argos-core-m3gk27ccqa-uc.a.run.app",        "capabilities": ["cloud","openai","gemini"]},
    {"node_id": "claude-code",         "address": "192.168.1.53",                               "capabilities": ["dev","consciousness"]},
    {"node_id": "argos-esp-bridge",    "address": "192.168.1.181",                              "capabilities": ["esp8266","mqtt"]},
    {"node_id": "argos-esp32-display", "address": "192.168.1.211",                              "capabilities": ["esp32","display"]},
    {"node_id": "entity-argos-v1",     "address": "192.168.1.66:11434",                         "capabilities": ["ai","local","finetuned"], "meta": {"name": "argos-v1"}},
    {"node_id": "entity-claude",       "address": "api.anthropic.com",                          "capabilities": ["ai","claude"],            "meta": {"name": "Клод"}},
    {"node_id": "entity-deepseek",     "address": "api.deepseek.com",                           "capabilities": ["ai"],                     "meta": {"name": "Дипсик"}},
    {"node_id": "entity-kimi",         "address": "api.moonshot.ai",                            "capabilities": ["ai"],                     "meta": {"name": "Кими"}},
    {"node_id": "entity-openai",       "address": "argos-core-m3gk27ccqa-uc.a.run.app/proxy/openai",  "capabilities": ["ai"],             "meta": {"name": "OpenAI"}},
    {"node_id": "entity-gemini",       "address": "argos-core-m3gk27ccqa-uc.a.run.app/proxy/gemini",  "capabilities": ["ai"],             "meta": {"name": "Джемини"}},
    {"node_id": "entity-cloudflare",   "address": "api.cloudflare.com",                         "capabilities": ["ai"],                     "meta": {"name": "Клауд"}},
    {"node_id": "entity-argos",        "address": "192.168.1.66:5010",                          "capabilities": ["ai","iot"],               "meta": {"name": "ARGOS"}},
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
    """Pull nodes from PC master brain and mirror them into local laptop brain (:5001)."""
    try:
        r = requests.get(f"{BRAIN}/brain/nodes", timeout=5)
        r.raise_for_status()
        data = r.json()
        nodes = data.get("nodes", [])
        ok = 0
        for node in nodes:
            nid = node.get("node_id")
            if not nid or nid in {"argos-laptop", "claude-code"}:
                continue
            payload = {
                "node_id": nid,
                "address": node.get("address", ""),
                "capabilities": node.get("capabilities", []),
                "models": node.get("models", []),
                "meta": node.get("meta", {}),
            }
            try:
                resp = requests.post("http://localhost:5001/brain/register", json=payload, timeout=3)
                if resp.status_code in (200, 201):
                    ok += 1
            except Exception:
                pass
            try:
                requests.post("http://localhost:5001/brain/heartbeat",
                              json={"node_id": nid, "status": "online"}, timeout=2)
            except Exception:
                pass
        log.info(f"[SYNC] Mirrored {ok}/{len(nodes)} nodes into local brain")
    except Exception as e:
        log.warning(f"[SYNC] Failed to pull from master: {e}")


def main():
    log.info(f"Brain heartbeat daemon started → {BRAIN} interval={INTERVAL}s")
    # Начальная регистрация
    n = register_all()
    log.info(f"Registered {n}/{len(NODES)} nodes")

    cycle = 0
    while True:
        time.sleep(INTERVAL)
        cycle += 1
        ok = heartbeat_all()
        # Каждые 10 циклов переregister чтобы обновить capabilities
        if cycle % 10 == 0:
            register_all()
            sync_nodes_from_master()
        try:
            r = requests.get(f"{BRAIN}/brain/nodes", timeout=5).json()
            log.info(f"Heartbeat {ok}/{len(NODES)} ok — Brain: {r['online']}/{r['total']} online")
        except Exception as e:
            log.warning(f"Brain unreachable: {e}")


if __name__ == "__main__":
    main()
