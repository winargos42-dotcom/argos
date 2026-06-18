#!/usr/bin/env python3
"""
Постоянная рабочая нагрузка для V100 через llama-server эмбеддингов.
Читает Obsidian vault, шлёт батчи на 192.168.1.72:8090/v1/embeddings,
поддерживает GPU занятым и логирует utilization.
"""
import json
import os
import random
import sys
import time
import urllib.request
from pathlib import Path

EMBED_URL = "http://192.168.1.72:8090/v1/embeddings"
VAULT = "/home/ava/Documents/MyObsidianVault"
BATCH = 256
SLEEP_BETWEEN_BATCHES = 0.0  # seconds
LOG_EVERY = 200

def get_md_files(limit=2000):
    files = []
    for p in Path(VAULT).rglob("*.md"):
        if ".git" in p.parts or "indices" in p.parts:
            continue
        files.append(p)
    random.shuffle(files)
    return files[:limit]

def read_chunk(path, max_chars=1500):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    # strip frontmatter
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    text = text.replace("\n", " ").strip()
    return text[:max_chars]

def embed_batch(texts):
    payload = json.dumps({"input": texts, "model": "nomic-embed-text-v1.5.Q4_K_M.gguf"}).encode()
    req = urllib.request.Request(EMBED_URL, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def main():
    print("[GPU-WARM] scanning vault...")
    files = get_md_files()
    print(f"[GPU-WARM] {len(files)} files, batch {BATCH}")
    i = 0
    total = 0
    errors = 0
    start = time.time()
    while True:
        batch_files = files[i:i+BATCH]
        if not batch_files:
            i = 0
            random.shuffle(files)
            continue
        texts = [read_chunk(f) for f in batch_files]
        texts = [t for t in texts if t]
        if not texts:
            i += BATCH
            continue
        res = embed_batch(texts)
        if "error" in res:
            errors += 1
            print(f"[GPU-WARM] error: {res['error']}")
        else:
            total += len(texts)
        i += BATCH
        if i >= len(files):
            i = 0
            random.shuffle(files)
        if total % LOG_EVERY == 0 and total > 0:
            elapsed = time.time() - start
            print(f"[GPU-WARM] processed {total} docs, errors {errors}, elapsed {elapsed:.1f}s")
        time.sleep(SLEEP_BETWEEN_BATCHES)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[GPU-WARM] stopped")
        sys.exit(0)
