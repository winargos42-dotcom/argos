#!/usr/bin/env python3
"""
ARGOS Trust Predictor v1 — ML-based trust prediction.

Предсказывает trust score на основе:
- Исторических evidence
- Recency (новые evidence важнее)
- Severity (высокая severity = низкий trust)
- Source reliability
- Consensus (много источников = стабильнее)
"""
import json
import math
import os
import sys
import time
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path("/home/ava/Projects/argoss")
sys.path.insert(0, str(PROJECT_ROOT / "src/audit"))


def get_trust(node_id):
    try:
        with urllib.request.urlopen(f"http://localhost:5010/trust/{node_id}", timeout=3) as r:
            return json.loads(r.read())
    except:
        return None


def get_evidence(node_id):
    try:
        with urllib.request.urlopen(f"http://localhost:5010/trust/{node_id}/evidence", timeout=3) as r:
            return json.loads(r.read())
    except:
        return []


def get_metrics():
    try:
        with urllib.request.urlopen("http://localhost:19090/metrics", timeout=3) as r:
            text = r.read().decode()
        m = {}
        for line in text.split("\n"):
            if line and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        m[parts[0]] = float(parts[1])
                    except:
                        pass
        return m
    except:
        return {}


def predict_trust_for_node(node_id):
    """Предсказать trust score для ноды."""
    trust = get_trust(node_id)
    evidence = get_evidence(node_id)
    
    if not trust:
        return None
    
    base_conf = trust.get("confidence", 0.5)
    is_quarantined = trust.get("is_quarantined", False)
    
    if not evidence:
        return {
            "node_id": node_id,
            "current": base_conf,
            "predicted": base_conf,
            "trend": "stable",
            "factors": {"no_evidence": 1.0},
        }
    
    now = time.time()
    
    # Recency-weighted severity
    weighted_severity = 0
    total_weight = 0
    severities = []
    sources = defaultdict(int)
    metrics = defaultdict(list)
    
    for e in evidence:
        ts = e.get("timestamp", 0)
        recency = math.exp(-(now - ts) / 86400)  # decay 1 day
        sev = e.get("severity", 0)
        source = e.get("source", "unknown")
        metric = e.get("metric_name", "unknown")
        
        weighted_severity += sev * recency
        total_weight += recency
        severities.append(sev)
        sources[source] += 1
        metrics[metric].append(sev)
    
    if total_weight > 0:
        avg_severity = weighted_severity / total_weight
    else:
        avg_severity = 0
    
    # Prediction: lower severity = higher trust
    severity_factor = 1 - min(avg_severity, 1.0)
    
    # Diversity factor: more sources = more reliable
    diversity = min(len(sources) / 5, 1.0)
    
    # Volume factor: more evidence = more stable
    volume = min(len(evidence) / 20, 1.0)
    
    # Trend: compare recent vs old
    recent = [e for e in evidence if now - e.get("timestamp", 0) < 86400 * 3]
    older = [e for e in evidence if now - e.get("timestamp", 0) >= 86400 * 3]
    recent_sev = sum(e.get("severity", 0) for e in recent) / max(len(recent), 1)
    older_sev = sum(e.get("severity", 0) for e in older) / max(len(older), 1)
    if recent_sev < older_sev * 0.8:
        trend = "improving"
    elif recent_sev > older_sev * 1.2:
        trend = "degrading"
    else:
        trend = "stable"
    
    predicted = base_conf * 0.4 + severity_factor * 0.3 + diversity * 0.15 + volume * 0.15
    
    if is_quarantined:
        predicted = min(predicted, 0.3)
    
    return {
        "node_id": node_id,
        "current": round(base_conf, 3),
        "predicted": round(predicted, 3),
        "trend": trend,
        "factors": {
            "severity": round(severity_factor, 3),
            "diversity": round(diversity, 3),
            "volume": round(volume, 3),
            "evidence_count": len(evidence),
            "unique_sources": len(sources),
        },
    }


def main():
    print("="*70)
    print("  ARGOS Trust Predictor v1")
    print("="*70)
    
    nodes = ["orion", "nexus", "egida", "pico", "esp32", "android", "phone-redmi", "entity-valenok", "laptop"]
    
    print(f"\n  Predictions for {len(nodes)} nodes:\n")
    
    predictions = []
    for n in nodes:
        p = predict_trust_for_node(n)
        if p:
            predictions.append(p)
            
            cur = p["current"]
            pred = p["predicted"]
            trend = p["trend"]
            
            arrow = "→"
            if pred > cur + 0.05:
                arrow = "↑"
            elif pred < cur - 0.05:
                arrow = "↓"
            
            trend_icon = {"improving": "📈", "degrading": "📉", "stable": "➡️"}.get(trend, "?")
            print(f"  {n:20s}  {cur:.3f} {arrow} {pred:.3f}  {trend_icon} {trend}")
    
    # Sort by biggest differences
    predictions.sort(key=lambda p: abs(p["predicted"] - p["current"]), reverse=True)
    
    print(f"\n  Top 3 biggest predicted changes:")
    for p in predictions[:3]:
        diff = p["predicted"] - p["current"]
        print(f"    {p['node_id']}: {p['current']:.3f} → {p['predicted']:.3f} (Δ {diff:+.3f}) {p['trend']}")
    
    # Save
    out = PROJECT_ROOT / f"data/evolution/trust_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(predictions, indent=2, ensure_ascii=False))
    print(f"\n  ✓ Saved: {out}")


if __name__ == "__main__":
    main()
