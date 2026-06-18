#!/usr/bin/env python3
"""
Постоянная inference-нагрузка для V100 :8085 + embedding-нагрузка :8090.
Чередует chat-completions (тяжёлые) и batch-эмбеддинги, чтобы держать GPU занятым.
"""
import json
import os
import random
import sys
import time
import urllib.request
from pathlib import Path

EMBED_URL = "http://192.168.1.72:8090/v1/embeddings"
CHAT_URL = "http://192.168.1.72:8085/v1/chat/completions"
VAULT = "/home/ava/Documents/MyObsidianVault"
BATCH_EMBED = 128
PROMPTS = [
    "Summarize the theory of relativity in 5 sentences.",
    "Write a short Python function to compute Fibonacci numbers.",
    "Explain the difference between TCP and UDP.",
    "Describe how a transformer neural network works.",
    "What are the main security risks in IoT devices?",
    "Generate a concise project plan for a distributed AI system.",
    "Compare RISC and CISC architectures.",
    "Explain backpropagation in simple terms.",
    "List pros and cons of vector databases.",
    "How does a blockchain reach consensus?",
]

def get_md_files(limit=1200):
    files = []
    for p in Path(VAULT).rglob("*.md"):
        if ".git" in p.parts or "indices" in p.parts:
            continue
        files.append(p)
    random.shuffle(files)
    return files[:limit]

def read_chunk(path, max_chars=1200):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    text = text.replace("\n", " ").strip()
    return text[:max_chars]

def embed_batch(texts):
    if not texts:
        return {"ok": True}
    payload = json.dumps({"input": texts, "model": "nomic-embed-text-v1.5.Q4_K_M.gguf"}).encode()
    req = urllib.request.Request(EMBED_URL, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            resp.read()
        return {"ok": True, "n": len(texts)}
    except Exception as e:
        return {"error": str(e)}

def chat_completion(prompt):
    payload = json.dumps({
        "model": "argos-v1.q8_0.gguf",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 128,
        "temperature": 0.7,
    }).encode()
    req = urllib.request.Request(CHAT_URL, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            resp.read()
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("[GPU-LOAD] scanning vault...")
    files = get_md_files()
    print(f"[GPU-LOAD] {len(files)} files, embed batch {BATCH_EMBED}")
    i = 0
    embed_total = 0
    chat_total = 0
    errors = 0
    start = time.time()
    last_log = start
    last_log = start
    last_log = start
    while True:
        # Inference load
        prompt = random.choice(PROMPTS)
        res = chat_completion(prompt)
        if "error" in res:
            errors += 1
            print(f"[GPU-LOAD] chat error: {res['error']}")
        else:
            chat_total += 1

        # Embedding load
        batch_files = files[i:i+BATCH_EMBED]
        if not batch_files:
            i = 0
            random.shuffle(files)
            continue
        texts = [read_chunk(f) for f in batch_files]
        texts = [t for t in texts if t]
        res = embed_batch(texts)
        if "error" in res:
            errors += 1
            print(f"[GPU-LOAD] embed error: {res['error']}")
        else:
            embed_total += res.get("n", 0)
        i += BATCH_EMBED
        if i >= len(files):
            i = 0
            random.shuffle(files)

        elapsed = time.time() - start
        if elapsed - last_log >= 30:
            last_log = elapsed
            print(f"[GPU-LOAD] chats={chat_total} embeds={embed_total} errors={errors} elapsed={elapsed:.1f}s")
        time.sleep(0.0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[GPU-LOAD] stopped")
        sys.exit(0)
