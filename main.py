import os, time, httpx, json, hashlib
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ARGOS API", version="2.1.4")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

START = time.time()
ARGOS_PC  = os.getenv("ARGOS_PC_URL", "http://192.168.1.66:8000")
OLLAMA    = os.getenv("OLLAMA_URL", "https://myollama123.ngrok.io")
P2P_TOKEN = os.getenv("ARGOS_P2P_TOKEN", "")
NODE_ID   = "railway-argos"

PEERS = {
    "pc":       "http://192.168.1.66:8000",
    "laptop":   "http://192.168.1.53:8000",
    "orangepi": "http://192.168.2.168:7778",
}

@app.get("/")
async def root():
    return {"name":"ARGOS","version":"2.1.4","node":NODE_ID,"status":"online","uptime":int(time.time()-START)}

@app.get("/health")
async def health():
    return {"ok":True,"node":NODE_ID,"uptime":int(time.time()-START)}

@app.get("/mcp")
async def mcp():
    return {"name":"argos","ok":True,"node":NODE_ID,"transport":"http"}

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
async def ask(body: dict):
    try:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(f"{OLLAMA}/api/generate",
                json={"model":body.get("model","llama3.1:8b"),"prompt":body.get("prompt",""),"stream":False})
            return {"response":r.json().get("response",""),"ok":True}
    except Exception as e:
        return {"error":str(e)}

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
            r = await c.post(f"{ARGOS_PC}/mcp",json=body)
            return r.json()
    except Exception as e:
        return {"error":str(e)}
