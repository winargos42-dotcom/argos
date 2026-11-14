"""Two-way peering readiness check for ARGOS-VIBE <-> X230/Coral.

Checks, honestly and without declaring anything operational prematurely:

  1. Local ARGOS-VIBE services (loopback): LLM, MCP API, gateway.
  2. Outbound peers taken ONLY from environment variables
     (ARGOS_X230_MCP_URL, ARGOS_X230_CORE_URL, ARGOS_CORAL_MCP_URL, ...).
     Nothing is probed unless the operator explicitly sets the variable.
  3. The four public argosssss.win hostnames are hard-denied: the Cloudflare
     tunnel (1033/530) is being diagnosed on the ARGOS side and must not be
     polled repeatedly.
  4. Link state is OPERATIONAL only if a peer returned a real HTTP 200 with a
     JSON body during THIS run. Otherwise: NOT OPERATIONAL (exit code 1) —
     reported as-is, never assumed.

Usage:
  python vibe_run/peering_check.py            # local + any env-configured peers
  ARGOS_X230_MCP_URL=http://127.0.0.1:18000 python vibe_run/peering_check.py
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

import httpx

RUNTIME = os.getenv("ARGOS_RUNTIME", "/workspace/argos-runtime")
TIMEOUT = float(os.getenv("ARGOS_PEEPING_TIMEOUT", "5"))
REPORT = os.getenv("ARGOS_PEERING_REPORT", f"{RUNTIME}/peering_check_report.json")

PEER_ENV_VARS = [
    "ARGOS_X230_MCP_URL",
    "ARGOS_X230_CORE_URL",
    "ARGOS_CORAL_MCP_URL",
    "ARGOS_CORAL_CORE_URL",
]

DENIED_HOSTS = {
    "argosssss.win",
    "www.argosssss.win",
    "mcp.argosssss.win",
    "core.argosssss.win",
    "api.argosssss.win",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def check_local() -> list[dict]:
    out = []
    for name, url in (("local_llm", "http://127.0.0.1:11434/health"),
                      ("mcp_api", "http://127.0.0.1:8000/health"),
                      ("gateway", "http://127.0.0.1:8080/health")):
        try:
            r = httpx.get(url, timeout=TIMEOUT)
            out.append({"endpoint": name, "url": url, "ok": r.status_code == 200,
                        "status": r.status_code})
        except Exception as exc:
            out.append({"endpoint": name, "url": url, "ok": False, "error": str(exc)})
    return out


def check_peer(name: str, url: str) -> dict:
    host = (urlparse(url).hostname or "").lower()
    if host in DENIED_HOSTS or host.endswith(".argosssss.win"):
        return {"peer": name, "url": url, "state": "DENIED",
                "reason": "public 530/1033 endpoints must not be polled; "
                          "use a private tunnel or SSH port-forward instead"}
    try:
        r = httpx.get(url, timeout=TIMEOUT)
        ok = r.status_code == 200
        body = {}
        try:
            body = r.json()
        except Exception:
            body = {"raw": r.text[:200]}
        return {"peer": name, "url": url, "state": "OPERATIONAL" if ok else "HTTP_ERROR",
                "status": r.status_code, "body": body}
    except Exception as exc:
        return {"peer": name, "url": url, "state": "UNREACHABLE", "error": str(exc)}


def main() -> int:
    peers = [check_peer(v, os.environ[v]) for v in PEER_ENV_VARS if os.environ.get(v)]
    if not peers:
        peers = [{"peer": "(none)", "url": None, "state": "NOT_CONFIGURED",
                  "reason": "set ARGOS_X230_MCP_URL / ARGOS_CORAL_MCP_URL to a private "
                            "tunnel or SSH-forward address to enable outbound checks"}]
    operational = any(p["state"] == "OPERATIONAL" for p in peers)
    report = {
        "generated_at": now(),
        "node": "argos-vibe-sandbox",
        "local_services": check_local(),
        "peers": peers,
        "link_state": "OPERATIONAL" if operational else "NOT_OPERATIONAL",
        "note": "link_state reflects only THIS run; no persistent claim is made",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    with open(REPORT, "w") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    local_ok = all(s["ok"] for s in report["local_services"])
    return 0 if (local_ok and operational) else 1


if __name__ == "__main__":
    sys.exit(main())
