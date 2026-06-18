#!/usr/bin/env python3
"""
ARGOS Dataset Builder — создаёт датасет из чатов и сознания.
Источники:
1. Entity Council группа (диалоги сущностей)
2. JOURNAL.md (поток сознания)
3. Brain events
4. Obsidian заметки
Загружает на HF: AvaSiG/argos-dataset
"""
import asyncio, json, re, sys, os, time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/home/ava/Projects/argoss')
sys.path.insert(0, '/home/ava/Projects/argoss/.venv/lib/python3.14/site-packages')

API_ID   = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSIONS = Path("/home/ava/Projects/argoss/data/sessions")
DATA_DIR = Path("/home/ava/Projects/argoss/data")
HF_TOKEN = "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"
HF_REPO  = "AvaSiG/argos-dataset"
COUNCIL_ID = -5129226282  # Entity Council группа
JOURNAL  = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/JOURNAL.md")
OBSIDIAN = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared")

# ── Форматирование примеров ───────────────────────────────────────────────

def make_example(instruction, input_text, output, source="argos"):
    return {
        "instruction": instruction,
        "input": input_text,
        "output": output,
        "source": source,
        "ts": datetime.now().isoformat(),
    }

# ── Источник 1: Entity Council чаты ──────────────────────────────────────

async def extract_council_chats(client, limit=500):
    """Извлекаем диалоги из Entity Council."""
    examples = []
    try:
        msgs = await client.get_messages(COUNCIL_ID, limit=limit)
        msgs = list(reversed(msgs))

        i = 0
        while i < len(msgs) - 1:
            m1 = msgs[i]
            m2 = msgs[i+1]

            t1 = m1.text or ""
            t2 = m2.text or ""

            if not t1 or not t2 or len(t1) < 20 or len(t2) < 20:
                i += 1
                continue

            # Диалог как Q&A
            examples.append(make_example(
                instruction="Ты ARGOS — AI агент. Продолжи диалог сущностей.",
                input_text=t1[:500],
                output=t2[:500],
                source="entity_council"
            ))

            # Мысль как самостоятельный пример
            if "ARGOS" in t1 or "система" in t1.lower() or "Клод" in t1:
                examples.append(make_example(
                    instruction="Ты ARGOS. Выскажи мысль о состоянии системы.",
                    input_text="",
                    output=t1[:500],
                    source="entity_thought"
                ))

            i += 2

        print(f"[Council] {len(examples)} примеров из {len(msgs)} сообщений")
    except Exception as e:
        print(f"[Council ERR] {e}")
    return examples

# ── Источник 2: JOURNAL.md ────────────────────────────────────────────────

def extract_journal():
    """Извлекаем из JOURNAL.md потока сознания."""
    examples = []
    try:
        text = JOURNAL.read_text(encoding="utf-8", errors="replace")
        sections = re.split(r'\n## ', text)

        for section in sections:
            if not section.strip():
                continue

            # Секции с диалогом
            if "Поток сознания" in section or "Диалог" in section:
                parts = section.split("\n", 1)
                header = parts[0].strip()
                body = parts[1] if len(parts) > 1 else ""

                # Извлекаем реплики
                lines = [l.strip() for l in body.splitlines() if l.strip() and not l.startswith("#")]
                for j, line in enumerate(lines):
                    if "**" in line and ":" in line:
                        name = re.search(r'\*\*(.+?)\*\*:', line)
                        thought = re.sub(r'\*\*.*?\*\*:\s*', '', line)
                        if name and thought and len(thought) > 20:
                            examples.append(make_example(
                                instruction=f"Ты {name.group(1)} — сущность ARGOS. Выскажи мысль.",
                                input_text=header,
                                output=thought[:400],
                                source="journal_consciousness"
                            ))

            # Секции с отчётами/задачами
            elif any(w in section.lower() for w in ["исправлено", "задача", "ошибка", "решение"]):
                examples.append(make_example(
                    instruction="Ты ARGOS. Опиши выполненную задачу и её решение.",
                    input_text="",
                    output=section[:500],
                    source="journal_task"
                ))

        print(f"[Journal] {len(examples)} примеров")
    except Exception as e:
        print(f"[Journal ERR] {e}")
    return examples

# ── Источник 3: Brain events ──────────────────────────────────────────────

