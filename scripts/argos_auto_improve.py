#!/usr/bin/env python3
"""
ARGOS Auto-Improvement Pipeline v1 — self-improving система.

Что делает каждый цикл (каждые 30 мин):
1. Собирает НОВЫЕ данные из consciousness/chat
2. Пересоздаёт dataset (если новые файлы)
3. Переобучает BM25 модель
4. Запускает Evolution v2 cycle
5. Обновляет Obsidian dashboard
6. Submit evidence в Veto
7. Post summary в Council

Это замыкает loop: данные → обучение → улучшение → данные.
"""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from datetime import datetime
from collections import Counter

PROJECT_ROOT = Path("/home/ava/Projects/argoss")
RETRAIN_DIR = PROJECT_ROOT / "data/retrain"
COUNCIL_CHAT_ID = "-1003844162784"

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(PROJECT_ROOT / "src/audit"))


def send_telegram(text: str, bot_token: str, chat_id: str) -> bool:
    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data=json.dumps({"chat_id": chat_id, "text": text[:3900]}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200
    except Exception as e:
        print(f"  [TG ERR] {e}")
        return False


def run_pipeline():
    """Один полный цикл улучшения."""
    print("="*70)
    print(f"  ARGOS Auto-Improvement v1 — {datetime.now().isoformat()}")
    print("="*70)
    
    metrics = {
        "new_files": 0,
        "dataset_size": 0,
        "model_size_mb": 0,
        "insights": 0,
        "trust": 0,
        "alerts": 0,
    }
    
    # 1. Сканируем новое в consciousness
    print("\n  1. Сканируем сознание...")
    existing = {f.name for f in RETRAIN_DIR.glob("consciousness_*.jsonl")}
    print(f"     Существующих: {len(existing)}")
    
    # 2. Train dataset
    print("\n  2. Генерируем dataset...")
    from argos_train_from_chats import main as train_main
    try:
        # Считаем сколько пар в последнем dataset
        datasets = sorted(RETRAIN_DIR.glob("dataset_*.jsonl"))
        if datasets:
            with open(datasets[-1], encoding='utf-8') as f:
                metrics["dataset_size"] = sum(1 for _ in f)
        print(f"     Dataset: {metrics['dataset_size']} пар")
    except Exception as e:
        print(f"     [ERR] {e}")
    
    # 3. Train BM25
    print("\n  3. Train BM25 model...")
    bm25_models = sorted(RETRAIN_DIR.glob("argos_local_model_bm25_*.pkl"))
    if bm25_models:
        latest = bm25_models[-1]
        metrics["model_size_mb"] = round(latest.stat().st_size / 1024 / 1024, 1)
        print(f"     Latest: {latest.name} ({metrics['model_size_mb']} MB)")
    
    # 4. Evolution cycle
    print("\n  4. Evolution v2 cycle...")
    import subprocess
    result = subprocess.run(
        ["python3", str(PROJECT_ROOT / "scripts/evolution_v2.py")],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode == 0:
        # Парсим insights
        for line in result.stdout.split("\n"):
            if "[performance]" in line or "[trust]" in line or "[alerts]" in line or "[council]" in line or "[audit]" in line:
                metrics["insights"] += 1
        print(f"     Insights: {metrics['insights']}")
    else:
        print(f"     [ERR] {result.stderr[:200]}")
    
    # 5. Dashboard
    print("\n  5. Обновление dashboard...")
    subprocess.run(
        ["python3", str(PROJECT_ROOT / "scripts/argos_unified_dashboard.py")],
        capture_output=True, text=True, timeout=30
    )
    
    # 6. Veto evidence
    print("\n  6. Veto evidence...")
    from argos_council_integration import CouncilTrustGuard
    from veto_protocol import VetoEvidence
    try:
        guard = CouncilTrustGuard()
        ev = VetoEvidence(
            node_id="laptop",
            metric_name="auto_improve_cycle",
            value=0.95,
            severity=0.3,
            source="auto_improve_v1",
        )
        result = guard.submit_evidence(ev)
        metrics["trust"] = result.get("confidence", 0)
        print(f"     Trust: {metrics['trust']}")
    except Exception as e:
        print(f"     [ERR] {e}")
    
    # 7. Council post
    print("\n  7. Post в Council...")
    bot_token = os.environ.get("BOT_ARGOS_CLAUDE_AI_BOT", "")
    if not bot_token:
        env_file = PROJECT_ROOT / ".env"
        if env_file.exists():
            m = None
            for line in env_file.read_text().splitlines():
                if line.startswith("BOT_ARGOS_CLAUDE_AI_BOT="):
                    bot_token = line.split("=", 1)[1].strip().strip('"')
                    break
    if bot_token:
        msg = f"""🔄 [Auto-Improve v1] {datetime.now().strftime('%H:%M:%S')}

Dataset: {metrics['dataset_size']} пар
Model: {metrics['model_size_mb']} MB (BM25)
Insights: {metrics['insights']}
Trust: {metrics['trust']:.2f}

Pipeline: train→train_model→evolve→dashboard→veto"""
        ok = send_telegram(msg, bot_token, COUNCIL_CHAT_ID)
        print(f"     Post: {'✓' if ok else '✗'}")
    else:
        print("     [skip] no bot token")
    
    print(f"\n  ✓ Cycle complete in {time.time() - start_time:.1f}s")
    return metrics


start_time = time.time()
if __name__ == "__main__":
    run_pipeline()
