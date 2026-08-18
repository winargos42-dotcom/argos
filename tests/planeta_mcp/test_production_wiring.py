from pathlib import Path

from cryptography.fernet import Fernet
from fastapi.testclient import TestClient

from integrations.planeta_mcp import server
from integrations.planeta_mcp.session_store import SessionStore


ROOT = Path(__file__).parents[2] / "integrations" / "planeta_mcp"


def test_default_service_loads_session_from_independent_directory(monkeypatch, tmp_path):
    state_path = tmp_path / "work" / "campaign.json"
    session_dir = tmp_path / "persistent"
    session_key = Fernet.generate_key()
    cookie_state = {
        "cookies": [
            {"name": "sid", "value": "saved", "domain": ".planeta.ru", "path": "/"}
        ],
        "origins": [],
    }
    SessionStore(session_dir / "session.enc", session_key).save_storage_state(cookie_state)
    monkeypatch.setenv("PLANETA_APPROVAL_SECRET", "approval-secret")
    monkeypatch.setenv("PLANETA_SESSION_KEY", session_key.decode("ascii"))
    monkeypatch.setenv("PLANETA_STATE_PATH", str(state_path))
    monkeypatch.setenv("PLANETA_SESSION_DIR", str(session_dir))

    service = server.build_default_service()

    assert service.store.path == state_path
    assert service.audit.path == state_path.parent / "audit.jsonl"
    assert service.browser.storage_state == cookie_state


def test_module_app_wires_live_login_from_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("PLANETA_APPROVAL_SECRET", "approval-secret")
    monkeypatch.setenv("PLANETA_SESSION_KEY", Fernet.generate_key().decode("ascii"))
    monkeypatch.setenv("PLANETA_STATE_PATH", str(tmp_path / "campaign.json"))
    monkeypatch.setenv("PLANETA_DRAFT_URL", "https://planeta.ru/campaigns/251138/edit/about")
    monkeypatch.setenv("PLANETA_LIVE_CONTROL_SECRET", "live-control-secret")
    monkeypatch.setenv("PLANETA_LIVE_TTL_SECONDS", "600")
    monkeypatch.setenv("PLANETA_SESSION_DURABILITY", "ephemeral")

    app = server._module_app()
    client = TestClient(app, base_url="https://testserver")
    response = client.get("/live-login/")

    assert response.status_code == 200
    assert "вход Planeta.ru" in response.text


def test_railway_entrypoint_repairs_volume_ownership_then_drops_root():
    dockerfile = (ROOT / "Dockerfile.railway").read_text(encoding="utf-8")
    entrypoint = (ROOT / "docker-entrypoint.sh").read_text(encoding="utf-8")

    assert "gosu" in dockerfile
    assert 'ENTRYPOINT ["/usr/local/bin/planeta-entrypoint"]' in dockerfile
    assert "chown -R app:app /data/planeta" in entrypoint
    assert 'exec gosu app "$@"' in entrypoint
