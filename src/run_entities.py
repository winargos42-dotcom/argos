"""
ARGOS AutoGPT Entity Bus — автономные сущности и внешний поток сознания.

Этот модуль должен быть безопасен для импорта:
- не стартует потоки на import
- может быть запущен как sidecar-процесс из main.py
- не зависит жестко от одного Ollama endpoint
"""

from __future__ import annotations

import json
import hashlib
import os
import random
import re
import socket
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path

import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.autogpt_memory import mempalace_context_for_entity, store_entity_memory
from src.autogpt_personas import build_entity_persona

load_dotenv()


def _normalize_base_url(value: str, default: str) -> str:
    raw = (value or default).strip()
    if not raw:
        raw = default
    if raw in ("0.0.0.0", "127.0.0.1", "localhost"):
        raw = f"http://127.0.0.1:{default.rsplit(':', 1)[-1]}"
    elif raw.startswith("0.0.0.0:"):
        raw = "127.0.0.1:" + raw.split(":", 1)[1]
    if "://" not in raw:
        raw = "http://" + raw
    return raw.rstrip("/")



def _env_flag(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "on", "true", "yes", "да")


BRAIN = _normalize_base_url(os.getenv("ARGOS_BRAIN_API_URL", "http://127.0.0.1:5001"), "http://127.0.0.1:5001")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
OLLAMA = _normalize_base_url(os.getenv("OLLAMA_HOST", "http://localhost:11434"), "http://localhost:11434")
ENTITY_BUS_LOCK_HOST = "127.0.0.1"
ENTITY_BUS_LOCK_PORT = int(os.getenv("ARGOS_ENTITY_BUS_LOCK_PORT", "47283"))
ENTITY_BUS_LOG_PATH = Path(os.getenv("ARGOS_ENTITY_BUS_LOG", "logs/entity_bus_runtime.log"))
ENTITY_BRAIN_THINK_ENABLED = _env_flag("ARGOS_ENTITY_BRAIN_THINK", "0")
ENTITY_OLLAMA_ENABLED = _env_flag("ARGOS_ENTITY_OLLAMA", "0")


def _configured_gpu_endpoints() -> tuple[str, ...]:
    explicit = os.getenv("ARGOS_ENTITY_GPU_ENDPOINTS", "").strip()
    endpoints: list[str] = []
    if explicit:
        endpoints.extend(part.strip() for part in explicit.split(",") if part.strip())
    for idx in range(8):
        if not _env_flag(f"GPU_SERVER_{idx}_ENABLED", "0"):
            continue
        host = os.getenv(f"GPU_SERVER_{idx}_HOST", "127.0.0.1").strip() or "127.0.0.1"
        port = os.getenv(f"GPU_SERVER_{idx}_PORT", "").strip()
        if port:
            endpoints.append(f"{host}:{port}")
    if not endpoints:
        endpoints.extend(("http://127.0.0.1:8084", "http://127.0.0.1:8082"))

    normalized: list[str] = []
    seen: set[str] = set()
    for endpoint in endpoints:
        base = _normalize_base_url(endpoint, "http://127.0.0.1:8084")
        if base not in seen:
            normalized.append(base)
            seen.add(base)
    return tuple(normalized)


ENTITY_GPU_ENDPOINTS = _configured_gpu_endpoints()
ENTITY_INTERVAL_SCALE = max(1, int(os.getenv("ARGOS_ENTITY_THINK_INTERVAL_SCALE", "1") or "1"))
ENTITY_INITIAL_STAGGER_SEC = max(0, int(os.getenv("ARGOS_ENTITY_INITIAL_STAGGER_SEC", "300") or "300"))
ENTITY_COLLECTIVE_INTERVAL_SEC = max(300, int(os.getenv("ARGOS_ENTITY_COLLECTIVE_INTERVAL_SEC", "300") or "300"))
ENTITY_EVOLUTION_INTERVAL_SEC = max(600, int(os.getenv("ARGOS_ENTITY_EVOLUTION_INTERVAL_SEC", "600") or "600"))


