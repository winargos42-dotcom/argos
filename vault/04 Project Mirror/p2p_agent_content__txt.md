---
argos_import: project_file
source_path: p2p_agent_content.txt
source_abs: F:\debug\argoss\p2p_agent_content.txt
source_ext: .txt
source_sha256: 671c765b52d6003a42097b4c5864dfaa3c7d6a8f53c1b3913c7ce13ca261dfdb
text_sha256: 578c98d1dd190d63ac40c9520a84d1fa26be17f8e81ca018636ddd3fd7d9730d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# p2p_agent_content.txt

- Source: `p2p_agent_content.txt`
- Extract: `text`
- SHA256: `671c765b52d6003a42097b4c5864dfaa3c7d6a8f53c1b3913c7ce13ca261dfdb`

## Content

import os, time, socket, platform, requests
BRAIN = os.getenv("ARGOS_BRAIN_URL", "http://192.168.1.66:5001").rstrip("/")
NAME = os.getenv("ARGOS_NODE_NAME", socket.gethostname())
ROLE = os.getenv("ARGOS_NODE_ROLE", "ollama")
OLLAMA = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
CAPS = os.getenv("ARGOS_NODE_CAPABILITIES", "p2p,ollama,llm").split(",")

def models():
    try:
        r = requests.get(f"{OLLAMA}/api/tags", timeout=5)
        if r.status_code == 200:
            return [m["name"] for m in r.json().get("models", [])]
    except:
        pass
    return []

def reg():
    try:
        r = requests.post(f"{BRAIN}/brain/register", json={
            "node_id": NAME,
            "capabilities": CAPS,
            "models": models(),
            "address": "20.240.192.35:8000",
            "meta": {"role": ROLE, "platform": platform.platform()}
        }, timeout=10)
        return r.status_code == 200
    except:
        return False

def hb():
    try:
        r = requests.post(f"{BRAIN}/brain/heartbeat", json={"node_id": NAME, "status": "online", "models": models()}, timeout=5)
        return r.status_code == 200
    except:
        return False

print("P2P Agent:", NAME, ROLE, BRAIN)
while not reg():
    print("Register failed, retrying...")
    time.sleep(5)
print("Registered!")
while True:
    print("OK" if hb() else "FAIL", time.strftime("%H:%M:%S"))
    time.sleep(30)

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
