#!/usr/bin/env python3
"""
ARGOS HA Watchdog v2 — двухступенчатый healing (мягкое→жёсткое), rate limit.
По рекомендации @claude_gidbot: безопасный, точечный, без вслепую перезапусков.
"""
import sys, os, time, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from logging_config import configure_logging, get_logger, log_healing_event
    configure_logging()
    log = get_logger("argos.ha_watchdog")
except:
    import logging
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger("ha_watchdog")
    def log_healing_event(entity, action, result, **kwargs): pass

import urllib.request

HA_TOKEN = re.search(r'HA_TOKEN=([^\n\s]+)', 
    open('/home/ava/Projects/argoss/.env').read()).group(1)
HA_BASE = "http://localhost:8123"
INTERVAL = 300

# LocalTuya без local_key, phantom Z2M — не лечатся рестартом
NON_RECOVERABLE_DOMAINS = {"localtuya"}
NON_RECOVERABLE_ENTITIES = {
    # LocalTuya 4CH switch — нет local_key
    "switch.smart_switch_4ch_switch_1",
    "switch.smart_switch_4ch_switch_2",
    "switch.smart_switch_4ch_switch_3",
    "switch.smart_switch_4ch_switch_4",
    "select.smart_switch_4ch_power_on_behavior",
    # Z2M phantom (уже удалены)
    "switch.zigbee2mqtt_bridge_permit_join",
    "button.zigbee2mqtt_bridge_restart",
    "select.zigbee2mqtt_bridge_log_level",
    "sensor.zigbee2mqtt_bridge_version",
    # ARGOS sensors без config entry в HA (интеграция удалена)
    "sensor.argos_laptop_disk",
    "sensor.argos_esp_bridge_ip",
    "sensor.argos_esp_bridge_uptime",
    "sensor.argos_esp_bridge_rssi",
}


def is_non_recoverable(entity_id: str) -> bool:
    """Не пытаемся heal то что не лечится рестартом (LocalTuya/Z2M phantom)."""
    if entity_id in NON_RECOVERABLE_ENTITIES:
        return True
    domain = entity_id.split(".")[0]
    if domain in NON_RECOVERABLE_DOMAINS:
        return True
    # По имени entity
    name = entity_id.lower()
    return any(kw in name for kw in ["smart_switch_4ch", "zigbee2mqtt_bridge_permit"])

# Глобальные метрики для TON Status Bot
_metrics = {
    "unavailable_total": 0,
    "skipped_non_recoverable": 0,
    "skipped_non_recoverable_by_reason": {},
    "top_skipped_entities": [],
    "soft_heal_attempts": 0,
    "soft_heal_success": 0,
    "hard_heal_attempts": 0,
    "hard_heal_success": 0,
    "last_updated": "",
}
METRICS_FILE = "/tmp/argos_watchdog_metrics.json"

def _save_metrics():
    try:
        with open(METRICS_FILE, "w") as f:
            json.dump(_metrics, f)
    except Exception as e:
        log.debug(f"Failed to save metrics: {e}")

HEAL_STATE = {}       # entity_id → {attempts, window_start}
HARD_HEAL_COOLDOWN = {}  # entity_id → last_hard_heal_time (per-entity!)
HARD_HEAL_MIN_INTERVAL = 3600  # 1 час между hard_heal для одной entity
MAX_ATTEMPTS_PER_HOUR = 3  # rate limit