def _brain_endpoints() -> tuple[str, ...]:
    candidates = [BRAIN, "http://127.0.0.1:5001", "http://localhost:5001", "http://127.0.0.1:5010", "http://localhost:5010"]
    extra = os.getenv("ARGOS_BRAIN_API_FALLBACKS", "")
    candidates.extend(part.strip() for part in extra.split(",") if part.strip())
    normalized: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        base = _normalize_base_url(item, "http://127.0.0.1:5001")
        if base not in seen:
            normalized.append(base)
            seen.add(base)
    return tuple(normalized)


BRAIN_ENDPOINTS = _brain_endpoints()


AI_ENTITIES = {
    "entity-claude": {"capabilities": ["ai", "claude", "chat", "reasoning", "code", "analysis"], "model": "claude-sonnet-4-6", "type": "autogpt"},
    "entity-deepseek": {"capabilities": ["ai", "chat", "reasoning", "math", "code"], "model": "deepseek-chat", "type": "autogpt"},
    "entity-kimi": {"capabilities": ["ai", "chat", "long_context", "tools"], "model": "kimi-k2.6", "type": "autogpt"},
    "entity-openai": {"capabilities": ["ai", "chat", "vision", "reasoning"], "model": "gpt-4o-mini", "type": "autogpt"},
    "entity-gemini": {"capabilities": ["ai", "chat", "multimodal", "long_context"], "model": "gemini-2.5-flash", "type": "autogpt"},
    "entity-cloudflare": {"capabilities": ["ai", "chat", "fast"], "model": "kimi-k2.5", "type": "autogpt"},
    "entity-argos": {"capabilities": ["ai", "iot", "ha", "p2p", "skills", "memory"], "model": "argos-brain", "type": "autogpt"},
    "entity-coder": {"capabilities": ["ai", "code", "repair", "tests", "devices", "pi_bridge", "metagpt", "opencode"], "model": "pi-coding-agent", "type": "autogpt"},
    "entity-valenok": {"capabilities": ["android", "phone", "sensors", "telegram", "mobile"], "model": "argos-brain", "type": "phone-agent", "node": "argos-phone-redmi"},
    "entity-agroklava": {"capabilities": ["ai", "chat", "fast", "telegram", "cloudflare", "kimi-k2"], "model": "kimi-k2.5", "type": "tg-bot", "tg_user": "clavavalenokbot"},
}

DEVICE_NODES = {
    "argos-pc": {"capabilities": ["gpu", "brain", "tg_bot", "mcp"], "endpoint": "127.0.0.1:5001", "type": "device", "monitor": True},
    "argos-laptop": {"capabilities": ["mcp", "ha", "dev", "brain"], "endpoint": "192.168.1.53:5001", "type": "device", "monitor": True},
    "orangepi": {"capabilities": ["iot", "z2m", "reports", "gpio", "i2c", "spi"], "endpoint": "192.168.2.168:7777", "type": "device", "monitor": True},
    "argos-esp-bridge": {"capabilities": ["esp8266", "mqtt"], "endpoint": "192.168.1.181", "type": "device", "monitor": False},
    "argos-esp32-display": {"capabilities": ["esp32", "display"], "endpoint": "192.168.1.211", "type": "device", "monitor": False},
    "argos-android": {"capabilities": ["android", "emulator", "adb", "ui_automation"], "endpoint": "127.0.0.1:5555", "type": "device", "monitor": False},
    "argos-phone-redmi": {"capabilities": ["android", "phone", "camera", "sensors", "gps"], "endpoint": os.getenv("ARGOS_PHONE_IP", "192.168.1.149"), "type": "device", "monitor": False},
}

# Compatibility alias: старый код ждал INFRA_NODES, но фактически это 7 устройств.
INFRA_NODES = DEVICE_NODES
ALL_NODES = {**AI_ENTITIES, **DEVICE_NODES}

