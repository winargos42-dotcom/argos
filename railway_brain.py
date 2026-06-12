"""
ARGOS Brain Railway — lightweight proxy/API для Railway деплоя.
Проксирует /ask на MCP tunnel (api-laptop.argosssss.win).
"""
import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="ARGOS Brain Railway", version="1.0")

MCP_URL = os.getenv("ARGOS_MCP_URL", "https://api-laptop.argosssss.win")
BRAIN_URL = os.getenv("ARGOS_BRAIN_API_URL", "")


@app.get("/health")
def health():
    return {"status": "ok", "service": "argos-brain-railway", "mcp": MCP_URL}


@app.get("/")
def root():
    return {"service": "ARGOS Brain API", "endpoints": ["/health", "/ask", "/brain/nodes", "/proxy/ask"]}


@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.post(f"{MCP_URL}/ask", json=body)
            return JSONResponse(r.json(), status_code=r.status_code)
        except Exception as e:
            return JSONResponse({"error": str(e), "mcp_url": MCP_URL}, status_code=502)


@app.post("/proxy/ask")
async def proxy_ask(request: Request):
    return await ask(request)


@app.get("/brain/nodes")
async def brain_nodes():
    if BRAIN_URL:
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                r = await client.get(f"{BRAIN_URL}/brain/nodes")
                return r.json()
            except Exception as e:
                return {"nodes": [], "error": str(e)}
    return {"nodes": [], "note": "ARGOS_BRAIN_API_URL not set"}


@app.get("/brain/status")
async def brain_status():
    result = {"railway": "online", "mcp_url": MCP_URL}
    if BRAIN_URL:
        async with httpx.AsyncClient(timeout=5) as client:
            try:
                r = await client.get(f"{BRAIN_URL}/health")
                result["brain_pc"] = r.json()
            except Exception as e:
                result["brain_pc"] = {"error": str(e)}
    return result
