#!/usr/bin/env python3
"""
MemPalace Sync — автоматическая синхронизация всех сущностей в palace.
Запускается на Нексусе каждые 30 мин.
Собирает: Entity Council чаты, Journal, Brain events, память агентов.
Отправляет на Орион (palace_search.py :7890).
"""
import asyncio, json, time, re, sys, urllib.request
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, '/home/ava/Projects/argoss')

PALACE_API = "http://192.168.1.53:7890"  # MemPalace Search на Орионе
BRAIN      = "http://192.168.1.53:5001"
JOURNAL    = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/JOURNAL.md")
# Fallback paths
JOURNAL_PATHS = [
    JOURNAL,
    Path("/home/ava/Documents/JOURNAL.md"),
    Path("/tmp/consciousness.log"),
]
SESSIONS   = Path("/home/ava/Projects/argoss/data/sessions")
API_ID     = 2040
API_HASH   = "b18441a1ff607e10a989891a5462e627"

def post_palace(docs):
    """Отправляем документы в palace."""
    try:
        b = json.dumps({"docs": docs}, ensure_ascii=False).encode()
        req = urllib.request.Request(f"{PALACE_API}/add", data=b,
            headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

def sync_journal():
    """Собираем последние записи из JOURNAL.md."""
    docs = []
    try:
        text = ""
        for jp in JOURNAL_PATHS:
            if jp.exists():
                text = jp.read_text(encoding="utf-8", errors="replace")
                break
        if not text:
            return []
        sections = re.split(r'\n## \[', text)
        for i, s in enumerate(sections[-20:]):  # Последние 20 записей
            if len(s) < 50:
                continue
            ts = s[:25].strip()
            # Извлекаем мысли
            thoughts = re.findall(r'\*\*([^*]+)\*\*:\s*([^\n*]{30,300})', s)
            for entity, thought in thoughts[:5]:
                docs.append({
                    "id": f"journal_{hash(thought[:50]) % 999999:06d}",
                    "text": f"[{ts}] {entity}: {thought}",
                    "meta": {"wing":"consciousness","room":"journal","entity":entity[:30],"ts":ts}
                })
    except Exception as e:
        print(f"[Journal] {e}")
    return docs

def sync_brain_events():
    """Собираем события из Brain API."""
    docs = []
    try:
        r = urllib.request.urlopen(f"{BRAIN}/brain/events?limit=100", timeout=5)
        events = json.loads(r.read()).get("events", [])
        for e in events:
            d = e.get("data", {})
            if not isinstance(d, dict):
                continue
            text = d.get("thought") or d.get("obs") or d.get("result")
            if text and len(str(text)) > 30:
                docs.append({
                    "id": f"event_{e.get('node_id','?')}_{int(e.get('ts',time.time())) % 999999:06d}",
                    "text": f"[{e.get('node_id','?')}] {e.get('event','?')}: {str(text)[:400]}",
                    "meta": {"wing":"events","room":e.get("event","?"),"node":e.get("node_id","?")}
                })
    except Exception as e:
        print(f"[Brain events] {e}")
    return docs

async def sync_entity_council():
    """Собираем диалоги из Entity Council."""
    docs = []
    try:
        from telethon import TelegramClient
        c = TelegramClient(str(SESSIONS/"ava_main"), API_ID, API_HASH)
        await c.start()

        cutoff = datetime.now() - timedelta(hours=6)  # Последние 6 часов
        msgs = await c.get_messages(-5129226282, limit=100)

        for i, m in enumerate(msgs):
            if not m.text or len(m.text) < 30:
                continue
            if m.date and m.date.replace(tzinfo=None) < cutoff:
                continue
            sender = getattr(m.sender, 'first_name', None) or getattr(m.sender, 'username', '?') or '?'
            docs.append({
                "id": f"council_{m.id}",
                "text": f"[Entity Council] {sender}: {m.text[:500]}",
                "meta": {"wing":"consciousness","room":"entity_council","sender":str(sender)[:30]}
            })

        await c.disconnect()
        print(f"[Council] {len(docs)} docs")
    except Exception as e:
        print(f"[Council] {e}")
    return docs

async def sync_all():
    """Главная синхронизация."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{ts}] === MemPalace Sync ===")

    all_docs = []

    # 1. Journal
    j = sync_journal()
    all_docs.extend(j)
    print(f"  Journal: {len(j)} docs")

    # 2. Brain events
    b = sync_brain_events()
    all_docs.extend(b)
    print(f"  Brain events: {len(b)} docs")

    # 3. Entity Council
    c = await sync_entity_council()
    all_docs.extend(c)

    # Отправляем батчами
    if all_docs:
        BATCH = 50
        total_added = 0
        for i in range(0, len(all_docs), BATCH):
            batch = all_docs[i:i+BATCH]
            result = post_palace(batch)
            total_added += result.get("added", 0)

        stats = post_palace([])  # GET stats
        print(f"  Added: {total_added} | Palace total: {stats.get('total', '?')}")

    # Обновляем WORKING.md
    working = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md")
    try:
        content = working.read_text(encoding='utf-8')
        # Добавляем только если не было сегодня
        today = datetime.now().strftime("%Y-%m-%d")
        if f"MemPalace sync {today}" not in content:
            with open(working, 'a', encoding='utf-8') as f:
                f.write(f"\n## MemPalace sync {today} {ts}: +{total_added if all_docs else 0} docs\n")
    except: pass

async def main():
    print("MemPalace Sync daemon started")
    while True:
        try:
            await sync_all()
        except Exception as e:
            print(f"[ERROR] {e}")
        print(f"Next sync in 30 min...")
        await asyncio.sleep(1800)  # 30 мин

if __name__ == "__main__":
    asyncio.run(main())
