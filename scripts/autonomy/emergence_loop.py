#!/usr/bin/env python3
"""
emergence_loop.py — Phase 5 ядро: AI читает WORKING.md, генерирует
следующую задачу, пишет файл-кандидат, гоняет auto_test, ждёт ручного
APPROVED, потом auto_rollback мониторит. NO autonomous deploy без APPROVED.
"""
import os, sys, time, json, subprocess, glob, hashlib
from pathlib import Path

WORKING_MD = os.environ.get("ARGOS_WORKING_MD",
    "/home/ava/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md")
CANDIDATES = Path(os.environ.get("ARGOS_CANDIDATES", "/tmp/argos_candidates"))
APPROVED_DIR = Path(os.environ.get("ARGOS_APPROVED", "/tmp/argos_approved"))
SCRIPT_DIR = Path(__file__).resolve().parent

CANDIDATES.mkdir(parents=True, exist_ok=True)
APPROVED_DIR.mkdir(parents=True, exist_ok=True)

def read_working():
    try:
        return open(WORKING_MD, encoding="utf-8").read()
    except Exception as e:
        return f"# WORKING.md недоступен: {e}"

def list_open_tasks(text):
    """Извлекает строки вида '- [ ] task' или '## TODO: task'."""
    tasks = []
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("- [ ]") or s.startswith("- [AUTO]"):
            tasks.append(s.lstrip("- []").lstrip("AUTO").strip(": ").strip())
        elif s.startswith("TODO:") or s.startswith("## TODO"):
            tasks.append(s.split(":", 1)[-1].strip())
    return tasks

def run_auto_test(file_path):
    """Прогон auto_test.py на кандидата."""
    test_script = SCRIPT_DIR / "auto_test.py"
    if not test_script.exists():
        return False, "auto_test.py не найден"
    r = subprocess.run([sys.executable, str(test_script), str(file_path)],
                      capture_output=True, text=True, timeout=60)
    return (r.returncode == 0), r.stdout + r.stderr

def is_approved(candidate):
    """Кандидат считается одобренным если рядом лежит файл .APPROVED."""
    return (APPROVED_DIR / f"{candidate.stem}.APPROVED").exists()

def tick():
    text = read_working()
    tasks = list_open_tasks(text)
    if not tasks:
        return {"status": "idle", "reason": "нет открытых задач в WORKING.md"}

    # Сейчас — НЕ генерируем код, только репортим что есть в очереди.
    # Реальная генерация требует подключения к Brain API / Claude API.
    return {
        "status": "scanning",
        "tasks_found": len(tasks),
        "first_3": tasks[:3],
        "note": "генерация отключена до явного APPROVED workflow"
    }

def deploy_approved():
    """Подхватываем одобренных кандидатов и складываем в production."""
    deployed = []
    for cand in CANDIDATES.glob("*.py"):
        if not is_approved(cand): continue
        ok, log = run_auto_test(cand)
        if not ok:
            print(f"[SKIP] {cand.name}: тест провален")
            continue
        # сюда — реальная замена production-файла
        # пока только лог
        print(f"[READY] {cand.name} прошёл тест и APPROVED — готов к ручному copy")
        deployed.append(str(cand))
    return deployed

if __name__ == "__main__":
    while True:
        try:
            state = tick()
            print(f"[TICK {time.strftime('%H:%M:%S')}] {json.dumps(state, ensure_ascii=False)}")
            deploy_approved()
        except Exception as e:
            print(f"[ERR] {e}")
        time.sleep(int(os.environ.get("ARGOS_LOOP_INTERVAL", "300")))
