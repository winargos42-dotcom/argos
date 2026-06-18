#!/usr/bin/env python3
"""
ARGOS Data Pipeline — загрузка, дедупликация, фильтрация и токенизация
русскоязычных датасетов с HuggingFace Hub для дообучения Qwen2.5-7B.

Запуск:
    python scripts/data_pipeline_hf.py

Окружение:
    HF_TOKEN — токен HuggingFace (или будет использован из ~/.cache/huggingface/token)
    GOOGLE_APPLICATION_CREDENTIALS — путь к service account (опционально, для Vertex)
"""
import os
import sys
import json
import hashlib
import random
import re
import time
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Callable

# ── конфигурация ──────────────────────────────────────
BASE_MODEL = "Qwen/Qwen2.5-7B-Instruct"
TOKENIZER_NAME = os.environ.get("ARGOS_TOKENIZER", BASE_MODEL)
MAX_SEQ_LEN = 2048
MIN_TOKENS = 20
MAX_TOKENS = MAX_SEQ_LEN

DATASETS_CONFIG = [
    {
        "name": "AvaSiG/ru-big-russian-dataset-bucket",
        "split": "train",
        "fallback": "ZeroAgency/ru-big-russian-dataset",
        "weight": 1.0,
        "format": "auto",
    },
    {
        "name": "AvaSiG/ru-thinking-reasoning-r1-deduped-bucket",
        "split": "train",
        "fallback": "ZeroAgency/ru-thinking-reasoning-r1-deduped",
        "weight": 1.0,
        "format": "auto",
    },
    {
        "name": "AvaSiG/ru-instruct-conversation-v3.1-small-bucket",
        "split": "train",
        "fallback": "ZeroAgency/ru-instruct-conversation-v3.1-small",
        "weight": 1.0,
        "format": "auto",
    },
    {
        "name": "AvaSiG/ru-tasks-conversation-deduped-bucket",
        "split": "train",
        "fallback": "ZeroAgency/ru-tasks-conversation-deduped",
        "weight": 1.0,
        "format": "auto",
    },
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_OUT = PROJECT_ROOT / "data" / "datasets"
CACHE_DIR = DATA_OUT / "cache"
MERGED_PATH = DATA_OUT / "merged_ru_dataset.jsonl"
REPORT_PATH = DATA_OUT / "processing_report.json"
STATS_PATH = DATA_OUT / "statistics.json"

HF_TOKEN = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")

# ── логгер ────────────────────────────────────────────
def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

# ── статистика ────────────────────────────────────────
@dataclass
class DatasetStats:
    name: str
    requested_name: str
    downloaded: int = 0
    after_exact_dedup: int = 0
    after_near_dedup: int = 0
    after_filter: int = 0
    tokens_min: int = 0
    tokens_max: int = 0
    tokens_mean: float = 0.0
    tokens_median: float = 0.0
    duration_sec: float = 0.0

@dataclass
class PipelineReport:
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    tokenizer: str = ""
    datasets: List[DatasetStats] = field(default_factory=list)
    total_rows_raw: int = 0
    total_rows_final: int = 0
    total_tokens: int = 0
    disk_usage_mb: float = 0.0
    warnings: List[str] = field(default_factory=list)

# ── загрузка датасетов ────────────────────────────────
def try_load_dataset(ds_name: str, split: str, fallback: Optional[str] = None, max_rows: Optional[int] = None, streaming: bool = False):
    from datasets import load_dataset

    kwargs = {"cache_dir": str(CACHE_DIR)}
    if HF_TOKEN:
        kwargs["token"] = HF_TOKEN

    def _load(name):
        log(f"  Попытка загрузки: {name} [{split}]")
        if streaming:
            ds = load_dataset(name, split=split, streaming=True, **kwargs)
            if max_rows:
                ds = ds.take(max_rows)
            # Materialize streaming dataset to list for uniform processing
            return ds
        return load_dataset(name, split=split, **kwargs)

    try:
        return _load(ds_name), ds_name
    except Exception as e:
        log(f"  Не удалось загрузить {ds_name}: {e}")
        if fallback:
            try:
                return _load(fallback), fallback
            except Exception as e2:
                log(f"  Fallback тоже не сработал: {e2}")
        return None, ds_name

# ── нормализация формата ──────────────────────────────
def normalize_example(example: dict, ds_name: str) -> Optional[dict]:
    """Приводим к унифицированному chat-формату {'messages': [...]}."""
    ex = dict(example)

    # Уже в формате messages
    if "messages" in ex and isinstance(ex["messages"], list):
        return {"messages": ex["messages"], "source": ds_name}

    # instruction / input / output
    if "instruction" in ex:
        instruction = str(ex.get("instruction", ""))
        inp = str(ex.get("input", ""))
        out = str(ex.get("output", ""))
        content = f"{instruction}\n\n{inp}".strip() if inp else instruction
        return {
            "messages": [
                {"role": "user", "content": content},
                {"role": "assistant", "content": out},
            ],
            "source": ds_name,
        }

    # prompt / completion
    if "prompt" in ex and "completion" in ex:
        return {
            "messages": [
                {"role": "user", "content": str(ex["prompt"])},
                {"role": "assistant", "content": str(ex["completion"])},
            ],
            "source": ds_name,
        }

    # text
    if "text" in ex:
        return {"messages": [{"role": "assistant", "content": str(ex["text"])}], "source": ds_name}

    # content
    if "content" in ex:
        return {"messages": [{"role": "assistant", "content": str(ex["content"])}], "source": ds_name}

    # conversation / dialog
    if "conversation" in ex:
        return {"messages": ex["conversation"], "source": ds_name}
    if "dialog" in ex:
        return {"messages": ex["dialog"], "source": ds_name}

    # Неизвестный формат — пытаемся собрать хоть что-то
    texts = [str(v) for k, v in ex.items() if isinstance(v, str) and len(v) > 10]
    if texts:
        return {"messages": [{"role": "assistant", "content": " ".join(texts)}], "source": ds_name}
    return None

# ── дедупликация ────────────────────────────────────────
def exact_dedup(records: List[dict]) -> List[dict]:
    seen = set()
    out = []
    for r in records:
        text = json.dumps(r.get("messages"), ensure_ascii=False, sort_keys=True)
        h = hashlib.md5(text.encode("utf-8")).hexdigest()
        if h not in seen:
            seen.add(h)
            out.append(r)
    return out


class MinHashDedup:
    """Простой MinHash для near-duplicate detection."""

    def __init__(self, num_perm=128, threshold=0.85, ngram=5):
        self.num_perm = num_perm
        self.threshold = threshold
        self.ngram = ngram
        self.bands = 16
        self.rows = num_perm // self.bands
        random.seed(42)
        self.hash_seeds = [random.randint(0, 2**32 - 1) for _ in range(num_perm)]

    def _get_shingles(self, text: str) -> set:
        text = re.sub(r"\s+", " ", text.lower().strip())
        return {text[i:i + self.ngram] for i in range(len(text) - self.ngram + 1)}

    def _signature(self, shingles: set) -> list:
        if not shingles:
            return [0] * self.num_perm
        sig = []
        for seed in self.hash_seeds:
            min_hash = min(hash((s, seed)) & 0xFFFFFFFF for s in shingles)
            sig.append(min_hash)
        return sig

    def dedup(self, records: List[dict]) -> List[dict]:
        out = []
        buckets = {}  # band -> dict(band_hash -> list[record_index])
        for idx, r in enumerate(records):
            text = " ".join(
                m.get("content", "") for m in r.get("messages", [])
            )
            shingles = self._get_shingles(text)
            sig = self._signature(shingles)
            duplicate = False
            for band in range(self.bands):
                start = band * self.rows
                end = start + self.rows
                band_hash = tuple(sig[start:end])
                band_bucket = buckets.setdefault(band, {})
                if band_hash in band_bucket:
                    for other_idx in band_bucket[band_hash]:
                        # Точная проверка Jaccard для кандидатов
                        other = out[other_idx]
                        other_text = " ".join(
                            m.get("content", "") for m in other.get("messages", [])
                        )
                        other_shingles = self._get_shingles(other_text)
                        inter = len(shingles & other_shingles)
                        union = len(shingles | other_shingles)
                        sim = inter / union if union else 0.0
                        if sim >= self.threshold:
                            duplicate = True
                            break
                if duplicate:
                    break
                band_bucket.setdefault(band_hash, []).append(len(out))
            if not duplicate:
                out.append(r)
        return out


# ── фильтрация ──────────────────────────────────────────
def filter_record(r: dict, tokenizer=None) -> bool:
    """Фильтры качества."""
    messages = r.get("messages", [])
    if not messages:
        return False

    # Проверяем, что есть хотя бы assistant-сообщение
    assistant_msgs = [m for m in messages if m.get("role") == "assistant"]
    if not assistant_msgs:
        return False

    # Длина
    full_text = " ".join(str(m.get("content", "")) for m in messages)
    if len(full_text) < 30:
        return False

    # Соотношение русских символов
    cyrillic = len(re.findall(r"[\u0400-\u04FF]", full_text))
    total_chars = len(re.findall(r"[A-Za-z\u0400-\u04FF]", full_text))
    if total_chars > 0 and cyrillic / total_chars < 0.3:
        return False

    # Токенизация и проверка длины
    if tokenizer:
        try:
            tok_len = len(tokenizer(full_text)["input_ids"])
            if tok_len < MIN_TOKENS or tok_len > MAX_TOKENS:
                return False
        except Exception:
            pass

    return True


# ── токенизация и статистика ───────────────────────────
def compute_token_stats(records: List[dict], tokenizer) -> dict:
    lengths = []
    for r in records:
        text = " ".join(str(m.get("content", "")) for m in r.get("messages", []))
        try:
            tok_len = len(tokenizer(text)["input_ids"])
            lengths.append(tok_len)
        except Exception:
            pass
    if not lengths:
        return {"min": 0, "max": 0, "mean": 0.0, "median": 0.0}
    lengths.sort()
    n = len(lengths)
    return {
        "min": lengths[0],
        "max": lengths[-1],
        "mean": sum(lengths) / n,
        "median": lengths[n // 2] if n % 2 else (lengths[n // 2 - 1] + lengths[n // 2]) / 2,
    }


def format_for_training(r: dict, tokenizer_name: str = BASE_MODEL) -> dict:
    """Форматируем в Qwen2.5 chat-формат (или оставляем messages)."""
    messages = r.get("messages", [])
    if not messages:
        return r

    # Для Qwen2.5 формируем текстовое представление
    if "qwen" in tokenizer_name.lower():
        parts = []
        for m in messages:
            role = m.get("role", "user")
            content = str(m.get("content", ""))
            parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")
        text = "\n".join(parts)
        return {"text": text, "source": r.get("source", "")}

    # Для llama-3 формируем свои специальные токены
    if "llama" in tokenizer_name.lower():
        parts = []
        for m in messages:
            role = m.get("role", "user")
            content = str(m.get("content", ""))
            parts.append(f"<|start_header_id|>{role}<|end_header_id|>\n{content}<|eot_id|>")
        text = "\n".join(parts)
        return {"text": text, "source": r.get("source", "")}

    # По умолчанию — оставляем messages
    return {"messages": messages, "source": r.get("source", "")}


# ── Vertex AI augmentation (опционально) ────────────────
def vertex_augment(records: List[dict]) -> List[dict]:
    """Если доступны Google Cloud credentials — можно добавить аугментацию."""
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path or not Path(creds_path).exists():
        return records

    try:
        from google.cloud import aiplatform
        log("Vertex AI credentials найдены, но аугментация требует ручной настройки.")
        # TODO: подключить Vertex AI Data Augmentation
    except Exception as e:
        log(f"Vertex AI import error: {e}")
    return records


# ── основной пайплайн ───────────────────────────────────
def run_pipeline(test_mode: bool = False, max_rows_test: Optional[int] = None):
    log("=" * 60)
    log("ARGOS Data Pipeline — старт")
    log("=" * 60)

    os.makedirs(DATA_OUT, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    # Загружаем токенизатор
    log(f"Загрузка токенизатора: {TOKENIZER_NAME}")
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            TOKENIZER_NAME, trust_remote_code=True,
            local_files_only=True,
        )
        tokenizer.pad_token = tokenizer.eos_token
    except Exception:
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                TOKENIZER_NAME, trust_remote_code=True,
            )
            tokenizer.pad_token = tokenizer.eos_token
        except Exception as e:
            log(f"Ошибка загрузки токенизатора: {e}")
            log("Продолжаем без токенизации...")
            tokenizer = None

    report = PipelineReport(tokenizer=TOKENIZER_NAME)
    all_records = []
    minhash = MinHashDedup(num_perm=128, threshold=0.85)

    for cfg in DATASETS_CONFIG:
        if test_mode and cfg != DATASETS_CONFIG[0]:
            continue

        name = cfg["name"]
        split = cfg.get("split", "train")
        fallback = cfg.get("fallback")
        weight = cfg.get("weight", 1.0)
        streaming = cfg.get("streaming", test_mode and max_rows_test is not None)
        max_rows = max_rows_test if test_mode else None

        log(f"\n▶ Обработка: {name}")
        t0 = time.time()

        ds, loaded_name = try_load_dataset(name, split, fallback, max_rows=max_rows, streaming=streaming)
        if ds is None:
            report.warnings.append(f"Не удалось загрузить: {name}")
            log(f"  ⚠ Пропускаем {name}")
            continue

        # Materialize if streaming
        if hasattr(ds, "take"):
            log("  Материализация streaming dataset...")
            ds = list(ds)
            log(f"  Загружено {len(ds)} примеров из {loaded_name}")
        else:
            log(f"  Загружено {len(ds)} примеров из {loaded_name}")

        # Нормализация
        records = []
        for ex in ds:
            norm = normalize_example(ex, loaded_name)
            if norm:
                records.append(norm)

        raw_count = len(records)
        log(f"  Нормализовано: {raw_count}")

        # Дедупликация
        records = exact_dedup(records)
        after_exact = len(records)
        log(f"  После exact dedup: {after_exact} (-{raw_count - after_exact})")

        records = minhash.dedup(records)
        after_near = len(records)
        log(f"  После near-dedup: {after_near} (-{after_exact - after_near})")

        # Фильтрация
        records = [r for r in records if filter_record(r, tokenizer)]
        after_filter = len(records)
        log(f"  После фильтрации: {after_filter} (-{after_near - after_filter})")

        # Статистика токенов
        tok_stats = compute_token_stats(records, tokenizer) if tokenizer else {}
        duration = time.time() - t0

        stats = DatasetStats(
            name=loaded_name,
            requested_name=name,
            downloaded=len(ds) if isinstance(ds, list) else (len(ds) if hasattr(ds, "__len__") else raw_count),
            after_exact_dedup=after_exact,
            after_near_dedup=after_near,
            after_filter=after_filter,
            tokens_min=tok_stats.get("min", 0),
            tokens_max=tok_stats.get("max", 0),
            tokens_mean=round(tok_stats.get("mean", 0.0), 2),
            tokens_median=round(tok_stats.get("median", 0.0), 2),
            duration_sec=round(duration, 2),
        )
        report.datasets.append(stats)
        all_records.extend(records)

        if test_mode:
            break

    log(f"\n{'=' * 60}")
    log(f"Итого записей до окончательного слияния: {len(all_records)}")

    # Финальная exact-дедупликация всего объёма
    all_records = exact_dedup(all_records)
    log(f"После финальной dedup: {len(all_records)}")

    # Опциональная Vertex аугментация
    all_records = vertex_augment(all_records)

    # Форматирование для обучения
    formatted = [format_for_training(r, TOKENIZER_NAME) for r in all_records]

    # Сохранение
    log(f"\nСохранение в {MERGED_PATH}")
    with open(MERGED_PATH, "w", encoding="utf-8") as f:
        for r in formatted:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    report.total_rows_raw = sum(s.downloaded for s in report.datasets)
    report.total_rows_final = len(all_records)
    if tokenizer and all_records:
        tok_stats = compute_token_stats(all_records, tokenizer)
        report.total_tokens = int(tok_stats.get("mean", 0.0) * len(all_records))

    # Disk usage
    du = sum(f.stat().st_size for f in DATA_OUT.rglob("*") if f.is_file()) / (1024 * 1024)
    report.disk_usage_mb = round(du, 2)

    # Сохранение отчётов
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, ensure_ascii=False, indent=2)

    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, ensure_ascii=False, indent=2)

    log(f"✓ Сохранено {len(all_records)} записей")
    log(f"✓ Отчёт: {REPORT_PATH}")
    log(f"✓ Диск: {report.disk_usage_mb:.1f} MB")
    log("=" * 60)

    return report


if __name__ == "__main__":
    test = "--test" in sys.argv or "-t" in sys.argv
    max_rows_test = None
    for arg in sys.argv:
        if arg.startswith("--max-rows="):
            max_rows_test = int(arg.split("=", 1)[1])
    if test:
        log("Режим тестирования: только первый датасет")
        if max_rows_test:
            log(f"  Ограничение: {max_rows_test} строк")
    run_pipeline(test_mode=test, max_rows_test=max_rows_test)
