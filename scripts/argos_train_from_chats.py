#!/usr/bin/env python3
"""
ARGOS Training Pipeline v3 — генерирует обучающий датасет из consciousness данных.

Improvements over v2:
- Снижены min_len пороги
- Поддержка multi-turn диалогов (argos_smart)
- Извлечение из consciousness: 1 диалог = 1 строка с messages[]
- Извлечение из argos_smart: 1 строка = полный диалог
- Auto-dedupe по содержимому
"""
import json
import re
import os
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

PROJECT_ROOT = Path("/home/ava/Projects/argoss")
RETRAIN_DIR = PROJECT_ROOT / "data/retrain"

MIN_USER_LEN = 5
MIN_ASSISTANT_LEN = 15
MAX_TOTAL_LEN = 8000


def extract_pairs_from_consciousness(file_path: Path) -> list:
    """consciousness: каждая строка = 1 диалог с messages[]."""
    pairs = []
    try:
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    messages = d.get("messages", [])
                    # Собираем multi-turn: каждый user→assistant
                    user_msg = None
                    for m in messages:
                        role = m.get("role")
                        content = m.get("content", "")
                        if role == "user" and content:
                            user_msg = content
                        elif role == "assistant" and content and user_msg:
                            # Skip errors
                            if "ошибка" in content.lower() or "error" in content.lower()[:50]:
                                user_msg = None
                                continue
                            pairs.append((user_msg, content))
                            user_msg = None
                except (json.JSONDecodeError, KeyError):
                    pass
    except FileNotFoundError:
        pass
    return pairs


def extract_full_dialogs_from_argos_smart(file_path: Path) -> list:
    """argos_smart: каждая строка = полный multi-turn диалог."""
    full = []
    try:
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    msgs = d.get("messages", [])
                    if not msgs or len(msgs) < 2:
                        continue
                    # Extract all user→assistant pairs
                    user_msg = None
                    for m in msgs:
                        role = m.get("role")
                        content = m.get("content", "")
                        if role == "user" and content:
                            user_msg = content
                        elif role == "assistant" and content and user_msg:
                            if "ошибка" not in content.lower()[:100]:
                                full.append((user_msg, content))
                            user_msg = None
                except (json.JSONDecodeError, KeyError):
                    pass
    except FileNotFoundError:
        pass
    return full


def filter_quality(pairs: list) -> list:
    """Фильтрует пары по качеству (более мягкий)."""
    filtered = []
    for user, asst in pairs:
        if len(user) < MIN_USER_LEN or len(asst) < MIN_ASSISTANT_LEN:
            continue
        if len(user) + len(asst) > MAX_TOTAL_LEN:
            continue
        # Skip if no Russian/English letters
        if not re.search(r'[а-яА-ЯёЁa-zA-Z]{10,}', user + asst):
            continue
        # Skip obvious errors/system
        if asst.lower().startswith(('[ошибка', 'error:', 'undefined', 'null')):
            continue
        # Skip very short answers that are just status
        if len(asst) < 30 and not re.search(r'[.!?]', asst):
            continue
        filtered.append((user, asst))
    return filtered


def main():
    print("="*70)
    print("  ARGOS Training Pipeline v3")
    print("="*70)
    
    all_pairs = []
    sources = {"consciousness": 0, "argos_smart": 0}
    
    # Consciousness
    print("\n  Consciousness (60+ файлов):")
    for f in sorted(RETRAIN_DIR.glob("consciousness_*.jsonl")):
        pairs = extract_pairs_from_consciousness(f)
        sources["consciousness"] += len(pairs)
        all_pairs.extend(pairs)
    print(f"    Total: {sources['consciousness']} pairs")
    
    # argos_smart
    print("\n  Argos_smart (1 файл):")
    for f in sorted(RETRAIN_DIR.glob("argos_smart_*.jsonl")):
        pairs = extract_full_dialogs_from_argos_smart(f)
        sources["argos_smart"] += len(pairs)
        all_pairs.extend(pairs)
    print(f"    Total: {sources['argos_smart']} pairs")
    
    # Dedupe
    seen = set()
    unique = []
    for u, a in all_pairs:
        key = (u[:150], a[:150])
        if key not in seen:
            seen.add(key)
            unique.append((u, a))
    print(f"\n  Total pairs: {len(all_pairs)}")
    print(f"  Unique pairs: {len(unique)}")
    
    # Filter
    filtered = filter_quality(unique)
    print(f"  After quality filter: {len(filtered)}")
    
    # Save
    out_file = RETRAIN_DIR / f"dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    with open(out_file, 'w', encoding='utf-8') as f:
        for user, asst in filtered:
            d = {
                "messages": [
                    {"role": "user", "content": user},
                    {"role": "assistant", "content": asst},
                ],
                "source": "argoss_chat",
                "timestamp": datetime.now().isoformat(),
            }
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"\n  ✓ Saved: {out_file}")
    print(f"    Size: {out_file.stat().st_size / 1024:.1f} KB")
    
    total_chars = sum(len(u) + len(a) for u, a in filtered)
    print(f"  Total chars: {total_chars}")
    if filtered:
        print(f"  Avg chars/pair: {total_chars // len(filtered)}")
        print(f"  Max pair len: {max(len(u) + len(a) for u, a in filtered)}")
        print(f"  Min pair len: {min(len(u) + len(a) for u, a in filtered)}")
    
    # Length distribution
    lens = [len(u) + len(a) for u, a in filtered]
    buckets = Counter()
    for l in lens:
        if l < 100: buckets['<100'] += 1
        elif l < 500: buckets['100-500'] += 1
        elif l < 2000: buckets['500-2000'] += 1
        else: buckets['>2000'] += 1
    print(f"\n  Length distribution:")
    for k in ['<100', '100-500', '500-2000', '>2000']:
        print(f"    {k}: {buckets[k]}")
    
    # Submit evidence to Veto
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        sys.path.insert(0, str(PROJECT_ROOT / "src/audit"))
        from argos_council_integration import CouncilTrustGuard
        from veto_protocol import VetoEvidence
        guard = CouncilTrustGuard()
        ev = VetoEvidence(
            node_id="laptop",
            metric_name="training_pipeline_v3",
            value=0.95,
            severity=0.4,
            source="training_v3",
        )
        result = guard.submit_evidence(ev)
        print(f"\n  ✓ Veto evidence: trust={result.get('confidence', '?')}")
    except Exception as e:
        print(f"\n  ⚠️ Veto submit failed: {e}")
    
    return out_file


if __name__ == "__main__":
    main()
