import json

from integrations.planeta_mcp.audit import AuditLogger


def test_audit_never_logs_secret_material(tmp_path):
    logger = AuditLogger(tmp_path / "audit.jsonl")
    logger.record("fill", "argos-reboot", "ok", {
        "cookie": "secret-cookie",
        "password": "secret-password",
        "passport": "1234 567890",
        "safe": "ok",
        "nested": {"authorization": "Bearer abc", "value": 1},
    })
    text = (tmp_path / "audit.jsonl").read_text(encoding="utf-8")
    assert "secret-cookie" not in text
    assert "secret-password" not in text
    assert "1234 567890" not in text
    assert "Bearer abc" not in text
    assert '"safe": "ok"' in text
    record = json.loads(text)
    assert record["result"]["cookie"] == "[REDACTED]"
    assert record["result"]["nested"]["value"] == 1
