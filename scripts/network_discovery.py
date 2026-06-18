#!/usr/bin/env python3
"""
ARGOS Network Discovery — авто-обнаружение ПК при смене IP.

Что делает:
- Сканирует 192.168.1.0/24, находит ПК по открытому Brain API (порт 5001)
- При изменении IP обновляет .env, скрипты, конфиги
- Синхронизирует обновления на телефон (ADB) и OPi (SSH)
- Пишет новый IP в SharedMemory/shared/STATUS.md
- Запускается каждые 5 мин через cron/systemd
"""
import os, sys, json, socket, subprocess, re, time
from pathlib import Path
from datetime import datetime

ARGOSS = Path(__file__).parent.parent
ENV_FILE = ARGOSS / ".env"
STATUS_FILE = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/STATUS.md")
CACHE_FILE = Path("/tmp/argos_pc_ip.cache")
SUBNET = "192.168.1"
BRAIN_PORT = 5001
TIMEOUT = 1.5

def is_pc_brain(ip: str) -> bool:
    """Проверяет что это ПК Orion: Brain API открыт И содержит node 'argos-pc'."""
    try:
        import urllib.request
        url = f"http://{ip}:{BRAIN_PORT}/brain/nodes"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read().decode())
            node_ids = [n.get("node_id","") for n in data.get("nodes", [])]
            return "argos-pc" in node_ids
    except Exception:
        return False

def scan_for_pc() -> str | None:
    """Сканирование — находим ПК по Brain API с node 'argos-pc' (не OPi/HA)."""
    import concurrent.futures

    def check(ip: str) -> str | None:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            r = s.connect_ex((ip, BRAIN_PORT))
            s.close()
            if r == 0 and is_pc_brain(ip):
                return ip
        except Exception:
            pass
        return None

    candidates = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=60) as ex:
        futures = {ex.submit(check, f"{SUBNET}.{i}"): i for i in range(1, 255)}
        for f in concurrent.futures.as_completed(futures):
            ip = f.result()
            if ip:
                candidates.append(ip)

    return candidates[0] if candidates else None

def get_cached_ip() -> str | None:
    try:
        data = json.loads(CACHE_FILE.read_text())
        if time.time() - data.get("ts", 0) < 300:   # кэш 5 мин
            return data.get("ip")
    except Exception:
        pass
    return None

def save_cache(ip: str):
    CACHE_FILE.write_text(json.dumps({"ip": ip, "ts": time.time()}))

def get_current_pc_ip() -> str | None:
    """Читает текущий IP из .env."""
    try:
        text = ENV_FILE.read_text(errors="ignore")
        m = re.search(r"BRAIN_HOST\s*=\s*(\d+\.\d+\.\d+\.\d+)", text)
        if m:
            return m.group(1)
        m = re.search(r"192\.168\.1\.(\d+)", text)
        if m:
            return f"192.168.1.{m.group(1)}"
    except Exception:
        pass
    return None

def update_env(old_ip: str, new_ip: str):
    """Заменяет IP в .env."""
    text = ENV_FILE.read_text(errors="ignore")
    new_text = text.replace(old_ip, new_ip)
    if old_ip in text:
        # Уточняем порт Brain
        new_text = re.sub(
            r"BRAIN_HOST\s*=\s*\d+\.\d+\.\d+\.\d+",
            f"BRAIN_HOST={new_ip}",
            new_text
        )
        ENV_FILE.write_text(new_text)
        print(f"  .env: {old_ip} → {new_ip}")

def update_scripts(old_ip: str, new_ip: str):
    """Заменяет IP во всех py/yml скриптах."""
    patterns = [ARGOSS / "scripts", ARGOSS / "src", ARGOSS / "config"]
    count = 0
    for d in patterns:
        for f in d.rglob("*.py"):
            if "backup" in str(f):
                continue
            try:
                t = f.read_text(errors="ignore")
                if old_ip in t:
                    f.write_text(t.replace(old_ip, new_ip))
                    count += 1
            except Exception:
                pass
    print(f"  Скриптов обновлено: {count}")

def sync_to_phone(new_ip: str):
    """Обновляет valenok_agent.py на телефоне через ADB."""
    try:
        agent = ARGOSS / "scripts" / "valenok_agent.py"
        # push
        r = subprocess.run(["adb", "push", str(agent), "/sdcard/valenok_agent.py"],
                           capture_output=True, timeout=15)
        if r.returncode != 0:
            print(f"  ADB push fail: {r.stderr.decode()[:100]}")
            return
        subprocess.run(["adb", "shell", "su -c 'cp /sdcard/valenok_agent.py "
                        "/data/data/com.termux/files/home/valenok_agent.py && "
                        "pkill -f valenok_agent 2>/dev/null; sleep 1; "
                        "cd /data/data/com.termux/files/home && "
                        "PATH=/data/data/com.termux/files/usr/bin:$PATH "
                        "nohup python3 -u valenok_agent.py > /data/local/tmp/valenok.log 2>&1 &'"],
                       timeout=20, capture_output=True)
        print(f"  Телефон: valenok_agent.py обновлён → Brain {new_ip}:5001")
    except Exception as e:
        print(f"  ADB sync err: {e}")