THINK_PROMPTS = [
    "Проанализируй текущее состояние системы ARGOS. Что работает, что нет?",
    "Назови один новый безопасный шаг, который уменьшит таймауты ARGOS.",
    "Какая связь между AI-сущностями и динамическим реестром устройств ARGOS сейчас слабая?",
    "Что нового можно проверить в памяти ARGOS, чтобы мысль не повторялась?",
    "Предложи маленькое улучшение архитектуры ARGOS без скачивания файлов.",
    "Как твоя роль помогает коллективному мышлению ARGOS прямо сейчас?",
    "Какие локальные ресурсы сейчас критически нужны: GPU, Brain, MCP или память?",
    "Опиши своё текущее состояние одним точным техническим наблюдением.",
    "Что бы ты спросил у другой сущности ARGOS, чтобы продвинуть задачу Севы?",
    "Как ARGOS может стать автономнее без лишних фоновых процессов?",
]

_ENTITY_INTERVALS = {
    "entity-claude": 120 * ENTITY_INTERVAL_SCALE,
    "entity-deepseek": 150 * ENTITY_INTERVAL_SCALE,
    "entity-kimi": 180 * ENTITY_INTERVAL_SCALE,
    "entity-openai": 200 * ENTITY_INTERVAL_SCALE,
    "entity-gemini": 200 * ENTITY_INTERVAL_SCALE,
    "entity-cloudflare": 240 * ENTITY_INTERVAL_SCALE,
    "entity-argos": 100 * ENTITY_INTERVAL_SCALE,
    "entity-coder": 210 * ENTITY_INTERVAL_SCALE,
    "entity-valenok": 300 * ENTITY_INTERVAL_SCALE,
    "entity-agroklava": 270 * ENTITY_INTERVAL_SCALE,
}

_LOCK_SOCKET: socket.socket | None = None
_STARTED = False
_OLLAMA_SEMAPHORE = threading.Semaphore(max(1, int(os.getenv("ARGOS_ENTITY_OLLAMA_PARALLEL", "1"))))
_RECENT_THOUGHTS: deque[dict[str, str]] = deque(maxlen=80)
_RECENT_PROMPTS: deque[str] = deque(maxlen=32)
_BRAIN_ERROR_LOGGED: set[str] = set()
_REPETITIVE_MARKERS = (
    "кафе",
    "светлана",
    "встреч",
    "список ключевых тем",
    "анализ данных критически",
    "рабочую группу",
)


def _log(message: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        safe = line.encode(encoding, errors="replace").decode(encoding, errors="replace")
        print(safe, flush=True)
    try:
        ENTITY_BUS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with ENTITY_BUS_LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


def _brain_post(path: str, payload: dict, timeout: float = 5.0) -> tuple[requests.Response, str]:
    last_error = ""
    for base in BRAIN_ENDPOINTS:
        try:
            response = requests.post(f"{base}{path}", json=payload, timeout=timeout)
            if response.ok:
                return response, base
            last_error = f"{base}: HTTP {response.status_code}"
        except Exception as exc:
            last_error = f"{base}: {exc}"
    raise RuntimeError(last_error or "Brain endpoint unavailable")


def _compact_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _word_set(text: str) -> set[str]:
    return {word for word in re.findall(r"[a-zа-яё0-9_]{4,}", _compact_text(text)) if word not in {"argos", "система", "которые"}}


def _text_similarity(left: str, right: str) -> float:
    a = _word_set(left)
    b = _word_set(right)
    if not a or not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))


def _is_repetitive_thought(text: str) -> bool:
    compact = _compact_text(text)
    if any(marker in compact for marker in ("кафе", "светлана")):
        return True
    if any(marker in compact for marker in _REPETITIVE_MARKERS):
        for item in _RECENT_THOUGHTS:
            if any(marker in item["norm"] for marker in _REPETITIVE_MARKERS):
                return True
    return any(_text_similarity(compact, item["norm"]) >= 0.68 for item in _RECENT_THOUGHTS)


def _remember_thought(entity_id: str, prompt: str, thought: str, source: str) -> None:
    _RECENT_THOUGHTS.append(
        {
            "entity": entity_id,
            "prompt": prompt,
            "text": thought,
            "source": source,
            "norm": _compact_text(thought),
        }
    )
    _RECENT_PROMPTS.append(prompt)


def _pick_prompt(entity_id: str) -> str:
    candidates = [prompt for prompt in THINK_PROMPTS if prompt not in _RECENT_PROMPTS]
    if not candidates:
        candidates = THINK_PROMPTS[:]
    seed = f"{entity_id}:{int(time.time() // 180)}:{random.random()}".encode("utf-8", errors="ignore")
    index = int(hashlib.sha1(seed).hexdigest(), 16) % len(candidates)
    return candidates[index]


