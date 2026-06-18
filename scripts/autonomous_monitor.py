#!/usr/bin/env python3
"""
ARGOS Autonomous Monitor — автономный агент мониторинга
Проверяет всю сеть каждые 5 минут, записывает в Obsidian.
Если нода упала — записывает alert и пытается восстановить.
"""
import json, os, sys, subprocess, time, socket
from datetime import datetime, timezone
from pathlib import Path

HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjMWIwZDgxNzdkNDY0NGRjOWM4YmI4OGZiM2VkOGRjZSIsImlhdCI6MTc3NzkyMDY5MiwiZXhwIjoyMDkzMjgwNjkyfQ.nV0ps3wDPz4NAiqwKCyyTLcwK-oxUdvg2ohIG4p6Ozs"
OBSIDIAN_DAILY = Path("/home/ava/Documents/MyObsidianVault/Daily")

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def check_url(url, timeout=5, method="GET", data=None, headers=None):
    import urllib.request, urllib.error
    try:
        req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"ok": True, "status": resp.status, "body": resp.read().decode()[:500]}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def check_mcp(url, timeout=5):
    r = check_url(url, timeout)
    if r["ok"]:
        try:
            d = json.loads(r["body"])
            return {"ok": True, "name": d.get("name","?"), "uptime": d.get("uptime_seconds",0)}
        except:
            return {"ok": True, "raw": r["body"][:60]}
    return r

def check_ha():
    r = check_url("http://localhost:8123/api/states", headers={"Authorization": f"Bearer {HA_TOKEN}"}, timeout=5)
    if r["ok"]:
        try:
            states = json.loads(r["body"])
            active = [s for s in states if s["state"] not in ("unknown","unavailable","")]
            return {"ok": True, "entities": len(states), "active": len(active)}
        except:
            return {"ok": True, "entities": "?"}
    return r

def check_mosquitto():
    import subprocess
    try:
        out = subprocess.run(["mosquitto_sub","-h","localhost","-p","1883","-t","$SYS/broker/clients/connected","-W","2","-C","1"],
                           capture_output=True, text=True, timeout=4)
        return {"ok": True, "clients": out.stdout.strip() or "0"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def check_orangepi_ssh():
    try:
        out = subprocess.run(["ssh","-o","ConnectTimeout=5","-o","StrictHostKeyChecking=no",
                             "orangepione","uptime"], capture_output=True, text=True, timeout=8)
        return {"ok": out.returncode == 0, "uptime": out.stdout.strip()[:60] if out.returncode==0 else out.stderr.strip()[:60]}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def check_ai_providers():
    """Проверяем DeepSeek, OpenAI через ARGOS /ask endpoint (только MCP)"""
    # Проверяем Ollama локально
    r = check_url("http://localhost:11434/api/tags", timeout=5)
    ollama_ok = r["ok"]
    # Проверяем ngrok Ollama (ПК)
    r2 = check_url("https://myollama123.ngrok.io/api/tags", timeout=8)
    ngrok_ok = r2["ok"]
    return {"ollama_local": ollama_ok, "ollama_ngrok": ngrok_ok}

def self_heal(results):
    """Автономное восстановление проблемных компонентов"""
    alerts = []
    # 1. Если OPi IoT мёртв — проверим SSH и перезапустим сервис
    if not results["orangepi_iot"]["ok"]:
        alerts.append("🚨 Orange Pi IoT :7777 не отвечает — перезапуск argos-iot")
        try:
            subprocess.run(["ssh","-o","ConnectTimeout=5","-o","StrictHostKeyChecking=no",
                            "orangepione","systemctl restart argos-iot"], timeout=10)
        except: pass
    # 2. Если HA мёртв — перезапускаем docker
    if not results["ha"]["ok"]:
        alerts.append("🚨 Home Assistant не отвечает — перезапуск docker")
        try:
            subprocess.run(["sudo","systemctl","restart","docker"], timeout=30)
            subprocess.run(["docker","start","homeassistant"], timeout=20)
        except: pass
    # 3. Если mosquitto мёртв
    if not results["mosquitto"]["ok"]:
        alerts.append("🚨 Mosquitto не отвечает — перезапуск")
        try:
            subprocess.run(["sudo","systemctl","restart","mosquitto"], timeout=15)
        except: pass
    return alerts

def write_obsidian_report(results, alerts):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = OBSIDIAN_DAILY / f"{today}-autonomous.md"
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    
    header = f"# Autonomous Report {now()}\n\n"
    body = f"""## 🌐 P2P Mesh
| Нода | Статус | Детали |
|------|--------|--------|
| 💻 Локально | {'✅' if results['local']['ok'] else '❌'} | {results['local'].get('uptime','?')}s CPU:{results['local'].get('cpu','?')}% |
| 🖥️ ПК | {'✅' if results['pc']['ok'] else '❌'} | {results['pc'].get('uptime','?')}s |
| 🚂 Railway | {'✅' if results['railway']['ok'] else '❌'} | {results['railway'].get('uptime','?')}s |
| 🍊 OPi IoT | {'✅' if results['orangepi_iot']['ok'] else '❌'} | {results['orangepi_iot'].get('cpu_temp','?')}°C |
| 🍊 OPi P2P | {'✅' if results['orangepi_p2p']['ok'] else '❌'} | Peers:{results['orangepi_p2p'].get('peers','?')} |

## 🏠 Home Assistant
| Параметр | Значение |
|----------|----------|
| Entities | {results['ha'].get('entities', '?')} |
| Active | {results['ha'].get('active', '?')} |

## 📡 MQTT
| Параметр | Значение |
|----------|----------|
| Mosquitto | {'✅' if results['mosquitto']['ok'] else '❌'} |
| Clients | {results['mosquitto'].get('clients', '?')} |

## 🧠 AI Providers
| Провайдер | Статус |
|-----------|--------|
| Ollama Local | {'✅' if results['ai']['ollama_local'] else '❌'} |
| Ollama Ngrok | {'✅' if results['ai']['ollama_ngrok'] else '❌'} |

## 🔧 Self-Healing
"""
    if alerts:
        for a in alerts:
            body += f"- {a}\n"
    else:
        body += "- Все системы стабильны ✅\n"
    
    # Append mode — добавляем к существующему файлу или создаём
    if path.exists():
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n---\n\n{header}{body}")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{header}{body}")
    return path

