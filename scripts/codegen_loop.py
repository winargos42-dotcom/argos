#!/usr/bin/env python3
"""
MetaGPT Codegen Loop — полный цикл: задача → код → draft.
Используем DeepSeek API или MetaGPT library.
"""
import os, json, subprocess, re, datetime
from pathlib import Path

# Читаем ключ из .env
env = open('/home/ava/Projects/argoss/.env').read()
def genv(k):
    m = re.search(rf"{k}=([^\n\s]+)", env)
    return m.group(1).strip().strip('"').strip("'") if m else ""

DS_KEY = genv("DEEPSEEK_API_KEY") or genv("DS_KEY")

META_DIR = Path("/tmp/metagpt_tasks")
META_DIR.mkdir(exist_ok=True)

def deepseek_codegen(prompt):
    """DeepSeekAPI fallback — быстро и работает."""
    if not DS_KEY:
        return "# No API key configured\n"
    key = DS_KEY
    try:
        body = json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Ты Python-разработчик. Пиши рабочий код с комментариями на русском. Только код, без markdown```."},
                {"role": "user", "content": f"Напиши Python скрипт: {prompt}\nТребования: argparse, logging, systemd совместимый."}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }).encode()
        import urllib.request
        req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions",
            data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"# Codegen error: {e}\n"

def save_draft(name, code):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    filename = META_DIR / f"{name}_{ts}.py"
    # Чистим markdown
    code_clean = re.sub(r'```python\n?', '', code)
    code_clean = re.sub(r'```\n?', '', code_clean)
    # Добавляем shebang если нет
    if not code_clean.lstrip().startswith("#!/"):
        code_clean = "#!/usr/bin/env python3\n" + code_clean
    filename.write_text(code_clean, encoding="utf-8")
    os.chmod(filename, 0o755)
    print(f"[Codegen] Draft saved: {filename}")
    return filename

def fetch_next_task():
    """Берёт первую [AUTO] задачу из WORKING.md."""
    working = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md")
    if not working.exists():
        return None
    text = working.read_text(encoding="utf-8")
    # Ищем строку с [AUTO]
    for line in text.splitlines():
        if "[AUTO]" in line:
            # Вычленяем текст после тире
            clean = re.sub(r'^\s*-\s*\[.\]\s*', '', line)
            clean = re.sub(r'\[AUTO\]\s*', '', clean)
            return clean.strip()
    return None

def run_codegen_loop():
    print("[Codegen] Fetching next [AUTO] task...")
    task = fetch_next_task()
    if not task:
        print("[Codegen] No [AUTO] tasks found")
        return None
    
    # Нормализуем имя файла
    safe_name = re.sub(r'[^a-zA-Zа-яА-Я0-9]+', '_', task)[:30].strip("_")
    print(f"[Codegen] Task: {task}")
    print(f"[Codegen] Generating code...")
    
    code = deepseek_codegen(task)
    
    if not code.strip() or code.startswith("# Codegen error"):
        print(f"[Codegen] FAILED: {code[:100]}")
        return None
    
    fp = save_draft(safe_name, code)
    print(f"[Codegen] DONE: {fp}")
    return fp

if __name__ == "__main__":
    run_codegen_loop()
