import os, time, httpx, json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="ARGOS API", version="2.1.5")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

START = time.time()
ARGOS_PC  = os.getenv("ARGOS_PC_URL", "http://192.168.1.72:8000")
MCP_URL   = os.getenv("ARGOS_MCP_URL", "https://api-laptop.argosssss.win")
BRAIN_URL = os.getenv("ARGOS_BRAIN_API_URL", "")
P2P_TOKEN = os.getenv("ARGOS_P2P_TOKEN", "")
NODE_ID   = "railway-argos"

PEERS = {
    "pc":       os.getenv("ARGOS_PC_URL", "http://192.168.1.72:8000"),
    "laptop":   "http://192.168.1.53:8000",
    "mcp":      MCP_URL,
}

@app.get("/")
async def root():
    return {"name":"ARGOS","version":"2.1.5","node":NODE_ID,"status":"online","uptime":int(time.time()-START)}

@app.get("/health")
async def health():
    return {"ok":True,"node":NODE_ID,"uptime":int(time.time()-START)}

@app.get("/mcp")
async def mcp():
    return {"name":"argos","ok":True,"node":NODE_ID,"transport":"http","mcp_url":MCP_URL}

@app.post("/p2p/announce")
async def p2p_announce(request: Request):
    token = request.headers.get("X-P2P-Token","")
    if P2P_TOKEN and token != P2P_TOKEN:
        return {"error":"invalid token"}
    body = await request.json()
    return {"ok":True,"node":NODE_ID,"received":body.get("node","")}

@app.get("/p2p/nodes")
async def p2p_nodes():
    nodes = {}
    async with httpx.AsyncClient(timeout=4) as c:
        for name, url in PEERS.items():
            try:
                r = await c.get(f"{url}/health")
                nodes[name] = {"ok":True,"url":url,"data":r.json()}
            except:
                nodes[name] = {"ok":False,"url":url}
    nodes[NODE_ID] = {"ok":True,"url":"self","uptime":int(time.time()-START)}
    return nodes

@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    async with httpx.AsyncClient(timeout=60) as c:
        try:
            r = await c.post(f"{MCP_URL}/ask", json=body)
            return JSONResponse(r.json(), status_code=r.status_code)
        except Exception as e:
            return JSONResponse({"error":str(e),"mcp_url":MCP_URL}, status_code=502)

@app.post("/proxy/ask")
async def proxy_ask(request: Request):
    return await ask(request)

@app.get("/brain/nodes")
async def brain_nodes():
    if BRAIN_URL:
        async with httpx.AsyncClient(timeout=10) as c:
            try:
                r = await c.get(f"{BRAIN_URL}/brain/nodes")
                return r.json()
            except Exception as e:
                return {"nodes":[],"error":str(e)}
    # Fallback: query MCP
    async with httpx.AsyncClient(timeout=8) as c:
        try:
            r = await c.get(f"{MCP_URL}/brain/nodes")
            return r.json()
        except:
            return {"nodes":[],"note":"ARGOS_BRAIN_API_URL not set"}

@app.get("/brain/status")
async def brain_status():
    result = {"railway":"online","mcp_url":MCP_URL,"node":NODE_ID,"uptime":int(time.time()-START)}
    async with httpx.AsyncClient(timeout=5) as c:
        try:
            r = await c.get(f"{MCP_URL}/health")
            result["mcp"] = r.json()
        except Exception as e:
            result["mcp"] = {"error":str(e)}
    return result

@app.get("/status")
async def status():
    res = {"railway":"online","node":NODE_ID,"uptime":int(time.time()-START),"peers":{}}
    async with httpx.AsyncClient(timeout=4) as c:
        for name, url in PEERS.items():
            try:
                r = await c.get(f"{url}/health")
                res["peers"][name] = {"ok":True}
            except:
                res["peers"][name] = {"ok":False}
    return res

@app.post("/mcp")
async def mcp_proxy(body: dict):
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(f"{ARGOS_PC}/mcp", json=body)
            return r.json()
    except Exception as e:
        return {"error":str(e)}
