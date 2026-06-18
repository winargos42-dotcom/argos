#!/usr/bin/env python3
"""ARGOS Orchestrator v1 — единый контроллер всех демонов
На основе Brain API /coordinate recommendations: кэширование, параллелизм, batch processing"""
import os, sys, time, json, subprocess, signal
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/Projects/argoss/src"))
from principles.audit_procedure import ProceduralAudit

PROJECT_ROOT = Path(os.path.expanduser("~/Projects/argoss"))
ORCH_LOG = PROJECT_ROOT / "logs/orchestrator.log"
PID_FILE = PROJECT_ROOT / ".orchestrator.pid"

SERVICES = {
    "autopilot_v3": {
        "cmd": " /home/ava/Projects/argoss/.venv/bin/python -u scripts/autopilot_v3.py >> logs/autopilot_v3_live.log 2>&1",
        "critical": True,
        "restart_delay": 10,
    },
    "voice_server": {
        "cmd": " /home/ava/Projects/argoss/.venv/bin/python -u scripts/voice_server.py >> logs/voice_server_live.log 2>&1",
        "critical": False,
        "restart_delay": 15,
    },
    "evolution_standalone": {
        "cmd": " /home/ava/Projects/argoss/.venv/bin/python -u scripts/standalone_evolution.py >> logs/evolution_standalone.log 2>&1",
        "critical": False,
        "restart_delay": 30,
    },
    "dreamer_standalone": {
        "cmd": " /home/ava/Projects/argoss/.venv/bin/python -u scripts/standalone_dreamer.py >> logs/dreamer_standalone.log 2>&1",
        "critical": False,
        "restart_delay": 30,
    },
    "recovered_daemons": {
        "cmd": "PYTHONPATH=/home/ava/Projects/argoss/src /home/ava/Projects/argoss/.venv/bin/python -u scripts/run_recovered_daemons.py >> logs/recovered_daemons_live.log 2>&1",
        "critical": False,
        "restart_delay": 20,
    },
    "prometheus_exporter": {
        "cmd": "ARGOS_PROMETHEUS_PORT=19090 /home/ava/Projects/argoss/.venv/bin/python -u scripts/prometheus_exporter.py >> logs/prometheus_exporter.log 2>&1",
        "critical": False,
        "restart_delay": 10,
    },
    "self_healer": {
        "cmd": " /home/ava/Projects/argoss/.venv/bin/python -u scripts/self_healer.py >> logs/self_healer.log 2>&1",
        "critical": False,
        "restart_delay": 10,
    },
}

class Orchestrator:
    def __init__(self):
        self.procs = {}
        self.restarts = {}
        self.audit = ProceduralAudit()
        self._running = True
        PID_FILE.write_text(str(os.getpid()))
        self.log("[ORCH] Orchestrator started")

    def log(self, msg):
        ts = datetime.now().isoformat()
        line = f"{ts} {msg}"
        print(line)
        with open(ORCH_LOG, "a") as f:
            f.write(line + "\n")

    def start_service(self, name):
        cfg = SERVICES[name]
        env = os.environ.copy()
        env["HOME"] = "/home/ava"
        env["USER"] = "ava"
        proc = subprocess.Popen(
            cfg["cmd"],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=PROJECT_ROOT,
            env=env,
        )
        self.procs[name] = proc
        self.restarts[name] = self.restarts.get(name, 0) + 1
        self.log(f"[ORCH] Started {name} PID={proc.pid} (restart #{self.restarts[name]})")
        self.audit.log_context(
            action_id=f"orch_start_{name}",
            axioms={"service_start": 1.0, "self_heal": 0.9},
            weights={"restart_count": self.restarts[name]},
            model="orchestrator"
        )

    def check_services(self):
        for name, proc in list(self.procs.items()):
            ret = proc.poll()
            if ret is not None:
                self.log(f"[ORCH] {name} exited with {ret}")
                cfg = SERVICES[name]
                if cfg["critical"] or self.restarts.get(name, 0) < 5:
                    time.sleep(cfg["restart_delay"])
                    self.start_service(name)
                else:
                    self.log(f"[ORCH] {name} exceeded restart limit, leaving dead")

    def start_all(self):
        for name in SERVICES:
            if name not in self.procs or self.procs[name].poll() is not None:
                self.start_service(name)

    def run(self):
        self.start_all()
        while self._running:
            time.sleep(10)
            self.check_services()
            # Periodic audit
            self.audit.log_context(
                action_id=f"orch_tick_{int(time.time())}",
                axioms={"heartbeat": 1.0},
                weights={"running": len(self.procs)},
                model="orchestrator"
            )

    def stop(self):
        self._running = False
        for name, proc in list(self.procs.items()):
            self.log(f"[ORCH] Stopping {name} PID={proc.pid}")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        PID_FILE.unlink(missing_ok=True)
        self.log("[ORCH] Shutdown complete")
    def status(self):
        s = []
        for name, proc in self.procs.items():
            alive = proc.poll() is None
            s.append(f"{name}: {'UP' if alive else 'DOWN'} (PID={proc.pid})")
        return "\n".join(s)

if __name__ == "__main__":
    orch = Orchestrator()
    def _sigterm(*_):
        orch.stop()
    signal.signal(signal.SIGTERM, _sigterm)
    signal.signal(signal.SIGINT, _sigterm)
    # Notify systemd if running as service
    try:
        import subprocess
        subprocess.run(["systemd-notify", "--ready"], check=False)
    except Exception:
        pass
    orch.run()
