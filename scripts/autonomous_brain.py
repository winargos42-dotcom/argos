#!/usr/bin/env python3
"""
ARGOS Autonomous Brain — цикл автономного мышления на ноутбуке.

Каждые 10 минут:
  1. Читает inbox из message bus
  2. Анализирует состояние всех нод (heartbeat)
  3. Принимает решения (если что-то упало — чинит, если нагрузка высокая — балансирует)
  4. Выполняет действия через MCP tools
  5. Публикует отчёт в bus + пишет в Obsidian

Решения:
  • CPU > 85% → nice +19 для non-critical, alert
  • RAM > 85% → drop_caches, alert
  • Нода мертва > 5 мин → restart command через bus
  • HA entity < 40 → проверить Z2M, permit_join
  • Нет heartbeat от ПК → SSH wakeup
  • Disk > 90% → cleanup suggestion
"""
import json, time, os, sys, subprocess, threading
from datetime import datetime, timezone
from pathlib import Path

import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MCP_URL = "http://localhost:8000/mcp"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjMWIwZDgxNzdkNDY0NGRjOWM4YmI4OGZiM2VkOGRjZSIsImlhdCI6MTc3NzkyMDY5MiwiZXhwIjoyMDkzMjgwNjkyfQ.nV0ps3wDPz4NAiqwKCyyTLcwK-oxUdvg2ohIG4p6Ozs"

OBSIDIAN_DAILY = Path("/home/ava/Documents/MyObsidianVault/Daily")

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def log_to_obsidian(content):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = OBSIDIAN_DAILY / f"{today}-brain.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n---\n\n{content}\n")

