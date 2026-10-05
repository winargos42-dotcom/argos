import os
import time

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="ARGOS API", version="2.1.6")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

START = time.time()
NODE_ID = os.getenv("ARGOS_NODE_ID", "argos-standalone")
ARGOS_PC = os.getenv("ARGOS_PC_URL", "").rstrip("/")
MCP_URL = os.getenv("ARGOS_MCP_URL", "").rstrip("/")
BRAIN_URL = os.getenv("ARGOS_BRAIN_API_URL", "").rstrip("/")
P2P_TOKEN = os.getenv("ARGOS_P2P_TOKEN", "")

# Standalone is the safe public default. No private/LAN peer is contacted unless
# its URL is explicitly supplied through the environment.
PEERS = {
    name: url
    for name, url in {
        "pc": ARGOS_PC,
        "mcp": MCP_URL,
        "brain": BRAIN_URL,
    }.items()
    if url
}


@app.get("/")
async def root():
    return {
        "name": "ARGOS",
        "version": "2.1.6",
        "node": NODE_ID,
        "status": "online",
        "mode": "standalone" if not PEERS else "connected",
        "uptime": int(time.time() - START),
    }


@app.get("/health")
async def health():
    return {
        "ok": True,
        "ready": True,
        "node": NODE_ID,
        "mode": "standalone" if not PEERS else "connected",
        "configured_peers": list(PEERS),
        "uptime": int(time.time() - START),
    }


@app.get("/mcp")
async def mcp():
    return {
        "name": "argos",
        "ok": True,
        "node": NODE_ID,
        "transport": "http",
        "configured": bool(MCP_URL),
    }


@app.post("/p2p/announce")
async def p2p_announce(request: Request):
    if not P2P_TOKEN:
        return JSONResponse(
            {"ok": False, "error": "P2P disabled; set ARGOS_P2P_TOKEN explicitly"},
            status_code=503,
        )
    token = request.headers.get("X-P2P-Token", "")
    if token != P2P_TOKEN:
        return JSONResponse({"ok": False, "error": "invalid token"}, status_code=401)
    body = await request.json()
    return {"ok": True, "node": NODE_ID, "received": body.get("node", "")}


@app.get("/p2p/nodes")
async def p2p_nodes():
    nodes = {}
    async with httpx.AsyncClient(timeout=4) as client:
        for name, url in PEERS.items():
            try:
                response = await client.get(f"{url}/health")
                response.raise_for_status()
                nodes[name] = {"ok": True, "url": url, "data": response.json()}
            except Exception as exc:
                nodes[name] = {"ok": False, "url": url, "error": type(exc).__name__}
    nodes[NODE_ID] = {"ok": True, "url": "self", "uptime": int(time.time() - START)}
    return nodes


@app.post("/ask")
async def ask(request: Request):
    if not MCP_URL:
        return JSONResponse(
            {"error": "MCP backend is not configured; set ARGOS_MCP_URL"},
            status_code=503,
        )
    body = await request.json()
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(f"{MCP_URL}/ask", json=body)
            return JSONResponse(response.json(), status_code=response.status_code)
        except Exception as exc:
            return JSONResponse({"error": type(exc).__name__}, status_code=502)


@app.post("/proxy/ask")
async def proxy_ask(request: Request):
    return await ask(request)


@app.get("/brain/nodes")
async def brain_nodes():
    if not BRAIN_URL:
        return {"nodes": [], "configured": False}
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(f"{BRAIN_URL}/brain/nodes")
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            return {"nodes": [], "error": type(exc).__name__}


@app.get("/brain/status")
async def brain_status():
    return {
        "node": NODE_ID,
        "online": True,
        "brain_configured": bool(BRAIN_URL),
        "mcp_configured": bool(MCP_URL),
        "uptime": int(time.time() - START),
    }


@app.get("/status")
async def status():
    return {
        "online": True,
        "node": NODE_ID,
        "mode": "standalone" if not PEERS else "connected",
        "configured_peers": list(PEERS),
        "uptime": int(time.time() - START),
    }


@app.post("/mcp")
async def mcp_proxy(body: dict):
    if not ARGOS_PC:
        return JSONResponse(
            {"error": "ARGOS PC backend is not configured; set ARGOS_PC_URL"},
            status_code=503,
        )
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{ARGOS_PC}/mcp", json=body)
            return JSONResponse(response.json(), status_code=response.status_code)
    except Exception as exc:
        return JSONResponse({"error": type(exc).__name__}, status_code=502)
