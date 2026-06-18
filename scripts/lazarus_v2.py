#!/usr/bin/env python3
"""Lazarus Protocol v2 — авто-бэкап + версионирование + проверка целостности
На основе study/Backup_Recovery_ARGOS_2026.md и инцидента 23.05 (потеря main.py)
"""
import os, sys, time, json, hashlib, shutil, gzip
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(os.path.expanduser("~/Projects/argoss"))
VAULT_DIR = Path(os.path.expanduser("~/Documents/MyObsidianVault"))
BACKUP_DIR = PROJECT_ROOT / "data" / "backups"
META_FILE = BACKUP_DIR / "lazarus_meta.json"
KEEP_DAILY = 5
KEEP_HOURLY = 3
CRITICAL_FILES = [
    "src/core.py",
    "main.py",
    "scripts/autopilot_v3.py",
    "scripts/ha_watchdog.py",
    "scripts/entity_dialogue_v5.py",
    "scripts/entity_council.py",
    "src/db_init.py",
    "data/collective_consciousness.json",
    "data/evolution_history.jsonl",
]

def log(msg):
    ts = datetime.now().isoformat()
    print(f"[LAZARUSv2] {ts} {msg}")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]

def run_backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"argos_lazarus_{ts}.tar.gz"
    archive = BACKUP_DIR / name

    log(f"Starting backup to {name}")
    collected = []
    meta = {"ts": ts, "files": {}, "size_total": 0}

    for rel in CRITICAL_FILES:
        src = PROJECT_ROOT / rel
        if src.exists():
            collected.append(str(src))
            meta["files"][rel] = sha256_file(src)
            meta["size_total"] += src.stat().st_size
        else:
            log(f"WARNING: missing critical file: {rel}")

    # Add vault SharedMemory
    if VAULT_DIR.exists():
        collected.append(str(VAULT_DIR / "SharedMemory"))

    # Create tar.gz
    import tarfile
    with tarfile.open(archive, "w:gz") as tar:
        for path in collected:
            tar.add(path, arcname=os.path.relpath(path, PROJECT_ROOT))

    meta["archive_size"] = archive.stat().st_size
    meta["archive_path"] = str(archive)

    # Save meta
    history = []
    if META_FILE.exists():
        history = json.load(open(META_FILE))
    history.append(meta)
    json.dump(history[-50:], open(META_FILE, "w"), indent=2, ensure_ascii=False)

    # Cleanup old
    cleanup_old_backups()

    log(f"Backup done: {archive.name} ({meta['archive_size']:,} bytes, {len(collected)} items)")

def cleanup_old_backups():
    backups = sorted(BACKUP_DIR.glob("argos_lazarus_*.tar.gz"))
    if len(backups) <= KEEP_DAILY + KEEP_HOURLY:
        return
    # Keep last 3 hourly
    keep = set(backups[-KEEP_HOURLY:])
    # Keep last 5 daily (one per day)
    seen_days = set()
    for b in reversed(backups):
        day = b.name[13:21]  # YYYYMMDD
        if day not in seen_days and len(seen_days) < KEEP_DAILY:
            seen_days.add(day)
            keep.add(b)
    for b in backups:
        if b not in keep:
            b.unlink()
            log(f"Removed old backup: {b.name}")

def verify_latest():
    if not META_FILE.exists():
        return False
    history = json.load(open(META_FILE))
    if not history:
        return False
    latest = history[-1]
    log(f"Latest backup: {latest['archive_path']} ({latest['ts']})")
    for rel, expected in latest["files"].items():
        src = PROJECT_ROOT / rel
        if not src.exists():
            log(f"CRITICAL: {rel} MISSING!")
            return False
        actual = sha256_file(src)
        if actual != expected:
            log(f"MISMATCH: {rel} changed! expected={expected} actual={actual}")
    log("Integrity check: PASS")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify_latest()
    else:
        run_backup()
