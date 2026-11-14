"""Local CPU inference server for ARGOS-VIBE — real model, thin wrapper.

Serves the downloaded Qwen2.5-0.5B-Instruct GGUF through llama.cpp
(llama-cpp-python) with the two API shapes ARGOS code already calls:

  * Ollama shape:            POST /api/generate        (NeuralNexus, mcp_api /ask)
  * OpenAI-compatible shape: POST /v1/chat/completions (ARGOS_MODEL_ROUTER path)

This is infrastructure glue only: the model, tokenizer and inference are real
llama.cpp execution on CPU.  Loopback only.  Responses are genuine model
output and are NOT tagged as test data.
"""
from __future__ import annotations

import os
import time

from fastapi import FastAPI, Request

from llama_cpp import Llama

MODEL_PATH = os.environ["ARGOS_MODEL_PATH"]
N_THREADS = int(os.getenv("ARGOS_LLM_THREADS", "4"))
N_CTX = int(os.getenv("ARGOS_LLM_CTX", "2048"))

print(f"loading {MODEL_PATH} (threads={N_THREADS}, ctx={N_CTX}) ...", flush=True)
_t0 = time.perf_counter()
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=N_CTX,
    n_threads=N_THREADS,
    n_batch=256,
    verbose=False,
)
print(f"model loaded in {time.perf_counter()-_t0:.1f}s", flush=True)

app = FastAPI(title="ARGOS-VIBE local LLM (llama.cpp, Qwen2.5-0.5B-Instruct Q4_K_M)")
START = time.time()
_system = "Ты — ARGOS HiveMind. Мастер-инженер. Отвечай технически и лаконично. Стиль: Absolute Candor."


@app.get("/health")
async def health():
    return {
        "ok": True,
        "backend": "llama.cpp",
        "model": "qwen2.5-0.5b-instruct-q4_k_m",
        "threads": N_THREADS,
        "ctx": N_CTX,
        "uptime_s": int(time.time() - START),
    }


@app.post("/api/generate")
async def ollama_generate(body: dict):
    prompt = body.get("prompt", "")
    system = body.get("system") or _system
    t0 = time.perf_counter()
    out = llm.create_chat_completion(
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        max_tokens=int(body.get("num_predict") or 256),
        temperature=0.7,
    )
    dt = time.perf_counter() - t0
    text = out["choices"][0]["message"]["content"].strip()
    n_gen = out["usage"]["completion_tokens"]
    return {
        "model": "qwen2.5-0.5b-instruct-q4_k_m",
        "response": text,
        "done": True,
        "eval_count": n_gen,
        "eval_duration_ns": int(dt * 1e9),
        "tokens_per_sec": round(n_gen / dt, 2) if dt else None,
    }


@app.post("/v1/chat/completions")
async def chat_completions(body: dict):
    messages = body.get("messages", [])
    if messages and messages[0].get("role") != "system":
        messages = [{"role": "system", "content": _system}] + messages
    t0 = time.perf_counter()
    out = llm.create_chat_completion(
        messages=messages,
        max_tokens=int(body.get("max_tokens") or 256),
        temperature=body.get("temperature", 0.7),
    )
    dt = time.perf_counter() - t0
    return {
        "choices": [{"message": out["choices"][0]["message"]}],
        "model": "qwen2.5-0.5b-instruct-q4_k_m",
        "usage": out["usage"],
        "tokens_per_sec": round(out["usage"]["completion_tokens"] / dt, 2) if dt else None,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("ADAPTER_PORT", "11434")), log_level="info")
