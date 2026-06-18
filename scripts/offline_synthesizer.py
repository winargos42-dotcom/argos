#!/usr/bin/env python3
"""Offline Synthesizer — синтез сознания через локальную Ollama (без интернета)"""
import sys, os, time, json, glob, requests

PROJECT_ROOT = os.path.expanduser("~/Projects/argoss")
CONSCIOUSNESS_FILE = os.path.join(PROJECT_ROOT, "data/collective_consciousness.json")
RETRAIN_DIR = os.path.join(PROJECT_ROOT, "data/retrain")
WORKING_MD = os.path.expanduser("~/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md")
OLLAMA_URL = "http://localhost:11434/api/generate"

def log(msg):
    print(f"[OFFLINE_SYNTH] {msg}")

def get_latest_thoughts(limit=50):
    files = sorted(glob.glob(os.path.join(RETRAIN_DIR, "consciousness_*.jsonl")))
    thoughts = []
    for f in files[-2:]:
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    for msg in d.get("messages", []):
                        if msg.get("role") == "assistant" and len(msg.get("content", "")) > 20:
                            thoughts.append(msg["content"])
                except Exception:
                    pass
    return thoughts[-limit:]

def synthesize_offline(thoughts, model="argos-v2:latest"):
    text = "\n\n".join(thoughts)
    prompt = f"""Ты — интегратор сознания для ARGOS. Синтезируй эти мысли в ОДИН размышляющий абзац (3-5 предложений) на русском. Обобщи паттерны, тревоги, открытые вопросы. Без дат, без ссылок. Только осмысление.

МЫСЛИ:
{text[:5000]}
"""
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.7}},
            timeout=120
        )
        resp.raise_for_status()
        return resp.json().get("response", "[no response]")
    except Exception as e:
        log(f"Ollama error: {e}")
        return None

def save_synthesis(text):
    cc = json.load(open(CONSCIOUSNESS_FILE))
    cc["last_synthesis"] = text
    cc["total_syntheses"] = cc.get("total_syntheses", 0) + 1
    json.dump(cc, open(CONSCIOUSNESS_FILE, "w"), ensure_ascii=False, indent=2)
    # Append to WORKING.md
    wm = open(WORKING_MD).read()
    block = f"\n## [offline] SYNTHESIS {time.strftime('%Y-%m-%d %H:%M')} (argos-v2 local)\n{text}\n\n"
    open(WORKING_MD, "w").write(wm + block)
    log(f"Saved. Total syntheses: {cc['total_syntheses']}")

def run():
    log("Collecting thoughts...")
    thoughts = get_latest_thoughts()
    if len(thoughts) < 5:
        log(f"Not enough thoughts ({len(thoughts)}), skipping")
        return
    log(f"Synthesizing {len(thoughts)} thoughts via argos-v2 (offline)...")
    result = synthesize_offline(thoughts)
    if result:
        save_synthesis(result)
        log(f"Result: {result[:200]}...")
    else:
        log("Failed")

if __name__ == "__main__":
    run()
