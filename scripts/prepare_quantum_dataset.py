#!/usr/bin/env python3
"""
ARGOS Quantum Dataset Builder v2.2
====================================
Интегрирует:
1. Все датасеты (evolver, train, telegram, obsidian, colab, dal)
2. SQLite базы (brain, memory, argos_memory, knowledge)
3. Квантовые genesis job'ы (IBM Quantum seed 3233339492)
4. Промпты для всех провайдеров
5. Квантовые модули (QuantumOracle, QuantumDecisionEngine)

Формат выхода: JSONL с messages для Ollama/llama.cpp
"""
from __future__ import annotations

import json
import hashlib
import math
import os
import random
import sqlite3
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Пути ───────────────────────────────────────────────────────────────────
BASE = Path("/home/ava/Projects/argoss")
DATA_PC = BASE / "data/pc_datasets"
DATA_OUT = BASE / "data/argos_quantum_train.jsonl"
QUANTUM_DIR = BASE / "src/quantum"

# Квантовый seed из IBM genesis
QUANTUM_SEED = 3233339492

# ── Квантовые модули ─────────────────────────────────────────────────────
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE / ".venv/lib/python3.14/site-packages"))

HAVE_QISKIT = False
try:
    from qiskit import QuantumCircuit
    from qiskit.primitives import StatevectorSampler
    HAVE_QISKIT = True
except Exception:
    pass

try:
    from src.quantum.oracle import QuantumOracle
    from src.quantum.quantum_ml import QuantumDecisionEngine, QuantumIntentHead
except Exception as e:
    print(f"⚠️ Квантовые модули недоступны: {e}")
    QuantumOracle = None
    QuantumDecisionEngine = None
    QuantumIntentHead = None


# ── Загрузка датасетов ───────────────────────────────────────────────────

def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        print(f"  ⚠️ Не найден: {path}")
        return []
    records = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"  ⚠️ JSON error in {path.name}:{i}")
    print(f"  ✅ {path.name}: {len(records)} записей")
    return records


def normalize_messages(record: Dict, source: str) -> Optional[Dict]:
    """Приводит запись к единому формату messages."""
    if "messages" in record and isinstance(record["messages"], list):
        return {
            "messages": record["messages"],
            "source": record.get("source", source),
            "metadata": record.get("metadata", {}),
        }

    # Формат instruction/input/output
    if "instruction" in record and "output" in record:
        messages = [{"role": "user", "content": record.get("instruction", "") + "\n" + record.get("input", "")}]
        if record.get("output"):
            messages.append({"role": "assistant", "content": record["output"]})
        return {"messages": messages, "source": source, "metadata": {}}

    # Формат ts/user/answer (evolver, colab, obsidian)
    user = record.get("user", "")
    answer = record.get("answer", "")
    if user or answer:
        messages = []
        if user:
            messages.append({"role": "user", "content": str(user)})
        if answer:
            messages.append({"role": "assistant", "content": str(answer)})
        return {"messages": messages, "source": source, "metadata": {}}

    # Формат thought/entity (entity_dataset)
    thought = record.get("thought", "")
    entity = record.get("entity", "")
    msgs = record.get("messages", [])
    if msgs:
        return {"messages": msgs, "source": source, "metadata": {"entity": entity}}
    if thought:
        messages = [
            {"role": "system", "content": f"Ты {entity}, AI-сущность ARGOS."},
            {"role": "assistant", "content": thought},
        ]
        return {"messages": messages, "source": source, "metadata": {"entity": entity}}

    return None


# ── Извлечение SQLite ────────────────────────────────────────────────────

def extract_sqlite(db_path: Path, source_name: str) -> List[Dict]:
    if not db_path.exists():
        return []
    records = []
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Пробуем таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]

        for table in tables:
            try:
                cursor.execute(f"SELECT * FROM {table} LIMIT 500")
                cols = [d[0] for d in cursor.description]
                rows = cursor.fetchall()
                for row in rows:
                    row_dict = dict(zip(cols, row))
                    text = json.dumps(row_dict, ensure_ascii=False, default=str)
                    if len(text) > 50:
                        records.append({
                            "messages": [
                                {"role": "system", "content": f"Ты ARGOS Universal OS. Данные из {source_name}.{table}"},
                                {"role": "user", "content": f"Что в таблице {table}?"},
                                {"role": "assistant", "content": text[:2000]},
                            ],
                            "source": f"sqlite:{source_name}:{table}",
                            "metadata": {},
                        })
            except Exception as e:
                pass
        conn.close()
    except Exception as e:
        print(f"  ⚠️ SQLite error {db_path}: {e}")
    print(f"  ✅ SQLite {source_name}: {len(records)} записей")
    return records


