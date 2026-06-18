"""
Argos Compressor — Pure-Python контекст-компрессор для ARGOS.
Аналог headroom SmartCrusher (JSON) без Rust-зависимостей.

Стратегии:
  - json_array: массив словарей → свёрнутая таблица
  - json_nested: вложенный JSON → flatten + сокращение ключей
  - logs: обрезка повторяющихся строк
  - text: truncate с сохранением структуры
  - passthrough: без изменений (маленький объём)

Usage:
    from argos_compressor import ArgosCompressor
    c = ArgosCompressor()
    result = c.compress(large_json_string, max_chars=4000)
    print(result.text)
    print(result.stats)
"""

from __future__ import annotations

import json, re, hashlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class CompressResult:
    text: str
    original_chars: int = 0
    compressed_chars: int = 0
    strategy: str = "unknown"
    stats: Dict[str, Any] = field(default_factory=dict)

    @property
    def ratio(self) -> float:
        if self.original_chars == 0:
            return 1.0
        return self.compressed_chars / self.original_chars

    @property
    def savings_pct(self) -> float:
        return (1.0 - self.ratio) * 100


class ArgosCompressor:
    """Main entry point for ARGOS context compression."""

    def __init__(
        self,
        max_chars: int = 4000,
        preserve_errors: bool = True,
        preserve_last_n: int = 5,
        array_item_limit: int = 20,
        dedupe_similarity: float = 0.85,
    ):
        self.max_chars = max_chars
        self.preserve_errors = preserve_errors
        self.preserve_last_n = preserve_last_n
        self.array_item_limit = array_item_limit
        self.dedupe_similarity = dedupe_similarity

    # ── Public API ──────────────────────────────────────────────────────

    def compress(self, raw: str, max_chars: Optional[int] = None) -> CompressResult:
        """Auto-detect content type and compress."""
        limit = max_chars or self.max_chars
        original_len = len(raw)

        if original_len <= limit:
            return CompressResult(
                text=raw,
                original_chars=original_len,
                compressed_chars=original_len,
                strategy="passthrough",
                stats={"reason": "under_limit"},
            )

        # Detect strategy
        strategy = self._detect_strategy(raw)

        if strategy == "json_array":
            text = self._compress_json_array(raw, limit)
        elif strategy == "json_nested":
            text = self._compress_json_nested(raw, limit)
        elif strategy == "logs":
            text = self._compress_logs(raw, limit)
        else:
            text = self._compress_text(raw, limit)

        compressed_len = len(text)
        stats = {
            "original_chars": original_len,
            "compressed_chars": compressed_len,
            "savings_pct": round((1 - compressed_len / original_len) * 100, 1),
            "strategy": strategy,
        }

        return CompressResult(
            text=text,
            original_chars=original_len,
            compressed_chars=compressed_len,
            strategy=strategy,
            stats=stats,
        )

    compress_json = compress  # alias

    # ── Strategy Detection ──────────────────────────────────────────────

    def _detect_strategy(self, raw: str) -> str:
        s = raw.strip()

        # Try JSON first
        try:
            obj = json.loads(s)
        except json.JSONDecodeError:
            obj = None

        if isinstance(obj, list) and len(obj) > 1 and isinstance(obj[0], dict):
            return "json_array"
        if isinstance(obj, dict):
            return "json_nested"

        # Log detection: repeated prefix patterns
        lines = s.splitlines()
        if len(lines) >= 10:
            repeats = sum(
                1
                for i in range(1, min(30, len(lines)))
                if lines[i][:15] == lines[i - 1][:15]
            )
            if repeats >= 5:
                return "logs"

        return "text"

    # ── JSON Array ────────────────────────────────────────────────────

    def _compress_json_array(self, raw: str, limit: int) -> str:
        """Compress array of dicts → columnar summary."""
        try:
            arr = json.loads(raw)
        except json.JSONDecodeError:
            return self._compress_text(raw, limit)

        if not isinstance(arr, list):
            return self._compress_text(raw, limit)

        total = len(arr)
        if total == 0:
            return "[]"

        # Collect all keys, compute column widths
        keys = list(arr[0].keys()) if isinstance(arr[0], dict) else ["item"]
        rows: List[Dict[str, Any]] = []

        for item in arr[: self.array_item_limit]:
            if isinstance(item, dict):
                rows.append({k: self._shorten_val(item.get(k, "")) for k in keys})
            else:
                rows.append({"item": self._shorten_val(item)})

        # Build compact table
        lines = ["--- JSON ARRAY ---"]
        lines.append(f"Items: {total} total")
        if total > self.array_item_limit:
            lines.append(f"  (showing first {self.array_item_limit})")

        # Header
        header = " | ".join(self._shorten_key(k) for k in keys)
        lines.append(header)
        lines.append("-" * len(header))

        # Rows
        for row in rows:
            line = " | ".join(
                str(row.get(k, ""))[:25] for k in keys
            )
            lines.append(line)

        if total > self.array_item_limit:
            lines.append(f"[{total - self.array_item_limit} more items...]")

        return "\n".join(lines)

    # ── JSON Nested ────────────────────────────────────────────────────

    def _compress_json_nested(self, raw: str, limit: int) -> str:
        """Flatten nested dict, shorten keys, truncate long values."""
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            return self._compress_text(raw, limit)

        if not isinstance(obj, dict):
            return self._compress_text(raw, limit)

        flat = self._flatten_dict(obj, depth=0)
        lines = ["--- JSON OBJECT ---"]
        for key, val in flat.items():
            v_str = self._shorten_val(val)
            if len(v_str) > 60:
                v_str = v_str[:57] + "..."
            lines.append(f"{key}: {v_str}")

        return "\n".join(lines)

    # ── Logs ──────────────────────────────────────────────────────────

    def _compress_logs(self, raw: str, limit: int) -> str:
        """Group identical log lines, keep first N + last N.
        Fixes: don't bloat on scattered error lines — collect them separately.
        """
        lines = raw.splitlines()
        if len(lines) <= self.preserve_last_n * 2 + 5:
            return raw  # too short to compress

        # Separate error/fatal lines (always preserved)
        normal_lines: List[str] = []
        error_lines: List[Tuple[int, str]] = []
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(kw in line_lower for kw in ("error", "fatal", "exception", "traceback", "failed")):
                error_lines.append((i + 1, line))
            else:
                normal_lines.append(line)

        def _pattern(line: str) -> str:
            # Strip timestamps, hexes, IDs
            s = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}\S*", r"TIME", line)
            s = re.sub(r"0x[0-9a-fA-F]{4,}", "ADDR", s)
            s = re.sub(r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", "UUID", s)
            s = re.sub(r"\b[0-9a-f]{32,}\b", "HASH", s)
            # collapse numbers in brackets or after =
            s = re.sub(r"\d+", "N", s)
            return s

        # Group normal lines by pattern
        groups: List[Tuple[str, int, int]] = []
        if normal_lines:
            current_pattern = _pattern(normal_lines[0])
            current_start = 0
            for i in range(1, len(normal_lines)):
                pat = _pattern(normal_lines[i])
                if pat == current_pattern:
                    continue
                groups.append((current_pattern, current_start, i - current_start))
                current_pattern = pat
                current_start = i
            groups.append((current_pattern, current_start, len(normal_lines) - current_start))

        # Build output — smart grouping: if group is small (≤3), keep inline; if large, collapse
        out: List[str] = []
        out.append(f"--- LOG COMPRESSION ({len(lines)} lines → {len(normal_lines)} normal + {len(error_lines)} errors) ---")

        for pat, start, count in groups:
            if count <= 3:
                for j in range(start, start + count):
                    out.append(normal_lines[j])
            else:
                out.append(f"[{normal_lines[start][:60]}]")
                out.append(f"  ... ({count} identical TIME-pattern lines) ...")
                out.append(f"[{normal_lines[start + count - 1][:60]}]")

        if error_lines:
            out.append(f"\n--- {len(error_lines)} ERROR/FATAL LINES ---")
            for ln, line in error_lines:
                out.append(f"L{ln}: {line}")

        return "\n".join(out)

    # ── Text ──────────────────────────────────────────────────────────

    def _compress_text(self, raw: str, limit: int) -> str:
        """Simple truncate with ellipsis and indicator."""
        if len(raw) <= limit:
            return raw
        head = int(limit * 0.6)
        tail = int(limit * 0.3)
        return raw[:head] + "\n\n... [truncated " + str(len(raw) - head - tail) + " chars] ...\n\n" + raw[-tail:]

    # ── Helpers ────────────────────────────────────────────────────────

    def _flatten_dict(self, obj: Any, prefix: str = "", depth: int = 0) -> Dict[str, Any]:
        """Flatten nested dicts, max depth 3."""
        if depth >= 3:
            return {prefix: json.dumps(obj)[:50] + "..."}

        flat: Dict[str, Any] = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    flat.update(self._flatten_dict(v, key, depth + 1))
                elif isinstance(v, list) and len(v) > 3:
                    flat[key] = f"[array: {len(v)} items]"
                else:
                    flat[key] = v
        elif isinstance(obj, list):
            flat[prefix] = f"[array: {len(obj)} items]"
        else:
            flat[prefix] = obj
        return flat

    def _shorten_key(self, key: str) -> str:
        """Shorten common JSON keys."""
        abbrevs = {
            "description": "desc",
            "timestamp": "ts",
            "message": "msg",
            "configuration": "cfg",
            "address": "addr",
            "authentication": "auth",
            "authorization": "authz",
            "username": "user",
            "password": "pass",
            "identifier": "id",
            "namespace": "ns",
            "environment": "env",
            "application": "app",
            "environment": "env",
            "information": "info",
            "parameter": "param",
            "reference": "ref",
            "resource": "res",
            "response": "resp",
            "request": "req",
            "metadata": "meta",
        }
        return abbrevs.get(key.lower(), key[:12] if len(key) > 12 else key)

    def _shorten_val(self, val: Any) -> str:
        """Shorten value for display."""
        if val is None:
            return "-"
        if isinstance(val, bool):
            return "T" if val else "F"
        if isinstance(val, (int, float)):
            s = str(val)
            return s[:12] if len(s) > 12 else s
        if isinstance(val, str):
            if val.startswith("http") and len(val) > 30:
                return val[:30] + "..."
            if len(val) > 40:
                return val[:37] + "..."
            return val
        if isinstance(val, list):
            return f"[{len(val)}]"
        if isinstance(val, dict):
            return f"{{{len(val)} keys}}"
        return str(val)[:30]


# ── MCP Middleware ──────────────────────────────────────────────────

class ArgosMCPMiddleware:
    """Wraps MCP tool calls to compress outputs before LLM context."""

    def __init__(self, compressor: Optional[ArgosCompressor] = None, **kw: Any):
        self.compressor = compressor or ArgosCompressor(**kw)

    def wrap(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
        raw_output: str,
        user_query: str = "",
    ) -> CompressResult:
        """Compress tool output, preserving errors if configured."""
        result = self.compressor.compress(raw_output)
        result.stats["tool_name"] = tool_name
        return result


# ── Standalone CLI ─────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python argos_compressor.py '<json_or_text>' [max_chars]")
        sys.exit(1)

    raw = sys.argv[1]
    max_c = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    c = ArgosCompressor(max_chars=max_c)
    res = c.compress(raw)
    print(f"=== Strategy: {res.strategy} | Savings: {res.savings_pct:.0f}% ===")
    print(res.text)
    print(f"\nStats: {json.dumps(res.stats, indent=2)}")