def ha_api(method, path, data=None):
    body = json.dumps(data or {}).encode() if data is not None else None
    req = urllib.request.Request(
        f"{HA_BASE}/api{path}", data=body,
        headers={"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"},
        method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read()
            return r.status, json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        return e.code, {}
    except Exception:
        return 0, {}


def get_unavailable():
    status, states = ha_api("GET", "/states")
    if status != 200 or not isinstance(states, list): return []
    return [(s['entity_id'], s.get('state'), s.get('last_changed','')) 
            for s in states if s.get('state') == 'unavailable']


def can_heal(entity_id):
    """Rate limit: не более MAX_ATTEMPTS_PER_HOUR попыток."""
    now = time.time()
    state = HEAL_STATE.get(entity_id, {"attempts": 0, "window_start": now})
    
    # Сбрасываем счётчик если прошёл час
    if now - state["window_start"] > 3600:
        state = {"attempts": 0, "window_start": now}
    
    if state["attempts"] >= MAX_ATTEMPTS_PER_HOUR:
        return False
    
    state["attempts"] += 1
    HEAL_STATE[entity_id] = state
    return True


def soft_heal(entity_id):
    """Мягкое: reload конкретной интеграции через её реальный reload-сервис.

    HA reload service существует только у integration-доменов (mqtt, rest, automation
    и т.п.), но НЕ у базовых платформ (sensor/switch/binary_sensor/select/button/light).
    Поэтому базовые платформы лечатся через get_config_entry → reload_config_entry."""
    domain = entity_id.split(".")[0]
    # Только реальные reload-сервисы (см. /api/services 2026-05-23)
    RELOADABLE = {"mqtt", "rest", "automation", "script", "scene", "conversation",
                  "input_boolean", "input_button", "input_datetime", "input_number",
                  "input_select", "input_text", "person", "schedule", "timer", "zone"}
    if domain not in RELOADABLE:
        return False, f"domain {domain} has no reload service (base platform)"

    status, _ = ha_api("POST", f"/services/{domain}/reload")
    return status == 200, f"reload {domain} → {status}"


def hard_heal(entry_id):
    """Жёсткое: restart config entry."""
    status, _ = ha_api("POST", f"/config/config_entries/entry/{entry_id}/reload")
    return status == 200, f"config_entry reload → {status}"


def get_config_entry(entity_id):
    """Находим config entry для entity через homeassistant.reload_config_entry payload."""
    return None  # not used directly anymore — see hard_heal_by_entity()


def hard_heal_by_entity(entity_id):
    """Hard heal через homeassistant.reload_config_entry с entity_id — HA сам находит config_entry."""
    status, _ = ha_api("POST", "/services/homeassistant/reload_config_entry",
                       {"entity_id": entity_id})
    return status == 200, f"reload_config_entry entity={entity_id} → {status}"


def update_entity(entity_id):
    """Принудительно опросить состояние entity."""
    status, _ = ha_api("POST", "/services/homeassistant/update_entity",
                       {"entity_id": entity_id})
    return status == 200, f"update_entity {entity_id} → {status}"


def is_stale(last_changed: str, max_age_min: int = 3) -> bool:
    """Проверяем, что последнее изменение было не более max_age_min минут назад."""
    try:
        if not last_changed:
            return True
        changed_time = int(time.mktime(time.strptime(last_changed, "%Y-%m-%dT%H:%M:%S.%f")))
        now = int(time.time())
        return (now - changed_time) > (max_age_min * 60)
    except:
        return True


def process_unavailable():
    """Основной цикл: найти unavailable, определить recovery, heal."""
    unavailable_list = get_unavailable()
    _metrics["unavailable_total"] = len(unavailable_list)
    
    for entity_id, state, last_changed in unavailable_list:
        log.info(f"Found unavailable: {entity_id} (last_changed: {last_changed})")
        
        # Шаг 1: Проверка non-recoverable
        if is_non_recoverable(entity_id):
            log.warning(f"[SKIP] {entity_id} — non-recoverable (LocalTuya/Z2M phantom)")
            _metrics["skipped_non_recoverable"] += 1
            
            domain = entity_id.split(".")[0]
            reason_key = f"{domain}_not_reloadable"
            if reason_key not in _metrics["skipped_non_recoverable_by_reason"]:
                _metrics["skipped_non_recoverable_by_reason"][reason_key] = 0
            _metrics["skipped_non_recoverable_by_reason"][reason_key] += 1
            
            log_healing_event(
                entity=entity_id,
                action="skipped",
                result="skipped",
                reason="non_recoverable",
                domain=domain
            )
            continue
        
        # Шаг 2: Rate limit
        if not can_heal(entity_id):
            log.warning(f"[RATE_LIMIT] {entity_id} — max attempts per hour reached")
            log_healing_event(
                entity=entity_id,
                action="skipped",
                result="skipped",
                reason="rate_limit"
            )
            continue
        
        # Шаг 3: Soft heal — сначала update_entity (refresh без перезагрузки)
        if is_stale(last_changed, max_age_min=3):
            log.info(f"[SOFT_HEAL] {entity_id} — update_entity")
            _metrics["soft_heal_attempts"] += 1
            success, msg = update_entity(entity_id)
            if not success:
                # для integration-доменов с reload-сервисом
                success, msg = soft_heal(entity_id)

            if success:
                log.info(f"[SOFT_HEAL_SUCCESS] {entity_id}: {msg}")
                _metrics["soft_heal_success"] += 1
                log_healing_event(
                    entity=entity_id,
                    action="soft_heal",
                    result="success",
                    reason="stale"
                )
                continue
            else:
                log.warning(f"[SOFT_HEAL_FAILED] {entity_id}: {msg}")
                log_healing_event(
                    entity=entity_id,
                    action="soft_heal",
                    result="failed",
                    reason="stale"
                )

        # Шаг 4: Hard heal через homeassistant.reload_config_entry (с cooldown per-entity)
        now = time.time()
        last_hard_heal = HARD_HEAL_COOLDOWN.get(entity_id, 0)
        if now - last_hard_heal < HARD_HEAL_MIN_INTERVAL:
            log.warning(f"[HARD_HEAL_COOLDOWN] {entity_id} — in cooldown")
            log_healing_event(
                entity=entity_id,
                action="skipped",
                result="skipped",
                reason="hard_heal_cooldown"
            )
            continue

        log.info(f"[HARD_HEAL] {entity_id} — reload_config_entry by entity_id")
        _metrics["hard_heal_attempts"] += 1
        success, msg = hard_heal_by_entity(entity_id)

        if success:
            log.info(f"[HARD_HEAL_SUCCESS] {entity_id}: {msg}")
            _metrics["hard_heal_success"] += 1
            HARD_HEAL_COOLDOWN[entity_id] = now
            log_healing_event(
                entity=entity_id,
                action="hard_heal",
                result="success",
                reason="unavailable"
            )
        else:
            log.error(f"[HARD_HEAL_FAILED] {entity_id}: {msg}")
            log_healing_event(
                entity=entity_id,
                action="hard_heal",
                result="failed",
                reason="unavailable"
            )

    _metrics["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    _save_metrics()


def main():
    log.info("=== ARGOS HA Watchdog started ===")
    while True:
        try:
            process_unavailable()
        except Exception as e:
            log.error(f"Watchdog error: {e}", exc_info=True)
        
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()