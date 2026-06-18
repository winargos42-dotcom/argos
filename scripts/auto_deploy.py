#!/usr/bin/env python3
"""
Auto-Deploy — деплой одобренных скриптов.
Смотрит в /tmp/metagpt_tasks/ на файлы с суффиксом .APPROVED.
Копирует в scripts/, git commit, restart.
"""
import os, subprocess, re, datetime, time
from pathlib import Path

SRC_DIR = Path("/tmp/metagpt_tasks")
DST_DIR = Path("/home/ava/Projects/argoss/scripts")
GIT_DIR = Path("/home/ava/Projects/argoss")
LOG = Path("/home/ava/Projects/argoss/data/mempalace/auto_deploy.log")

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())

def pre_deploy_snapshot():
    """Сохраняем git hash перед деплоем для rollback."""
    try:
        import json
        r = subprocess.run(["git","-C",str(GIT_DIR),"rev-parse","HEAD"],
            capture_output=True, text=True, timeout=5)
        h = r.stdout.strip() if r.returncode == 0 else "unknown"
        state = {"hash": h, "ts": datetime.datetime.now().isoformat()}
        state_file = Path("/home/ava/Projects/argoss/data/mempalace/rollback_state.json")
        state_file.write_text(json.dumps(state, ensure_ascii=False))
        log(f"Snapshot taken: {h[:8]}")
    except Exception as e:
        log(f"Snapshot error: {e}")

def trigger_rollback_check():
    """Запускаем rollback проверку через 3 минуты в bg."""
    subprocess.Popen([
        "bash","-c",
        "sleep 180 && source /home/ava/Projects/argoss/.venv/bin/activate && python3 /home/ava/Projects/argoss/scripts/auto_rollback.py"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log("Rollback check scheduled in 3 min")

def deploy_approved():
    if not SRC_DIR.exists():
        log("No metagpt_tasks dir")
        return 0
    
    approved = sorted(SRC_DIR.glob("*.APPROVED"))
    if not approved:
        log("No .APPROVED files")
        return 0
    
    # Snapshot ПЕРЕД деплоем
    pre_deploy_snapshot()
    
    deployed = 0
    for f in approved:
        # Убираем .APPROVED — получаем имя скрипта
        base = f.name.replace(".APPROVED", "")
        dst = DST_DIR / base
        
        try:
            content = f.read_text(encoding="utf-8")
            dst.write_text(content, encoding="utf-8")
            os.chmod(dst, 0o755)
            log(f"Copied {base} → scripts/")
            
            # Git commit
            os.chdir(GIT_DIR)
            subprocess.run(["git", "add", str(dst)], capture_output=True, timeout=10)
            r = subprocess.run(["git", "commit", "-m", f"Auto-deploy: {base}"],
                capture_output=True, text=True, timeout=10)
            if r.returncode == 0:
                log(f"Git committed: {base}")
            else:
                log(f"Git: nothing to commit or error")
            
            # Restart если есть юнит
            svc = base.replace(".py", "").replace("_", "-")
            r2 = subprocess.run(["systemctl", "is-active", f"argos-{svc}"],
                capture_output=True, text=True, timeout=5)
            if r2.returncode == 0:
                subprocess.run(["sudo", "systemctl", "restart", f"argos-{svc}"],
                    capture_output=True, timeout=10)
                log(f"Restarted argos-{svc}")
            
            # Удаляем .APPROVED
            f.unlink()
            os.remove(f.with_suffix('')) if f.with_suffix('').exists() else None
            deployed += 1
            
        except Exception as e:
            log(f"FAIL {base}: {e}")
    
    log(f"Deployed {deployed} files")
    
    if deployed > 0:
        trigger_rollback_check()
    
    return deployed

if __name__ == "__main__":
    deploy_approved()