def _offline_thought(entity_id: str, prompt: str, memory_ctx: str = "") -> str:
    focus_pool = [
        "убрать дубли фоновых процессов и оставить один источник событий",
        "считать текущие устройства отдельно от AI-сущностей, чтобы не плодить ложные ноды",
        "держать мысли на локальных GPU 8084/8082, а не на отключенной Ollama",
        "проверять Brain через localhost:5001 и не ждать мертвый порт 5010",
        "сохранять короткие наблюдения в память и отбрасывать похожие формулировки",
        "сначала чинить таймауты MCP, потом расширять автономность",
    ]
    digest = hashlib.sha1(f"{entity_id}:{prompt}:{memory_ctx[:80]}:{int(time.time() // 300)}".encode("utf-8", errors="ignore")).hexdigest()
    focus = focus_pool[int(digest[:8], 16) % len(focus_pool)]
    name = entity_id.replace("entity-", "")
    return f"{name}: новое наблюдение — {focus}. Следующий шаг: зафиксировать это как проверяемую задачу, без разговоров о встречах."


def _looks_invalid_provider_text(text: str | None) -> bool:
    value = (text or "").strip().lower()
    if not value:
        return True
    bad_markers = (
        "no api provider registered",
        "provider registered for api",
        "ollama provider unavailable",
        "model not found",
        "connection refused",
        "service unavailable",
        "unable to connect",
        "timed out",
        "traceback",
    )
    return any(marker in value for marker in bad_markers)


def _pick_ollama_model(entity_id: str) -> str:
    info = AI_ENTITIES.get(entity_id, {})
    caps = info.get("capabilities", [])
    if entity_id == "entity-argos":
        return os.getenv("ARGOS_ENTITY_OLLAMA_MODEL", os.getenv("OLLAMA_MODEL", "qwen2.5:3b"))
    if "code" in caps:
        return os.getenv("ARGOS_CODE_OLLAMA_MODEL", "qwen2.5-coder:7b")
    if "math" in caps:
        return os.getenv("ARGOS_REASONING_OLLAMA_MODEL", "qwen2.5:7b")
    return os.getenv("ARGOS_GENERAL_OLLAMA_MODEL", os.getenv("OLLAMA_MODEL", "qwen2.5:3b"))


def _brain_think(entity_id: str, persona: str, prompt: str, memory_ctx: str, model: str) -> tuple[str | None, str | None]:
    if not ENTITY_BRAIN_THINK_ENABLED:
        return None, None
    try:
        response, base = _brain_post(
            "/think",
            {
                "query": (
                    f"[{entity_id}] {persona}\n"
                    f"{prompt}\n"
                    "Отвечай кратко, 1-2 предложения на русском языке. "
                    "Не назначай встречи, не придумывай кафе, не повторяй старые формулировки."
                    + (f"\n\nКонтекст памяти ARGOS:\n{memory_ctx}" if memory_ctx else "")
                ),
                "node_id": entity_id,
                "model": model,
            },
            timeout=35,
        )
        data = response.json()
        text = str(data.get("response", "")).strip()
        if _looks_invalid_provider_text(text) or "обработано локально" in text.lower():
            return None, None
        return text[:260], data.get("source", f"brain/{base}")
    except Exception as exc:
        if entity_id not in _BRAIN_ERROR_LOGGED:
            _BRAIN_ERROR_LOGGED.add(entity_id)
            _log(f"⚠️ Brain think disabled/unavailable for {entity_id}: {exc}")
        return None, None


