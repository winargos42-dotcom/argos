import os, time, httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ARGOS API", version="2.1.4")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

START = time.time()
ARGOS_PC = os.getenv("ARGOS_PC_URL", "http://192.168.1.66:8000")
OLLAMA   = os.getenv("OLLAMA_URL", "https://myollama123.ngrok.io")

@app.get("/")
async def root():
    return {"name":"ARGOS","version":"2.1.4","status":"online","uptime":int(time.time()-START)}

@app.get("/health")
async def health():
    return {"ok":True,"uptime":int(time.time()-START)}

@app.get("/mcp")
async def mcp():
    return {"name":"argos","ok":True,"transport":"http"}

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
    res = {"railway":"online","uptime":int(time.time()-START)}
    try:
        async with httpx.AsyncClient(timeout=4) as c:
            r = await c.get(f"{ARGOS_PC}/health")
            res["argos_pc"] = r.json()
    except:
        res["argos_pc"] = "offline"
    return res

@app.post("/mcp")
async def mcp_proxy(body: dict):
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(f"{ARGOS_PC}/mcp",json=body)
            return r.json()
    except Exception as e:
        return {"error":str(e)}
