#!/usr/bin/env python3
"""
ARGOS Evolution Engine v2 — самообучающаяся система.

Интеграция с VetoProtocol + AuditLog + Trust:
1. Анализирует audit log — какие действия успешны, какие fail
2. Смотрит trust scores — какие ноды надёжны
3. Submit evidence в Veto на основе паттернов
4. Генерирует рекомендации для Council

Запускается каждые 30 мин через systemd timer.
"""
import sys, os, time, json, re, urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional

PROJECT_ROOT = Path(os.path.expanduser("~/Projects/argoss"))
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(PROJECT_ROOT / "src/audit"))

AUDIT_API = "http://localhost:5010"
PROMETHEUS = "http://localhost:19090"
BRAIN_API = "http://192.168.1.53:5001"
OUT_DIR = PROJECT_ROOT / "data/evolution"
OUT_DIR.mkdir(exist_ok=True, parents=True)


def get_json(url: str, timeout: int = 10) -> Optional[Dict]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"⚠️ GET {url}: {e}")
        return None


def get_text(url: str, timeout: int = 10) -> Optional[str]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.read().decode()
    except Exception as e:
        return None


class EvolutionEngineV2:
    """Self-improving system: анализ паттернов → рекомендации → Veto evidence."""
    
    def __init__(self):
        self.session_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self.learnings: List[Dict[str, Any]] = []
        self.recommendations: List[Dict[str, Any]] = []
        self.evidence_submitted: List[Dict[str, Any]] = []
    
    def fetch_metrics(self) -> Dict[str, float]:
        """Читает метрики из Brain API (Prometheus отключён)."""
        metrics = {}
        # Brain /system: GPU, RAM
        try:
            data = get_json(f"{BRAIN_API}/system")
            if data:
                if data.get("ram_used") is not None:
                    metrics["argos_ram_percent"] = float(data["ram_used"])
                if data.get("gpu_temp") is not None:
                    metrics["argos_gpu_temp"] = float(data["gpu_temp"])
                if data.get("gpu_vram") is not None:
                    metrics["argos_gpu_vram_mb"] = float(data["gpu_vram"])
        except Exception:
            pass
        # Laptop CPU/RAM через psutil напрямую
        try:
            import psutil
            metrics["argos_cpu_percent"] = psutil.cpu_percent(interval=0.5)
            metrics["argos_ram_percent"] = psutil.virtual_memory().percent
            metrics["argos_disk_percent"] = psutil.disk_usage("/").percent
        except Exception:
            pass
        # Brain nodes — считаем offline как сигнал
        try:
            data = get_json(f"{BRAIN_API}/brain/nodes")
            if data:
                total = data.get("total", 0)
                online = data.get("online", 0)
                offline = total - online
                metrics["argos_nodes_total"] = float(total)
                metrics["argos_nodes_online"] = float(online)
                metrics["argos_nodes_offline"] = float(offline)
        except Exception:
            pass
        return metrics
    
    def fetch_audit_events(self, since: float = None) -> List[Dict]:
        """Читает audit events с фильтром по времени."""
        url = f"{AUDIT_API}/audit/query?min_severity=INFO&limit=200"
        if since:
            url += f"&since={since}"
        data = get_json(url)
        return data if isinstance(data, list) else []
    
    def fetch_trust(self) -> Dict[str, Dict]:
        """Trust scores всех нод через HTTP API."""
        data = get_json(f"{AUDIT_API}/trust")
        if not isinstance(data, list):
            return {}
        return {n["node_id"]: n for n in data}
    
    def fetch_alerts(self) -> List[Dict]:
        """Активные алерты."""
        data = get_json(f"{AUDIT_API}/alerts?min_severity=LOW")
        return data if isinstance(data, list) else []
    
    def analyze_patterns(self, metrics: Dict, trust: Dict, events: List) -> List[Dict]:
        """Анализ паттернов → список insights."""
        insights = []
        
        # Insight 1: CPU/RAM/Disk thresholds
        cpu = metrics.get("argos_cpu_percent", 0)
        ram = metrics.get("argos_ram_percent", 0)
        disk = metrics.get("argos_disk_percent", 0)
        if cpu > 70:
            insights.append({
                "type": "performance",
                "severity": "high" if cpu > 85 else "medium",
                "title": f"High CPU: {cpu:.1f}%",
                "description": f"CPU load {cpu:.1f}% > 70% threshold",
                "action": "consider scaling or optimization",
                "evidence": {"metric": "cpu_percent", "value": cpu, "node": "laptop"},
            })
        if ram > 80:
            insights.append({
                "type": "performance",
                "severity": "high" if ram > 90 else "medium",
                "title": f"High RAM: {ram:.1f}%",
                "description": f"RAM {ram:.1f}% > 80% threshold",
                "action": "restart memory-heavy services or add swap",
                "evidence": {"metric": "ram_percent", "value": ram, "node": "laptop"},
            })
        if disk > 75:
            insights.append({
                "type": "performance",
                "severity": "high" if disk > 85 else "medium",
                "title": f"Disk: {disk:.1f}%",
                "description": f"Disk {disk:.1f}% > 75% threshold",
                "action": "run ArgosDiskCleaner or expand storage",
                "evidence": {"metric": "disk_percent", "value": disk, "node": "laptop"},
            })
        
        # Insight 2: Trust degradation
        for node_id, profile in trust.items():
            conf = profile.get("confidence", 1.0)
            if conf < 0.7:
                insights.append({
                    "type": "trust",
                    "severity": "high" if conf < 0.4 else "medium",
                    "title": f"Trust drop: {node_id}={conf:.2f}",
                    "description": f"Node {node_id} trust degraded to {conf:.2f}",
                    "action": "investigate node health, check evidence sources",
                    "evidence": {"node": node_id, "confidence": conf, "ev_count": profile.get("evidence_count", 0)},
                })
        
        # Insight 3: Active alerts
        alerts = self.fetch_alerts()
        if len(alerts) > 3:
            insights.append({
                "type": "alerts",
                "severity": "high",
                "title": f"Too many active alerts: {len(alerts)}",
                "description": f"{len(alerts)} alerts firing simultaneously",
                "action": "investigate alert storm, consider cooldown tuning",
                "evidence": {"alert_count": len(alerts)},
            })
        
        # Insight 4: Entity cycles pattern
        cycles = int(metrics.get("argos_entity_cycles_total", 0))
        if cycles > 0 and cycles < 100:
            insights.append({
                "type": "council",
                "severity": "medium",
                "title": f"Low entity cycles: {cycles}",
                "description": f"Only {cycles} cycles since restart — Council idle",
                "action": "check entity_council.service health",
                "evidence": {"metric": "entity_cycles_total", "value": cycles},
            })
        
        # Insight 5: Offline nodes
        offline_count = int(metrics.get("argos_nodes_offline", 0))
        total_count = int(metrics.get("argos_nodes_total", 0))
        if offline_count > 0 and total_count > 0:
            insights.append({
                "type": "availability",
                "severity": "high" if offline_count > 3 else "medium",
                "title": f"Offline nodes: {offline_count}/{total_count}",
                "description": f"{offline_count} brain nodes offline",
                "action": "check network connectivity and node heartbeat",
                "evidence": {"offline": offline_count, "total": total_count},
            })

        # Insight 6: GPU temperature
        gpu_temp = metrics.get("argos_gpu_temp", 0)
        if gpu_temp > 75:
            insights.append({
                "type": "thermal",
                "severity": "high" if gpu_temp > 85 else "medium",
                "title": f"GPU temp: {gpu_temp}C",
                "description": f"V100 temperature {gpu_temp}C exceeds threshold",
                "action": "reduce power limit, check cooling",
                "evidence": {"gpu_temp": gpu_temp},
            })
        
        return insights
    
    def submit_evidence_for_insights(self, insights: List[Dict]):
        """Submit evidence в Veto для каждого insight."""
        try:
            from veto_protocol import VetoEvidence
        except ImportError:
            print("⚠️ veto_protocol unavailable, skipping evidence submission")
            return
        
        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        from argos_council_integration import CouncilTrustGuard
        guard = CouncilTrustGuard()
        
        for insight in insights:
            ev_data = insight.get("evidence", {})
            node_id = ev_data.get("node", "laptop")
            metric_name = insight.get("type", "unknown")
            value = ev_data.get("value", 0.5)
            severity = 0.7 if insight["severity"] == "high" else 0.4
            
            # Normalize value to 0-1
            if isinstance(value, (int, float)):
                value = min(1.0, value / 100.0) if value > 1 else max(0.0, min(1.0, value))
            
            ev = VetoEvidence(
                node_id=node_id,
                metric_name=f"evolution_{metric_name}",
                value=value,
                severity=severity,
                source="evolution_v2",
            )
            try:
                result = guard.submit_evidence(ev)
                self.evidence_submitted.append({
                    "node": node_id, "metric": metric_name, "value": value, "result": result,
                })
            except Exception as e:
                print(f"⚠️ submit_evidence failed: {e}")
    
    def run_cycle(self) -> Dict[str, Any]:
        """Один цикл эволюции."""
        print(f"\n{'='*70}")
        print(f"  EVOLUTION CYCLE {self.session_id}")
        print(f"{'='*70}")
        
        start = time.time()
        metrics = self.fetch_metrics()
        trust = self.fetch_trust()
        events = self.fetch_audit_events()
        
        print(f"  Metrics: {len(metrics)} values")
        print(f"  Trust: {len(trust)} nodes")
        print(f"  Events: {len(events)} audit")
        
        insights = self.analyze_patterns(metrics, trust, events)
        print(f"  Insights: {len(insights)}")
        
        for i, ins in enumerate(insights, 1):
            icon = "🔴" if ins["severity"] == "high" else "🟡" if ins["severity"] == "medium" else "🟢"
            print(f"  {icon} [{ins['type']}] {ins['title']}")
        
        # Submit evidence
        self.submit_evidence_for_insights(insights)
        print(f"  Evidence submitted: {len(self.evidence_submitted)}")
        
        # Save learnings
        cycle_data = {
            "session_id": self.session_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "duration_sec": round(time.time() - start, 2),
            "insights": insights,
            "evidence_submitted": self.evidence_submitted,
            "metrics_snapshot": {
                k: v for k, v in metrics.items()
                if k in ("argos_cpu_percent", "argos_ram_percent", "argos_disk_percent",
                         "argos_nodes_online", "argos_nodes_total", "argos_brain_api_up")
            },
        }
        out_file = OUT_DIR / f"evolution_{self.session_id}.json"
        out_file.write_text(json.dumps(cycle_data, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"  Saved: {out_file}")
        
        return cycle_data


if __name__ == "__main__":
    engine = EvolutionEngineV2()
    result = engine.run_cycle()
    
    # Post to Council
    try:
        env_path = PROJECT_ROOT / ".env"
        env = {}
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v
        token = env.get("BOT_ARGOS_CLAUDE_AI_BOT", "")
        chat_id = env.get("CHAT_ID", "-1003844162784")
        if token:
            insights = result.get("insights", [])
            msg = f"🧬 [Evolution v2] Cycle {result['session_id']}\n\n"
            msg += f"Insights: {len(insights)}\n"
            for ins in insights[:5]:
                icon = "🔴" if ins["severity"] == "high" else "🟡" if ins["severity"] == "medium" else "🟢"
                msg += f"{icon} [{ins['type']}] {ins['title']}\n"
            msg += f"\nEvidence submitted: {len(result.get('evidence_submitted', []))}\n"
            msg += f"Duration: {result.get('duration_sec', 0)}s"
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data=json.dumps({"chat_id": chat_id, "text": msg[:3900]}).encode(),
                headers={"Content-Type": "application/json"},
            )
            urllib.request.urlopen(req, timeout=15)
            print(f"\n✓ Posted to Council")
    except Exception as e:
        print(f"⚠️ Failed to post: {e}")