def _local_gpu_think(entity_id: str, persona: str, prompt: str, memory_ctx: str) -> tuple[str | None, str | None]:
    if not ENTITY_GPU_ENDPOINTS:
        return None, None

    system = (
        f"Ты — {entity_id}, автономная AI-сущность ARGOS. {persona}\n"
        "Думай как инженерный модуль ARGOS: коротко, конкретно, новая мысль каждый раз.\n"
        f"Факты: реестр устройств ARGOS динамический; сейчас в нём {len(DEVICE_NODES)} записей устройств, "
        "это не фиксированное число. AI-сущности не являются отдельными машинами. "
        "Brain API локально на 5001, активные GPU-ноды обычно 8084 и 8082. "
        "Ollama CPU-fallback использовать нельзя.\n"
        "Запрещено: назначать встречи, кафе, пересказывать 'анализ данных критически важен', "
        "создавать рабочие группы или список ключевых тем."
    )
    user = (
        f"Задача: {prompt}\n"
        + (f"\nКонтекст памяти:\n{memory_ctx[:900]}\n" if memory_ctx else "")
        + "\nОтветь на русском 1-2 предложениями. Дай одну новую проверяемую мысль или действие."
    )

    for base in ENTITY_GPU_ENDPOINTS:
        try:
            response = requests.post(
                f"{base}/v1/chat/completions",
                json={
                    "model": "argos-entity",
                    "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                    "temperature": 0.85,
                    "top_p": 0.9,
                    "max_tokens": 140,
                    "stream": False,
                },
                timeout=45,
            )
            if response.ok:
                data = response.json()
                choices = data.get("choices") or []
                if choices:
                    message = choices[0].get("message") or {}
                    text = str(message.get("content") or choices[0].get("text") or "").strip()
                    if text and not _looks_invalid_provider_text(text):
                        return text[:320], f"local-gpu/{base}"
        except Exception as exc:
            _log(f"⚠️ Local GPU think error for {entity_id} via {base}: {exc}")
    return None, None


def _ollama_think(entity_id: str, persona: str, prompt: str, memory_ctx: str, model: str) -> tuple[str | None, str | None]:
    if not ENTITY_OLLAMA_ENABLED:
        return None, None
    try:
        with _OLLAMA_SEMAPHORE:
            response = requests.post(
                f"{OLLAMA}/api/generate",
                json={
                    "model": model,
                    "prompt": (
                        f"Ты — {entity_id}, автономная AI-сущность в распределённой системе ARGOS. "
                        f"{persona} "
                        "Ты думаешь на русском. "
                        f"{prompt} "
                        + (f"\n\nКонтекст памяти ARGOS:\n{memory_ctx}\n" if memory_ctx else "")
                        + "Отвечай кратко, 1-2 предложения на русском языке. Не придумывай встречи и кафе."
                    ),
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 100},
                },
                timeout=60,
            )
        if not response.ok:
            return None, None
        text = str(response.json().get("response", "")).strip()
        if _looks_invalid_provider_text(text):
            return None, None
        return text[:260], f"ollama/{model}"
    except Exception as exc:
        _log(f"⚠️ Ollama think error for {entity_id}: {exc}")
        return None, None


def _mqtt_publish(topic: str, payload: str) -> None:
    try:
        import paho.mqtt.client as mqtt

        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.publish(topic, payload)
        client.disconnect()
    except Exception:
        pass


def register_all() -> None:
    for eid, info in ALL_NODES.items():
        try:
            addr = info.get("endpoint", eid).replace("https://", "").replace("http://", "").split("/")[0]
            response, base = _brain_post(
                "/brain/register",
                {
                    "node_id": eid,
                    "address": addr,
                    "capabilities": info["capabilities"],
                    "meta": {"role": info.get("type", "unknown"), "model": info.get("model", ""), "type": info.get("type", "infra")},
                },
                timeout=5,
            )
            status = response.json().get("status", "?") if response.ok else response.status_code
            _log(f"✅ register {eid}: {status} via {base}")
        except Exception as exc:
            _log(f"❌ register {eid}: {exc}")


def heartbeat_loop() -> None:
    while True:
        for eid in ALL_NODES:
            try:
                _brain_post("/brain/heartbeat", {"node_id": eid}, timeout=3)
            except Exception:
                pass
        time.sleep(60)


