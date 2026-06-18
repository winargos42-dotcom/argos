#!/usr/bin/env python3
"""
Lazarus v2 — Off-site backup на OPi (192.168.2.168)
Копирует последний локальный backup + критичные файлы на Orange Pi
"""
import os, sys, pathlib, subprocess, datetime, json

HOME             = pathlib.Path("/home/ava")
LOCAL_BACKUP_DIR = HOME / "Projects/lazarus_backups"
OPi_HOST         = "root@192.168.2.168"
OPi_KEY          = HOME / ".ssh/id_ed25519"
OPi_REMOTE_DIR   = "/home/ava/backups"
LOG_PATH         = HOME / "Projects/argoss/logs/lazarus_offsite.log"

CRITICAL_FILES = [
    HOME / "Documents/MyObsidianVault/SharedMemory/shared/WORKING.md",
    HOME / "Documents/MyObsidianVault/SharedMemory/shared/STATUS.md",
    HOME / "Documents/MyObsidianVault/SharedMemory/shared/AGENTS.md",
    HOME / "Documents/MyObsidianVault/SharedMemory/shared/JOURNAL.md",
    HOME / "Documents/MyObsidianVault/SharedMemory/entities/council/EVOLUTION_LOG.md",
    HOME / "Projects/argoss/data/collective_consciousness.json",
    HOME / "Projects/argoss/data/knowledge_graph.json",
    HOME / "Projects/argoss/data/evolution/metrics.json",
    HOME / "Projects/argoss/scripts/entity_council.py",
    HOME / "Projects/argoss/scripts/orchestrator.py",
]

def log(msg: str):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def ssh_cmd(cmd: str, timeout: int = 60) -> dict:
    full = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5",
            "-i", str(OPi_KEY), OPi_HOST, cmd]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout, check=False)
        return {"ok": r.returncode == 0, "stdout": r.stdout, "stderr": r.stderr}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e)}

def scp_file(local: pathlib.Path, remote: str) -> bool:
    full = ["scp", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10",
            "-i", str(OPi_KEY), str(local), f"{OPi_HOST}:{remote}"]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=120, check=False)
        return r.returncode == 0
    except Exception as e:
        log(f"scp fail {local}: {e}")
        return False

def ensure_remote_dir():
    r = ssh_cmd(f"mkdir -p {OPi_REMOTE_DIR}")
    if not r["ok"]:
        log(f"WARNING: mkdir remote failed: {r['stderr'][:100]}")

def backup_latest_tarball():
    if not LOCAL_BACKUP_DIR.exists():
        log(f"Local backup dir missing: {LOCAL_BACKUP_DIR}")
        return
    tars = sorted(LOCAL_BACKUP_DIR.glob("lazarus_*.tar.gz"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not tars:
        log("No local tarballs found")
        return
    latest = tars[0]
    log(f"Off-site tarball: {latest.name}")
    if scp_file(latest, f"{OPi_REMOTE_DIR}/{latest.name}"):
        log(f"  ✅ Tarball copied")
    else:
        log(f"  ❌ Tarball failed")

def backup_critical_files():
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    remote_subdir = f"{OPi_REMOTE_DIR}/critical_{now}"
    ssh_cmd(f"mkdir -p {remote_subdir}")
    ok = 0; fail = 0
    for local in CRITICAL_FILES:
        if not local.exists():
            fail += 1
            continue
        dest = f"{remote_subdir}/{local.name}"
        if scp_file(local, dest):
            ok += 1
        else:
            fail += 1
    log(f"  Critical files: {ok} ok, {fail} failed")

def main():
    log("=== Lazarus v2 off-site backup START ===")
    ensure_remote_dir()
    backup_latest_tarball()
    backup_critical_files()
    # Remote cleanup: keep last 7 tarballs
    ssh_cmd(f"ls -t {OPi_REMOTE_DIR}/lazarus_*.tar.gz 2>/dev/null | tail -n +8 | xargs rm -f")
    log("=== Lazarus v2 off-site backup DONE ===")

if __name__ == "__main__":
    main()
