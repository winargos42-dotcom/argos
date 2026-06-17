"""
p2p_network_scanner/skill.py — P2P Health Monitor Argos

Возможности:
• Валидация узлов (host, port), таймауты, обработка сетевых/HTML-ошибок.
• Конфигурация узлов из config/p2p_nodes.json, env P2P_NODES или core.config.
• История состояний (health history) с uptime / last_seen / consecutive_failures.
• События на шину: p2p.node_up / p2p.node_down / skill.executed.
• Асинхронный batch-скан с семафором.
• Тестируемость: DI-зависимости, нет print, нет sys.exit.
"""

from __future__ import annotations

import asyncio
import json
import os
import socket
import threading
import time
from collections import deque
from typing import Any, Callable, Coroutine

# ARGOS internals — graceful fallback if event_bus/logger unavailable
try:
    from src.event_bus import get_bus, Events
except Exception:  # pragma: no cover
    get_bus = None  # type: ignore[assignment]
    Events = None  # type: ignore[assignment,misc]

try:
    from src.argos_logger import get_logger
except Exception:  # pragma: no cover
    get_logger = None  # type: ignore[assignment]

__all__ = ["P2PNetworkSkill", "execute", "status", "setup", "teardown"]

SKILL_NAME = "p2p_network_scanner"
SKILL_VERSION = "2.0.0"
SKILL_AUTHOR = "ArgosUniversal"
SKILL_DESCRIPTION = "P2P health scanner с историей, событиями и асинхронным batch-сканом"

DEFAULT_NODES: list[tuple[str, int]] = [
    ("192.168.1.10", 5000),
    ("192.168.1.11", 5000),
    ("192.168.1.12", 5000),
]
DEFAULT_TIMEOUT = 3
DEFAULT_CONCURRENCY = 10
DEFAULT_HISTORY_LIMIT = 100

log = get_logger("argos.p2p_scanner") if get_logger else None


class NodeState:
    """Состояние одного узла + краткая история."""

    def __init__(self, host: str, port: int):
        self.key = (host, port)
        self.host = host
        self.port = port
        self.online = False
        self.status: str | None = None
        self.code: int | None = None
        self.error: str | None = None
        self.last_seen: float | None = None
        self.last_change: float | None = None
        self.consecutive_failures = 0
        self.history: deque[dict[str, Any]] = deque(maxlen=DEFAULT_HISTORY_LIMIT)

    def update(self, info: dict[str, Any]) -> bool:
        """
        Применяет результат проверки. Возвращает True, если online изменился.
        """
        now = time.time()
        was_online = self.online
        self.online = bool(info.get("online"))
        self.status = info.get("status")
        self.code = info.get("code")
        self.error = info.get("error")
        if self.online:
            self.last_seen = now
            self.consecutive_failures = 0
        else:
            self.consecutive_failures += 1

        if was_online != self.online:
            self.last_change = now

        self.history.append(
            {
                "ts": now,
                "online": self.online,
                "status": self.status,
                "code": self.code,
                "error": self.error,
            }
        )
        return was_online != self.online

    def to_dict(self) -> dict[str, Any]:
        return {
            "host": self.host,
            "port": self.port,
            "online": self.online,
            "status": self.status,
            "code": self.code,
            "error": self.error,
            "last_seen": self.last_seen,
            "last_change": self.last_change,
            "consecutive_failures": self.consecutive_failures,
            "history": list(self.history),
        }


