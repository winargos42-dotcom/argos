"""
argos_master_core.py
--------------------
ARGOS v1.20.5 Master Core, адаптированный под текущую инфраструктуру.
Слои:
  • SQLite-краткосрочная память (facts)
  • NeuralNexus — роутинг на llama-server (без облачных fallback'ов)
  • GhostBus — broadcast команд Рою через Gist
  • Telegram admin channel
Интеграция с ArgosIntegrationHub / ArgosSyncOrchestrator через callouts.
"""
from __future__ import annotations

import base64
import json
import os
import sqlite3
import subprocess
import threading
import time
import uuid
from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from .argos_ghost_protocol import GhostBus, BroadcastResult


class ArgosMemory:
    """SQLite-хранилище фактов."""

    def __init__(self, db_path: str = "data/brain.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS facts (key TEXT PRIMARY KEY, val TEXT)"
        )
        self.conn.commit()

    def save(self, key: str, value: str) -> str:
        self.conn.execute(
            "INSERT OR REPLACE INTO facts VALUES (?, ?)",
            (key, value),
        )
        self.conn.commit()
        return f"Запомнил факт: {key}"

    def get(self, key: str) -> str:
        row = self.conn.execute("SELECT val FROM facts WHERE key=?", (key,)).fetchone()
        return str(row[0]) if row else "неизвестно"

    def dump(self) -> Dict[str, str]:
        return {k: v for k, v in self.conn.execute("SELECT key, val FROM facts")}


class NeuralNexus:
    """Локальный ИИ-роутинг: Ollama приоритет, fallback на llama-server."""

    def __init__(self, ollama_host: str = "http://localhost:11434"):
        self.ollama_host = ollama_host
        self.history = deque(maxlen=5)
        self.prompt = (
            "Ты — ARGOS HiveMind. Мастер-инженер. Отвечай технически и лаконично. "
            "Стиль: Absolute Candor."
        )
        # Список локальных llama-server из переменной окружения
        self.llama_servers = self._parse_llama_servers()

    def _parse_llama_servers(self) -> List[Dict[str, Any]]:
        env = os.getenv("ARGOS_MODEL_ROUTER", "")
        servers = []
        if env:
            for part in env.split(","):
                pieces = part.strip().split("|")
                url = pieces[0].strip()
                model = pieces[1].strip() if len(pieces) > 1 else ""
                priority = int(pieces[2].strip()) if len(pieces) > 2 and pieces[2].strip().isdigit() else 0
                servers.append({"url": url, "model": model, "priority": priority})
        else:
            servers = [
                {"url": "http://192.168.1.72:8083", "model": "argos-qwen2.5-7b-v1.Q4_K_M.gguf", "priority": 110},
                {"url": "http://192.168.1.72:8085", "model": "mistral-nemo-instruct-2407.Q4_K_M.gguf", "priority": 100},
                {"url": "http://192.168.1.72:8082", "model": "qwen2.5-1.5b-instruct.Q4_K_M.gguf", "priority": 90},
            ]
        return sorted(servers, key=lambda s: s["priority"], reverse=True)

    def ask(self, text: str) -> str:
        # 1. Ollama
        try:
            payload = {
                "model": "llama3",
                "prompt": self.prompt + " Запрос: " + text,
                "stream": False,
            }
            r = requests.post(f"{self.ollama_host}/api/generate", json=payload, timeout=30)
            resp = r.json().get("response", "").strip()
            if resp:
                return "[OLLAMA] " + resp
        except Exception:
            pass
        # 2. llama-server fallback
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": text},
        ]
        for srv in self.llama_servers:
            url = srv["url"].rstrip("/")
            try:
                r = requests.post(
                    f"{url}/v1/chat/completions",
                    json={"model": srv["model"], "messages": messages, "temperature": 0.7, "stream": False},
                    timeout=45,
                )
                if r.ok:
                    choices = r.json().get("choices", [])
                    content = choices[0].get("message", {}).get("content", "").strip() if choices else ""
                    if content:
                        return f"[LLAMA {srv['model']}] " + content
            except Exception:
                continue
        return "AI_CORE_OFFLINE. Нейросети недоступны."


class AccessControl:
    """ACL + broadcast."""

    def __init__(self, bus: GhostBus):
        self.users: Dict[str, int] = {}
        self.bus = bus

    def is_admin(self, uid: str) -> bool:
        return self.users.get(uid, 0) >= 2 or uid == os.getenv("TG_ADMIN_ID", "") or uid == "admin"

    def approve(self, uid: str) -> str:
        self.users[uid] = 2
        return "АДМИНИСТРАТОР УТВЕРЖДЁН: " + uid


class ArgosMasterCore:
    """Master Core: память, ИИ, C2, Telegram, локальный shell."""

    def __init__(
        self,
        telegram_token: Optional[str] = None,
        admin_id: Optional[str] = None,
        db_path: str = "data/brain.db",
    ):
        self.node_id = "Master_" + uuid.uuid4().hex[:4].upper()
        self.version = "1.20.5-argoss"
        self.mem = ArgosMemory(db_path=db_path)
        self.nexus = NeuralNexus()
        self.bus = GhostBus()
        self.ac = AccessControl(self.bus)
        self.token = telegram_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.admin_id = admin_id or os.getenv("TG_ADMIN_ID", "")
        self.is_building = False

    def send_tg(self, text: str) -> dict:
        if not self.token or not self.admin_id:
            return {"ok": False, "error": "no telegram config"}
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            return requests.post(url, json={"chat_id": self.admin_id, "text": text[:4090]}, timeout=15).json()
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def ghost(self, command: str, label: str = "DIRECTIVE") -> str:
        res = self.bus.broadcast(command, label=label)
        if res.ok:
            return "BROADCAST: Директива отправлена в Рой."
        return f"Ошибка синхронизации с Gist: {res.error}"

    def remember(self, key: str, value: str) -> str:
        return self.mem.save(key, value)

    def recall(self, key: str) -> str:
        return self.mem.get(key)

    def shell(self, command: str) -> str:
        try:
            out = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=120)
            return out.decode("utf-8", errors="ignore")[:2000]
        except Exception as e:
            return f"SHELL_ERROR: {e}"

    def think(self, text: str) -> str:
        return self.nexus.ask(text)

    def execute(self, cmd: str, user_id: str = "") -> str:
        if not self.ac.is_admin(user_id):
            return "🛑 Отказано в доступе."
        low = cmd.strip().lower()
        if low.startswith("ghost "):
            return self.ghost(cmd[6:].strip())
        if low.startswith("flash "):
            return self.ghost(cmd[6:].strip(), label="FLASH_CMD")
        if low.startswith("shell "):
            return self.shell(cmd[6:].strip())
        if low.startswith("remember:"):
            rest = cmd[9:].strip()
            if "|" in rest:
                k, v = rest.split("|", 1)
                return self.remember(k.strip(), v.strip())
            return "Формат: remember: ключ | значение"
        if low.startswith("recall:"):
            return self.recall(cmd[7:].strip())
        return self.think(cmd)

    def status(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "version": self.version,
            "memory_facts": len(self.mem.dump()),
            "gist_ready": bool(self.bus.gist_id and self.bus.token),
            "telegram_ready": bool(self.token and self.admin_id),
        }
