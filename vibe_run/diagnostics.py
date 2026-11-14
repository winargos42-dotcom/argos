"""ARGOS-VIBE diagnostics: component health + honest resource report.

Probes only what actually exists in this sandbox:
  - loopback services: local LLM (:11434), MCP API (:8000), gateway (:8080),
    Brain API (:5001, only if restored from X230)
  - cgroup v2 CPU/memory limits and current usage
  - disk usage of the runtime dir
  - SQLite memory backends (brain.db, cognitive_memory.db)
  - accelerators: P100 / SPR2801S / Coral Edge TPU are reported UNAVAILABLE,
    never simulated; GPU presence is detected, not assumed.

Output: JSON to stdout and (if ARGOS_DIAG_PATH is set) to that file.
"""
from __future__ import annotations

import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

RUNTIME = os.getenv("ARGOS_RUNTIME", "/workspace/argos-runtime")
TIMEOUT = float(os.getenv("ARGOS_DIAG_TIMEOUT", "5"))


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def probe(name: str, url: str) -> dict:
    try:
        r = httpx.get(url, timeout=TIMEOUT)
        body = {}
        try:
            body = r.json()
        except Exception:
            body = {"raw": r.text[:200]}
        return {"component": name, "url": url, "status": r.status_code, "ok": r.status_code == 200,
                "body": body}
    except Exception as exc:
        return {"component": name, "url": url, "status": None, "ok": False, "error": str(exc)}


def cgroup_info() -> dict:
    info: dict = {"cgroup_version": "v2" if Path("/sys/fs/cgroup/cpu.max").exists() else "unknown"}
    base = Path("/sys/fs/cgroup")
    try:
        quota, period = (base / "cpu.max").read_text().split()
        info["cpu_quota_cores"] = None if quota == "max" else round(int(quota) / int(period), 2)
        info["memory_max_bytes"] = int((base / "memory.max").read_text())
        info["memory_current_bytes"] = int((base / "memory.current").read_text())
    except OSError as exc:
        info["error"] = str(exc)
    try:
        count = len(Path("/proc/self/status").read_text().splitlines())
        info["proc_status_lines"] = count
    except OSError:
        pass
    return info


def gpu_and_accelerators() -> dict:
    gpu = {"cuda": False, "rocm": False, "vram_bytes": None}
    if Path("/dev/nvidia0").exists() or Path("/usr/bin/nvidia-smi").exists():
        gpu["cuda"] = True
    if Path("/dev/kfd").exists():
        gpu["rocm"] = True
    return {
        "gpu": gpu,
        "accelerators": {
            "nvidia_p100": "unavailable",
            "google_spr2801s": "unavailable",
            "coral_edge_tpu": "unavailable" if not Path("/dev/apex_0").exists() else "present",
        },
    }


def disk_usage(path: str) -> dict:
    st = os.statvfs(path)
    return {"path": path,
            "total_gb": round(st.f_blocks * st.f_frsize / 2**30, 2),
            "free_gb": round(st.f_bavail * st.f_frsize / 2**30, 2)}


def sqlite_counts() -> dict:
    out: dict = {}
    for label, db in (("brain", f"{RUNTIME}/data/brain.db"),
                      ("cognitive_memory", f"{RUNTIME}/data/cognitive_memory.db")):
        p = Path(db)
        if not p.exists():
            out[label] = {"exists": False}
            continue
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            tables = [r[0] for r in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")]
            counts = {}
            for t in tables:
                try:
                    counts[t] = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                except sqlite3.Error:
                    counts[t] = None
            con.close()
            out[label] = {"exists": True, "size_bytes": p.stat().st_size, "tables": counts}
        except sqlite3.Error as exc:
            out[label] = {"exists": True, "error": str(exc)}
    return out


def processes() -> list[dict]:
    procs = []
    for pid_file, label in (("mcp_api.pid", "mcp_api"), ("gateway.pid", "gateway"),
                            ("local_llm.pid", "local_llm")):
        p = Path(f"{RUNTIME}/logs/{pid_file}")
        if not p.exists():
            procs.append({"component": label, "pid": None, "alive": False})
            continue
        pid = int(p.read_text().strip() or 0)
        alive = Path(f"/proc/{pid}").exists()
        procs.append({"component": label, "pid": pid, "alive": alive})
    return procs


def main() -> int:
    report = {
        "generated_at": now(),
        "node": "argos-vibe-sandbox",
        "services": [
            probe("local_llm", "http://127.0.0.1:11434/health"),
            probe("mcp_api", "http://127.0.0.1:8000/health"),
            probe("gateway", "http://127.0.0.1:8080/health"),
            probe("brain_api", "http://127.0.0.1:5001/health"),
        ],
        "processes": processes(),
        "cgroup": cgroup_info(),
        "disk": disk_usage(RUNTIME),
        "hardware": gpu_and_accelerators(),
        "memory_backends": sqlite_counts(),
    }
    print(report_text := _format(report))
    out = os.getenv("ARGOS_DIAG_PATH")
    if out:
        import json
        Path(out).write_text(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if all(s["ok"] for s in report["services"][:3]) else 1


def _format(report: dict) -> str:
    lines = [f"ARGOS-VIBE diagnostics @ {report['generated_at']}"]
    for s in report["services"]:
        state = "OK" if s["ok"] else ("DOWN" if s["status"] is None else f"HTTP {s['status']}")
        lines.append(f"  {s['component']:<12} {state:<9} {s['url']}")
    for p in report["processes"]:
        lines.append(f"  proc {p['component']:<10} pid={p['pid']} alive={p['alive']}")
    cg = report["cgroup"]
    if "cpu_quota_cores" in cg:
        mem_cur = cg.get("memory_current_bytes", 0) / 2**30
        mem_max = cg.get("memory_max_bytes", 0) / 2**30
        lines.append(f"  cgroup: cpu={cg.get('cpu_quota_cores')} cores, "
                     f"mem={mem_cur:.2f}/{mem_max:.2f} GiB")
    lines.append(f"  disk: {report['disk']['free_gb']} GiB free of {report['disk']['total_gb']} GiB")
    acc = report["hardware"]["accelerators"]
    lines.append(f"  accelerators: P100={acc['nvidia_p100']} SPR2801S={acc['google_spr2801s']} "
                 f"EdgeTPU={acc['coral_edge_tpu']} (honest report, no simulation)")
    for name, info in report["memory_backends"].items():
        lines.append(f"  sqlite {name}: exists={info.get('exists')} tables={info.get('tables')}")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
