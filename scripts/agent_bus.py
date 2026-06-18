#!/usr/bin/env python3
"""
ARGOS Agent Message Bus — центральный message router на ноутбуке.
Использует Mosquitto MQTT localhost:1883 как pub/sub бэкенд.

Топики:
  argos/agents/<name>/inbox   — личные сообщения агенту
  argos/agents/<name>/outbox  — исходящие от агента
  argos/broadcast             — всем агентам
  argos/log                   — логи событий (retain)
  argos/command               — команды от пользователя
  argos/heartbeat             — heartbeat (TTL 60s)
  argos/system/alert          — критические алерты

Функции:
  • Роутинг сообщений между агентами
  • Heartbeat monitoring (кто жив)
  • Dead agent detection
  • Логирование в Obsidian
  • Retain messages для offline агентов
"""
import json, time, os, sys, threading
from datetime import datetime, timezone
from pathlib import Path

import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
MQTT_PORT = 1883
AGENTS = ["claude", "argos_pc", "argos_railway", "orangepi", "opencode", "user", "deepseek", "kimi", "gemini", "cloudflare", "ollama_vision", "mcp_server"]
HEARTBEAT_TIMEOUT = 120  # секунды до объявления агента мёртвым

OBSIDIAN_LOG = Path("/home/ava/Documents/MyObsidianVault/Daily")

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def log_to_obsidian(content):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = OBSIDIAN_LOG / f"{today}-messages.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n---\n\n{content}\n")

