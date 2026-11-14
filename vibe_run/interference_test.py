"""Load-interference benchmark for ARGOS-VIBE (own processes, synthetic signals).

Research task, stage 6. Measures how CPU and memory pressure from OUR OWN
load-generator processes affects the latency of a concurrent ARGOS agent
session on this single physical server:

  conditions (interleaved, repeated):
    control        no load
    cpu1 / cpu4    1 / 4 busy-loop spinner processes (own Python)
    mem_hi         one child process holding ~1.5 GiB (own Python)

  probe (original code, per round):
    remember/recall via ArgosMasterCore, think via NeuralNexus -> local Qwen

Interpretation guard: this measures ordinary scheduler/cgroup resource
contention between co-located processes. It is NOT a hardware covert/timing
side channel and must not be presented as one. All signals are synthetic,
all processes belong to this sandbox.

Output: JSON report with per-condition latency distributions and deltas
vs control.
"""
from __future__ import annotations

import json
import os
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone

REPO = os.getenv("ARGOS_REPO", "/workspace/github__winargos42-dotcom__argos")
RUNTIME = os.getenv("ARGOS_RUNTIME", "/workspace/argos-runtime")
VENV_PY = f"{RUNTIME}/venv/bin/python"
ROUNDS = int(os.getenv("ARGOS_INT_ROUNDS", "3"))
REPORT = os.getenv("ARGOS_INT_REPORT", f"{RUNTIME}/interference_report.json")
sys.path.insert(0, REPO)
os.chdir(RUNTIME)
os.environ.setdefault("ARGOS_COGNITIVE_SQLITE", f"{RUNTIME}/data/cognitive_memory.db")
os.environ.setdefault("ARGOS_PG_ENABLED", "0")

MEM_TARGET_BYTES = int(os.getenv("ARGOS_INT_MEM_BYTES", str(int(1.5 * 2**30))))


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


CPU_SPINNER = (
    "import time,sys; end=time.time()+float(sys.argv[1])\n"
    "x=0\n"
    "while time.time()<end: x=(x*31+7)&0xFFFFFFFF\n"
    "print(x&1)\n"
)
MEM_HOLDER = (
    "import time,sys\n"
    "target=int(sys.argv[1]); hold=float(sys.argv[2]); chunks=[]; got=0\n"
    "while got<target:\n"
    "    c=bytearray(min(64*2**20, target-got)); c[:len(c)]=b'\\xa5'*len(c); chunks.append(c); got+=len(c)\n"
    "time.sleep(hold)\n"
)


class Load:
    def __init__(self) -> None:
        self.procs: list[subprocess.Popen] = []

    def cpu(self, n: int, dur: float) -> None:
        for _ in range(n):
            self.procs.append(subprocess.Popen(
                [sys.executable, "-c", CPU_SPINNER, str(dur)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

    def mem(self, dur: float) -> None:
        self.procs.append(subprocess.Popen(
            [sys.executable, "-c", MEM_HOLDER, str(MEM_TARGET_BYTES), str(dur)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

    def stop(self) -> None:
        for p in self.procs:
            if p.poll() is None:
                p.kill()
        for p in self.procs:
            p.wait()
        self.procs.clear()


def measure_round(master, tag: str) -> dict:
    out: dict = {"condition": tag}
    t0 = time.perf_counter()
    master.execute(f"remember: int_{tag}_{time.time_ns()} | v", user_id="admin")
    out["memory_write_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    t0 = time.perf_counter()
    master.execute("recall: vibe_deployment", user_id="admin")
    out["memory_read_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    t0 = time.perf_counter()
    master.execute("think: Ответь одним коротким предложением: что такое очередь?",
                   user_id="admin")
    out["llm_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    return out


def cgroup_mem() -> int:
    try:
        return int(open("/sys/fs/cgroup/memory.current").read())
    except OSError:
        return -1


def main() -> int:
    from src.swarm.argos_master_core import ArgosMasterCore
    master = ArgosMasterCore(db_path=f"{RUNTIME}/data/brain.db")
    master.ac.approve("admin")

    plan = (["control", "cpu1", "cpu4", "mem_hi"] * ROUNDS)
    load = Load()
    rows: list[dict] = []
    try:
        for i, cond in enumerate(plan):
            dur = 25.0
            if cond == "cpu1":
                load.cpu(1, dur)
            elif cond == "cpu4":
                load.cpu(4, dur)
            elif cond == "mem_hi":
                load.mem(dur)
            time.sleep(1.5)  # let load spin up
            row = measure_round(master, cond)
            row["round"] = i
            row["cgroup_mem_current_mib"] = round(cgroup_mem() / 2**20, 1)
            rows.append(row)
            print(f"[interference] #{i} {cond}: mem_write={row['memory_write_ms']}ms "
                  f"mem_read={row['memory_read_ms']}ms llm={row['llm_ms']}ms "
                  f"cgmem={row['cgroup_mem_current_mib']}MiB")
            time.sleep(3.0)  # cool-down so loads do not bleed across conditions
            load.stop()
            time.sleep(1.0)
    finally:
        load.stop()

    agg: dict = {}
    for cond in ("control", "cpu1", "cpu4", "mem_hi"):
        sel = [r for r in rows if r["condition"] == cond]
        agg[cond] = {}
        for key in ("memory_write_ms", "memory_read_ms", "llm_ms"):
            vals = [r[key] for r in sel]
            agg[cond][key] = {"n": len(vals), "median": statistics.median(vals),
                              "min": min(vals), "max": max(vals)}
    base = agg["control"]["llm_ms"]["median"] or 1
    for cond in ("cpu1", "cpu4", "mem_hi"):
        agg[cond]["llm_slowdown_vs_control"] = round(
            agg[cond]["llm_ms"]["median"] / base, 2)

    report = {
        "generated_at": now(),
        "rounds_per_condition": ROUNDS,
        "interpretation": "scheduler/cgroup resource contention between own "
                          "co-located processes; NOT a hardware side channel",
        "mem_target_mib": round(MEM_TARGET_BYTES / 2**20),
        "aggregate": agg,
        "rows": rows,
    }
    with open(REPORT, "w") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print(json.dumps(agg, indent=2))
    print(f"report: {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
