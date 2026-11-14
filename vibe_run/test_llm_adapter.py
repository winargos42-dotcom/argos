"""EXPLICIT TEST ADAPTER — not part of ARGOS.

Stands in for the missing external AI backends (Ollama / llama-server) during
sandbox deployment.  Implements the two call shapes the real ARGOS code makes:

  * Ollama:            POST /api/generate        {"model","prompt","stream"}
  * OpenAI-compatible: POST /v1/chat/completions {"model","messages",...}

Responses are deterministic and clearly tagged "[TEST-ADAPTER]" so no result
can be mistaken for a real model run.  Listens on loopback only.
"""
from __future__ import annotations

import os
import time

from fastapi import FastAPI, Request

app = FastAPI(title="ARGOS TEST LLM ADAPTER (deterministic, not a model)")
START = time.time()


def _reply(prompt: str) -> str:
    snippet = " ".join(prompt.split())[:160]
    return f"[TEST-ADAPTER] LLM-бэкенды (Ollama/llama-server) в этой среде отсутствуют; детерминированный ответ на: {snippet}"


@app.get("/health")
async def health():
    return {"ok": True, "adapter": "test-llm", "note": "explicit test adapter, no real model"}


@app.post("/api/generate")
async def ollama_generate(body: dict):
    return {
        "model": body.get("model", "test-adapter"),
        "response": _reply(body.get("prompt", "")),
        "done": True,
    }


@app.post("/v1/chat/completions")
async def chat_completions(body: dict):
    messages = body.get("messages", [])
    content = messages[-1].get("content", "") if messages else ""
    return {
        "choices": [
            {"message": {"role": "assistant", "content": _reply(content)}}
        ],
        "model": body.get("model", "test-adapter"),
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("ADAPTER_HOST", "127.0.0.1")
    port = int(os.getenv("ADAPTER_PORT", "11434"))
    uvicorn.run(app, host=host, port=port, log_level="info")