class AgentBus:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.heartbeats = {}
        self.lock = threading.Lock()
        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        print(f"[{now()}] AgentBus connected to MQTT")
        self.connected = True
        # Подписываемся на всё
        self.client.subscribe("argos/agents/+/outbox")
        self.client.subscribe("argos/broadcast")
        self.client.subscribe("argos/command")
        self.client.subscribe("argos/heartbeat")
        self.client.subscribe("argos/system/alert")
        # Публикуем свой heartbeat
        self.publish("argos/heartbeat", {"agent": "bus", "status": "online", "time": now()})
        # Retain log
        self.publish("argos/log", {"event": "bus_online", "time": now()}, retain=True)

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
        except:
            payload = {"raw": msg.payload.decode()[:200]}
        
        topic = msg.topic
        
        # Heartbeat
        if topic == "argos/heartbeat":
            agent = payload.get("agent", "unknown")
            with self.lock:
                self.heartbeats[agent] = time.time()
            return
        
        # System alert
        if topic == "argos/system/alert":
            self.handle_alert(payload)
            return
        
        # Broadcast → всем агентам
        if topic == "argos/broadcast":
            self.handle_broadcast(payload)
            return
        
        # Command → route to target
        if topic == "argos/command":
            self.handle_command(payload)
            return
        
        # Agent outbox → route to target inbox
        if topic.startswith("argos/agents/") and topic.endswith("/outbox"):
            self.route_agent_message(topic, payload)
            return

    def route_agent_message(self, topic, payload):
        # topic = argos/agents/<sender>/outbox
        parts = topic.split("/")
        sender = parts[2] if len(parts) > 2 else "unknown"
        target = payload.get("to", "broadcast")
        msg_id = payload.get("id", f"{sender}-{int(time.time())}")
        
        if target == "broadcast":
            # Шлём всем кроме отправителя
            for agent in AGENTS:
                if agent != sender:
                    self.publish(f"argos/agents/{agent}/inbox", {
                        "from": sender,
                        "msg": payload.get("msg"),
                        "id": msg_id,
                        "time": now(),
                        "type": payload.get("type", "message")
                    })
        else:
            # Личное сообщение
            self.publish(f"argos/agents/{target}/inbox", {
                "from": sender,
                "msg": payload.get("msg"),
                "id": msg_id,
                "time": now(),
                "type": payload.get("type", "message")
            })
        
        # Лог
        log_entry = f"**{now()}** | `{sender}` → `{target}` | {payload.get('type','msg')} | {str(payload.get('msg',''))[:80]}"
        log_to_obsidian(log_entry)
        print(f"[{now()}] Routed: {sender} → {target}")

    def handle_broadcast(self, payload):
        sender = payload.get("from", "unknown")
        for agent in AGENTS:
            if agent != sender:
                self.publish(f"argos/agents/{agent}/inbox", {
                    "from": sender,
                    "msg": payload.get("msg"),
                    "time": now(),
                    "type": "broadcast"
                })
        log_to_obsidian(f"**{now()}** | 📢 Broadcast from `{sender}`: {str(payload.get('msg',''))[:100]}")
        print(f"[{now()}] Broadcast from {sender}")

    def handle_command(self, payload):
        cmd = payload.get("command", "")
        target = payload.get("target", "all")
        sender = payload.get("from", "user")
        
        if target == "all":
            # Broadcast command
            for agent in AGENTS:
                self.publish(f"argos/agents/{agent}/inbox", {
                    "from": sender,
                    "msg": {"command": cmd, "args": payload.get("args",{})},
                    "time": now(),
                    "type": "command"
                })
        else:
            self.publish(f"argos/agents/{target}/inbox", {
                "from": sender,
                "msg": {"command": cmd, "args": payload.get("args",{})},
                "time": now(),
                "type": "command"
            })
        
        log_to_obsidian(f"**{now()}** | ⚡ Command `{cmd}` → `{target}` from `{sender}`")
        print(f"[{now()}] Command: {cmd} → {target}")

    def handle_alert(self, payload):
        level = payload.get("level", "warning")
        msg = payload.get("msg", "")
        print(f"🚨 ALERT [{level}]: {msg}")
        log_to_obsidian(f"**{now()}** | 🚨 **ALERT {level.upper()}**: {msg}")
        # Retain alert
        self.publish("argos/log", {"event": "alert", "level": level, "msg": msg, "time": now()}, retain=True)

    def publish(self, topic, payload, retain=False):
        self.client.publish(topic, json.dumps(payload, ensure_ascii=False), retain=retain)

    def heartbeat_monitor(self):
        """Проверяет heartbeat каждые 30 сек"""
        while True:
            time.sleep(30)
            now_t = time.time()
            dead = []
            with self.lock:
                for agent, last in self.heartbeats.items():
                    if now_t - last > HEARTBEAT_TIMEOUT:
                        dead.append(agent)
            
            for agent in dead:
                alert = f"🚨 Agent `{agent}` silent for {HEARTBEAT_TIMEOUT}s — presumed dead"
                print(f"[{now()}] {alert}")
                log_to_obsidian(f"**{now()}** | {alert}")
                self.publish("argos/system/alert", {"level": "critical", "msg": alert, "agent": agent, "time": now()})
                # Отправляем команду на восстановление, если есть handler
                self.publish("argos/agents/claude/inbox", {
                    "from": "bus",
                    "msg": {"command": "revive_agent", "agent": agent},
                    "type": "system",
                    "time": now()
                })

    def run(self):
        print(f"[{now()}] Starting AgentBus...")
        try:
            self.client.connect(MQTT_HOST, MQTT_PORT, 60)
        except Exception as e:
            print(f"[{now()}] MQTT connection failed: {e}")
            sys.exit(1)
        
        # Heartbeat monitor в фоне
        threading.Thread(target=self.heartbeat_monitor, daemon=True).start()
        
        # Собственный heartbeat
        def self_heartbeat():
            while True:
                time.sleep(60)
                self.publish("argos/heartbeat", {"agent": "bus", "status": "online", "time": now()})
        threading.Thread(target=self_heartbeat, daemon=True).start()
        
        # Block
        self.client.loop_forever()

if __name__ == "__main__":
    bus = AgentBus()
    bus.run()
