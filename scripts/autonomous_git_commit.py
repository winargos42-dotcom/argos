#!/usr/bin/env python3
"""
ARGOS Autonomous Git Commit — автокоммит Obsidian vault.
Каждый час проверяет изменения, коммитит с intelligible сообщением.
Если изменений нет — skip.
"""
import subprocess, os, sys
from datetime import datetime, timezone
from pathlib import Path

VAULT = Path("/home/ava/Documents/MyObsidianVault")

def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or VAULT)

def get_diff_summary():
    # Получить список изменённых файлов
    out = run(["git","status","--short"])
    files = [l.strip() for l in out.stdout.strip().split("\n") if l.strip()]
    return files

def ai_commit_message(files):
    """Генерирует commit message на основе изменений"""
    if not files:
        return None
    # Категоризируем
    daily = [f for f in files if "Daily/" in f]
    memory = [f for f in files if "Memory/" in f or "03 Memory/" in f]
    shared = [f for f in files if "SharedMemory/" in f]
    logs = [f for f in files if "Logs/" in f or "02 Logs/" in f]
    
    parts = []
    if daily:
        parts.append(f"daily logs ({len(daily)} files)")
    if memory:
        parts.append(f"knowledge base ({len(memory)} files)")
    if shared:
        parts.append(f"shared memory ({len(shared)} files)")
    if logs:
        parts.append(f"session logs ({len(logs)} files)")
    if not parts:
        parts.append(f"vault updates ({len(files)} files)")
    
    return "autonomous: " + ", ".join(parts)

def main():
    os.chdir(VAULT)
    
    # Проверяем, что это git repo
    if not (VAULT / ".git").exists():
        print(f"[{datetime.now(timezone.utc)}] No git repo in {VAULT}")
        sys.exit(1)
    
    files = get_diff_summary()
    if not files:
        print(f"[{datetime.now(timezone.utc)}] No changes to commit")
        sys.exit(0)
    
    msg = ai_commit_message(files)
    
    # add all
    run(["git","add","-A"])
    
    # commit
    out = run(["git","commit","-m",msg])
    if out.returncode == 0:
        print(f"[{datetime.now(timezone.utc)}] Committed: {msg}")
        # push если есть remote
        rem = run(["git","remote"])
        if rem.stdout.strip():
            push = run(["git","push"])
            if push.returncode == 0:
                print(f"  → pushed to remote")
            else:
                print(f"  → push failed: {push.stderr.strip()}")
    else:
        print(f"[{datetime.now(timezone.utc)}] Commit failed: {out.stderr.strip()}")

if __name__ == "__main__":
    main()