def sync_to_opi(new_ip: str):
    """Опционально — синхронизируем OPi (если доступна)."""
    # Сначала ищем OPi в leases
    try:
        leases = Path("/var/lib/misc/dnsmasq.leases").read_text()
        opi_ip = None
        for line in leases.splitlines():
            parts = line.split()
            if len(parts) >= 4 and "orange" in parts[3].lower():
                opi_ip = parts[2]
                break
        if not opi_ip:
            return
        r = subprocess.run(["ssh", "-o", "ConnectTimeout=3", "-o", "BatchMode=yes",
                             "-i", "/home/ava/.ssh/id_ed25519",
                             f"root@{opi_ip}",
                             f"sed -i 's/192\\.168\\.1\\.[0-9]\\+:5001/{new_ip}:5001/g' "
                             f"/root/argos/*.py /root/argoss/*.py 2>/dev/null || true"],
                           capture_output=True, timeout=10)
        print(f"  OPi {opi_ip}: {'OK' if r.returncode==0 else 'SKIP'}")
    except Exception:
        pass

def update_status_md(new_ip: str):
    """Пишем новый IP в STATUS.md."""
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n## PC IP обновлён {ts}\n- Brain API: http://{new_ip}:5001\n"
        if STATUS_FILE.exists():
            txt = STATUS_FILE.read_text()
            # Убираем старые PC IP записи (последние 3)
            txt = re.sub(r"\n## PC IP обновлён [^\n]+\n.*?(?=\n##|\Z)", "", txt, flags=re.DOTALL)
            STATUS_FILE.write_text(txt + entry)
        else:
            STATUS_FILE.write_text(f"# STATUS\n{entry}")
        print(f"  STATUS.md обновлён")
    except Exception as e:
        print(f"  STATUS.md err: {e}")

def restart_local_services():
    """Перезапускаем entity_valenok.py на ноутбуке."""
    try:
        subprocess.run(["pkill", "-f", "entity_valenok.py"], capture_output=True)
        time.sleep(1)
        subprocess.Popen(
            [str(ARGOSS / ".venv/bin/python3"), "-u", "scripts/entity_valenok.py"],
            cwd=str(ARGOSS), stdout=open("/tmp/entity_valenok.log", "a"),
            stderr=subprocess.STDOUT, start_new_session=True
        )
        print("  entity_valenok.py перезапущен")
    except Exception as e:
        print(f"  restart err: {e}")

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ARGOS Network Discovery")

    # 1. Проверяем кэш
    cached = get_cached_ip()
    if cached:
        try:
            s = socket.socket()
            s.settimeout(1)
            if s.connect_ex((cached, BRAIN_PORT)) == 0:
                s.close()
                print(f"  ПК {cached} — онлайн (кэш OK)")
                save_cache(cached)
                return
            s.close()
        except Exception:
            pass

    # 2. Сканируем
    print("  Сканируем 192.168.1.0/24...")
    new_ip = scan_for_pc()
    if not new_ip:
        print("  ПК не найден!")
        return

    print(f"  ПК найден: {new_ip}:5001")
    save_cache(new_ip)

    # 3. Сравниваем с текущим
    old_ip = get_current_pc_ip()
    if old_ip == new_ip:
        print(f"  IP не изменился ({new_ip})")
        return

    print(f"  IP изменился: {old_ip} → {new_ip}")

    # 4. Обновляем везде
    if old_ip:
        update_env(old_ip, new_ip)
        update_scripts(old_ip, new_ip)

    # Записываем новый IP
    try:
        txt = ENV_FILE.read_text(errors="ignore")
        if "BRAIN_HOST=" not in txt:
            ENV_FILE.write_text(txt + f"\nBRAIN_HOST={new_ip}\n")
        else:
            ENV_FILE.write_text(re.sub(r"BRAIN_HOST=\S+", f"BRAIN_HOST={new_ip}", txt))
    except Exception:
        pass

    # 5. Синхронизируем
    sync_to_phone(new_ip)
    sync_to_opi(new_ip)
    update_status_md(new_ip)
    restart_local_services()

    print(f"  Готово! Brain: http://{new_ip}:5001")

if __name__ == "__main__":
    main()