def check_url(url, timeout=5, headers=None, max_body=2_000_000):
    import urllib.request, urllib.error
    try:
        req = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"ok": True, "status": resp.status, "body": resp.read(max_body).decode()}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def mcp_call(tool, args, timeout=30):
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": tool, "arguments": args},
        "id": int(time.time())
    }
    try:
        req = urllib.request.Request(MCP_URL, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def get_system_metrics():
    """CPU, RAM, disk, temp"""
    metrics = {}
    # CPU
    try:
        with open("/proc/stat") as f:
            line = f.readline()
            fields = list(map(int, line.split()[1:]))
            metrics["cpu_total"] = sum(fields)
            metrics["cpu_idle"] = fields[3]
    except: pass
    # RAM
    try:
        with open("/proc/meminfo") as f:
            for l in f:
                if l.startswith("MemTotal:"):
                    metrics["mem_total"] = int(l.split()[1]) * 1024
                elif l.startswith("MemAvailable:"):
                    metrics["mem_avail"] = int(l.split()[1]) * 1024
    except: pass
    # Temp
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            metrics["temp"] = int(f.read().strip()) / 1000
    except: pass
    # Disk
    try:
        st = os.statvfs("/")
        metrics["disk_total"] = st.f_blocks * st.f_frsize
        metrics["disk_free"] = st.f_bavail * st.f_frsize
    except: pass
    return metrics

_ha_cooldown = {}

def get_ha_status():
    r = check_url("http://localhost:8123/api/states", headers={"Authorization": f"Bearer {HA_TOKEN}"}, timeout=10, max_body=5_000_000)
    if r["ok"]:
        try:
            states = json.loads(r["body"])
            return {"ok": True, "entities": len(states), "active": len([s for s in states if s["state"] not in ("unknown","unavailable","")])}
        except Exception as e:
            return {"ok": False, "error": f"json_parse: {e}"}
    return r

def get_node_status():
    """Проверяем все ноды"""
    nodes = {}
    # Local
    r = check_url("http://localhost:8000/health")
    nodes["local"] = {"ok": r["ok"], "url": "http://localhost:8000"}
    # PC
    r = check_url("http://192.168.1.53:8000/health")
    nodes["pc"] = {"ok": r["ok"], "url": "http://192.168.1.53:8000"}
    # Railway
    r = check_url("https://argos-v2-production.up.railway.app/health")
    nodes["railway"] = {"ok": r["ok"], "url": "https://argos-v2-production.up.railway.app"}
    # Orange Pi
    r = check_url("http://192.168.2.168:7777/")
    nodes["orangepi"] = {"ok": r["ok"], "url": "http://192.168.2.168:7777"}
    # ESP32 Display
    r = check_url("http://192.168.1.211/?text=HEARTBEAT")
    nodes["esp32_display"] = {"ok": r["ok"], "url": "http://192.168.1.211", "type": "esp32"}
    # ESP8266 Bridge
    r = check_url("http://192.168.1.181/")
    nodes["esp8266_bridge"] = {"ok": r["ok"], "url": "http://192.168.1.181", "type": "esp8266"}
    return nodes

def take_decisions(metrics, nodes, ha):
    """Принимаем решения на основе метрик"""
    decisions = []
    
    # 1. CPU check
    if "cpu_total" in metrics and "cpu_idle" in metrics and metrics["cpu_total"] > 0:
        cpu_pct = 100 * (1 - metrics["cpu_idle"] / metrics["cpu_total"])
        if cpu_pct > 85:
            decisions.append({
                "priority": "high",
                "action": "cpu_throttle",
                "reason": f"CPU {cpu_pct:.1f}% > 85%",
                "command": "renice_non_critical"
            })
    
    # 2. RAM check
    if "mem_total" in metrics and "mem_avail" in metrics and metrics["mem_total"] > 0:
        ram_pct = 100 * (1 - metrics["mem_avail"] / metrics["mem_total"])
        if ram_pct > 85:
            decisions.append({
                "priority": "high",
                "action": "ram_cleanup",
                "reason": f"RAM {ram_pct:.1f}% > 85%",
                "command": "drop_caches"
            })
    
    # 3. Temperature
    if "temp" in metrics and metrics["temp"] > 90:
        decisions.append({
            "priority": "critical",
            "action": "thermal_alert",
            "reason": f"Temp {metrics['temp']}°C > 90°C",
            "command": "alert_thermal"
        })
    
    # 4. Node health
    for name, node in nodes.items():
        if not node["ok"]:
            decisions.append({
                "priority": "high",
                "action": "revive_node",
                "reason": f"Node {name} unreachable",
                "command": f"restart_{name}",
                "target": name
            })
    
    # 5. ESP device checks
    for name, node in nodes.items():
        node_type = node.get("type", "")
        if not node["ok"] and node_type in ("esp32", "esp8266"):
            decisions.append({
                "priority": "high",
                "action": "esp_alert",
                "reason": f"ESP device {name} unreachable",
                "command": "alert_esp_down",
                "target": name
            })
    
    # 6. HA check
    if ha.get("ok") and "active" in ha:
        active = ha.get("active", 0)
        last_ha_check = _ha_cooldown.get("ha_check", 0)
        if active < 40 and (time.time() - last_ha_check) > 3600:
            _ha_cooldown["ha_check"] = time.time()
            decisions.append({
                "priority": "medium",
                "action": "ha_check",
                "reason": f"HA active entities {active} < 40",
                "command": "check_zigbee_devices"
            })
    else:
        decisions.append({
            "priority": "critical",
            "action": "revive_ha",
            "reason": "Home Assistant unreachable",
            "command": "restart_ha"
        })
    
    # 6. Disk
    if "disk_total" in metrics and "disk_free" in metrics and metrics["disk_total"] > 0:
        disk_pct = 100 * (1 - metrics["disk_free"] / metrics["disk_total"])
        if disk_pct > 90:
            decisions.append({
                "priority": "high",
                "action": "disk_cleanup",
                "reason": f"Disk {disk_pct:.1f}% full",
                "command": "cleanup_disk"
            })
    
    # 7. Runaway git processes (high CPU from many git-remote-https)
    try:
        git_remote_count = int(subprocess.run(
            ["pgrep", "-c", "-f", "git-remote-https"],
            capture_output=True, text=True
        ).stdout.strip() or "0")
        if git_remote_count > 5:
            decisions.append({
                "priority": "critical",
                "action": "kill_runaway_git",
                "reason": f"{git_remote_count} git-remote-https processes eating CPU",
                "command": "kill_runaway_git"
            })
    except Exception:
        pass
    
    return decisions

def execute_decision(decision, client):
    """Выполняем решение"""
    cmd = decision.get("command", "")
    
    if cmd == "renice_non_critical":
        try:
            # renice openclaw, argos background jobs
            subprocess.run(["renice","+19","-p","$(pgrep -f openclaw | head -5)"], shell=True, capture_output=True)
            # Also kill any runaway git-remote processes
            git_count = subprocess.run(["pgrep","-c","-f","git-remote-https"], capture_output=True, text=True)
            if int(git_count.stdout.strip() or "0") > 5:
                subprocess.run(["pkill","-f","git-remote-https"], capture_output=True)
                return f"Applied nice +19 to non-critical + killed {git_count.stdout.strip()} runaway git processes"
            return "Applied nice +19 to non-critical processes"
        except Exception as e:
            return f"Failed: {e}"
    
    elif cmd == "drop_caches":
        try:
            with open("/proc/sys/vm/drop_caches", "w") as f:
                f.write("1")
            return "Dropped caches"
        except Exception as e:
            return f"Failed (need root): {e}"
    
    elif cmd == "alert_thermal":
        client.publish("argos/system/alert", json.dumps({
            "level": "critical",
            "msg": f"🔥 THERMAL ALERT: {decision['reason']}",
            "time": now()
        }))
        return "Published thermal alert to bus"
    
    elif cmd.startswith("restart_"):
        target = decision.get("target", cmd.replace("restart_", ""))
        if target == "pc":
            # Try to wake PC via SSH
            try:
                subprocess.run(["ssh","-o","ConnectTimeout=5","AvA@192.168.1.53","echo 'PC alive'"], capture_output=True, timeout=10)
                return "PC SSH reachable, no restart needed"
            except:
                client.publish("argos/command", json.dumps({
                    "from": "brain",
                    "target": "argos_pc",
                    "command": "wake",
                    "time": now()
                }))
                return "Sent wake command to PC"
        elif target == "ha" or target == "homeassistant":
            try:
                subprocess.run(["docker","start","homeassistant"], capture_output=True, timeout=20)
                return "Restarted HA docker"
            except Exception as e:
                return f"Failed: {e}"
        elif target == "orangepi":
            client.publish("argos/command", json.dumps({
                "from": "brain",
                "target": "orangepi",
                "command": "restart_argos_iot",
                "time": now()
            }))
            return "Sent restart command to Orange Pi"
        else:
            client.publish("argos/command", json.dumps({
                "from": "brain",
                "target": target,
                "command": "wake",
                "time": now()
            }))
            return f"Sent wake command to {target}"
    
    elif cmd == "check_zigbee_devices":
        # Publish permit join request
        client.publish("argos/command", json.dumps({
            "from": "brain",
            "target": "argos_pc",
            "command": "zigbee_permit_join",
            "args": {"time": 254},
            "time": now()
        }))
        return "Sent zigbee permit_join to PC"
    
    elif cmd == "alert_esp_down":
        target = decision.get("target", "unknown")
        # Send alert to ESP32 display (if it's not the one that's down)
        try:
            import urllib.request
            msg = f"ALERT: {target} DOWN"
            url = f"http://192.168.1.211/?msg={msg.replace(' ','+')}&color=FF0000"
            urllib.request.urlopen(url, timeout=5)
        except:
            pass
        client.publish("argos/system/alert", json.dumps({
            "level": "high",
            "msg": f"⚠️ ESP device {target} is unreachable",
            "time": now()
        }))
        return f"Published ESP alert for {target}"
    
    elif cmd == "cleanup_disk":
        try:
            # Clean journal, tmp, pacman cache, pip cache
            results = []
            r1 = subprocess.run(["journalctl","--vacuum-time=3d"], capture_output=True, text=True)
            results.append(f"journal: {r1.stdout[:100]}")
            r2 = subprocess.run(["sudo","-n","pacman","-Sc","--noconfirm"], capture_output=True, text=True)
            results.append(f"pacman: {r2.stdout[:100]}")
            # Clean pip cache
            r3 = subprocess.run(["rm","-rf",
                os.path.expanduser("~/.cache/pip"),
                "/tmp/pip-unpack-*",
                "/tmp/pip-install-*"
            ], capture_output=True, text=True)
            results.append(f"pip_cache: cleaned")
            # Clean ARGOS tmp
            argos_tmp = Path("/home/ava/Projects/argoss/tmp")
            if argos_tmp.exists():
                for f in argos_tmp.iterdir():
                    if f.is_file():
                        f.unlink(missing_ok=True)
                results.append(f"argos_tmp: cleaned")
            return "Cleaned: " + "; ".join(results)
        except Exception as e:
            return f"Partial cleanup: {e}"
    
    elif cmd == "kill_runaway_git":
        try:
            result = subprocess.run(
                ["pkill", "-f", "git-remote-https"],
                capture_output=True, text=True
            )
            # Also kill parent repo sync if exists
            repo_pids = subprocess.run(
                ["pgrep", "-f", "repo sync"],
                capture_output=True, text=True
            )
            if repo_pids.stdout.strip():
                for pid in repo_pids.stdout.strip().split('\n'):
                    if pid.strip():
                        subprocess.run(["kill", pid.strip()], capture_output=True)
            return f"Killed runaway git processes (exit={result.returncode})"
        except Exception as e:
            return f"Failed: {e}"
    
    return f"Unknown command: {cmd}"

def memory_maintenance():
    """Очистка памяти ARGOS: удаляет дубликаты dreamer, обрезает до лимита."""
    import re
    db_path = "/home/ava/Projects/argoss/data/memory.db"
    if not os.path.exists(db_path):
        return "no memory.db"
    
    MAX_DREAMER = 200
    MAX_EDGES = 5000
    cleaned = 0
    
    try:
        import sqlite3
        db = sqlite3.connect(db_path)
        cur = db.cursor()
        
        # 1. Удалить dreamer факты с тривиальными паттернами
        trivial_patterns = [
            r"пользователь ценит результат",
            r"пользователь ценит (?:конкретный|готовый|оптимизацию|скорость|актуальную|лаконичность|структурированност)",
            r"я мог (?:ответить|быть|бы) лучше",
            r"я узнал,? что пользователь",
            r"ничего нового я не узнал",
        ]
        for pattern in trivial_patterns:
            cur.execute("SELECT id, value FROM facts WHERE category='dreamer'")
            to_del = [row[0] for row in cur.fetchall() if re.search(pattern, row[1], re.IGNORECASE)]
            if to_del:
                cur.execute(f"DELETE FROM facts WHERE id IN ({','.join(['?']*len(to_del))})", to_del)
                cleaned += cur.rowcount
        
        # 2. Обрезать dreamer до MAX_DREAMER (удаляем самые старые)
        count = cur.execute("SELECT COUNT(*) FROM facts WHERE category='dreamer'").fetchone()[0]
        if count > MAX_DREAMER:
            to_del = count - MAX_DREAMER
            cur.execute(
                "DELETE FROM facts WHERE category='dreamer' AND id IN "
                "(SELECT id FROM facts WHERE category='dreamer' ORDER BY id ASC LIMIT ?)",
                (to_del,),
            )
            cleaned += cur.rowcount
        
        # 3. Удалить orphaned dreamer edges (has_insight_X ссылки на удалённые факты)
        cur.execute("DELETE FROM knowledge_edges WHERE source='dreamer' AND predicate LIKE 'has_insight_%'")
        cleaned += cur.rowcount
        
        # 4. Обрезать edges до MAX_EDGES
        edge_count = cur.execute("SELECT COUNT(*) FROM knowledge_edges").fetchone()[0]
        if edge_count > MAX_EDGES:
            to_del = edge_count - MAX_EDGES
            cur.execute(
                "DELETE FROM knowledge_edges WHERE id IN "
                "(SELECT id FROM knowledge_edges ORDER BY id ASC LIMIT ?)",
                (to_del,),
            )
            cleaned += cur.rowcount
        
        # 5. Удалить dialogue edges старше 3 дней (временные данные)
        cur.execute(
            "DELETE FROM knowledge_edges WHERE source='dialogue' AND ts < datetime('now', '-3 days')"
        )
        cleaned += cur.rowcount
        
        db.commit()
        db.close()
        return f"cleaned {cleaned} rows"
    except Exception as e:
        return f"error: {e}"


def think_cycle(client):
    """Один цикл мышления"""
    print(f"\n🧠 [{now()}] Brain cycle starting...")
    
    # 0. Memory maintenance (каждый 6-й цикл = каждый час)
    if not hasattr(think_cycle, '_cycle_count'):
        think_cycle._cycle_count = 0
    think_cycle._cycle_count += 1
    
    if think_cycle._cycle_count % 6 == 0:
        mem_result = memory_maintenance()
        print(f"  → Memory maintenance: {mem_result}")
    
    # 1. Собираем данные
    metrics = get_system_metrics()
    nodes = get_node_status()
    ha = get_ha_status()
    
    # 2. Принимаем решения
    decisions = take_decisions(metrics, nodes, ha)
    
    # 3. Выполняем
    results = []
    for d in decisions:
        print(f"  → Decision: {d['action']} | {d['reason']} | priority={d['priority']}")
        result = execute_decision(d, client)
        results.append({"decision": d, "result": result})
        print(f"    Result: {result}")
        
        # Publish to bus
        client.publish("argos/log", json.dumps({
            "event": "brain_decision",
            "action": d["action"],
            "reason": d["reason"],
            "priority": d["priority"],
            "result": result,
            "time": now()
        }, ensure_ascii=False))
    
    # 4. Публикуем heartbeat
    client.publish("argos/heartbeat", json.dumps({
        "agent": "brain",
        "status": "online",
        "decisions": len(decisions),
        "time": now()
    }))
    
    # 5. Пишем в Obsidian
    report = f"""## 🧠 Brain Cycle {now()}

### System Metrics
| Metric | Value |
|--------|-------|
| CPU | {metrics.get('cpu_total', '?')} |
| RAM | {metrics.get('mem_avail', '?')} / {metrics.get('mem_total', '?')} |
| Temp | {metrics.get('temp', '?')}°C |
| Disk free | {metrics.get('disk_free', '?')} |

### Nodes
| Node | Status |
|------|--------|
| Local | {'✅' if nodes.get('local',{}).get('ok') else '❌'} |
| PC | {'✅' if nodes.get('pc',{}).get('ok') else '❌'} |
| Railway | {'✅' if nodes.get('railway',{}).get('ok') else '❌'} |
| Orange Pi | {'✅' if nodes.get('orangepi',{}).get('ok') else '❌'} |

### ESP Devices
| Device | Status |
|--------|--------|
| ESP32 Display | {'✅' if nodes.get('esp32_display',{}).get('ok') else '❌'} |
| ESP8266 Bridge | {'✅' if nodes.get('esp8266_bridge',{}).get('ok') else '❌'} |

### HA
| Entities | {ha.get('entities', '?')} | Active | {ha.get('active', '?')} |

### Decisions ({len(decisions)})
"""
    for r in results:
        d = r["decision"]
        report += f"- **{d['priority'].upper()}**: `{d['action']}` — {d['reason']} → {r['result']}\n"
    if not decisions:
        report += "- Все системы стабильны ✅\n"
    
    log_to_obsidian(report)
    
    print(f"🧠 [{now()}] Cycle complete. Decisions: {len(decisions)} | Report: Daily/{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-brain.md")

def main():
    client = mqtt.Client()
    
    def on_connect(c, userdata, flags, rc, properties=None):
        print(f"🧠 Brain connected to MQTT")
        client.subscribe("argos/command")
        client.subscribe("argos/agents/brain/inbox")
    
    def on_message(c, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
        except:
            return
        if msg.topic == "argos/agents/brain/inbox":
            # Direct command to brain
            print(f"🧠 Direct message to brain: {payload}")
            # Could trigger immediate think cycle
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()
    
    print(f"🧠 Autonomous Brain started. Cycle interval: 10 minutes")
    
    # Immediate first cycle
    think_cycle(client)
    
    # Loop
    while True:
        time.sleep(600)  # 10 minutes
        think_cycle(client)

if __name__ == "__main__":
    main()
