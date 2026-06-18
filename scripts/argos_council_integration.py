#!/usr/bin/env python3
"""
Интеграция VetoProtocol + AuditLog в entity_council.py.

Добавляет:
- Проверку trust scores перед действием (VetoEnvironment)
- Логирование в audit_log
- Auto-quarantine при confidence < 0.3
"""
import sys
import json
import urllib.request
from pathlib import Path
from typing import Optional, Dict, Any

sys.path.insert(0, '/home/ava/Projects/argoss/src/audit')
from veto_protocol import VetoEnvironment, VetoAction, VetoEvidence
from audit_log import AuditLog, EventType, Severity

AUDIT_API = "http://localhost:5010"
QUARANTINE_THRESHOLD = 0.3


class CouncilTrustGuard:
    """Защита entity_council через VetoProtocol."""
    
    def __init__(self, audit_api: str = AUDIT_API):
        self.audit_api = audit_api
        # Используем прямой VetoEnvironment (быстрее, не через HTTP)
        self.veto = VetoEnvironment(
            nodes=["orion", "nexus", "egida", "pico", "esp32", "android", "phone-redmi", "entity-valenok", "laptop"],
            db_path="/home/ava/Projects/argoss/data/veto.db",
        )
        self.audit = AuditLog(db_path="/home/ava/Projects/argoss/data/audit.db")
    
    def check_node(self, node_id: str) -> Dict[str, Any]:
        """Проверяет trust score ноды. Возвращает профиль."""
        profile = self.veto.get_node(node_id)
        if profile is None:
            return {"node_id": node_id, "confidence": 1.0, "warning": "unknown"}
        if profile.get("is_quarantined"):
            self.audit.log(
                EventType.QUARANTINE_ACTIVATED,
                f"Node {node_id} is in quarantine",
                Severity.WARN,
                actor="council_guard",
                target=node_id,
            )
            return {**profile, "blocked": True}
        if profile.get("confidence", 1.0) < QUARANTINE_THRESHOLD:
            # Авто-карантин
            self.veto.step(VetoAction.QUARANTINE_NODE, node_id=node_id, duration=3600)
            self.audit.log(
                EventType.QUARANTINE_ACTIVATED,
                f"Auto-quarantined {node_id} (confidence {profile.get('confidence', 0):.2f})",
                Severity.ERROR,
                actor="council_guard",
                target=node_id,
            )
            return {**profile, "blocked": True, "auto_quarantined": True}
        return profile
    
    def submit_evidence(self, evidence: VetoEvidence):
        """Отправляет evidence в VetoEnvironment."""
        result = self.veto.step(VetoAction.SUBMIT_EVIDENCE, evidence=evidence)
        self.audit.log(
            EventType.EVIDENCE_SUBMITTED,
            f"Evidence: {evidence.metric_name}={evidence.value:.2f} for {evidence.node_id}",
            Severity.INFO if evidence.severity < 0.5 else Severity.WARN,
            actor="council_guard",
            target=evidence.node_id,
            metadata={"metric": evidence.metric_name, "value": evidence.value, "severity": evidence.severity},
        )
        return result
    
    def log_action(self, action: str, target: str, severity: str = "INFO", metadata: Optional[Dict] = None):
        """Логирует действие Council в audit_log."""
        sev_map = {"DEBUG": Severity.DEBUG, "INFO": Severity.INFO, "WARN": Severity.WARN,
                   "ERROR": Severity.ERROR, "CRITICAL": Severity.CRITICAL}
        self.audit.log(
            EventType.API_REQUEST,
            action,
            sev_map.get(severity.upper(), Severity.INFO),
            actor="entity_council",
            target=target,
            metadata=metadata,
        )
    
    def get_dashboard_url(self) -> str:
        """URL для просмотра dashboard."""
        return f"{self.audit_api}/status"


# Пример использования
if __name__ == "__main__":
    guard = CouncilTrustGuard()
    print("Trust scores:")
    for node in ["orion", "nexus", "egida", "pico", "esp32", "android", "phone-redmi"]:
        profile = guard.check_node(node)
        status = "🟢" if profile.get("confidence", 1.0) > 0.7 else "🟡" if profile.get("confidence", 1.0) > 0.3 else "🔴"
        print(f"  {status} {node}: confidence={profile.get('confidence', 1.0):.2f}")
    print(f"\nDashboard: {guard.get_dashboard_url()}")
