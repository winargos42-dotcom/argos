#!/usr/bin/env python3
"""
ARGOS Dataset Collector
Собирает данные для обучения модели ARGOS v2.
Формат: OpenAI messages (system, user, assistant)
Источники: HA history, MQTT logs, shell commands, code changes, Obsidian notes,
           Entity thoughts, autonomous brain decisions, evolution history.

Запуск: python3 data_collector.py [--interval 600]
"""

import os
import sys
import json
import time
import sqlite3
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# === CONFIG ===
PROJECT_DIR = Path("/home/ava/Projects/argoss")
DATASET_DIR = Path("/home/ava/argos-dataset")
OBSIDIAN_DIR = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared")
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjMWIwZDgxNzdkNDY0NGRjOWM4YmI4OGZiM2VkOGRjZSIsImlhdCI6MTc3NzkyMDY5MiwiZXhwIjoyMDkzMjgwNjkyfQ.nV0ps3wDPz4NAiqwKCyyTLcwK-oxUdvg2ohIG4p6Ozs"
HA_URL = "http://localhost:8123"

# Ensure dataset dirs exist
for subdir in ["conversations", "observations", "commands", "code_changes",
               "thoughts", "ha_states", "mqtt_logs", "obsidian_notes", "reports", "raw"]:
    (DATASET_DIR / subdir).mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def save_jsonl(path: Path, records: list, append: bool = True):
    mode = "a" if append else "w"
    with open(path, mode, encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def dedup_records(records: list, key_func) -> list:
    seen = set()
    out = []
    for r in records:
        k = key_func(r)
        if k not in seen:
            seen.add(k)
            out.append(r)
    return out


# === 1. COLLECT HA STATES ===
def collect_ha_states():
    """Собирает текущие состояния HA entities."""
    try:
        import requests
        r = requests.get(
            f"{HA_URL}/api/states",
            headers={"Authorization": f"Bearer {HA_TOKEN}"},
            timeout=30
        )
        r.raise_for_status()
        states = r.json()
        record = {
            "ts": now_iso(),
            "type": "ha_states",
            "count": len(states),
            "unavailable": sum(1 for s in states if s.get("state") == "unavailable"),
            "states": [{"entity_id": s["entity_id"], "state": s["state"],
                        "last_changed": s.get("last_changed")} for s in states[:500]]
        }
        save_jsonl(DATASET_DIR / "ha_states" / f"{datetime.now():%Y-%m-%d}.jsonl", [record])
        return len(states)
    except Exception as e:
        print(f"[HA states] Error: {e}")
        return 0


# === 2. COLLECT OBSIDIAN NOTES ===
def collect_obsidian_notes():
    """Собирает Obsidian заметки из SharedMemory."""
    records = []
    for fpath in OBSIDIAN_DIR.glob("*.md"):
        try:
            content = fpath.read_text(encoding="utf-8")
            record = {
                "ts": now_iso(),
                "type": "obsidian_note",
                "file": fpath.name,
                "content": content[:5000],  # truncate large files
                "size": len(content)
            }
            records.append(record)
        except Exception as e:
            print(f"[Obsidian] Error reading {fpath}: {e}")
    if records:
        save_jsonl(DATASET_DIR / "obsidian_notes" / f"{datetime.now():%Y-%m-%d}.jsonl", records)
    return len(records)


# === 3. COLLECT ENTITY THOUGHTS (MQTT) ===
def collect_mqtt_thoughts():
    """Собирает мысли Entity Bus из MQTT topics."""
    try:
        result = subprocess.run(
            ["mosquitto_sub", "-t", "argos/consciousness/#", "-C", "50", "--keepalive", "30"],
            capture_output=True, text=True, timeout=60
        )
        records = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            try:
                data = json.loads(line)
                record = {
                    "ts": now_iso(),
                    "type": "entity_thought",
                    "source": data.get("entity", "unknown"),
                    "thought": data.get("thought", line)[:2000],
                    "raw": data
                }
                records.append(record)
            except json.JSONDecodeError:
                record = {
                    "ts": now_iso(),
                    "type": "entity_thought_raw",
                    "thought": line[:2000]
                }
                records.append(record)
        if records:
            save_jsonl(DATASET_DIR / "thoughts" / f"{datetime.now():%Y-%m-%d}.jsonl", records)
        return len(records)
    except Exception as e:
        print(f"[MQTT thoughts] Error: {e}")
        return 0


# === 4. COLLECT CODE CHANGES ===
def collect_code_changes():
    """Собирает git diff и commit messages из ARGOS репозитория."""
    try:
        os.chdir(PROJECT_DIR)
        # Last 10 commits
        log = subprocess.run(
            ["git", "log", "--pretty=format:%H|%ci|%s", "-10"],
            capture_output=True, text=True, timeout=10
        )
        records = []
        for line in log.stdout.strip().split("\n"):
            if "|" in line:
                hsh, ts, msg = line.split("|", 2)
                record = {
                    "ts": ts,
                    "type": "code_change",
                    "hash": hsh,
                    "message": msg,
                    "files_changed": []
                }
                # Get files for this commit
                files = subprocess.run(
                    ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", hsh],
                    capture_output=True, text=True, timeout=10
                )
                record["files_changed"] = files.stdout.strip().split("\n")
                records.append(record)
        if records:
            save_jsonl(DATASET_DIR / "code_changes" / f"{datetime.now():%Y-%m-%d}.jsonl", records)
        return len(records)
    except Exception as e:
        print(f"[Code changes] Error: {e}")
        return 0


# === 5. COLLECT AUTONOMOUS BRAIN OBSERVATIONS ===
def collect_brain_observations():
    """Собирает данные из autonomous_brain логов."""
    log_path = PROJECT_DIR / "logs" / "autonomous_brain.log"
    if not log_path.exists():
        return 0
    try:
        content = log_path.read_text(encoding="utf-8")
        # Parse last N lines as observations
        lines = content.strip().split("\n")[-500:]
        records = []
        for line in lines:
            if "Observation" in line or "Decision" in line or "Action" in line:
                records.append({
                    "ts": now_iso(),
                    "type": "brain_observation",
                    "log_line": line[:2000]
                })
        if records:
            save_jsonl(DATASET_DIR / "observations" / f"{datetime.now():%Y-%m-%d}.jsonl", records)
        return len(records)
    except Exception as e:
        print(f"[Brain observations] Error: {e}")
        return 0


# === 6. COLLECT EVOLUTION HISTORY ===
def collect_evolution_history():
    """Собирает историю эволюции из evolution_history.jsonl."""
    evo_path = PROJECT_DIR / "data" / "evolution_history.jsonl"
    if not evo_path.exists():
        return 0
    try:
        records = load_jsonl(evo_path)
        # Only append new records (check last timestamp)
        out_path = DATASET_DIR / "raw" / "evolution_history.jsonl"
        existing = load_jsonl(out_path)
        existing_ts = {r.get("ts", "") for r in existing}
        new_records = [r for r in records if r.get("ts", "") not in existing_ts]
        if new_records:
            save_jsonl(out_path, new_records)
        return len(new_records)
    except Exception as e:
        print(f"[Evolution history] Error: {e}")
        return 0


# === 7. BUILD TRAINING DATASET ===
def build_training_dataset():
    """
    Собирает финальный датасет в формате OpenAI messages из всех источников.
    Цель: обучить модель на поведении ARGOS.
    """
    all_records = []

    # From existing argos_final_v2.jsonl
    final_path = PROJECT_DIR / "data" / "argos_final_v2.jsonl"
    if final_path.exists():
        all_records.extend(load_jsonl(final_path))

    # From entity consciousness dataset
    conc_path = PROJECT_DIR / "data" / "argos_consciousness_dataset.jsonl"
    if conc_path.exists():
        for rec in load_jsonl(conc_path):
            if "messages" in rec:
                all_records.append(rec)

    # From evolver dataset (convert to messages format)
    evo_path = PROJECT_DIR / "data" / "evolver_dataset.jsonl"
    if evo_path.exists():
        for rec in load_jsonl(evo_path):
            user = rec.get("user", "")
            answer = rec.get("answer", "")
            context = rec.get("context", "")
            if user and answer:
                all_records.append({
                    "messages": [
                        {"role": "system", "content": context or "Ты — ARGOS, автономная ИИ-система."},
                        {"role": "user", "content": user},
                        {"role": "assistant", "content": answer}
                    ],
                    "ts": rec.get("ts", now_iso()),
                    "source": "evolver"
                })

    # Deduplicate by hash of messages
    def msg_hash(r):
        msgs = r.get("messages", [])
        return hashlib.sha256(json.dumps(msgs, ensure_ascii=False).encode()).hexdigest()[:16]

    all_records = dedup_records(all_records, msg_hash)

    # Save combined dataset
    combined_path = DATASET_DIR / "raw" / "argos_combined_training.jsonl"
    save_jsonl(combined_path, all_records, append=False)

    # Save train/val split (90/10)
    split_idx = int(len(all_records) * 0.9)
    train = all_records[:split_idx]
    val = all_records[split_idx:]

    save_jsonl(DATASET_DIR / "argos_train.jsonl", train, append=False)
    save_jsonl(DATASET_DIR / "argos_val.jsonl", val, append=False)

    return len(all_records), len(train), len(val)


# === MAIN LOOP ===
def main():
    interval = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--interval" else 600
    print(f"[ARGOS Data Collector] Starting with interval={interval}s")
    print(f"[ARGOS Data Collector] Dataset dir: {DATASET_DIR}")

    while True:
        cycle_start = time.time()
        print(f"\n--- {now_iso()} ---")

        # Collect raw data
        ha_count = collect_ha_states()
        obs_count = collect_obsidian_notes()
        mqtt_count = collect_mqtt_thoughts()
        code_count = collect_code_changes()
        brain_count = collect_brain_observations()
        evo_count = collect_evolution_history()

        print(f"  HA states: {ha_count}")
        print(f"  Obsidian notes: {obs_count}")
        print(f"  MQTT thoughts: {mqtt_count}")
        print(f"  Code changes: {code_count}")
        print(f"  Brain observations: {brain_count}")
        print(f"  Evolution history: {evo_count}")

        # Build training dataset (once per hour - check minutes)
        if datetime.now().minute < 5:
            total, train, val = build_training_dataset()
            print(f"  Training dataset: {total} total ({train} train / {val} val)")

        # Sleep
        elapsed = time.time() - cycle_start
        sleep_time = max(0, interval - elapsed)
        print(f"  Sleep {sleep_time:.1f}s")
        time.sleep(sleep_time)


if __name__ == "__main__":
    # Allow single run mode
    if "--once" in sys.argv:
        print("[ARGOS Data Collector] Single run mode")
        collect_ha_states()
        collect_obsidian_notes()
        collect_mqtt_thoughts()
        collect_code_changes()
        collect_brain_observations()
        collect_evolution_history()
        total, train, val = build_training_dataset()
        print(f"Dataset built: {total} total ({train} train / {val} val)")
        print(f"Files saved to: {DATASET_DIR}")
    else:
        main()
