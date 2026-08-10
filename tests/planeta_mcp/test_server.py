import asyncio
import re

import pytest
from fastapi.testclient import TestClient

from integrations.planeta_mcp.audit import AuditLogger
from integrations.planeta_mcp.browser import BrowserResult
from integrations.planeta_mcp.defaults import default_argos_reboot_campaign
from integrations.planeta_mcp.security import ApprovalError, ApprovalGate
from integrations.planeta_mcp.server import REGISTERED_TOOL_NAMES, create_app
from integrations.planeta_mcp.service import PlanetaCampaignService
from integrations.planeta_mcp.store import CampaignStore


class NoopBrowser:
    async def fill_draft(self, campaign):
        return BrowserResult(status="ok", reason="noop")

    async def read_draft(self):
        return BrowserResult(status="ok", reason="noop")

    async def submit_for_moderation(self):
        return BrowserResult(status="ok", reason="noop")


def make_service(tmp_path):
    return PlanetaCampaignService(
        store=CampaignStore(tmp_path / "campaign.json"),
        browser=NoopBrowser(),
        approval_gate=ApprovalGate(b"approval-secret", ttl_seconds=300),
        audit=AuditLogger(tmp_path / "audit.jsonl"),
    )


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


def test_approval_get_is_read_only_and_post_confirms(tmp_path):
    service = make_service(tmp_path)
    campaign = default_argos_reboot_campaign()
    asyncio.run(service.prepare_campaign(campaign))
    request = asyncio.run(service.request_submit_approval())

    client = TestClient(create_app(service=service, enable_mcp=False))
    response = client.get(f"/approve/{request.request_id}")
    assert response.status_code == 200
    assert "Подтвердить отправку на модерацию" in response.text

    with pytest.raises(ApprovalError, match="human confirmation"):
        service.approval_gate.consume(request.request_id, campaign)

    match = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
    assert match is not None
    confirmed = client.post(
        f"/approve/{request.request_id}",
        data={"csrf_token": match.group(1)},
    )
    assert confirmed.status_code == 200
    assert "Подтверждение принято" in confirmed.text

    service.approval_gate.consume(request.request_id, campaign)