class P2PNetworkSkill:
    """Навык для проверки доступности узлов P2P-сети Argos."""

    CONFIG_FILE = "config/p2p_nodes.json"
    HISTORY_FILE = "config/p2p_health_history.json"

    def __init__(
        self,
        core: Any = None,
        nodes: list[tuple[str, int]] | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        concurrency: int = DEFAULT_CONCURRENCY,
        check_fn: Callable[[str, int, int], dict[str, Any]] | None = None,
    ):
        """
        :param core: Ссылка на AWA-Core для чтения config и публикации событий.
        :param nodes: Список узлов (host, port). Если None — из конфига/env/дефолтов.
        :param timeout: Таймаут HTTP-запроса.
        :param concurrency: Максимум параллельных проверок.
        :param check_fn: DI-точка для тестов (заменяет _check_node).
        """
        self.timeout = max(1, int(timeout))
        self.concurrency = max(1, int(concurrency))
        self.check_fn = check_fn or _check_node
        self.core = core
        self._nodes: list[tuple[str, int]] = []
        self.states: dict[tuple[str, int], NodeState] = {}
        self._semaphore = threading.Semaphore(self.concurrency)
        self._lock = threading.Lock()

        self._load_nodes(nodes)
        self._load_history()

    # ------------------------------------------------------------------ config
    def _load_nodes(self, override_nodes: list[tuple[str, int]] | None) -> None:
        raw: list[Any] = []
        if override_nodes is not None:
            raw = list(override_nodes)
        else:
            # 1) env
            env_nodes = os.getenv("P2P_NODES", "").strip()
            if env_nodes:
                raw = _parse_nodes_env(env_nodes)
            # 2) core.config
            elif self.core is not None:
                try:
                    cfg = getattr(self.core, "config", {}) or {}
                    raw = cfg.get("p2p_nodes", [])
                except Exception:
                    raw = []
            # 3) config file
            if not raw and os.path.exists(self.CONFIG_FILE):
                try:
                    with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                        raw = json.load(f).get("nodes", [])
                except Exception as exc:
                    if log:
                        log.warning("p2p_nodes config read error: %s", exc)
            # 4) defaults
            if not raw:
                raw = list(DEFAULT_NODES)

        for node in raw:
            try:
                self._nodes.append(_validate_node(node))
            except ValueError as exc:
                key = _fallback_key(node)
                self.states[key] = NodeState(key[0], key[1])
                self.states[key].update(
                    {"online": False, "status": None, "code": None, "error": f"invalid node: {exc}"}
                )
                if log:
                    log.warning("P2P invalid node %r: %s", node, exc)

        # Ensure state objects exist for all configured nodes (default offline).
        for host, port in self._nodes:
            self.states.setdefault((host, port), NodeState(host, port))

    def _load_history(self) -> None:
        path = getattr(self, "HISTORY_FILE", self.HISTORY_FILE)
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                host = item.get("host", "")
                port = item.get("port", 0)
                state = NodeState(host, port)
                state.online = bool(item.get("online"))
                state.status = item.get("status")
                state.code = item.get("code")
                state.error = item.get("error")
                state.last_seen = item.get("last_seen")
                state.last_change = item.get("last_change")
                state.consecutive_failures = item.get("consecutive_failures", 0)
                for h in item.get("history", []):
                    state.history.append(h)
                self.states[(host, port)] = state
        except Exception as exc:
            if log:
                log.warning("p2p health history read error: %s", exc)

    def _save_history(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.HISTORY_FILE) or ".", exist_ok=True)
            with open(self.HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    [s.to_dict() for s in self.states.values()],
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
        except Exception as exc:
            if log:
                log.error("p2p health history save error: %s", exc)

    # ------------------------------------------------------------------ scan
    def _check_one(self, host: str, port: int) -> dict[str, Any]:
        with self._semaphore:
            return self.check_fn(host, port, self.timeout)

    async def scan_async(self) -> dict[tuple[str, int], NodeState]:
        """Асинхронный batch-скан всех узлов."""
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(None, self._check_one, host, port)
            for host, port in self._nodes
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        changed_states: list[NodeState] = []
        with self._lock:
            for (host, port), result in zip(self._nodes, results):
                if isinstance(result, Exception):
                    info = {
                        "online": False,
                        "status": None,
                        "code": None,
                        "error": str(result),
                    }
                else:
                    info = result
                assert isinstance(info, dict), f"expected dict, got {type(info).__name__}"

                state = self.states.setdefault((host, port), NodeState(host, port))
                if state.update(info):
                    changed_states.append(state)

            self._save_history()

        self._emit_changes(changed_states)
        return dict(self.states)

    def scan(self) -> dict[tuple[str, int], NodeState]:
        """Синхронная обёртка над scan_async."""
        return asyncio.run(self.scan_async())

    # ------------------------------------------------------------------ events
    def _emit_changes(self, changed_states: list[NodeState]) -> None:
        if get_bus is None:
            return
        bus = get_bus()
        for state in changed_states:
            event_type = Events.P2P_NODE_JOINED if state.online else Events.P2P_NODE_LEFT
            bus.emit(
                event_type,
                {
                    "host": state.host,
                    "port": state.port,
                    "status": state.status,
                    "consecutive_failures": state.consecutive_failures,
                },
                SKILL_NAME,
            )

    def _emit_executed(self, text: str) -> None:
        if get_bus is None:
            return
        bus = get_bus()
        bus.emit(
            Events.SKILL_EXECUTED,
            {"skill": SKILL_NAME, "input": text[:80]},
            SKILL_NAME,
        )

    # ------------------------------------------------------------------ report
    def report(self) -> str:
        """Формирует человекочитаемый отчёт."""
        lines = [
            f"🌐 P2P Health Monitor v{SKILL_VERSION}",
            f"Локальный IP: {_get_local_ip()}",
            f"Узлов в конфигурации: {len(self._nodes)}",
            "Результаты:",
        ]
        with self._lock:
            for (host, port), state in sorted(self.states.items()):
                if state.online:
                    lines.append(
                        f"  ✅ {host}:{port} → ONLINE (status: {state.status}, code: {state.code})"
                    )
                else:
                    err = state.error or f"failures={state.consecutive_failures}"
                    lines.append(f"  ❌ {host}:{port} → OFFLINE ({err})")
        return "\n".join(lines)

    def summary(self) -> dict[str, Any]:
        """JSON-сводка для API / MCP / автоматизации."""
        with self._lock:
            total = len(self.states)
            online = sum(1 for s in self.states.values() if s.online)
        return {
            "skill": SKILL_NAME,
            "version": SKILL_VERSION,
            "total_nodes": total,
            "online": online,
            "offline": total - online,
            "local_ip": _get_local_ip(),
            "nodes": [s.to_dict() for s in self.states.values()],
        }

    # ------------------------------------------------------------------ SkillLoader API
    def execute(self, text: str = "") -> str:
        """Точка входа SkillLoader."""
        self.scan()
        self._emit_executed(text)
        return self.report()

    def handle(self, text: str, core: Any = None) -> str | None:
        """Диспетчер команд."""
        t = (text or "").strip().lower()
        if not any(tr in t for tr in ("p2p", "scan", "скан", "health", "статус")):
            return None
        if "summary" in t or "json" in t or "сводка" in t:
            return json.dumps(self.summary(), ensure_ascii=False, indent=2)
        return self.execute(text)

    def start(self, core: Any = None) -> str:
        """Вызывается SkillLoader при загрузке."""
        if core is not None:
            self.core = core
        # Always re-resolve nodes from core/env/file so runtime config is honoured.
        self._nodes = []
        self._load_nodes(override_nodes=None)
        return f"🌐 {SKILL_NAME} v{SKILL_VERSION} loaded ({len(self._nodes)} nodes)"

    def stop(self) -> None:
        """Вызывается SkillLoader при выгрузке."""
        self._save_history()


# ---------------------------------------------------------------------- helpers

def _validate_node(node: Any) -> tuple[str, int]:
    """Принимает (host, port), [host, port] или {'host': ..., 'port': ...}."""
    if isinstance(node, dict):
        host = node.get("host")
        port = node.get("port")
    elif isinstance(node, (list, tuple)) and len(node) == 2:
        host, port = node
    else:
        raise ValueError(f"Узел должен быть парой (host, port) или dict, получено: {node!r}")
    host = str(host).strip() if host is not None else ""
    if not host:
        raise ValueError("host не может быть пустым")
    try:
        port = int(port)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"порт должен быть целым числом: {port!r}") from exc
    if not 1 <= port <= 65535:
        raise ValueError(f"порт вне диапазона 1..65535: {port}")
    return host, port


