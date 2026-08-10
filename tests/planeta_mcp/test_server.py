from fastapi.testclient import TestClient

from integrations.planeta_mcp.server import REGISTERED_TOOL_NAMES, create_app


def test_health():
    client = TestClient(create_app(service=None, enable_mcp=False))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["service"] == "planeta-mcp"


def test_tool_names_are_registered():
    assert {
        "planeta_campaign_status",
        "planeta_campaign_preview",
        "planeta_validate_campaign",
        "planeta_prepare_campaign",
        "planeta_fill_draft",
        "planeta_sync_draft",
        "planeta_request_submit_approval",
        "planeta_submit_for_moderation",
    } == set(REGISTERED_TOOL_NAMES)