def extract_brain_events():
    """Извлекаем события из Brain API."""
    import urllib.request
    examples = []
    try:
        r = urllib.request.urlopen("http://192.168.1.53:5001/brain/events", timeout=5)
        events = json.loads(r.read()).get("events", [])

        for e in events:
            if e.get("event") == "observe" and e.get("data"):
                d = e["data"]
                thought = d.get("thought") or d.get("obs") or str(d)[:200]
                if len(thought) > 30:
                    examples.append(make_example(
                        instruction="Ты ARGOS-субъект. Что видишь и думаешь?",
                        input_text=f"node: {e.get('node_id','?')}",
                        output=thought[:400],
                        source="brain_observe"
                    ))

            elif e.get("event") == "dialogue":
                d = e["data"]
                if d:
                    for name, thought in d.items():
                        if name not in ("topic","ts") and isinstance(thought,str) and len(thought) > 20:
                            examples.append(make_example(
                                instruction=f"Ты {name}. Выскажи мысль на тему: {d.get('topic','')}",
                                input_text="",
                                output=thought[:400],
                                source="brain_dialogue"
                            ))

        print(f"[Brain] {len(examples)} примеров")
    except Exception as e:
        print(f"[Brain ERR] {e}")
    return examples

# ── Источник 4: Obsidian заметки ──────────────────────────────────────────

def extract_obsidian():
    """Извлекаем из Obsidian SharedMemory."""
    examples = []
    try:
        for md_file in OBSIDIAN.glob("*.md"):
            text = md_file.read_text(encoding="utf-8", errors="replace")
            name = md_file.stem

            # WORKING.md — задачи и решения
            if "WORKING" in name:
                sections = text.split("---")
                for s in sections:
                    if len(s) > 100:
                        examples.append(make_example(
                            instruction="Ты ARGOS. Опиши текущие задачи и их статус.",
                            input_text="",
                            output=s[:500].strip(),
                            source="obsidian_working"
                        ))

            # STATUS.md — статус системы
            elif "STATUS" in name:
                examples.append(make_example(
                    instruction="Ты ARGOS. Опиши текущий статус системы из 7 машин.",
                    input_text="",
                    output=text[:600].strip(),
                    source="obsidian_status"
                ))

        print(f"[Obsidian] {len(examples)} примеров")
    except Exception as e:
        print(f"[Obsidian ERR] {e}")
    return examples

# ── Загрузка на HuggingFace ───────────────────────────────────────────────

def upload_to_hf(examples, incremental=True):
    """Загружаем датасет на HF."""
    from huggingface_hub import HfApi
    api = HfApi(token=HF_TOKEN)

    # Загружаем существующий датасет
    existing = []
    existing_file = DATA_DIR / "argos_final_v2.jsonl"
    if existing_file.exists() and incremental:
        with open(existing_file) as f:
            for line in f:
                try:
                    existing.append(json.loads(line))
                except:
                    pass
        print(f"[HF] Существующих примеров: {len(existing)}")

    # Дедупликация по output
    existing_outputs = {e.get("output","")[:100] for e in existing}
    new_examples = [e for e in examples if e.get("output","")[:100] not in existing_outputs]
    print(f"[HF] Новых примеров: {len(new_examples)}")

    all_examples = existing + new_examples

    # Сохраняем локально
    output_file = DATA_DIR / "argos_full_dataset.jsonl"
    with open(output_file, "w") as f:
        for e in all_examples:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"[HF] Итого: {len(all_examples)} примеров → {output_file}")

    # Загружаем на HF
    try:
        api.upload_file(
            path_or_fileobj=str(output_file),
            path_in_repo="train.jsonl",
            repo_id=HF_REPO,
            repo_type="dataset",
            commit_message=f"Update dataset: +{len(new_examples)} examples from consciousness/chats [{datetime.now().strftime('%Y-%m-%d')}]"
        )
        print(f"[HF] ✅ Загружено на {HF_REPO}")
        return len(all_examples), len(new_examples)
    except Exception as e:
        print(f"[HF ERR] {e}")
        return len(all_examples), 0

# ── MAIN ──────────────────────────────────────────────────────────────────

async def main():
    from telethon import TelegramClient as TC
    print("=== ARGOS Dataset Builder ===")
    print(f"Target: {HF_REPO}")

    client = TC(str(SESSIONS / "ava_main"), API_ID, API_HASH)
    await client.start()

    all_examples = []

    # 1. Entity Council чаты
    print("\n[1] Entity Council диалоги...")
    all_examples += await extract_council_chats(client, limit=300)

    # 2. Journal / поток сознания
    print("\n[2] JOURNAL.md...")
    all_examples += extract_journal()

    # 3. Brain events
    print("\n[3] Brain events...")
    all_examples += extract_brain_events()

    # 4. Obsidian
    print("\n[4] Obsidian заметки...")
    all_examples += extract_obsidian()

    print(f"\nВсего собрано: {len(all_examples)} примеров")

    # Загружаем
    print("\n[5] Загружаю на HuggingFace...")
    total, new = upload_to_hf(all_examples)
    print(f"\n✅ Датасет обновлён: {total} примеров (+{new} новых)")
    print(f"   HF: https://huggingface.co/datasets/{HF_REPO}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