def _fallback_key(node: Any) -> tuple[str, int]:
    if isinstance(node, dict):
        return (str(node.get("host", "")), int(node.get("port", 0)))
    if isinstance(node, (list, tuple)) and len(node) == 2:
        return (str(node[0]), 0)
    return (str(node), 0)


def _parse_nodes_env(value: str) -> list[tuple[str, int]]:
    """Парсит 'host1:port1,host2:port2' или JSON-список пар/объектов."""
    value = value.strip()
    if value.startswith("["):
        try:
            parsed = json.loads(value)
            return [_validate_node(item) for item in parsed]
        except Exception as exc:
            raise ValueError(f"P2P_NODES JSON invalid: {exc}") from exc
    out: list[tuple[str, int]] = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise ValueError(f"P2P_NODES часть без порта: {part!r}")
        host, _, port_str = part.rpartition(":")
        out.append((host.strip(), int(port_str)))
    return out


def _get_local_ip() -> str:
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except OSError as exc:
        return f"0.0.0.0 (ошибка: {exc})"
    except Exception as exc:
        return f"0.0.0.0 (ошибка: {exc})"


def _check_node(host: str, port: int, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Проверяет один узел http://host:port/status."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError as exc:
        return {
            "online": False,
            "status": None,
            "code": None,
            "error": f"отсутствуют зависимости: {exc}",
        }

    url = f"http://{host}:{port}/status"
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return {"online": False, "status": None, "code": None, "error": str(exc)}

    text = resp.text or ""
    if not text.strip():
        return {
            "online": True,
            "status": "EMPTY_BODY",
            "code": resp.status_code,
            "error": None,
        }

    try:
        soup = BeautifulSoup(text, "html.parser")
    except Exception as exc:
        return {
            "online": True,
            "status": "PARSE_ERROR",
            "code": resp.status_code,
            "error": f"BeautifulSoup: {exc}",
        }

    status_tag = soup.find("div", {"id": "status"})
    status = status_tag.get_text(strip=True) if status_tag else "UNKNOWN"
    return {"online": True, "status": status, "code": resp.status_code, "error": None}


# ---------------------------------------------------------------------- module-level hooks

def setup(core: Any = None) -> None:
    """Инициализация при загрузке flat-скилла."""
    pass


def teardown() -> None:
    """Завершение работы."""
    pass


def status(text: str = "") -> str:
    return f"🌐 {SKILL_NAME} v{SKILL_VERSION}: мониторинг P2P-узлов"


def execute(text: str = "") -> str:
    return P2PNetworkSkill().execute(text)
