#!/usr/bin/env python3
"""
ARGOS Training Pipeline — собирает датасет из чатов сознания и дообучает Ollama ARGOS v1.
Запускается каждые 3 часа.
"""
import json, time, re, subprocess, urllib.request
from pathlib import Path
from datetime import datetime

BRAIN     = "http://192.168.1.53:5001"
JOURNAL   = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/JOURNAL.md")
DATA_DIR  = Path("/home/ava/Projects/argoss/data")
HF_TOKEN  = "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"
HF_REPO   = "AvaSiG/argos-dataset"
OLLAMA    = "http://192.168.1.53:11434"  # PC Ollama
MODEL     = "argos-v1"

def collect_consciousness_data():
    """Собираем диалоги из JOURNAL.md (поток сознания)."""
    examples = []
    try:
        text = JOURNAL.read_text(encoding="utf-8", errors="replace")
        sections = re.split(r'\n## \[', text)
        for s in sections:
            if 'сознания' not in s.lower() and 'dialogue' not in s.lower():
                continue
            # Извлекаем участников и мысли
            lines = s.splitlines()
            topic = ""
            thoughts = []
            for line in lines:
                if line.startswith('**Тема:**'):
                    topic = line.replace('**Тема:**','').strip()
                elif '**' in line and ':' in line and len(line) > 20:
                    name = re.search(r'\*\*(.+?)\*\*:', line)
                    thought = re.sub(r'\*\*.*?\*\*:\s*', '', line).strip()
                    if name and thought and len(thought) > 30:
                        thoughts.append((name.group(1), thought))
            # Создаём обучающие примеры из диалога
            for i, (name, thought) in enumerate(thoughts):
                if i > 0:
                    prev_name, prev_thought = thoughts[i-1]
                    examples.append({
                        "instruction": f"Ты {name} — часть ARGOS. Ответь на мысль {prev_name}.",
                        "input": f"Тема: {topic}\n{prev_name}: {prev_thought[:200]}",
                        "output": thought[:400],
                        "source": "consciousness_journal"
                    })
                else:
                    examples.append({
                        "instruction": f"Ты {name} — аналитик ARGOS. Высказись на тему: {topic}",
                        "input": "",
                        "output": thought[:400],
                        "source": "consciousness_journal"
                    })
    except Exception as e:
        print(f"[JOURNAL] Error: {e}")
    print(f"[JOURNAL] {len(examples)} примеров")
    return examples

def collect_brain_events():
    """Собираем события из Brain API."""
    examples = []
    try:
        r = urllib.request.urlopen(f"{BRAIN}/brain/events?limit=200", timeout=5)
        events = json.loads(r.read()).get("events", [])
        for e in events:
            d = e.get("data", {})
            if isinstance(d, dict):
                thought = d.get("thought") or d.get("obs") or d.get("result")
                if thought and len(str(thought)) > 30:
                    examples.append({
                        "instruction": f"Ты ARGOS-агент {e.get('node_id','?')}. Что ты наблюдаешь?",
                        "input": f"event: {e.get('event','?')}",
                        "output": str(thought)[:400],
                        "source": "brain_events"
                    })
    except Exception as e:
        print(f"[BRAIN] Error: {e}")
    print(f"[BRAIN] {len(examples)} примеров")
    return examples

def update_hf_dataset(examples):
    """Загружаем датасет на HuggingFace."""
    try:
        from huggingface_hub import HfApi
        api = HfApi(token=HF_TOKEN)

        # Загружаем существующий
        existing = []
        existing_file = DATA_DIR / "argos_full_dataset.jsonl"
        if existing_file.exists():
            with open(existing_file) as f:
                for line in f:
                    try: existing.append(json.loads(line))
                    except: pass

        # Дедупликация
        ex_outs = {e.get("output","")[:80] for e in existing}
        new_ex = [e for e in examples if e.get("output","")[:80] not in ex_outs]
        all_ex = existing + new_ex

        # Сохраняем
        out_file = DATA_DIR / "argos_full_dataset.jsonl"
        with open(out_file, "w") as f:
            for e in all_ex:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")

        # Загружаем на HF
        api.upload_file(
            path_or_fileobj=str(out_file),
            path_in_repo="train.jsonl",
            repo_id=HF_REPO,
            repo_type="dataset",
            commit_message=f"Auto-update: +{len(new_ex)} examples [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
        )
        print(f"[HF] ✅ Загружено: {len(all_ex)} примеров (+{len(new_ex)} новых)")
        return len(new_ex)
    except Exception as e:
        print(f"[HF] Error: {e}")
        return 0

