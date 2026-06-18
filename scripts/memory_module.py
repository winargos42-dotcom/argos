#!/usr/bin/env python3
"""
ARGOS Long-Term Memory Module.
При старте любого агента — загружает контекст из Obsidian SharedMemory.
При завершении — дописывает результат.
"""
import json, os, re, datetime
from pathlib import Path

SHARED = Path("/home/ava/Documents/MyObsidianVault/SharedMemory/shared")
CACHE = Path("/home/ava/Projects/argoss/data/mempalace/argos_memory.json")

class Memory:
    def __init__(self):
        self.working = []
        self.status = {}
        self.journal = []
        self._load()

    def _load(self):
        # 1. WORKING.md — активные задачи
        w = SHARED / "WORKING.md"
        if w.exists():
            txt = w.read_text(encoding="utf-8")
            self.working = [m.group(0) for m in re.finditer(r'- \[\s?\] .+', txt)]

        # 2. STATUS.md — состояние системы
        s = SHARED / "STATUS.md"
        if s.exists():
            self.status["lines"] = s.read_text(encoding="utf-8").splitlines()[-20:]

        # 3. JOURNAL.md — история сессий
        j = SHARED / "JOURNAL.md"
        if j.exists():
            lines = j.read_text(encoding="utf-8").splitlines()
            self.journal = [l for l in lines if l.strip().startswith("-")][-10:]

        # Кеш для быстрого доступа других скриптов
        CACHE.write_text(json.dumps({
            "ts": datetime.datetime.now().isoformat(),
            "working_count": len(self.working),
            "last_status": self.status.get("lines", ["empty"])[-1:] if self.status else ["empty"],
        }), encoding="utf-8")

        print(f"[Memory] Loaded {len(self.working)} tasks, {len(self.journal)} journal entries")

    def get_context(self, limit: int = 5) -> str:
        """Контекст для передачи в Entity Council или Valenok."""
        ctx = "## ARGOS Memory Context\n"
        ctx += f"_Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n"
        ctx += "### Active Tasks\n"
        for t in self.working[:limit]:
            ctx += f"{t}\n"
        ctx += "\n### Last Journal\n"
        for j in self.journal[-limit:]:
            ctx += f"{j}\n"
        ctx += "\n### Status\n"
        for s in self.status.get("lines", [])[-3:]:
            ctx += f"{s}\n"
        return ctx

    def append_journal(self, event: str, source: str = "ARGOS"):
        j = SHARED / "JOURNAL.md"
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        line = f"- **{ts}** [{source}] {event}\n"
        with open(j, "a", encoding="utf-8") as f:
            f.write(line)
        print(f"[Memory] Journal: {event}")

    def close_task(self, task_line: str):
        w = SHARED / "WORKING.md"
        if w.exists():
            txt = w.read_text(encoding="utf-8")
            txt = txt.replace(task_line, task_line.replace("- [ ]", "- [x]"))
            w.write_text(txt, encoding="utf-8")
            print(f"[Memory] Closed: {task_line[:50]}")

if __name__ == "__main__":
    m = Memory()
    print(m.get_context())
