#!/usr/bin/env python3
"""
MetaTasker — берёт [AUTO] задачу из WORKING.md,
генерирует черновик кода через DeepSeek API,
сохраняет в /tmp/metagpt_tasks/ на рассмотрение.
Пользователь одобряет → деплой.
"""
import re, json, urllib.request, os, datetime
from pathlib import Path

WORKING = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/orchestrator/WORKING.md")
OUTDIR = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/factory/drafts")
TMPDIR = Path("/tmp/metagpt_tasks")

# ENV
def genv(k):
    env = open("/home/ava/Projects/argoss/.env").read()
    m = re.search(rf"{k}=([^\n]+)", env)
    return m.group(1).strip() if m else ""

DS_KEY = genv("DEEPSEEK_API_KEY")

def get_next_auto_task():
    txt = WORKING.read_text(encoding="utf-8")
    m = re.search(r'- \[\s?\] .+\[AUTO\] (.+)', txt)
    return m.group(1).strip() if m else None

def generate_code(task: str):
    prompt = f"Напиши Python скрипт для: {task}. Требования: чистый Python 3, стандартные библиотеки, __main__, docstring на русском. Код в ```python"
    body = json.dumps({
        "model": "deepseek-chat", "max_tokens": 800,
        "messages": [
            {"role": "system", "content": "Senior Python Developer. Production-ready код."},
            {"role": "user", "content": prompt}
        ]
    }).encode()
    req = urllib.request.Request("https://api.deepseek.com/chat/completions",
        data=body, headers={"Authorization": f"Bearer {DS_KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.loads(r.read())
            return res["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERR: {e}]"

def extract_python(text: str):
    m = re.search(r'```python\n(.*?)```', text, re.DOTALL)
    return m.group(1) if m else text

def save_draft(task: str, code: str):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    TMPDIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    safe = re.sub(r'[^\w]','_', task[:30])
    filename = OUTDIR / f"{safe}_{ts}.py.md"
    tmpfile = TMPDIR / f"{safe}_{ts}.py"
    content = f'"""Generated for: {task}\nStatus: DRAFT — APPROVE BEFORE DEPLOY\n"""\n\n{code}\n'
    filename.write_text(content, encoding="utf-8")
    tmpfile.write_text(content, encoding="utf-8")
    return filename

if __name__ == "__main__":
    task = get_next_auto_task()
    if not task:
        print("[MetaTasker] No pending [AUTO] tasks")
        exit(0)
    print(f"[MetaTasker] Task: {task[:60]}")
    raw = generate_code(task)
    if raw.startswith("[ERR"):
        print(raw)
        exit(1)
    code = extract_python(raw)
    path = save_draft(task, code)
    print(f"[MetaTasker] Draft saved: {path}")
    print("[MetaTasker] APPROVE: cat", path, "&& review")
