#!/usr/bin/env python3
"""
auto_rollback.py — health-check + git revert + restart если сервис упал.
Использовать как:
    python auto_rollback.py <service_name> [<health_url>] [<cwd>]
"""
import sys, time, subprocess, urllib.request

def check_health(url, retries=3, delay=5, timeout=3):
    for i in range(retries):
        try:
            r = urllib.request.urlopen(url, timeout=timeout)
            if 200 <= r.status < 400:
                return True
        except Exception:
            pass
        print(f"[WARN] {url} не отвечает (попытка {i+1}/{retries})")
        time.sleep(delay)  # ИСПРАВЛЕНО (было time.time.sleep)
    return False

def git_revert(cwd):
    """Откатить последний коммит. Возвращает True/False."""
    try:
        r = subprocess.run(["git", "revert", "HEAD", "--no-edit"],
                          cwd=cwd, capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            print(f"[WARN] git revert: {r.stderr[:300]}")
            # fallback — git reset --hard HEAD~1
            r2 = subprocess.run(["git", "reset", "--hard", "HEAD~1"],
                              cwd=cwd, capture_output=True, text=True, timeout=30)
            return r2.returncode == 0
        return True
    except Exception as e:
        print(f"[ERR] git: {e}")
        return False

def restart_service(name):
    """Перезапуск через docker service / docker compose / systemctl."""
    for cmd in [
        ["docker", "service", "update", "--force", name],
        ["docker", "compose", "restart", name],
        ["systemctl", "restart", name],
    ]:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if r.returncode == 0:
                print(f"[OK] restart via: {' '.join(cmd)}")
                return True
        except FileNotFoundError:
            continue
        except Exception:
            continue
    print(f"[FAIL] не смог перезапустить {name}")
    return False

if __name__ == "__main__":
    service = sys.argv[1] if len(sys.argv) > 1 else "argos"
    url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:5010/health"
    cwd = sys.argv[3] if len(sys.argv) > 3 else "."

    if check_health(url):
        print(f"[OK] {url} здоров — откат не нужен")
        sys.exit(0)

    print(f"[CRITICAL] {service} упал по {url}, откат...")
    if git_revert(cwd):
        print("[OK] git revert успешен")
    else:
        print("[WARN] git revert провален, restart всё равно пробую")
    restart_service(service)

    time.sleep(15)
    if check_health(url):
        print("[ROLLBACK COMPLETE] система восстановлена")
        sys.exit(0)
    else:
        print("[ROLLBACK FAILED] сервис ещё не отвечает")
        sys.exit(1)
