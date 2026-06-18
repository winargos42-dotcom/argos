#!/usr/bin/env python3
"""
ARGOS Auto-Retrain: каждые 12 часов собирает мысли сущностей → fine-tune argos-v1
"""
import os, json, time, subprocess, glob
from pathlib import Path
from datetime import datetime

VAULT = "/home/ava/Documents/MyObsidianVault/SharedMemory/entities"
OUTPUT_DIR = "/home/ava/Projects/argoss/data/retrain"
HF_REPO = "AvaSiG/argos-dataset"
HF_TOKEN = "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"
INTERVAL = 12 * 3600  # 12 часов

def collect_thoughts():
    """Собираем мысли из Obsidian файлов"""
    examples = []
    memory_dir = Path(VAULT) / "memory"
    
    for md_file in sorted(memory_dir.glob("*.md")):
        entity = md_file.stem
        content = md_file.read_text(errors="replace")
        
        # Парсим мысли из секций ## YYYY-MM-DD HH:MM
        import re
        sections = re.split(r'## \d{4}-\d{2}-\d{2}', content)
        for section in sections[1:]:
            text = section.strip()[:500]
            if len(text) > 50:
                examples.append({
                    "messages": [
                        {"role": "user", "content": f"Ты {entity} в системе ARGOS. Что ты думаешь?"},
                        {"role": "assistant", "content": text}
                    ]
                })
    
    # COLLECTIVE.md
    collective = Path(VAULT) / "council" / "COLLECTIVE.md"
    if collective.exists():
        ctext = collective.read_text(errors="replace")
        sections = ctext.split("\n## ")[1:]
        for s in sections[:20]:
            lines = s.strip().split("\n", 1)
            if len(lines) >= 2:
                examples.append({
                    "messages": [
                        {"role": "user", "content": "Что происходит в системе ARGOS?"},
                        {"role": "assistant", "content": lines[1][:300]}
                    ]
                })
    
    return examples

def save_dataset(examples, ts):
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    out_file = f"{OUTPUT_DIR}/consciousness_{ts}.jsonl"
    with open(out_file, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"Dataset: {len(examples)} примеров → {out_file}")
    return out_file

def upload_to_hf(dataset_file):
    """Загружаем на HuggingFace"""
    try:
        result = subprocess.run([
            "/home/ava/Projects/argoss/.venv/bin/python3", "-c",
            f"""
from huggingface_hub import HfApi
import os
api = HfApi(token="{HF_TOKEN}")
api.upload_file(
    path_or_fileobj="{dataset_file}",
    path_in_repo="consciousness/{os.path.basename(dataset_file)}",
    repo_id="{HF_REPO}",
    repo_type="dataset"
)
print("HF upload OK")
"""
        ], capture_output=True, text=True, timeout=60)
        print(result.stdout.strip())
        if result.returncode != 0:
            print(f"HF error: {result.stderr[:100]}")
    except Exception as e:
        print(f"HF upload error: {e}")

def main():
    print(f"ARGOS Retrain Scheduler запущен (интервал: 12ч)")
    while True:
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        print(f"\n[{ts}] Сбор мыслей сущностей...")
        
        examples = collect_thoughts()
        print(f"  Собрано: {len(examples)} примеров")
        
        if len(examples) >= 10:
            ds_file = save_dataset(examples, ts)
            upload_to_hf(ds_file)
            print(f"  Dataset загружен на HuggingFace ✅")
        else:
            print(f"  Мало примеров ({len(examples)}), пропускаем")
        
        print(f"  Следующий цикл через 12 часов...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
