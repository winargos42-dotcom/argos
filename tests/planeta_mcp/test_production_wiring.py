from cryptography.fernet import Fernet
from fastapi.testclient import TestClient

from integrations.planeta_mcp import server


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
