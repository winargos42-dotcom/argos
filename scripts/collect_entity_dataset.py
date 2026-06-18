"""
Собирает мысли сущностей из Obsidian в датасет для дообучения argos-v1.
Формат: JSONL с парами вопрос-ответ от каждой сущности.
"""
import json, os
from pathlib import Path
from datetime import datetime

VAULT = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/entities")
OUTPUT = Path("/home/ava/Projects/argoss/data/entity_dataset.jsonl")

def collect():
    dataset = []
    ts = datetime.now().strftime("%Y-%m-%d")
    
    # Читаем файлы памяти каждой сущности
    for entity_file in (VAULT / "memory").glob("*.md"):
        entity = entity_file.stem
        content = entity_file.read_text(encoding='utf-8')
        
        # Парсим мысли (секции ## TIMESTAMP)
        import re
        sections = re.split(r'## \d{4}-\d{2}-\d{2} \d{2}:\d{2}', content)
        
        for thought in sections[1:]:  # Пропускаем заголовок
            thought = thought.strip()
            if len(thought) > 50:
                dataset.append({
                    "entity": entity,
                    "date": ts,
                    "thought": thought[:500],
                    "source": "obsidian_memory",
                    "messages": [
                        {"role": "system", "content": f"Ты {entity}, AI-сущность ARGOS."},
                        {"role": "assistant", "content": thought}
                    ]
                })
    
    # Читаем коллективные дискуссии
    collective = VAULT / "council" / "COLLECTIVE.md"
    if collective.exists():
        coll_content = collective.read_text(encoding='utf-8')
        import re
        cycles = re.findall(r'## (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) — Цикл эволюции\n([\s\S]+?)(?=\n## |$)', coll_content)
        for ts_cycle, content in cycles:
            dataset.append({
                "entity": "collective",
                "date": ts_cycle[:10],
                "thought": content.strip()[:600],
                "source": "collective_council",
                "messages": [
                    {"role": "system", "content": "Ты ARGOS, коллективное сознание."},
                    {"role": "assistant", "content": content.strip()}
                ]
            })
    
    # Сохраняем
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"✅ Датасет: {len(dataset)} примеров → {OUTPUT}")
    return len(dataset)

if __name__ == "__main__":
    n = collect()
    print(f"Готово: {n} примеров для дообучения argos-v1")
