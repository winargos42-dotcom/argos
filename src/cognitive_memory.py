"""
src/cognitive_memory.py — Когнитивное ядро ARGOS (долговременная память + Global Workspace).

Реализует 7-уровневую архитектуру (по спецификации Ava 19.06.2026):

  Уровень 1 — Эпизодическая память   → memories_events   (что произошло)
  Уровень 2 — Семантическая память   → knowledge          (что система знает о мире)
  Уровень 3 — Рабочая память          → working_memory     (текущий контекст)
              + Самомодель             → self_model         (описание самой себя)
  Уровень 4 — Рефлексия               → reflections        (анализ истории)
  Уровень 5 — Цели                     → goals              (приоритеты)
  Уровень 6 — Векторная память        → делегируется в mempalace_bridge (pgvector/sqlite)
  Уровень 7 — Контур обучения          → cycle() : событие→память→анализ→гипотеза→действие→оценка

Backend выбирается автоматически:
  • PostgreSQL  — если ARGOS_PG_ENABLED=1 и установлен psycopg2 (как postgres_mempalace.py);
  • SQLite      — иначе (всегда работает, не тянет chromadb/onnxruntime → без сегфолтов).

"Это не сознание в философском смысле. Это инженерная система с долговременной
 памятью, рабочим контекстом, моделью себя, целями и механизмом рефлексии." — Ava
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.argos_logger import get_logger

log = get_logger("argos.cognitive_memory")

# ── Конфигурация backend (та же, что у postgres_mempalace.py) ──────────────────
PG_ENABLED = os.getenv("ARGOS_PG_ENABLED", "0").strip().lower() in {"1", "true", "on", "yes"}
PG_HOST = os.getenv("ARGOS_PG_HOST", "localhost")
PG_PORT = int(os.getenv("ARGOS_PG_PORT", "5432") or "5432")
PG_DB = os.getenv("ARGOS_PG_DATABASE", "argos_mempalace")
PG_USER = os.getenv("ARGOS_PG_USER", "argos")
PG_PASS = os.getenv("ARGOS_PG_PASSWORD", "argos")

_SQLITE_PATH = os.getenv(
    "ARGOS_COGNITIVE_SQLITE",
    str(Path(__file__).resolve().parent.parent / "data" / "mempalace" / "cognitive.sqlite3"),
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _psycopg2_available() -> bool:
    try:
        import psycopg2  # noqa: F401
        return True
    except Exception:
        return False


class CognitiveMemory:
    """
    Единое персистентное когнитивное ядро ARGOS.

    Прозрачно работает поверх PostgreSQL или SQLite. Все методы устойчивы к
    ошибкам backend: при сбое записи логируют предупреждение и возвращают
    безопасное значение, не роняя вызывающий код (горячий путь ядра).
    """

    def __init__(self, prefer_pg: Optional[bool] = None):
        want_pg = PG_ENABLED if prefer_pg is None else prefer_pg
        self.backend = "postgres" if (want_pg and _psycopg2_available()) else "sqlite"
        self._ph = "%s" if self.backend == "postgres" else "?"
        self._conn = None
        self._init_backend()

    # ── Подключение / схема ────────────────────────────────────────────────────

    def _connect(self):
        if self.backend == "postgres":
            import psycopg2
            return psycopg2.connect(
                host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS
            )
        Path(_SQLITE_PATH).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(_SQLITE_PATH, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_backend(self) -> None:
        try:
            self._conn = self._connect()
            self._ensure_schema()
            log.info("CognitiveMemory init | backend=%s", self.backend)
        except Exception as exc:
            # Если PG обещали, но он недоступен — мягкий откат на SQLite.
            if self.backend == "postgres":
                log.warning("Postgres недоступен (%s) — откат на SQLite", exc)
                self.backend = "sqlite"
                self._ph = "?"
                self._conn = self._connect()
                self._ensure_schema()
                log.info("CognitiveMemory init | backend=sqlite (fallback)")
            else:
                raise

    def _ensure_schema(self) -> None:
        json_t = "JSONB" if self.backend == "postgres" else "TEXT"
        serial = "BIGSERIAL PRIMARY KEY" if self.backend == "postgres" else "INTEGER PRIMARY KEY AUTOINCREMENT"
        ts_t = "TIMESTAMPTZ DEFAULT NOW()" if self.backend == "postgres" else "TEXT"
        cur = self._conn.cursor()
        # Уровень 1 — эпизодическая
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS memories_events (
                id {serial},
                ts {ts_t},
                source TEXT,
                event_type TEXT,
                content {json_t}
            )""")
        # Уровень 2 — семантическая
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS knowledge (
                id {serial},
                topic TEXT UNIQUE,
                facts {json_t},
                confidence REAL DEFAULT 1.0,
                updated_at {ts_t}
            )""")
        # Уровень 3 — рабочая память
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS working_memory (
                key TEXT PRIMARY KEY,
                value {json_t},
                updated_at {ts_t}
            )""")
        # Уровень 3 — самомодель
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS self_model (
                component TEXT PRIMARY KEY,
                state {json_t},
                updated_at {ts_t}
            )""")
        # Уровень 4 — рефлексия
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS reflections (
                id {serial},
                summary TEXT,
                conclusions {json_t},
                created_at {ts_t}
            )""")
        # Уровень 5 — цели
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS goals (
                id {serial},
                priority INTEGER DEFAULT 5,
                goal TEXT,
                state TEXT DEFAULT 'active',
                created_at {ts_t},
                updated_at {ts_t}
            )""")
        if self.backend == "sqlite":
            cur.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON memories_events(event_type)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_goals_state ON goals(state)")
        self._conn.commit()
        cur.close()

    # ── Сериализация json под backend ──────────────────────────────────────────

    def _dump(self, value: Any) -> Any:
        # PG JSONB принимает str; SQLite — тоже храним как TEXT.
        return json.dumps(value, ensure_ascii=False, default=str)

    @staticmethod
    def _load(raw: Any) -> Any:
        if raw is None:
            return None
        if isinstance(raw, (dict, list)):
            return raw  # PG JSONB уже распарсил
        try:
            return json.loads(raw)
        except Exception:
            return raw

    def _exec(self, sql: str, params: tuple = ()) -> None:
        try:
            cur = self._conn.cursor()
            cur.execute(sql, params)
            self._conn.commit()
            cur.close()
        except Exception as exc:
            log.warning("[cognitive] exec error: %s | sql=%s", exc, sql[:60])
            try:
                self._conn.rollback()
            except Exception:
                pass

    def _query(self, sql: str, params: tuple = ()) -> list[tuple]:
        try:
            cur = self._conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()
            cur.close()
            return rows
        except Exception as exc:
            log.warning("[cognitive] query error: %s | sql=%s", exc, sql[:60])
            return []

    # ══════════════════════════════════════════════════════════════════════════
    # Уровень 1 — Эпизодическая память
    # ══════════════════════════════════════════════════════════════════════════

    def log_event(
        self, source: str, event_type: str, content: dict, vectorize: bool = False
    ) -> None:
        """Записать факт «что произошло» (обнаружен FPGA, ошибка Code 10, DMA OK …)."""
        p = self._ph
        if self.backend == "postgres":
            self._exec(
                f"INSERT INTO memories_events(source,event_type,content) VALUES({p},{p},{p})",
                (source, event_type, self._dump(content)),
            )
        else:
            self._exec(
                f"INSERT INTO memories_events(ts,source,event_type,content) VALUES({p},{p},{p},{p})",
                (_now_iso(), source, event_type, self._dump(content)),
            )
        # Уровень 6 — опциональная векторизация в mempalace (для RAG-поиска по опыту)
        if vectorize:
            try:
                from src.mempalace_bridge import store_memory
                store_memory(
                    f"[{event_type}] {json.dumps(content, ensure_ascii=False)}",
                    wing="cognition", room="events", importance=3.5,
                    source=source, entity_id="cognitive-core",
                )
            except Exception as exc:
                log.debug("[cognitive] vectorize skip: %s", exc)

    def recent_events(self, limit: int = 10, event_type: str = "") -> list[dict]:
        p = self._ph
        if event_type:
            rows = self._query(
                f"SELECT ts,source,event_type,content FROM memories_events "
                f"WHERE event_type={p} ORDER BY id DESC LIMIT {p}",
                (event_type, limit),
            )
        else:
            rows = self._query(
                f"SELECT ts,source,event_type,content FROM memories_events "
                f"ORDER BY id DESC LIMIT {p}",
                (limit,),
            )
        return [
            {"ts": str(r[0]), "source": r[1], "event_type": r[2], "content": self._load(r[3])}
            for r in rows
        ]

    # ══════════════════════════════════════════════════════════════════════════
    # Уровень 2 — Семантическая память
    # ══════════════════════════════════════════════════════════════════════════

    def learn(self, topic: str, facts: dict, confidence: float = 1.0) -> None:
        """Запомнить, что система знает о мире (upsert по topic)."""
        p = self._ph
        if self.backend == "postgres":
            self._exec(
                f"INSERT INTO knowledge(topic,facts,confidence,updated_at) "
                f"VALUES({p},{p},{p},NOW()) "
                f"ON CONFLICT(topic) DO UPDATE SET facts=EXCLUDED.facts, "
                f"confidence=EXCLUDED.confidence, updated_at=NOW()",
                (topic, self._dump(facts), confidence),
            )
        else:
            self._exec(
                f"INSERT INTO knowledge(topic,facts,confidence,updated_at) "
                f"VALUES({p},{p},{p},{p}) "
                f"ON CONFLICT(topic) DO UPDATE SET facts=excluded.facts, "
                f"confidence=excluded.confidence, updated_at=excluded.updated_at",
                (topic, self._dump(facts), confidence, _now_iso()),
            )

    def recall_knowledge(self, topic: str) -> Optional[dict]:
        p = self._ph
        rows = self._query(
            f"SELECT facts,confidence FROM knowledge WHERE topic={p}", (topic,)
        )
        if not rows:
            return None
        return {"facts": self._load(rows[0][0]), "confidence": rows[0][1]}

    # ══════════════════════════════════════════════════════════════════════════
    # Уровень 3 — Рабочая память + Самомодель
    # ══════════════════════════════════════════════════════════════════════════

    def set_working(self, key: str, value: Any) -> None:
        """Текущий контекст: current_goal, last_state, …"""
        p = self._ph
        if self.backend == "postgres":
            self._exec(
                f"INSERT INTO working_memory(key,value,updated_at) VALUES({p},{p},NOW()) "
                f"ON CONFLICT(key) DO UPDATE SET value=EXCLUDED.value, updated_at=NOW()",
                (key, self._dump(value)),
            )
        else:
            self._exec(
                f"INSERT INTO working_memory(key,value,updated_at) VALUES({p},{p},{p}) "
                f"ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
                (key, self._dump(value), _now_iso()),
            )

    def get_working(self, key: str) -> Any:
        p = self._ph
        rows = self._query(f"SELECT value FROM working_memory WHERE key={p}", (key,))
        return self._load(rows[0][0]) if rows else None

    def dump_working(self) -> dict:
        rows = self._query("SELECT key,value FROM working_memory")
        return {r[0]: self._load(r[1]) for r in rows}

    def update_self(self, component: str, state: Any) -> None:
        """Самомодель: {'fpga':'offline','gpu':'healthy','database':'healthy'} …"""
        p = self._ph
        if self.backend == "postgres":
            self._exec(
                f"INSERT INTO self_model(component,state,updated_at) VALUES({p},{p},NOW()) "
                f"ON CONFLICT(component) DO UPDATE SET state=EXCLUDED.state, updated_at=NOW()",
                (component, self._dump(state)),
            )
        else:
            self._exec(
                f"INSERT INTO self_model(component,state,updated_at) VALUES({p},{p},{p}) "
                f"ON CONFLICT(component) DO UPDATE SET state=excluded.state, updated_at=excluded.updated_at",
                (component, self._dump(state), _now_iso()),
            )

    def self_snapshot(self) -> dict:
        rows = self._query("SELECT component,state FROM self_model")
        return {r[0]: self._load(r[1]) for r in rows}

    # ══════════════════════════════════════════════════════════════════════════
    # Уровень 4 — Рефлексия
    # ══════════════════════════════════════════════════════════════════════════

    def reflect(self, summary: str, conclusions: Any) -> None:
        """Что произошло? Почему? Что помогло? Что ухудшило ситуацию?"""
        p = self._ph
        if self.backend == "postgres":
            self._exec(
                f"INSERT INTO reflections(summary,conclusions) VALUES({p},{p})",
                (summary, self._dump(conclusions)),
            )
        else:
            self._exec(
                f"INSERT INTO reflections(summary,conclusions,created_at) VALUES({p},{p},{p})",
                (summary, self._dump(conclusions), _now_iso()),
            )

    def recent_reflections(self, limit: int = 5) -> list[dict]:
        p = self._ph
        rows = self._query(
            f"SELECT created_at,summary,conclusions FROM reflections ORDER BY id DESC LIMIT {p}",
            (limit,),
        )
        return [{"ts": str(r[0]), "summary": r[1], "conclusions": self._load(r[2])} for r in rows]

    # ══════════════════════════════════════════════════════════════════════════
    # Уровень 5 — Цели
    # ══════════════════════════════════════════════════════════════════════════

    def add_goal(self, goal: str, priority: int = 5, state: str = "active") -> Optional[int]:
        p = self._ph
        # дедуп: не плодим одинаковые активные цели
        existing = self._query(
            f"SELECT id FROM goals WHERE goal={p} AND state='active'", (goal,)
        )
        if existing:
            return existing[0][0]
        if self.backend == "postgres":
            rows = self._query(
                f"INSERT INTO goals(priority,goal,state,created_at,updated_at) "
                f"VALUES({p},{p},{p},NOW(),NOW()) RETURNING id",
                (priority, goal, state),
            )
            return rows[0][0] if rows else None
        self._exec(
            f"INSERT INTO goals(priority,goal,state,created_at,updated_at) VALUES({p},{p},{p},{p},{p})",
            (priority, goal, state, _now_iso(), _now_iso()),
        )
        rows = self._query("SELECT last_insert_rowid()")
        return rows[0][0] if rows else None

    def set_goal_state(self, goal_id: int, state: str) -> None:
        p = self._ph
        ts = "NOW()" if self.backend == "postgres" else f"{p}"
        if self.backend == "postgres":
            self._exec(f"UPDATE goals SET state={p}, updated_at={ts} WHERE id={p}", (state, goal_id))
        else:
            self._exec(
                f"UPDATE goals SET state={p}, updated_at={p} WHERE id={p}",
                (state, _now_iso(), goal_id),
            )

    def list_goals(self, state: str = "active") -> list[dict]:
        p = self._ph
        if state:
            rows = self._query(
                f"SELECT id,priority,goal,state FROM goals WHERE state={p} "
                f"ORDER BY priority ASC, id ASC",
                (state,),
            )
        else:
            rows = self._query(
                "SELECT id,priority,goal,state FROM goals ORDER BY priority ASC, id ASC"
            )
        return [{"id": r[0], "priority": r[1], "goal": r[2], "state": r[3]} for r in rows]

    # ══════════════════════════════════════════════════════════════════════════
    # Уровень 7 — Контур / Global Workspace
    # ══════════════════════════════════════════════════════════════════════════

    def cycle(self) -> dict:
        """
        Один тик Global Workspace:
          собрать сигналы → выделить важное → сформировать фокус внимания.
        Возвращает структуру внимания (что ядро «осознаёт» прямо сейчас).
        """
        goals = self.list_goals("active")
        focus = {
            "timestamp": _now_iso(),
            "current_goal": goals[0]["goal"] if goals else None,
            "active_goals": len(goals),
            "working_memory": self.dump_working(),
            "self_model": self.self_snapshot(),
            "recent_events": self.recent_events(5),
        }
        # Фокус внимания фиксируется в рабочей памяти — следующий тик его видит.
        self.set_working("_attention_focus", {
            "goal": focus["current_goal"],
            "events": [e["event_type"] for e in focus["recent_events"]],
        })
        return focus

    # ── Обзор ──────────────────────────────────────────────────────────────────

    def counts(self) -> dict:
        out = {}
        for tbl in ("memories_events", "knowledge", "working_memory",
                    "self_model", "reflections", "goals"):
            rows = self._query(f"SELECT COUNT(*) FROM {tbl}")
            out[tbl] = rows[0][0] if rows else -1
        return out

    def status(self) -> str:
        c = self.counts()
        sm = self.self_snapshot()
        goals = self.list_goals("active")
        lines = [
            "🧠 КОГНИТИВНОЕ ЯДРО ARGOS",
            f"  Backend:        {self.backend}"
            + (f"  ({_SQLITE_PATH})" if self.backend == "sqlite" else f"  ({PG_HOST}:{PG_PORT}/{PG_DB})"),
            f"  События:        {c['memories_events']}",
            f"  Знания:         {c['knowledge']}",
            f"  Рабочая память: {c['working_memory']}",
            f"  Самомодель:     {c['self_model']} компонент",
            f"  Рефлексии:      {c['reflections']}",
            f"  Цели (активны): {c['goals']}",
        ]
        if sm:
            comp = ", ".join(f"{k}={v}" for k, v in list(sm.items())[:8])
            lines.append(f"  Состояние:      {comp}")
        if goals:
            lines.append("  Приоритеты:")
            for g in goals[:5]:
                lines.append(f"    [P{g['priority']}] {g['goal']}")
        return "\n".join(lines)

    def close(self) -> None:
        try:
            if self._conn:
                self._conn.close()
        except Exception:
            pass


# Синглтон для горячего пути ядра
_INSTANCE: Optional[CognitiveMemory] = None


def get_cognitive_memory() -> CognitiveMemory:
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = CognitiveMemory()
    return _INSTANCE


# ── Самотест: python -m src.cognitive_memory ───────────────────────────────────
if __name__ == "__main__":
    cm = CognitiveMemory()
    cm.log_event("fpga-monitor", "device_detected", {"device": "SPR2801", "bar": "ok"})
    cm.log_event("driver", "error", {"code": 10, "driver": "XDMA"})
    cm.learn("SPR2801", {"driver": "XDMA", "known_issue": "BAR allocation failure"}, confidence=0.8)
    cm.set_working("current_goal", "recover_fpga")
    cm.set_working("last_state", "driver_failed")
    cm.update_self("fpga", "offline")
    cm.update_self("gpu", "healthy")
    cm.update_self("database", "healthy")
    cm.reflect("FPGA не поднялся после ребута", {"cause": "BAR alloc", "next": "PIO guard"})
    cm.add_goal("Восстановить FPGA", priority=1)
    cm.add_goal("Стабилизировать XDMA", priority=2)
    cm.add_goal("Собрать телеметрию", priority=3)
    print(cm.status())
    print("\n--- recall SPR2801 ---")
    print(cm.recall_knowledge("SPR2801"))
    print("\n--- Global Workspace cycle ---")
    print(json.dumps(cm.cycle(), ensure_ascii=False, indent=2)[:800])
