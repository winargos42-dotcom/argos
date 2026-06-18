"""
Строит датасет из Словаря Даля + объединяет с существующими данными.
Источники: Wikisource, NLTK Russian corpora, существующий argos_final_v2.jsonl
"""
import json, urllib.request, re, os, time
from pathlib import Path

DATA_DIR = Path("/home/ava/Projects/argoss/data")
OUTPUT = DATA_DIR / "argos_dal_dataset.jsonl"

# Словарь Даля - статьи через Wikisource API
def fetch_dal_article(letter: str, limit: int = 30) -> list:
    """Скачиваем статьи словаря Даля с Wikisource."""
    entries = []
    
    url = f"https://ru.wikisource.org/w/api.php?action=query&list=categorymembers&cmtitle=Категория:Толковый_словарь_Даля/{letter}&cmlimit={limit}&format=json"
    
    req = urllib.request.Request(url, headers={"User-Agent": "ARGOS-Bot/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
            pages = d.get("query", {}).get("categorymembers", [])
            
            for page in pages[:10]:
                title = page.get("title", "")
                pageid = page.get("pageid", 0)
                
                # Получаем текст статьи
                content_url = f"https://ru.wikisource.org/w/api.php?action=query&pageids={pageid}&prop=extracts&exintro&format=json"
                req2 = urllib.request.Request(content_url, headers={"User-Agent": "ARGOS-Bot/1.0"})
                try:
                    with urllib.request.urlopen(req2, timeout=8) as r2:
                        d2 = json.loads(r2.read())
                        pages2 = d2.get("query", {}).get("pages", {})
                        for _, page_data in pages2.items():
                            extract = page_data.get("extract", "")
                            # Убираем HTML теги
                            extract = re.sub(r'<[^>]+>', '', extract).strip()
                            if extract and len(extract) > 50:
                                entries.append({
                                    "word": title.split("/")[-1] if "/" in title else title,
                                    "definition": extract[:500]
                                })
                except: pass
                time.sleep(0.3)
    except Exception as e:
        print(f"  Ошибка {letter}: {e}")
    
    return entries

# Генерируем датасет из записей Даля
def create_training_examples(entries: list) -> list:
    """Создаём обучающие примеры из словарных статей."""
    examples = []
    
    templates = [
        # Вопрос-ответ
        lambda w, d: {
            "messages": [
                {"role": "system", "content": "Ты ARGOS — AI-ассистент со знанием русского языка и словаря Даля."},
                {"role": "user", "content": f"Что означает слово '{w}' по Далю?"},
                {"role": "assistant", "content": d}
            ]
        },
        # Толкование
        lambda w, d: {
            "messages": [
                {"role": "system", "content": "Ты ARGOS — знаток русского языка."},
                {"role": "user", "content": f"Объясни слово '{w}'"},
                {"role": "assistant", "content": f"Из словаря Даля: {d}"}
            ]
        },
        # Завершение предложения
        lambda w, d: {
            "messages": [
                {"role": "system", "content": "Ты ARGOS — русскоязычный AI-ассистент."},
                {"role": "user", "content": f"Расскажи о слове '{w}' из живого великорусского языка"},
                {"role": "assistant", "content": d}
            ]
        },
    ]
    
    import random
    for entry in entries:
        if entry["definition"] and len(entry["definition"]) > 30:
            template = random.choice(templates)
            example = template(entry["word"], entry["definition"])
            examples.append(example)
    
    return examples

# Также используем встроенные данные - русские пословицы Даля
POSLOVITSY = [
    ("Без труда не вытащишь и рыбку из пруда", "О необходимости трудиться для достижения цели. Даль собрал тысячи русских пословиц в своём сборнике."),
    ("Не всё коту масленица", "Не вечно длится хорошее время, наступит и будничное, скромное существование."),
    ("Семь раз отмерь — один отрежь", "Прежде чем что-то сделать, нужно хорошо подумать и всё взвесить."),
    ("Слово — не воробей, вылетит — не поймаешь", "Сказанное слово нельзя взять обратно, поэтому говорить нужно обдуманно."),
    ("На вкус и цвет товарищей нет", "У каждого человека свои вкусы и пристрастия."),
    ("Лучше поздно, чем никогда", "Лучше сделать что-то с опозданием, чем не сделать совсем."),
    ("Терпение и труд всё перетрут", "При усердии и настойчивости можно преодолеть любые трудности."),
    ("Друг познаётся в беде", "Настоящая дружба проверяется в трудных обстоятельствах."),
    ("Не имей сто рублей, а имей сто друзей", "Дружба дороже денег и материальных ценностей."),
    ("Один в поле не воин", "Одному человеку трудно справиться с серьёзным делом без поддержки."),
    ("Любишь кататься — люби и саночки возить", "За удовольствие нужно платить трудом."),
    ("Что посеешь, то и пожнёшь", "Каков твой поступок, таков будет и результат."),
    ("Своя рубашка ближе к телу", "Каждый прежде всего заботится о своих интересах."),
    ("В гостях хорошо, а дома лучше", "Нет ничего лучше родного дома."),
    ("Утро вечера мудренее", "Многие вопросы лучше решать после отдыха, на свежую голову."),
]

def build_poslovitsy_examples():
    examples = []
    for poslovitsa, tolkovanie in POSLOVITSY:
        # Разные форматы
        examples.append({"messages": [
            {"role": "system", "content": "Ты ARGOS — знаток русских пословиц и Словаря Даля."},
            {"role": "user", "content": f"Объясни пословицу: '{poslovitsa}'"},
            {"role": "assistant", "content": tolkovanie}
        ]})
        examples.append({"messages": [
            {"role": "system", "content": "Ты ARGOS — русскоязычный AI-ассистент."},
            {"role": "user", "content": f"Что означает '{poslovitsa}'?"},
            {"role": "assistant", "content": f"Эта пословица из сборника Даля означает: {tolkovanie}"}
        ]})
        examples.append({"messages": [
            {"role": "system", "content": "Ты ARGOS."},
            {"role": "user", "content": "Приведи пример русской пословицы с объяснением"},
            {"role": "assistant", "content": f"'{poslovitsa}' — {tolkovanie}"}
        ]})
    return examples

print("📚 Строим датасет Словаря Даля...")

# 1. Пословицы (быстро, без сети)
all_examples = build_poslovitsy_examples()
print(f"  Пословицы: {len(all_examples)} примеров")

# 2. Скачиваем статьи из Wikisource
print("  Скачиваю статьи Даля из Wikisource...")
for letter in ["А", "Б", "В", "Г", "Д"]:
    entries = fetch_dal_article(letter, limit=15)
    if entries:
        examples = create_training_examples(entries)
        all_examples.extend(examples)
        print(f"  Буква {letter}: {len(entries)} статей → {len(examples)} примеров")
    time.sleep(0.5)

# 3. Объединяем с существующим датасетом
print(f"\n  Существующий argos_final_v2.jsonl...")
existing = []
final_v2 = DATA_DIR / "argos_final_v2.jsonl"
if final_v2.exists():
    with open(final_v2) as f:
        for line in f:
            try: existing.append(json.loads(line))
            except: pass
    print(f"  Загружено {len(existing)} примеров из final_v2")

# 4. Объединяем всё
combined = existing + all_examples

# Перемешиваем
import random
random.shuffle(combined)

# Сохраняем
with open(OUTPUT, "w", encoding="utf-8") as f:
    for ex in combined:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print(f"\n✅ Датасет создан: {OUTPUT}")
print(f"   Всего примеров: {len(combined)}")
print(f"   Из Даля: {len(all_examples)}")
print(f"   Из existing: {len(existing)}")
