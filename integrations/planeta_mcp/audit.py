from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


_REDACT = "[REDACTED]"
_SENSITIVE_TERMS = {
    "password",
    "cookie",
    "cookies",
    "authorization",
    "token",
    "secret",
    "passport",
    "inn",
    "document",
    "session",
    "storage_state",
}


def _is_sensitive_key(key: object) -> bool:
    normalized = str(key).strip().lower().replace("-", "_")
    return any(term in normalized for term in _SENSITIVE_TERMS)


def sanitize_for_audit(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): (_REDACT if _is_sensitive_key(key) else sanitize_for_audit(item))
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [sanitize_for_audit(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


class AuditLogger:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def record(
        self,
        tool: str,
        campaign_id: str,
        status: str,
        result: dict[str, Any],
    ) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool": tool,
            "campaign_id": campaign_id,
            "status": status,
            "result": sanitize_for_audit(result),
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