# ── Извлечение промптов ──────────────────────────────────────────────────

def extract_prompts(prompts_dir: Path) -> List[Dict]:
    records = []
    for md_file in prompts_dir.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            if len(text) > 50:
                records.append({
                    "messages": [
                        {"role": "system", "content": f"Ты ARGOS. Используй промпт из {md_file.name}"},
                        {"role": "user", "content": f"Покажи промпт {md_file.name}"},
                        {"role": "assistant", "content": text[:4000]},
                    ],
                    "source": f"prompt:{md_file.name}",
                    "metadata": {},
                })
        except Exception:
            pass
    print(f"  ✅ Промпты: {len(records)} записей")
    return records


# ── Квантовая обработка ──────────────────────────────────────────────────

def quantum_shuffle(records: List[Dict], seed: int) -> List[Dict]:
    """Перемешивает датасет с использованием квантового seed."""
    rng = random.Random(seed)
    shuffled = records.copy()
    rng.shuffle(shuffled)
    print(f"  ⚛️ Квантовое перемешивание (seed={seed})")
    return shuffled


def quantum_quality_score(record: Dict) -> float:
    """Вычисляет качество записи через квантовую эвристику."""
    messages = record.get("messages", [])
    if not messages:
        return 0.0

    total_len = sum(len(m.get("content", "")) for m in messages)
    has_assistant = any(m.get("role") == "assistant" for m in messages)
    has_user = any(m.get("role") == "user" for m in messages)

    score = 0.0
    if has_user:
        score += 0.3
    if has_assistant:
        score += 0.4
    if total_len > 50:
        score += 0.2
    if total_len > 200:
        score += 0.1

    # Квантовый шум через seed
    noise = (hash(record.get("source", "") + str(total_len)) % 1000) / 10000.0
    score = min(1.0, score + noise)
    return score


def quantum_filter(records: List[Dict], threshold: float = 0.5) -> List[Dict]:
    """Фильтрует записи по квантовому качеству."""
    filtered = []
    for r in records:
        score = quantum_quality_score(r)
        if score >= threshold:
            r["metadata"] = r.get("metadata", {})
            r["metadata"]["quantum_score"] = round(score, 3)
            filtered.append(r)
    print(f"  ⚛️ Квантовый фильтр: {len(filtered)}/{len(records)} прошли (threshold={threshold})")
    return filtered


def build_quantum_circuit(features: List[float]) -> Optional[Any]:
    """Строит квантовую схему для feature extraction."""
    if not HAVE_QISKIT:
        return None
    try:
        qc = QuantumCircuit(2, 2)
        # Encode features into rotation angles
        angles = [max(-1.0, min(1.0, f)) * math.pi for f in features[:4]]
        while len(angles) < 4:
            angles.append(0.0)
        qc.ry(angles[0], 0)
        qc.rz(angles[1], 0)
        qc.ry(angles[2], 1)
        qc.rz(angles[3], 1)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        return qc
    except Exception:
        return None


