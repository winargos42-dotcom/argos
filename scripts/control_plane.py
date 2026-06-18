#!/usr/bin/env python3
"""ARGOS Control Plane — BFF + Dashboard
Агрегирует Brain API, контейнеры, Entity Council.
"""
import json, time, asyncio
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import httpx

app = FastAPI(title="ARGOS Control Plane")

CORE_IP = "192.168.1.53"
BRAIN_URL = f"http://{CORE_IP}:5010"
PROM_URL = "http://127.0.0.1:9090"
MCP_URL = "http://127.0.0.1:8000"

DASHBOARD_DIR = Path(__file__).parent / "dashboard"

@app.get("/api/health")
async def health():
    return {"status": "ok", "time": datetime.now().isoformat()}

@app.get("/api/dashboard")
async def dashboard():
    """Агрегированный статус ARGOS."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            brain = await client.get(f"{BRAIN_URL}/health")
            brain_ok = brain.status_code == 200
    except:
        brain_ok = False

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            prom = await client.get(f"{PROM_URL}/api/v1/query?query=up")
            prom_data = prom.json().get("data", {}).get("result", [])
    except:
        prom_data = []

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            mcp = await client.get(f"{MCP_URL}/mcp")
            mcp_ok = mcp.status_code == 200
    except:
        mcp_ok = False

    try:
        with open("/tmp/entity_dialogue_v5.log", "r", encoding="utf-8") as f:
            lines = f.readlines()[-20:]
        dialogues = [l.strip() for l in lines if l.strip()]
        last_thought = dialogues[-1] if dialogues else "Нет данных"
    except:
        last_thought = "Нет данных"

    return {
        "timestamp": datetime.now().isoformat(),
        "brain": {"status": "online" if brain_ok else "offline", "url": BRAIN_URL},
        "mcp": {"status": "online" if mcp_ok else "offline", "url": MCP_URL},
        "prometheus": {"targets": len(prom_data), "url": PROM_URL},
        "entities": {"council": "active", "last_thought": last_thought[:200]},
        "containers": {"prometheus": True, "grafana": True, "redis": True}
    }

@app.get("/api/brain/nodes")
async def brain_nodes():
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(f"{BRAIN_URL}/brain/nodes")
            return JSONResponse(content=r.json())
    except Exception as e:
        return {"error": str(e), "status": "offline"}

@app.get("/api/topology")
async def topology():
    """Mesh топология для дашборда."""
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(f"{BRAIN_URL}/brain/nodes")
            nodes_data = r.json().get("nodes", [])
    except:
        nodes_data = []

    nodes = []
    links = []
    
    groups = {
        "argos-pc": "LAN", "argos-laptop": "LAN", "orangepi": "IoT",
        "argos-phone-redmi": "Mobile",
        "gcp-35-194-61-206": "Cloud", "gcp-34-53-142-129": "Cloud", "gcp-104-155-192-165": "Cloud",
    }
    
    for n in nodes_data:
        nid = n.get("node_id", "unknown")
        nodes.append({
            "id": nid,
            "name": nid,
            "group": groups.get(nid, "Other"),
            "status": n.get("status", "unknown"),
            "authority": 200 if n.get("status") == "online" else 50
        })
    
    # Links — звезда от orion
    for n in nodes:
        if n["id"] != "argos-pc":
            links.append({"source": "argos-pc", "target": n["id"], "value": 3})

    return {"nodes": nodes, "links": links}

# ── Dashboard HTML ──────────────────────

DASHBOARD_HTML = '''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🌐 ARGOS Control Plane</title>
<style>
:root{--bg:#0b0d14;--card:#151922;--cyan:#00ffcc;--blue:#60a5fa;--green:#34d399;--red:#f87171;--yellow:#fbbf24;--text:#e2e8f0;}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--text);font-family:system-ui,sans-serif;min-height:100vh;padding:20px}
h1{color:var(--cyan);margin-bottom:20px;font-size:1.6rem}
.grid{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin-bottom:20px}
.card{background:var(--card);border-radius:12px;padding:20px;border:1px solid #1e293b}
.card h2{color:var(--blue);font-size:1rem;margin-bottom:12px}
.status{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.badge{padding:4px 10px;border-radius:6px;font-size:0.8rem;font-weight:600}
.badge-online{background:var(--green);color:#064e3b}
.badge-offline{background:var(--red);color:#450a0a}
.badge-warn{background:var(--yellow);color:#451a03}
.metric{font-size:24px;font-weight:700;color:var(--cyan)}
#log{background:#0a0a0a;border-radius:8px;padding:12px;font-family:monospace;font-size:0.78rem;height:200px;overflow-y:auto;border:1px solid #1e293b;color:#94a3b8}
#log .line{margin-bottom:4px}
.topo{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin-top:12px}
.node-box{background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid #334155;font-size:0.85rem}
.node-box.online{border-color:var(--green)}
.node-box.offline{border-color:var(--red)}
.node-name{font-weight:600;margin-bottom:4px}
.node-group{color:#94a3b8;font-size:0.75rem}
footer{margin-top:30px;color:#64748b;font-size:0.8rem;text-align:center}
a{color:var(--blue);text-decoration:none}
a:hover{text-decoration:underline}
</style>
</head>
<body>
<h1>🟡 ARGOS Control Plane</h1>

<div class="grid">
  <div class="card">
    <h2>🧠 Core API</h2>
    <div id="core-status"><span class="badge badge-warn">loading...</span></div>
    <div style="margin-top:8px"><a href="http://192.168.1.53:5001/health" target="_blank">Brain</a> |
      <a href="/api/dashboard" target="_blank">Dashboard JSON</a> |
      <a href="http://127.0.0.1:3000" target="_blank">Grafana</a></div>
  </div>

  <div class="card">
    <h2>🔗 Nodes</h2>
    <div class="metric" id="nodes-count">—</div>
    <div style="color:#94a3b8;font-size:0.85rem">online / total</div>
  </div>

  <div class="card">
    <h2>💭 Entity Council</h2>
    <div id="entity-status" style="font-size:0.85rem;color:#94a3b8">—</div>
    <div style="margin-top:8px;font-size:0.8rem"><a href="/api/topology">Topology JSON</a></div>
  </div>

  <div class="card">
    <h2>🐳 Containers</h2>
    <div class="status" id="docker-status"><span class="badge badge-offline">—</span></div>
  </div>
</div>

<div class="card">
  <h2>🌐 Mesh Topology</h2>
  <div class="topo" id="topology">Loading...</div>
</div>

<div class="card" style="margin-top:20px">
  <h2>📝 Entity Dialogue Log</h2>
  <div id="log">Loading...</div>
</div>

<footer>ARGOS Universal OS · Phase 1 · Control Plane v0.1 · <span id="timestamp">—</span></footer>

<script>
async function load() {
  // Dashboard
  try {
    const r = await fetch('/api/dashboard');
    const d = await r.json();
    document.getElementById('core-status').innerHTML = `
      <span class="badge ${d.brain.status==='online'?'badge-online':'badge-offline'}">Brain: ${d.brain.status}</span>
      <span class="badge ${d.mcp.status==='online'?'badge-online':'badge-offline'}">MCP: ${d.mcp.status}</span>
    `;
    document.getElementById('docker-status').innerHTML = `
      <span class="badge badge-online">Prometheus</span>
      <span class="badge badge-online">Grafana</span>
      <span class="badge badge-online">Redis</span>
    `;
    document.getElementById('timestamp').textContent = new Date(d.timestamp).toLocaleString('ru');
  } catch(e) { console.error(e); }

  // Nodes
  try {
    const r = await fetch('/api/brain/nodes');
    const d = await r.json();
    const nodes = d.nodes || [];
    const online = nodes.filter(n=>n.status==='online').length;
    document.getElementById('nodes-count').textContent = `${online}/${nodes.length}`;
    
    // Topology
    const topo = document.getElementById('topology');
    topo.innerHTML = '';
    nodes.forEach(n=>{
      const div = document.createElement('div');
      div.className = 'node-box ' + n.status;
      div.innerHTML = `<div class="node-name">${n.node_id}</div><div class="node-group">${n.group||'Other'}</div>`;
      topo.appendChild(div);
    });
  } catch(e) { console.error(e); }

  // Entity last thought
  try {
    const r = await fetch('/api/dashboard');
    const d = await r.json();
    document.getElementById('entity-status').textContent = d.entities.last_thought;
  } catch(e) {}
}

// Auto-refresh
load();
setInterval(load, 5000);
</script>
</body></html>
'''

@app.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(content=DASHBOARD_HTML)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3456)
