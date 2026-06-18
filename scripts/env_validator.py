#!/usr/bin/env python3
"""ARGOS .env Validator — проверяет конфигурацию при старте.

Запуск: python3 scripts/env_validator.py
Код выхода: 0 = OK, 1 = предупреждения, 2 = критические ошибки
"""
import os
import re
import sys
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"

PLACEHOLDER_PATTERNS = [
    r"^your[_-]?key",
    r"^changeme$",
    r"^xxx+$",
    r"^INSERT_",
    r"^REPLACE_",
    r"^TODO",
    r"^get[_-]?your",
    r"^sk-\s*$",
    r"^test[_-]",
    r"^example",
    r"^placeholder",
    r"^fake",
    r"^dummy",
    r"^none$",
    r"^null$",
    r"^n/a$",
]

CRITICAL_KEYS = [
    "DEEPSEEK_API_KEY",
    "KIMI_API_KEY",
    "OLLAMA_HOST",
    "ARGOS_AI_MODE",
]

DISABLE_KEYS_PATTERN = re.compile(r"^ARGOS_DISABLE_(\w+)=")
ENABLE_KEYS_PATTERN = re.compile(r"^ARGOS_AI_PRIORITY=")


def parse_env(path: Path) -> dict:
    """Parse .env file, returning {key: [(line_num, value)]}."""
    entries = {}
    if not path.exists():
        print(f"❌ Файл {path} не найден!")
        sys.exit(2)
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Z_][A-Z0-9_]*)=(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"').strip("'")
            entries.setdefault(key, []).append((i, val))
    return entries


def is_placeholder(value: str) -> bool:
    lower = value.lower()
    for pat in PLACEHOLDER_PATTERNS:
        if re.match(pat, lower):
            return True
    return False


def main():
    entries = parse_env(ENV_PATH)
    errors = []
    warnings = []

    # 1. Duplicate keys
    for key, occurrences in entries.items():
        if len(occurrences) > 1:
            lines = ", ".join(str(l) for l, _ in occurrences)
            vals = set(v for _, v in occurrences)
            if len(vals) > 1:
                msg = f"🔴 {key}: дубликат с РАЗНЫМИ значениями (строки {lines})"
                errors.append(msg)
            else:
                msg = f"🟡 {key}: дубликат с одинаковыми значениями (строки {lines})"
                warnings.append(msg)

    # 2. Placeholder values
    for key, occurrences in entries.items():
        for line, val in occurrences:
            if is_placeholder(val):
                msg = f"🔴 {key}={val} (строка {line}): placeholder значение!"
                errors.append(msg)

    # 3. Empty critical keys
    for key in CRITICAL_KEYS:
        if key not in entries:
            msg = f"🔴 {key}: отсутствует в .env!"
            errors.append(msg)
        elif entries[key][0][1] == "":
            msg = f"🔴 {key}: пустое значение!"
            errors.append(msg)

    # 4. Gemini keys (5 keys but geo-blocked)
    gemini_keys = [k for k in entries if k.startswith("GEMINI_API_KEY")]
    if gemini_keys and entries.get("ARGOS_DISABLE_GEMINI", [(0, "0")])[0][1] == "0":
        warnings.append(f"🟡 Gemini включён ({len(gemini_keys)} ключей), но geo-blocked в РФ")

    # 5. Disabled providers that still have keys
    provider_map = {
        "GROK": "XAI_API_KEY",
        "OPENAI": "OPENAI_API_KEY",
        "WATSONX": "WATSONX_API_KEY",
        "GIGACHAT": "GIGACHAT_CLIENT_ID",
        "GROQ": "GROQ_API_KEY",
        "YANDEX": "YANDEX_IAM_TOKEN",
    }
    for prov, key in provider_map.items():
        disable_key = f"ARGOS_DISABLE_{prov}"
        if disable_key in entries and entries[disable_key][0][1] == "1":
            # Check if key exists and is non-empty
            if key in entries and entries[key][0][1] not in ("", "None", "none"):
                warnings.append(f"🟡 {prov}: отключён, но {key} задан — рассмотрите удаление ключа")

    # 6. AI_MODE sanity
    mode = entries.get("ARGOS_AI_MODE", [(0, "")])[0][1]
    if mode not in ("auto", "ollama", "cloud", "local"):
        warnings.append(f"🟡 ARGOS_AI_MODE={mode} — неизвестный режим")

    # 7. Provider failure cooldown too aggressive
    cooldown = entries.get("ARGOS_PROVIDER_FAILURE_COOLDOWN", [(0, "300")])[0][1]
    if cooldown and int(cooldown) > 120:
        warnings.append(f"🟡 ARGOS_PROVIDER_FAILURE_COOLDOWN={cooldown}s — слишком долго, рекомендую ≤120s")

    # Report
    print("=" * 60)
    print("🔍 ARGOS .env Validator")
    print("=" * 60)
    print(f"Файл: {ENV_PATH}")
    print(f"Записей: {len(entries)} уникальных ключей")
    print()

    if errors:
        print(f"🔴 КРИТИЧЕСКИЕ ОШИБКИ ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        print()

    if warnings:
        print(f"🟡 ПРЕДУПРЕЖДЕНИЯ ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")
        print()

    if not errors and not warnings:
        print("✅ .env валиден — проблем не найдено!")
    else:
        active = sum(1 for k, v in entries.items() if k.startswith("ARGOS_DISABLE_") and v[0][1] == "0")
        disabled = sum(1 for k, v in entries.items() if k.startswith("ARGOS_DISABLE_") and v[0][1] == "1")
        print(f"📊 Провайдеры: {active} активных, {disabled} отключённых")
        print(f"📋 Приоритет: {entries.get('ARGOS_AI_PRIORITY', [(0, '?')])[0][1]}")

    print("=" * 60)
    return 2 if errors else (1 if warnings else 0)


if __name__ == "__main__":
    sys.exit(main())