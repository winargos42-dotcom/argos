"""
Батч-эмбеддинг Obsidian vault через llama-server /v1/embeddings.
Сохраняет индекс в .npz для последующего поиска/кластеризации.
"""
from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import aiohttp
import numpy as np

from src.utils.v100_utils import GPUStat, get_gpu_stats, get_llama_server_processes


DEFAULT_MAX_CHARS = 8192
DEFAULT_MAX_FILE_SIZE = 1_000_000
DEFAULT_BATCH_SIZE = 16
DEFAULT_TIMEOUT = 60


@dataclass
class EmbedderConfig:
    vault_path: Path
    embed_url: str
    model: str
    index_path: Path
    batch_size: int = DEFAULT_BATCH_SIZE
    max_chars: int = DEFAULT_MAX_CHARS
    max_file_size: int = DEFAULT_MAX_FILE_SIZE
    timeout: int = DEFAULT_TIMEOUT
    max_vram_mb: float = 15_360  # 95% of 16 GB V100
    max_gpu_util: int = 90


def safe_read_text(path: Path, max_file_size: int = DEFAULT_MAX_FILE_SIZE) -> Optional[str]:
    """Безопасное чтение .md файла с ограничением размера."""
    try:
        size = path.stat().st_size
        if size == 0 or size > max_file_size:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except (PermissionError, OSError):
        return None


def check_gpu_safe(gpu: GPUStat, cfg: EmbedderConfig) -> Tuple[bool, str]:
    """Проверка, что GPU готова принять нагрузку."""
    if gpu.memory_used_mb > cfg.max_vram_mb:
        return False, (
            f"GPU перегружена VRAM: {gpu.memory_used_mb:.0f}/"
            f"{gpu.memory_total_mb:.0f} MiB > {cfg.max_vram_mb:.0f}"
        )
    if gpu.gpu_util_pct > cfg.max_gpu_util:
        return False, f"GPU занята: {gpu.gpu_util_pct}% util > {cfg.max_gpu_util}%"
    return True, "OK"


async def embed_batch(
    session: aiohttp.ClientSession,
    texts: List[str],
    cfg: EmbedderConfig,
    retries: int = 3,
) -> np.ndarray:
    """Отправить батч на embedding endpoint. Возвращает матрицу [N, dim]."""
    if not texts:
        return np.zeros((0, 0), dtype=np.float32)

    truncated = [t[: cfg.max_chars] for t in texts]
    payload = {"input": truncated, "model": cfg.model}

    for attempt in range(retries):
        try:
            async with session.post(
                cfg.embed_url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=cfg.timeout),
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    print(f"[RETRY {attempt + 1}] HTTP {resp.status}: {body[:200]}")
                    await asyncio.sleep(2**attempt)
                    continue

                data = await resp.json()
                if "data" not in data or not data["data"]:
                    print(f"[ERROR] пустой embedding ответ: {json.dumps(data)[:200]}")
                    return np.zeros((0, 0), dtype=np.float32)

                items = sorted(data["data"], key=lambda x: x.get("index", 0))
                embeddings = np.array([item["embedding"] for item in items], dtype=np.float32)
                if embeddings.shape[0] != len(texts):
                    print(
                        f"[WARN] размер батча не совпал: "
                        f"{embeddings.shape[0]} vs {len(texts)}"
                    )
                return embeddings
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"[RETRY {attempt + 1}] сетевая ошибка: {e}")
            await asyncio.sleep(2**attempt)

    print(f"[ERROR] батч из {len(texts)} текстов не удалось обработать")
    return np.zeros((0, 0), dtype=np.float32)


async def process_vault(cfg: EmbedderConfig) -> Tuple[List[Path], np.ndarray]:
    """Главная функция: .md -> эмбеддинги -> .npz индекс."""
    # GPU check
    try:
        gpu = get_gpu_stats(0)
        ok, msg = check_gpu_safe(gpu, cfg)
        if not ok:
            raise RuntimeError(msg)
        print(f"[GPU] {gpu.name}: {gpu.memory_used_mb:.0f}/{gpu.memory_total_mb:.0f} MiB, "
              f"{gpu.gpu_util_pct}% util — OK")
    except Exception as e:
        print(f"[WARN] GPU check skipped: {e}")

    # Read files
    files = [p for p in cfg.vault_path.rglob("*.md") if p.is_file()]
    print(f"[VAULT] найдено {len(files)} .md файлов")

    docs: List[Tuple[Path, str]] = []
    for p in files:
        text = safe_read_text(p, cfg.max_file_size)
        if text:
            docs.append((p, text))
    print(f"[VAULT] загружено {len(docs)} документов")

    if not docs:
        return [], np.zeros((0, 0), dtype=np.float32)

    # Embed in batches
    all_paths: List[Path] = []
    all_embeddings: List[np.ndarray] = []

    connector = aiohttp.TCPConnector(limit=5)
    async with aiohttp.ClientSession(connector=connector) as session:
        for i in range(0, len(docs), cfg.batch_size):
            batch = docs[i : i + cfg.batch_size]
            paths = [d[0] for d in batch]
            texts = [d[1] for d in batch]

            emb = await embed_batch(session, texts, cfg)
            if emb.shape[0] > 0:
                all_paths.extend(paths)
                all_embeddings.append(emb)

            print(f"[PROGRESS] {min(i + cfg.batch_size, len(docs))}/{len(docs)}")

    if not all_embeddings:
        return [], np.zeros((0, 0), dtype=np.float32)

    matrix = np.vstack(all_embeddings)

    # Save index
    cfg.index_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        cfg.index_path,
        paths=np.array([str(p) for p in all_paths]),
        embeddings=matrix,
        model=cfg.model,
        url=cfg.embed_url,
    )
    print(f"[INDEX] сохранён: {cfg.index_path} — {matrix.shape[0]} docs, dim {matrix.shape[1]}")

    return all_paths, matrix


def load_index(path: Path) -> Tuple[List[Path], np.ndarray, dict]:
    """Загрузить сохранённый индекс."""
    data = np.load(path)
    meta = {k: data[k].item() if isinstance(data[k], np.ndarray) and data[k].ndim == 0 else data[k]
            for k in data.files if k not in ("paths", "embeddings")}
    return [Path(p) for p in data["paths"]], data["embeddings"], meta


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Embed Obsidian vault via llama-server")
    parser.add_argument("--vault", type=Path, default=Path("/home/ava/Documents/MyObsidianVault"))
    parser.add_argument("--url", default="http://localhost:8086/v1/embeddings")
    parser.add_argument("--model", default="nomic-embed-text")
    parser.add_argument("--output", type=Path, default=Path("data/vault_index.npz"))
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    args = parser.parse_args()

    cfg = EmbedderConfig(
        vault_path=args.vault,
        embed_url=args.url,
        model=args.model,
        index_path=args.output,
        batch_size=args.batch_size,
    )

    print("llama-server процессы:", get_llama_server_processes())
    asyncio.run(process_vault(cfg))
