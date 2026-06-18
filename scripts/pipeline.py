#!/usr/bin/env python3
"""
ARGOS Full Auto-Pipeline — Phase 4.5.
Единый скрипт, связывающий:
  WORKING.md [AUTO] → Codegen → Auto-Test → (Approve) → Auto-Deploy → Auto-Rollback
"""
import re, subprocess, sys, json, time
from pathlib import Path
from datetime import datetime

WORKING = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md")
TASK_DIR = Path("/tmp/metagpt_tasks")
SCRIPTS = Path("/home/ava/Projects/argoss/scripts")
VENV = "/home/ava/Projects/argoss/.venv/bin/activate"

def extract_first_auto_task():
    """Находит первую [AUTO]-строку в WORKING.md."""
    if not WORKING.exists(): return None
    text = WORKING.read_text(encoding="utf-8")
    m = re.search(r"- \[AUTO[^\]]*\] (.+)", text)
    return m.group(1).strip() if m else None

def remove_task_from_working(task_text):
    """Удаляет выполненную задачу из WORKING.md."""
    text = WORKING.read_text(encoding="utf-8")
    text = re.sub(rf"- \[AUTO[^\]]*\] {re.escape(task_text)}.*\n", "", text)
    WORKING.write_text(text, encoding="utf-8")

def run_codegen(task):
    """Вызывает codegen_loop для генерации кода."""
    print(f"[Pipeline] Codegen for: {task[:60]}...")
    r = subprocess.run(
        ["bash","-c",f"source {VENV} && python3 {SCRIPTS}/codegen_loop.py"],
        capture_output=True, text=True, timeout=120
    )
    # Находим последний .py в TASK_DIR
    files = sorted(TASK_DIR.glob("*.py"))
    if not files:
        return None
    latest = files[-1]
    print(f"[Pipeline] Generated: {latest.name}")
    return latest

def run_test(py_file):
    """Запускает auto_test.py на файле."""
    print(f"[Pipeline] Testing {py_file.name}...")
    r = subprocess.run(
        ["bash","-c",f"source {VENV} && python3 {SCRIPTS}/auto_test.py {py_file}"],
        capture_output=True, text=True, timeout=30
    )
    tested = Path(str(py_file) + ".TESTED")
    return tested.exists()

def trigger_approve(py_file):
    """Если auto_approve=True (Phase 5) — мгновенно .APPROVED. Иначе ждёт human."""
    # Phase 4.5: human-in-the-loop
    # Phase 5: auto_approve = True
    tested = Path(str(py_file) + ".TESTED")
    if tested.exists():
        approved = Path(str(py_file) + ".APPROVED")
        # Для Phase 4.5 требуется ручной approve
        print(f"[Pipeline] ⏳ WAITING for .APPROVED: {tested}")
        print(f"[Pipeline]    Run: mv {tested} {approved}")
        return False
    return False

def run_deploy():
    """Запускает auto_deploy.py (со snapshot + rollback)."""
    print("[Pipeline] Deploying approved files...")
    subprocess.run(
        ["bash","-c",f"source {VENV} && python3 {SCRIPTS}/auto_deploy.py"],
        capture_output=True, text=True, timeout=60
    )

def append_status(task, status, detail=""):
    """Дописывает результат в WORKING.md."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"\n- [{ts}] Pipeline: '{task[:40]}...' → {status}"
    if detail:
        line += f" ({detail})"
    with open(WORKING, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def run_pipeline(auto_approve=False):
    task = extract_first_auto_task()
    if not task:
        print("[Pipeline] No [AUTO] tasks found")
        return
    
    print(f"\n{'='*60}")
    print(f"[Pipeline] TASK: {task}")
    print(f"{'='*60}")
    
    # Step 1: Codegen
    py_file = run_codegen(task)
    if not py_file:
        append_status(task, "FAIL", "codegen error")
        return
    
    # Step 2: Test
    if not run_test(py_file):
        append_status(task, "FAIL", "auto-test failed")
        return
    
    # Step 3: Approve
    if not auto_approve:
        trigger_approve(py_file)
        append_status(task, "TESTED", "awaiting .APPROVED")
        return
    
    # Auto-approve (Phase 5)
    tested = Path(str(py_file) + ".TESTED")
    approved = Path(str(py_file) + ".APPROVED")
    tested.rename(approved)
    print(f"[Pipeline] Auto-approved: {approved.name}")
    
    # Step 4: Deploy
    run_deploy()
    append_status(task, "DEPLOYED", "with rollback snapshot")
    
    # Step 5: Очистка задачи из WORKING
    remove_task_from_working(task)
    print(f"[Pipeline] ✅ COMPLETE")

if __name__ == "__main__":
    auto = "--auto" in sys.argv
    run_pipeline(auto_approve=auto)
