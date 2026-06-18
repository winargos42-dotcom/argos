#!/usr/bin/env python3
"""
Git Auto-Backup — daily backup всех конфигов и памяти.
Журналы (JOURNAL.md, STATUS.md, WORKING.md → git + Obsidian).
"""
import subprocess, datetime
from pathlib import Path

ARGOS_DIR = Path("/home/ava/Projects/argoss")
VAULT_DIR = Path("/home/ava/Documents/MyObsidianVault")
LOG = Path("/home/ava/Projects/argoss/data/mempalace/git_backup.log")

# Только ключевые файлы (не data/)
BACKUP_PATTERNS = [
    "scripts/*.py", "scripts/*.sh",
    "*.yml", "*.yaml", "*.json",
    "esphome/*.yaml",
    "config/*",
    "monitoring/*",
    "*.md"
]

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())

def run_git_cmd(args, cwd=None):
    r = subprocess.run(["git"] + args, capture_output=True, text=True, timeout=30, cwd=cwd or ARGOS_DIR)
    return r.returncode == 0, r.stdout.strip(), r.stderr.strip()

def backup_argos():
    log("ARGOS backup...")
    # Добавляем только ключевые файлы
    for pattern in BACKUP_PATTERNS:
        subprocess.run(["git", "add", "-f", pattern],
            capture_output=True, timeout=10, cwd=ARGOS_DIR)
    
    # Коммит если есть изменения
    ok, _, _ = run_git_cmd(["diff", "--cached", "--quiet"])
    if ok:
        log("  No changes")
        return True
    
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    ok, out, err = run_git_cmd(["commit", "-m", f"Auto-backup {ts}"])
    if ok:
        log("  Committed")
    else:
        log(f"  Commit: {err[:100]}")
    
    # Push если есть remote
    ok, _, _ = run_git_cmd(["remote"])
    if ok:
        ok, out, err = run_git_cmd(["push"])
        if ok:
            log("  Pushed")
        else:
            log(f"  Push skipped: {err[:80]}")
    else:
        log("  No remote configured")
    return True

def backup_vault():
    log("Vault backup...")
    if not (VAULT_DIR / ".git").exists():
        log("  Vault not a git repo, skipping")
        return False
    
    ok, _, _ = run_git_cmd(["add", "."], cwd=VAULT_DIR)
    ok, _, _ = run_git_cmd(["diff", "--cached", "--quiet"], cwd=VAULT_DIR)
    if ok:
        log("  No changes")
        return True
    
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    ok, out, err = run_git_cmd(["commit", "-m", f"Vault auto-backup {ts}"], cwd=VAULT_DIR)
    if ok:
        log("  Committed")
    else:
        log(f"  Commit: {err[:100]}")
    return True

if __name__ == "__main__":
    log("="*40)
    log("DAILY BACKUP STARTED")
    backup_argos()
    backup_vault()
    log("DAILY BACKUP COMPLETE")
    log("="*40)
