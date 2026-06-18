#!/usr/bin/env python3
"""Lazarus v2 — автоматический backup всех критических файлов ARGOS.
Study: Self_Healing_SRE_2026.md (безопасность)
"""
import os, shutil, tarfile, datetime, json
from pathlib import Path

PROJECT = Path("/home/ava/Projects/argoss")
BACKUP_ROOT = PROJECT / "backups"
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M")
DAILY_DIR = BACKUP_ROOT / f"lazarus_{TIMESTAMP}"

CRITICAL_FILES = [
    "scripts/orchestrator.py",
    "scripts/entity_council.py",
    "scripts/entity_roles.py",
    "scripts/entity_obsidian_bridge.py",
    "scripts/brain_heartbeat.py",
    "scripts/prometheus_exporter.py",
    "scripts/self_healer.py",
    "scripts/claude_tg_bridge.py",
    "scripts/auto_synthesizer.py",
    "data/collective_consciousness.json",
    "data/evolution/metrics.json",
]

def ensure_daily():
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    if DAILY_DIR.exists():
        return
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[LAZARUS] Backup dir: {DAILY_DIR}")

    for rel in CRITICAL_FILES:
        src = PROJECT / rel
        if not src.exists():
            print(f"  skip (missing): {rel}")
            continue
        dst = DAILY_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        print(f"  copied: {rel}")

    # Metadata
    info = {
        "timestamp": TIMESTAMP,
        "hostname": os.uname().nodename,
        "files": CRITICAL_FILES,
        "notes": "Lazarus v2 auto-backup"
    }
    (DAILY_DIR / "manifest.json").write_text(json.dumps(info, indent=2, ensure_ascii=False))
    print(f"[LAZARUS] {len(CRITICAL_FILES)} files backed up.")

    # Cleanup old backups (keep last 7)
    dirs = sorted(BACKUP_ROOT.glob("lazarus_*"))
    for old in dirs[:-7]:
        shutil.rmtree(str(old))
        print(f"[LAZARUS] Removed old: {old.name}")

def restore_latest():
    dirs = sorted(BACKUP_ROOT.glob("lazarus_*"))
    if not dirs:
        print("[LAZARUS] No backups found.")
        return
    latest = dirs[-1]
    manifest = json.load(open(latest / "manifest.json"))
    print(f"[LAZARUS] Restoring from {latest.name} ({manifest['timestamp']})")
    for rel in manifest.get("files", []):
        src = latest / rel
        dst = PROJECT / rel
        if src.exists():
            shutil.copy2(str(src), str(dst))
            print(f"  restored: {rel}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        restore_latest()
    else:
        ensure_daily()
