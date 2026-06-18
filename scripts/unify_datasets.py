#!/usr/bin/env python3
"""
ARGOS Unified Dataset Builder
Объединяет все .jsonl датасеты в один, дедуплицирует,
фильтрует по качеству и делит на train/val.
"""
import json, hashlib, re, os, sys
from pathlib import Path
from collections import Counter

DATA_DIR = Path("/home/ava/Projects/argoss/data")
OUT_DIR = DATA_DIR / "datasets"
OUT_DIR.mkdir(exist_ok=True)

# Датасеты для объединения (по приоритету)
DATASETS = [
    "argos_quantum_train.jsonl",
    "argos_canonical_train.jsonl",
    "argos_final_train.jsonl",
    "argos_dal_dataset.jsonl",
    "argos_all_combined.jsonl",
    "argos_train_v2.jsonl",
    "argos_memory_train.jsonl",
    "argos_ru_classic.jsonl",
]

def normalize_text(text: str) -> str:
    """Нормализация для дедупликации."""
    t = text.lower().strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^\w\sа-яё]", "", t)
    return t[:200]

def hash_message(msg: dict) -> str:
    """Хеш по нормализованному assistant content."""
    content = ""
    for m in msg.get("messages", []):
        if m.get("role") == "assistant":
            content += m.get("content", "")
    return hashlib.sha256(normalize_text(content).encode()).hexdigest()[:16]

def is_quality_sample(msg: dict) -> bool:
    """Фильтр качества."""
    messages = msg.get("messages", [])
    if len(messages) < 2:
        return False
    total_len = sum(len(m.get("content", "")) for m in messages)
    if total_len < 50:
        return False
    if total_len > 8000:
        return False  # слишком длинные — обрежем позже
    # Проверка на мусор
    assistant_text = ""
    for m in messages:
        if m.get("role") == "assistant":
            assistant_text = m.get("content", "")
    if len(assistant_text) < 20:
        return False
    # Пропорция русского текста
    ru_chars = len(re.findall(r"[а-яё]", assistant_text.lower()))
    if ru_chars > 0 and ru_chars / max(len(assistant_text), 1) < 0.1:
        # Мало русского — пропускаем если это не код
        if "```" not in assistant_text:
            return False
    return True

def load_all():
    all_samples = []
    seen_hashes = set()
    stats = Counter()
    for ds_name in DATASETS:
        path = DATA_DIR / ds_name
        if not path.exists():
            print(f"[SKIP] {ds_name} not found")
            continue
        loaded = 0
        dupes = 0
        bad = 0
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    sample = json.loads(line)
                except json.JSONDecodeError:
                    continue
                h = hash_message(sample)
                if h in seen_hashes:
                    dupes += 1
                    continue
                if not is_quality_sample(sample):
                    bad += 1
                    continue
                seen_hashes.add(h)
                all_samples.append(sample)
                loaded += 1
        stats[ds_name] = loaded
        print(f"[LOAD] {ds_name}: {loaded} loaded, {dupes} dupes, {bad} filtered")
    print(f"[TOTAL] Unique quality samples: {len(all_samples)}")
    return all_samples, stats

def split_and_save(samples):
    import random
    random.seed(42)
    random.shuffle(samples)
    n_val = max(1, len(samples) // 10)
    val = samples[:n_val]
    train = samples[n_val:]

    # Сохраняем в chat format (для unsloth/trl)
    with open(OUT_DIR / "train_chat.jsonl", "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with open(OUT_DIR / "val_chat.jsonl", "w", encoding="utf-8") as f:
        for s in val:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    # Сохраняем в text+completion format (для llama.cpp)
    def to_text_completion(sample):
        msgs = sample.get("messages", [])
        system = ""
        prompt = ""
        completion = ""
        for m in msgs:
            role = m.get("role", "")
            content = m.get("content", "")
            if role == "system":
                system = content
            elif role == "user":
                prompt = content
            elif role == "assistant":
                completion = content
        return {"system": system, "prompt": prompt, "completion": completion}

    with open(OUT_DIR / "train_text.jsonl", "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(to_text_completion(s), ensure_ascii=False) + "\n")
    with open(OUT_DIR / "val_text.jsonl", "w", encoding="utf-8") as f:
        for s in val:
            f.write(json.dumps(to_text_completion(s), ensure_ascii=False) + "\n")

    # Сохраняем в alpaca format
    def to_alpaca(sample):
        msgs = sample.get("messages", [])
        instruction = ""
        input_text = ""
        output = ""
        system = ""
        for m in msgs:
            role = m.get("role", "")
            content = m.get("content", "")
            if role == "system":
                system = content
            elif role == "user":
                instruction = content
            elif role == "assistant":
                output = content
        return {"instruction": instruction, "input": input_text, "output": output, "system": system}

    with open(OUT_DIR / "train_alpaca.jsonl", "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(to_alpaca(s), ensure_ascii=False) + "\n")
    with open(OUT_DIR / "val_alpaca.jsonl", "w", encoding="utf-8") as f:
        for s in val:
            f.write(json.dumps(to_alpaca(s), ensure_ascii=False) + "\n")

    # Статистика
    stats = {
        "total": len(samples),
        "train": len(train),
        "val": len(val),
        "avg_chars": sum(sum(len(m.get("content","")) for m in s.get("messages",[])) for s in samples) / max(len(samples),1),
    }
    with open(OUT_DIR / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"[SAVE] train={len(train)}, val={len(val)}")
    print(f"[SAVE] Formats: chat, text, alpaca")
    print(f"[SAVE] Avg chars per sample: {stats['avg_chars']:.0f}")
    print(f"[OUT]  {OUT_DIR}")

if __name__ == "__main__":
    print("=" * 50)
    print("ARGOS Unified Dataset Builder")
    print("=" * 50)
    samples, stats = load_all()
    if samples:
        split_and_save(samples)
    else:
        print("[ERROR] No samples loaded.")
        sys.exit(1)