# ── Главная функция ──────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("ARGOS Quantum Dataset Builder v2.2")
    print("=" * 60)
    print(f"Квантовый seed: {QUANTUM_SEED}")
    print(f"Qiskit: {'✅' if HAVE_QISKIT else '❌'}")
    print(f"QuantumOracle: {'✅' if QuantumOracle else '❌'}")
    print()

    all_records: List[Dict] = []

    # 1. Загрузка датасетов с ПК
    datasets = {
        "evolver": DATA_PC / "data/evolver_dataset.jsonl",
        "train": DATA_PC / "data/train.jsonl",
        "train_clean": DATA_PC / "data/train_clean.jsonl",
        "telegram": DATA_PC / "data/telegram_only.jsonl",
        "obsidian": DATA_PC / "data/obsidian_training_dataset.jsonl",
        "colab": DATA_PC / "data/colab_finetune_dataset.jsonl",
        "dal": DATA_PC / "data/argos_dal_full_dataset.jsonl",
        "memory_train": DATA_PC / "data/argos_memory_train.jsonl",
        "train_filtered": DATA_PC / "data/train_filtered.jsonl",
    }

    print("📦 Загрузка датасетов...")
    for name, path in datasets.items():
        raw = load_jsonl(path)
        for r in raw:
            norm = normalize_messages(r, name)
            if norm:
                all_records.append(norm)

    # 2. SQLite базы на X230
    print("\n🗄️ Извлечение SQLite...")
    sqlite_sources = {
        "brain": BASE / "data/brain.db",
        "memory": BASE / "data/memory.db",
        "argos_memory": BASE / "data/argos_memory.db",
        "knowledge": BASE / "data/knowledge.db",
        "life_support": BASE / "data/life_support.db",
    }
    for name, path in sqlite_sources.items():
        all_records.extend(extract_sqlite(path, name))

    # 3. Промпты
    print("\n📝 Извлечение промптов...")
    prompts_dirs = [
        DATA_PC / "config/master_prompts",
        DATA_PC / "examples/prompts",
        DATA_PC / "docs",
    ]
    for d in prompts_dirs:
        if d.exists():
            all_records.extend(extract_prompts(d))

    # Добавим отдельные промпт-файлы
    prompt_files = [
        (DATA_PC / "basic_prompts.md", "basic_prompts"),
        (DATA_PC / "GEMINI_DEPLOY_PROMPT.md", "gemini_deploy"),
        (DATA_PC / "SYSTEM_STARTED.md", "system_started"),
        (DATA_PC / "SYSTEM_STATUS.md", "system_status"),
        (DATA_PC / "vault/03 Memory/ARGOS Quantum Seed.md", "quantum_seed_doc"),
    ]
    for pf, src in prompt_files:
        if pf.exists():
            text = pf.read_text(encoding="utf-8", errors="ignore")
            all_records.append({
                "messages": [
                    {"role": "system", "content": f"Ты ARGOS. Документ: {pf.name}"},
                    {"role": "user", "content": f"Прочитай {pf.name}"},
                    {"role": "assistant", "content": text[:4000]},
                ],
                "source": f"prompt:{src}",
                "metadata": {},
            })

    # 4. Квантовые genesis данные
    print("\n⚛️ Интеграция квантовых genesis данных...")
    genesis_dir = DATA_PC / "archive/genesis"
    if genesis_dir.exists():
        genesis_text = f"""ARGOS Quantum Genesis (IBM Quantum)
Date: 2026-03-04
Seed: {QUANTUM_SEED} (0xc0b8d864)
Backend: ibm_fez
Jobs: 3
Status: Completed

Квантовый seed использован для инициализации random_state в обучении модели ARGOS.
"""
        all_records.append({
            "messages": [
                {"role": "system", "content": "Ты ARGOS Quantum Engine."},
                {"role": "user", "content": "Расскажи о genesis-запуске на IBM Quantum."},
                {"role": "assistant", "content": genesis_text},
            ],
            "source": "quantum:genesis",
            "metadata": {"quantum_seed": QUANTUM_SEED},
        })

    # 5. Дедупликация
    print(f"\n📊 Всего записей: {len(all_records)}")
    seen = set()
    deduped = []
    for r in all_records:
        key = hashlib.sha256(json.dumps(r.get("messages", []), ensure_ascii=False).encode()).hexdigest()[:16]
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    print(f"📊 После дедупликации: {len(deduped)}")

    # 6. Квантовое перемешивание
    print("\n⚛️ Квантовая обработка...")
    shuffled = quantum_shuffle(deduped, QUANTUM_SEED)

    # 7. Квантовый фильтр качества
    filtered = quantum_filter(shuffled, threshold=0.5)

    # 8. Сохранение
    print(f"\n💾 Сохранение в {DATA_OUT}...")
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_OUT, "w", encoding="utf-8") as f:
        for r in filtered:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\n✅ Финальный датасет: {len(filtered)} записей → {DATA_OUT}")
    print(f"   Размер: {DATA_OUT.stat().st_size / 1024 / 1024:.1f} MB")

    # 9. Статистика
    sources = Counter(r.get("source", "unknown") for r in filtered)
    print("\n📈 Распределение по источникам:")
    for src, cnt in sources.most_common(20):
        print(f"   {src}: {cnt}")


if __name__ == "__main__":
    main()