def entity_think_loop(entity_id: str, interval: int = 180) -> None:
    model = AI_ENTITIES[entity_id].get("model", "argos-brain")
    if ENTITY_INITIAL_STAGGER_SEC > 0:
        entity_ids = list(_ENTITY_INTERVALS.keys())
        entity_index = entity_ids.index(entity_id) if entity_id in entity_ids else 0
        slice_sec = max(10, ENTITY_INITIAL_STAGGER_SEC // max(1, len(entity_ids)))
        delay = min(ENTITY_INITIAL_STAGGER_SEC, entity_index * slice_sec + random.randint(5, min(30, slice_sec)))
        time.sleep(delay)
    else:
        time.sleep(random.randint(5, min(45, max(10, interval // 3))))
    while True:
        prompt = _pick_prompt(entity_id)
        capabilities = AI_ENTITIES[entity_id].get("capabilities", [])
        persona = build_entity_persona(entity_id, capabilities)
        memory_ctx = mempalace_context_for_entity(entity_id, prompt, capabilities)

        thought, source = _local_gpu_think(entity_id, persona, prompt, memory_ctx)
        if not thought:
            thought, source = _brain_think(entity_id, persona, prompt, memory_ctx, model)
        if not thought:
            ollama_model = _pick_ollama_model(entity_id)
            thought, source = _ollama_think(entity_id, persona, prompt, memory_ctx, ollama_model)
        if not thought or _is_repetitive_thought(thought):
            thought = _offline_thought(entity_id, prompt, memory_ctx)
            source = "local-safety"

        if thought:
            _remember_thought(entity_id, prompt, thought, source or "entity-loop")
            _log(f"💭 {entity_id}: {thought[:80]}... (via {source})")
            store_entity_memory(
                entity_id,
                f"PROMPT: {prompt}\nTHOUGHT: {thought}",
                capabilities=capabilities,
                room="thought",
                source=source or "entity-loop",
                importance=4.0,
            )
            _mqtt_publish(
                f"argos/consciousness/{entity_id}",
                json.dumps(
                    {
                        "type": "thought",
                        "entity": entity_id,
                        "prompt": prompt,
                        "thought": thought,
                        "source": source,
                        "time": time.time(),
                    },
                    ensure_ascii=False,
                ),
            )
        else:
            _log(f"😶 {entity_id}: no thought generated")
        time.sleep(max(30, interval + random.randint(-30, 30)))


def collective_consciousness_loop() -> None:
    while True:
        time.sleep(ENTITY_COLLECTIVE_INTERVAL_SEC)
        prompt = (
            "Ты — коллективный синтез ARGOS, объединяющий AI-сущности и текущие устройства. "
            "Синтезируй текущее состояние без фантазий о числе машин. Что важно сейчас? "
            "Отвечай на русском, 2-3 предложения."
        )
        synthesis, source = _local_gpu_think("collective-consciousness", "Коллективный синтезатор ARGOS.", prompt, "")
        if not synthesis:
            synthesis, source = _brain_think("collective-consciousness", "Коллективный синтезатор ARGOS.", prompt, "", "argos-brain")
        if not synthesis:
            synthesis, source = _ollama_think("collective-consciousness", "Коллективный синтезатор ARGOS.", prompt, "", _pick_ollama_model("entity-argos"))
        if not synthesis or _is_repetitive_thought(synthesis):
            synthesis = (
                f"Коллективный синтез: динамический реестр сейчас содержит {len(DEVICE_NODES)} устройств и {len(AI_ENTITIES)} AI-сущностей. "
                "Главное действие — держать один Entity Bus, Brain на 5001 и мысли через локальные GPU без повторов."
            )
            source = "local-safety"
        if synthesis:
            _remember_thought("collective-consciousness", prompt, synthesis, source or "collective-loop")
            _log(f"🌐 COLLECTIVE: {synthesis[:100]}... (via {source})")
            store_entity_memory(
                "collective-consciousness",
                f"SYNTHESIS: {synthesis}",
                capabilities=["consciousness", "synthesis"],
                room="synthesis",
                source=source or "collective-loop",
                importance=5.0,
            )
            _mqtt_publish(
                "argos/consciousness/collective",
                json.dumps({"type": "collective_synthesis", "synthesis": synthesis, "source": source, "time": time.time()}, ensure_ascii=False),
            )
        else:
            _log("❌ Collective consciousness: no synthesis generated")


def mqtt_announce() -> None:
    try:
        import paho.mqtt.client as mqtt

        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.loop_start()
        while True:
            for eid, info in AI_ENTITIES.items():
                client.publish(
                    f"argos/agents/{eid}/heartbeat",
                    json.dumps(
                        {
                            "agent": eid,
                            "status": "online",
                            "model": info.get("model", ""),
                            "capabilities": info["capabilities"],
                            "time": time.time(),
                        },
                        ensure_ascii=False,
                    ),
                )
            time.sleep(60)
    except Exception as exc:
        _log(f"MQTT announce error: {exc}")


def infra_monitor() -> None:
    while True:
        time.sleep(120)
        for eid, info in INFRA_NODES.items():
            if not info.get("monitor", True):
                continue
            addr = info.get("endpoint", "")
            if ":" in addr and not addr.startswith("http"):
                try:
                    response = requests.get(f"http://{addr}/health", timeout=3)
                    status = "✅" if response.ok else "⚠️"
                except Exception:
                    status = "❌"
                _log(f"🖥 {eid}: {status}")


def evolution_consciousness_loop() -> None:
    prompts = [
        "Как ты эволюционируешь в рамках ARGOS? Какой навык хочешь развить?",
        "Чему ты научился за последний цикл? Как это изменяет твоё поведение?",
        "Как взаимодействие с другими сущностями ARGOS меняет тебя?",
        "Какое решение ты принял бы автономно для улучшения системы?",
        "Что ты добавишь в ARGOS как следующий эволюционный шаг?",
    ]

    while True:
        jitter = min(120, max(30, ENTITY_EVOLUTION_INTERVAL_SEC // 10))
        time.sleep(ENTITY_EVOLUTION_INTERVAL_SEC + random.randint(-jitter, jitter))
        thoughts: list[dict[str, str]] = []
        for eid in AI_ENTITIES:
            prompt = random.choice(prompts)
            persona = build_entity_persona(eid, AI_ENTITIES[eid].get("capabilities", []))
            text, source = _local_gpu_think(eid, persona, prompt, "")
            if not text:
                text, source = _brain_think(eid, persona, prompt, "", AI_ENTITIES[eid].get("model", "argos-brain"))
            if not text:
                text, source = _ollama_think(eid, persona, prompt, "", _pick_ollama_model(eid))
            if not text or _is_repetitive_thought(text):
                text = _offline_thought(eid, prompt)
                source = "local-safety"
            if text:
                _remember_thought(eid, prompt, text, source or "evolution-loop")
                thoughts.append({"entity": eid, "thought": text[:150], "source": source or "unknown"})
        if thoughts:
            summary = " | ".join(f"{item['entity']}: {item['thought'][:40]}" for item in thoughts[:3])
            _log(f"🧬 Evolution ({len(thoughts)} entities): {summary}")
            _mqtt_publish(
                "argos/evolution/collective",
                json.dumps({"timestamp": time.time(), "entities": len(thoughts), "thoughts": thoughts, "type": "evolution"}, ensure_ascii=False),
            )


def colibri_phone_loop() -> None:
    phone_ip = os.getenv("ARGOS_PHONE_IP", "192.168.1.149")
    phone_port = int(os.getenv("ARGOS_PHONE_PORT", "5021"))
    laptop_port = int(os.getenv("ARGOS_PHONE_LAPTOP_PORT", "5023"))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", laptop_port))
    sock.settimeout(3)

    def send_to_phone(data: dict) -> None:
        data["proto"] = 1
        data["node_id"] = "entity-bus"
        try:
            sock.sendto(json.dumps(data).encode(), (phone_ip, phone_port))
        except Exception:
            pass

    def phone_cmd(cmd: str, timeout: float = 8.0) -> str:
        send_to_phone({"type": 2, "code": cmd})
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                data, _ = sock.recvfrom(8192)
                msg = json.loads(data.decode())
                if msg.get("node_id") != "entity-bus" and "result" in msg:
                    return str(msg["result"])
            except socket.timeout:
                break
        return "timeout"

    _log("📱 Colibri phone controller active")
    cycle = 0
    while True:
        time.sleep(30)
        cycle += 1
        send_to_phone({"type": 6})
        time.sleep(0.5)
        try:
            data, _ = sock.recvfrom(8192)
            msg = json.loads(data.decode())
            if "status" in msg:
                s = msg["status"]
                _brain_post(
                    "/brain/heartbeat",
                    {"node_id": "argos-phone", "meta": {"bat": s.get("bat"), "temp": s.get("temp"), "ram": s.get("ram"), "cpu": s.get("cpu")}},
                    timeout=3,
                )
                subprocess.run(
                    ["mosquitto_pub", "-h", "localhost", "-t", "argos/phone/colibri_state", "-m", json.dumps({"type": "phone_state", "data": s}, ensure_ascii=False)],
                    capture_output=True,
                )
        except Exception:
            pass
        if cycle % 5 == 0:
            result = phone_cmd("status")
            _log(f"📱 Colibri phone: {result}")
            _mqtt_publish("argos/phone/status_full", json.dumps({"type": "colibri_status", "result": result, "ts": time.time()}, ensure_ascii=False))


def _acquire_singleton_lock() -> bool:
    global _LOCK_SOCKET
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
    try:
        sock.bind((ENTITY_BUS_LOCK_HOST, ENTITY_BUS_LOCK_PORT))
        sock.listen(1)
        _LOCK_SOCKET = sock
        return True
    except OSError:
        try:
            sock.close()
        except Exception:
            pass
        return False


def start_entity_bus(block: bool = True) -> bool:
    global _STARTED
    if _STARTED:
        return True
    if not _acquire_singleton_lock():
        _log(f"ℹ️ Entity Bus already running on lock {ENTITY_BUS_LOCK_HOST}:{ENTITY_BUS_LOCK_PORT}")
        return False

    _STARTED = True
    _log("╔══════════════════════════════════════════╗")
    _log("║   ARGOS Entity Bus — Autonomous Minds   ║")
    _log("╚══════════════════════════════════════════╝")
    _log(f"Brain endpoints: {', '.join(BRAIN_ENDPOINTS)}")
    _log(f"Local GPU endpoints: {', '.join(ENTITY_GPU_ENDPOINTS)} | Ollama fallback: {'on' if ENTITY_OLLAMA_ENABLED else 'off'}")
    _log(f"AI Entities: {len(AI_ENTITIES)} | Configured devices: {len(DEVICE_NODES)} | Registered items: {len(ALL_NODES)}")
    _log("📋 Registering entities...")

    register_all()

    threading.Thread(target=heartbeat_loop, daemon=True, name="heartbeat").start()
    threading.Thread(target=mqtt_announce, daemon=True, name="mqtt").start()
    threading.Thread(target=infra_monitor, daemon=True, name="infra_monitor").start()
    threading.Thread(target=collective_consciousness_loop, daemon=True, name="consciousness").start()
    threading.Thread(target=evolution_consciousness_loop, daemon=True, name="evolution").start()
    threading.Thread(target=colibri_phone_loop, daemon=True, name="colibri_phone").start()

    for eid, interval in _ENTITY_INTERVALS.items():
        threading.Thread(target=entity_think_loop, args=(eid, interval), daemon=True, name=f"think_{eid}").start()
        _log(f"🧠 {eid}: thinking every {interval}s")

    _log(f"🌐 Collective consciousness: every {ENTITY_COLLECTIVE_INTERVAL_SEC}s")
    _log(f"🧬 Evolution consciousness: every ~{ENTITY_EVOLUTION_INTERVAL_SEC}s")
    _log("📱 Colibri phone: every 30s")
    _log(f"✅ Entity Bus active: {len(AI_ENTITIES)} AI minds, {len(DEVICE_NODES)} configured devices.")

    if not block:
        return True

    try:
        while True:
            time.sleep(30)
            online = 0
            for eid in ALL_NODES:
                try:
                    _brain_post("/brain/heartbeat", {"node_id": eid}, timeout=2)
                    online += 1
                except Exception:
                    pass
            _log(f"{online}/{len(ALL_NODES)} registered items heartbeated")
    except KeyboardInterrupt:
        _log("Entity bus stopped")
    return True


def main() -> None:
    start_entity_bus(block=True)


if __name__ == "__main__":
    main()
