"""
argos_ghost_drone.py
--------------------
Автономная дочерняя нода ARGOS Роя (Ghost Drone).
Поллит GhostBus Gist каждые 30 сек, выполняет shell/IoT команды,
отправляет лог обратно в Gist.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
import uuid
from typing import Optional

import requests

from .argos_ghost_protocol import GhostBus


class ArgosGhostDrone:
    """Автономный исполнитель Роя."""

    def __init__(self, drone_id: Optional[str] = None, poll_interval: int = 30):
        self.drone_id = drone_id or ("Drone_" + uuid.uuid4().hex[:4].upper())
        self.bus = GhostBus()
        self.poll_interval = poll_interval
        self.last_processed_ts = 0
        self.running = False

    def _bootstrap(self) -> None:
        print(f"Подготовка Ноды-Дочки: {self.drone_id}")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "requests", "esptool", "-q"],
                check=False,
                timeout=120,
            )
        except Exception:
            pass
        print("DRONE READY. Переход в режим скрытности.")

    def _report(self, message: str) -> None:
        print(f"[{self.drone_id}] {message}")
        self.bus.drone_log(self.drone_id, message)

    def _handle_iot(self, command: str) -> None:
        low = command.lower()
        if low.startswith("tasmota update "):
            ip = command.split()[-1]
            try:
                r = requests.get(f"http://{ip}/cm?cmnd=Upgrade%201", timeout=10)
                self._report(f"TASMOTA_OTA_START: {ip} | Status: {r.status_code}")
            except Exception as e:
                self._report(f"TASMOTA_ERR: {e}")
        elif low.startswith("pr2350 "):
            try:
                out = subprocess.check_output("esptool.py flash_id", shell=True, stderr=subprocess.STDOUT).decode("utf-8", errors="ignore")
                self._report("PR2350_USB_CHECK:\n" + out[:500])
            except Exception as e:
                self._report(f"PR2350_ERR: {e}")
        else:
            self._report(f"IoT Command Not Recognized: {command}")

    def _handle_shell(self, command: str) -> None:
        try:
            out = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=120).decode("utf-8", errors="ignore")
            self._report(f"SUCCESS: {command}\n{out[:1000]}")
        except Exception as e:
            self._report(f"FAIL: {command}\n{e}")

    def _tick(self) -> None:
        commands, self.last_processed_ts = self.bus.read_commands(self.last_processed_ts)
        for item in commands:
            command = item["command"]
            tag = item.get("raw_tag", "")
            print(f"Получен приказ ({tag}): {command}")
            if "FLASH_CMD" in tag:
                self._handle_iot(command)
            else:
                self._handle_shell(command)

    def run(self) -> None:
        self.running = True
        self._bootstrap()
        print(f"Ghost Link установлен. Поллинг каждые {self.poll_interval} секунд...")
        try:
            while self.running:
                self._tick()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        self.running = False
        self._report("Drone shutting down.")


def main() -> None:
    drone = ArgosGhostDrone()
    drone.run()


if __name__ == "__main__":
    main()
