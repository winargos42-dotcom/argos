"""
GCP Gemini Proxy — Cloud Run / Cloud Functions compatible.

Deploy to Cloud Run:
    gcloud run deploy argos-core \
        --source . \
        --region us-central1 \
        --project argos-489214 \
        --allow-unauthenticated

Or run locally:
    uvicorn main:app --host 0.0.0.0 --port 8080
"""

import os
import httpx
import logging
from urllib.parse import unquote
from fastapi import FastAPI, Request, Response, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ARGOS Gemini Proxy")

GOOGLE_API = "https://generativelanguage.googleapis.com"

def _extract_api_key(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    return os.getenv("GEMINI_API_KEY", "")

async def _proxy(request: Request, path: str, method: str | None = None) -> Response:
    key = _extract_api_key(request)
    if not key:
        raise HTTPException(status_code=403, detail="Missing API key")

    target = f"{GOOGLE_API}/{path}"
    qs = str(request.query_params)
    if qs:
        target = f"{target}?{qs}"

    logger.info(f"PROXY {method or request.method} -> {target}")

    body = await request.body()
    headers_out = {
        "Content-Type": request.headers.get("Content-Type", "application/json"),
        "x-goog-api-key": key,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=method or request.method,
            url=target,
            headers=headers_out,
            content=body,
            timeout=120.0,
        )

    logger.info(f"PROXY response: {resp.status_code}")
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers={"Content-Type": resp.headers.get("Content-Type", "application/json")},
    )


# ── Health ─────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


# ── One catch-all for everything under /proxy/gemini ─
# Cloud Run may URL-encode ':' as '%3A'. We unquote it here.
@app.api_route("/proxy/gemini/{raw_path:path}", methods=["GET", "POST", "DELETE", "PATCH"])
async def gemini_any(raw_path: str, request: Request):
    # Decode %3A back to : so model paths like gemini-2.5-flash:batchCreate work
    clean_path = unquote(raw_path)
    return await _proxy(request, clean_path)
