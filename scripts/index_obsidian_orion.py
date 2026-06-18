# -*- coding: utf-8 -*-
"""Index Obsidian vault on Orion into MemPalace ChromaDB."""
import os, re, hashlib, time, sys
from pathlib import Path
from datetime import datetime, timezone

VAULT_ROOT = Path(r"F:\debug\аргос")
PALACE_PATH = Path(r"F:\debug\argoss\data\mempalace")
COLLECTION_NAME = "mempalace_drawers"
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200

import chromadb


def parse_frontmatter(text: str):
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            raw = text[3:end].strip()
            body = text[end + 3:].strip()
            # Simple key: value parsing (no nested structures)
            fm = {}
            for line in raw.splitlines():
                if ":" in line and not line.startswith("-"):
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"').strip("'")
            return fm, body
    return {}, text.strip()


def extract_tags(text: str):
    return list(set(re.findall(r"#([\w\-/]+)", text)))


def extract_links(text: str):
    return list(set(re.findall(r"\[\[([^\]]+)\]\]", text)))


def chunk_text(text: str, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        if end >= len(text):
            chunks.append(text[start:])
            break
        search_start = end - overlap
        split_pos = text.rfind("\n", search_start, end)
        if split_pos == -1:
            split_pos = text.rfind(" ", search_start, end)
        if split_pos == -1:
            split_pos = end
        chunks.append(text[start:split_pos])
        start = split_pos + 1 if split_pos > start else end
    return chunks


def main():
    PALACE_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(PALACE_PATH))
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
        print(f"[+] Collection '{COLLECTION_NAME}' exists with {collection.count()} docs")
    except Exception:
        collection = client.create_collection(
            name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
        )
        print(f"[+] Created collection '{COLLECTION_NAME}'")

    md_files = list(VAULT_ROOT.rglob("*.md"))
    print(f"[*] Found {len(md_files)} markdown files")

    total_chunks = 0
    total_files = 0
    start_t = time.time()

    for idx, md_path in enumerate(md_files, 1):
        try:
            rel = md_path.relative_to(VAULT_ROOT)
        except ValueError:
            continue
        parts = rel.parts
        wing = parts[0] if len(parts) > 1 else "general"
        room = parts[1] if len(parts) > 2 else "general"

        try:
            raw = md_path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            print(f"[!] Cannot read {rel}: {exc}")
            continue

        frontmatter, body = parse_frontmatter(raw)
        tags = extract_tags(raw)
        links = extract_links(raw)
        title = frontmatter.get("title", md_path.stem)
        try:
            importance = float(frontmatter.get("importance", 3.0))
        except (ValueError, TypeError):
            importance = 3.0

        chunks = chunk_text(body)
        if not chunks:
            continue

        for chunk_idx, chunk in enumerate(chunks):
            chunk_id = hashlib.sha256(
                f"{rel}::{chunk_idx}::{chunk[:200]}".encode("utf-8")
            ).hexdigest()[:16]

            meta = {
                "wing": wing,
                "room": room,
                "source": "obsidian",
                "entity_id": "",
                "importance": importance,
                "file": str(rel),
                "chunk": chunk_idx,
                "tags": ",".join(tags),
                "links": ",".join(links),
                "title": title,
                "mined_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            }
            try:
                collection.upsert(
                    documents=[chunk],
                    ids=[chunk_id],
                    metadatas=[meta],
                )
                total_chunks += 1
            except Exception as exc:
                print(f"[!] Upsert failed {rel} chunk {chunk_idx}: {exc}")
                continue

        total_files += 1
        if idx % 100 == 0:
            elapsed = time.time() - start_t
            print(f"[*] {idx}/{len(md_files)} files, {total_chunks} chunks, {elapsed:.1f}s")

    final_count = collection.count()
    print(f"[✓] Done: {total_files} files, {total_chunks} chunks, {final_count} total docs")


if __name__ == "__main__":
    main()
