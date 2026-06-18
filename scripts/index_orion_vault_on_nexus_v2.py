#!/usr/bin/env python3
"""Index Obsidian vault into MemPalace ChromaDB for Orion (batch mode, Nexus)."""
import os, re, hashlib, time, yaml, sys
from pathlib import Path
from datetime import datetime, timezone

VAULT_ROOT = Path("/tmp/orion_vault")
PALACE_PATH = Path("/home/ava/Projects/argoss/data/mempalace_orion")
COLLECTION_NAME = "mempalace_drawers"
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 300
BATCH_SIZE = 64

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mempalace-develop"))
import chromadb


def parse_frontmatter(text: str):
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            try:
                fm = yaml.safe_load(text[3:end])
                if isinstance(fm, dict):
                    return fm, text[end + 3 :].strip()
            except Exception:
                pass
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
        print(f"[+] Using existing collection '{COLLECTION_NAME}' with {collection.count()} docs")
    except Exception:
        collection = client.create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
        print(f"[+] Created collection '{COLLECTION_NAME}'")

    md_files = sorted(VAULT_ROOT.rglob("*.md"))
    print(f"[*] Found {len(md_files)} markdown files")

    total_chunks = collection.count()
    total_files = 0
    start_t = time.time()

    batch_docs = []
    batch_ids = []
    batch_metas = []

    def flush_batch():
        nonlocal batch_docs, batch_ids, batch_metas, total_chunks
        if not batch_docs:
            return
        try:
            collection.upsert(documents=batch_docs, ids=batch_ids, metadatas=batch_metas)
            total_chunks += len(batch_docs)
        except Exception as exc:
            print(f"[!] Batch upsert failed: {exc}")
        batch_docs.clear()
        batch_ids.clear()
        batch_metas.clear()

    for idx, md_path in enumerate(md_files, 1):
        rel = md_path.relative_to(VAULT_ROOT)
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
            batch_docs.append(chunk)
            batch_ids.append(chunk_id)
            batch_metas.append(meta)
            if len(batch_docs) >= BATCH_SIZE:
                flush_batch()

        total_files += 1
        if idx % 100 == 0:
            elapsed = time.time() - start_t
            print(f"[*] {idx}/{len(md_files)} files, {total_chunks} chunks, {elapsed:.1f}s")

    flush_batch()
    final_count = collection.count()
    print(f"[✓] Done: {total_files} files, {total_chunks} chunks, {final_count} total docs")


if __name__ == "__main__":
    main()