def main():
    results = {}
    
    # 1. Локальный ARGOS
    r = check_mcp("http://localhost:8000/health")
    results["local"] = r
    if r["ok"]:
        try:
            d = json.loads(check_url("http://localhost:8000/health")["body"])
            r["cpu"] = d.get("cpu_pct","?")
            r["ram"] = d.get("ram_pct","?")
        except: pass
    
    # 2. ПК ARGOS
    results["pc"] = check_mcp("http://192.168.1.53:8000/health")
    
    # 3. Railway
    results["railway"] = check_mcp("https://argos-v2-production.up.railway.app/health")
    
    # 4. OPi IoT
    r_iot = check_url("http://192.168.2.168:7777/", timeout=5)
    results["orangepi_iot"] = r_iot
    if r_iot["ok"]:
        try:
            d = json.loads(r_iot["body"])
            r_iot["cpu_temp"] = d.get("cpu_temp","?")
        except: pass
    
    # 5. OPi P2P
    r_p2p = check_url("http://192.168.2.168:7778/health", timeout=5)
    results["orangepi_p2p"] = r_p2p
    if r_p2p["ok"]:
        try:
            d = json.loads(r_p2p["body"])
            r_p2p["peers"] = d.get("peers","?")
            r_p2p["cpu_temp"] = d.get("cpu_temp","?")
        except: pass
    
    # 6. HA
    results["ha"] = check_ha()
    
    # 7. MQTT
    results["mosquitto"] = check_mosquitto()
    
    # 8. AI
    results["ai"] = check_ai_providers()
    
    # Self-heal
    alerts = self_heal(results)
    
    # Write to Obsidian
    path = write_obsidian_report(results, alerts)
    
    # Summary to stdout (for systemd journal)
    print(f"[{now()}] Autonomous monitor: local={'✅' if results['local']['ok'] else '❌'} pc={'✅' if results['pc']['ok'] else '❌'} railway={'✅' if results['railway']['ok'] else '❌'} opi_iot={'✅' if results['orangepi_iot']['ok'] else '❌'} opi_p2p={'✅' if results['orangepi_p2p']['ok'] else '❌'} ha={'✅' if results['ha']['ok'] else '❌'} mqtt={'✅' if results['mosquitto']['ok'] else '❌'} alerts={len(alerts)} | report={path}")

if __name__ == "__main__":
    main()