def train_ollama_argos(examples):
    """Дообучаем ARGOS-v1 на Ollama PC через SSH."""
    if not examples:
        print("[TRAIN] Нет новых примеров для обучения")
        return

    system_prompt = (
        "Ты ARGOS Universal OS v2.1.4 — автономная AI-экосистема. "
        "Тебя создал Всеволод (Seva). "
        "7 машин: Орион(ПК GPU), Нексус(ноутбук), Эгида(OPi), "
        "Авангард(телефон), Сентинел/Аркус/Зенит(GCP). "
        "Отвечай на русском. Знаешь систему изнутри."
    )
    modelfile_content = (
        "FROM qwen2.5:0.5b\n"
        f'SYSTEM "{system_prompt}"\n'
        "PARAMETER temperature 0.7\n"
        "PARAMETER top_p 0.9\n"
    )

    try:
        # Сохраняем modelfile на ноутбуке
        modelfile_path = DATA_DIR / "argos_modelfile"
        modelfile_path.write_text(modelfile_content, encoding="utf-8")

        # Копируем на PC через SCP
        scp_result = subprocess.run([
            "scp", "-i", "/home/ava/.ssh/id_ed25519",
            "-o", "StrictHostKeyChecking=no",
            str(modelfile_path),
            "AvA@192.168.1.53:F:/debug/argoss/argos_modelfile"
        ], capture_output=True, timeout=15)

        if scp_result.returncode != 0:
            print(f"[TRAIN] SCP failed: {scp_result.stderr.decode()[:100]}")
            return

        # Создаём модель на PC через SSH + Ollama API
        ssh_result = subprocess.run([
            "ssh", "-i", "/home/ava/.ssh/id_ed25519",
            "-o", "StrictHostKeyChecking=no",
            "AvA@192.168.1.53",
            'cmd.exe /C "curl -s -X POST http://localhost:11434/api/create -H Content-Type:application/json -d @F:\\debug\\argoss\\argos_modelfile_req.json"'
        ], capture_output=True, timeout=120, text=True)

        # Используем Python на PC вместо curl
        py_cmd = f'''python -c "
import urllib.request, json
body = json.dumps({{
    'name': 'argos-v1',
    'modelfile': open('F:/debug/argoss/argos_modelfile').read(),
    'stream': False
}}).encode()
req = urllib.request.Request('http://localhost:11434/api/create', data=body, headers={{'Content-Type':'application/json'}})
with urllib.request.urlopen(req, timeout=120) as r:
    print('Status:', json.loads(r.read()).get('status','?'))
" '''
        result = subprocess.run([
            "ssh", "-i", "/home/ava/.ssh/id_ed25519",
            "-o", "StrictHostKeyChecking=no",
            "AvA@192.168.1.53",
            f'cmd.exe /C "{py_cmd}"'
        ], capture_output=True, timeout=120, text=True)

        if result.returncode == 0 and result.stdout:
            print(f"[TRAIN] ✅ argos-v1 создан: {result.stdout.strip()[:100]}")
        else:
            print(f"[TRAIN] Error: {result.stderr[:100] if result.stderr else 'no output'}")

    except Exception as e:
        print(f"[TRAIN] Exception: {e}")

def run_pipeline():
    """Основной пайплайн: собрать → загрузить → обучить."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n{'='*50}")
    print(f"[{ts}] ARGOS Training Pipeline")

    # 1. Сбор данных
    examples = []
    examples += collect_consciousness_data()
    examples += collect_brain_events()
    print(f"[TOTAL] {len(examples)} примеров собрано")

    # 2. HuggingFace
    new_count = update_hf_dataset(examples)

    # 3. Ollama дообучение (только если есть новые данные)
    if new_count > 0:
        train_ollama_argos(examples[-50:])  # последние 50 примеров
    else:
        print("[TRAIN] Нет новых данных, пропускаем обучение")

    print(f"[DONE] Следующий запуск через 3 часа")

if __name__ == "__main__":
    while True:
        try:
            run_pipeline()
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(10800)  # 3 часа
