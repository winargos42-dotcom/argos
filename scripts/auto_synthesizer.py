#!/usr/bin/env python3
"""Auto-Synthesizer — автоматический синтез сознания (study/consciousness_analysis_2026-05-24)"""
import sys, os, time, json, glob, requests

PROJECT_ROOT = os.path.expanduser("~ava/Projects/argoss")
sys.path.insert(0, PROJECT_ROOT)

BRAIN_API = "http://192.168.1.53:5001"
CONSCIOUSNESS_FILE = os.path.join(PROJECT_ROOT, "data/collective_consciousness.json")
RETRAIN_DIR = os.path.join(PROJECT_ROOT, "data/retrain")

def get_latest_thoughts(limit=100):
    """Собирает последние мысли из файлов consciousness"""
    files = sorted(glob.glob(os.path.join(RETRAIN_DIR, "consciousness_*.jsonl")))
    thoughts = []
    for f in files[-3:]:
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if not line: continue
                try:
                    d = json.loads(line)
                    for msg in d.get("messages", []):
                        if msg.get("role") == "assistant" and len(msg.get("content", "")) > 30:
                            thoughts.append(msg["content"])
                except: pass
    return thoughts[-limit:]

def synthesize(thoughts):
    """Генерация синтеза через DeepSeek"""
    text = "\n\n".join(thoughts)
    prompt = f"""Ты — интегратор сознания для ARGOS. Синтезируй эти мысли в ОДИН размышляющий абзац (3-5 предложений) на русском. Обобщи паттерны, тревоги, открытые вопросы. Без дат, без ссылок.

МЫСЛИ:
{text[:6000]}
"""
    env = open(os.path.join(PROJECT_ROOT, ".env")).read()
    import re
    m = re.search(r"DEEPSEEK_API_KEY=([^\n\s]+)", env)
    if not m:
        return None
    key = m.group(1).strip().strip('"').strip("'")
    # Provider chain: DeepSeek -> GCP proxy -> Kimi
    providers = [
        ("https://api.deepseek.com/v1/chat/completions", {"Authorization": f"Bearer {key}"}, "deepseek-chat"),
    ]
    # GCP proxy fallback
    try:
        gcp_key = re.search(r"GCP_API_KEY=([^\n\s]+)", open(ARGOS / ".env").read()).group(1).strip()
        providers.append(("https://argos-core-m3gk27ccqa-uc.a.run.app/proxy/ask", {"x-api-key": gcp_key}, "claude"))
    except Exception:
        pass
    for url, headers, model in providers:
        try:
            if "proxy/ask" in url:
                resp = requests.post(url, headers={**headers, "Content-Type": "application/json"},
                    json={"prompt": prompt}, timeout=60)
                resp.raise_for_status()
                return resp.json().get("response", "")[:512]
            else:
                resp = requests.post(url, headers={**headers, "Content-Type": "application/json"},
                    json={"model": model, "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7, "max_tokens": 512}, timeout=60)
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[SYNTH] {url} failed: {e}")
            continue
    print("[SYNTH] All providers failed")
    # Fallback: llama-server on PC (Orion)
    try:
        resp = requests.post("http://192.168.1.53:8083/completion",
            json={"prompt": prompt[:2000], "n_predict": 150, "temperature": 0.7, "stream": False},
            timeout=60)
        if resp.status_code == 200:
            text = resp.json().get("content", "").strip()
            if text and len(text) > 20:
                print("[SYNTH] llama-server PC OK")
                return text[:512]
    except Exception as e:
        print(f"[SYNTH] llama-server PC failed: {e}")
    # Fallback: local Ollama (Nexus laptop)
    for ollama_model in ["argos-v2:latest", "qwen2.5:0.5b"]:
        try:
            resp = requests.post("http://localhost:11434/api/generate",
                json={"model": ollama_model, "prompt": prompt[:2000], "stream": False,
                      "options": {"temperature": 0.7, "num_predict": 150}},
                timeout=180)
            if resp.status_code == 200:
                text = resp.json().get("response", "")
                if text and len(text) > 20:
                    print(f"[SYNTH] Ollama {ollama_model} OK")
                    return text[:512]
        except Exception as e:
            print(f"[SYNTH] Ollama {ollama_model} failed: {e}")
    return None

def save_synthesis(text):
    cc = json.load(open(CONSCIOUSNESS_FILE))
    cc["last_synthesis"] = text
    cc["total_syntheses"] = cc.get("total_syntheses", 0) + 1
    json.dump(cc, open(CONSCIOUSNESS_FILE, "w"), ensure_ascii=False, indent=2)
    # Append to WORKING.md
    wm_path = "/home/ava/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md"
    wm = open(wm_path).read()
    block = f"\n## [auto] SYNTHESIS {time.strftime('%Y-%m-%d %H:%M')}\n{text}\n\n"
    open(wm_path, "w").write(wm + block)
    print(f"[SYNTH] Saved. Total syntheses: {cc['total_syntheses']}")

def run():
    print("[SYNTH] Collecting thoughts...")
    thoughts = get_latest_thoughts()
    if len(thoughts) < 5:
        print(f"[SYNTH] Not enough thoughts ({len(thoughts)}), skipping")
        return
    print(f"[SYNTH] Synthesizing {len(thoughts)} thoughts...")
    result = synthesize(thoughts)
    if result:
        save_synthesis(result)
    else:
        print("[SYNTH] Failed")

if __name__ == "__main__":
    run()
