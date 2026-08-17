import pytest

from integrations.planeta_mcp.audit import AuditLogger
from integrations.planeta_mcp.browser import BrowserResult
from integrations.planeta_mcp.defaults import default_argos_reboot_campaign
from integrations.planeta_mcp.security import ApprovalError, ApprovalGate
from integrations.planeta_mcp.service import CampaignValidationError, PlanetaCampaignService
from integrations.planeta_mcp.store import CampaignStore


class FakeBrowser:
    def __init__(self):
        self.submit_calls = 0
        self.fill_calls = 0
        self.reward_fill_calls = 0
        self.reward_read_calls = 0
        self.snapshot = {"title": "", "target_amount": "", "summary": "", "story": ""}
        self.rewards_snapshot = []
        self.submit_result = BrowserResult(status="ok", reason="submitted")

    async def fill_draft(self, campaign):
        self.fill_calls += 1
        self.snapshot = {
            "title": campaign.title,
            "target_amount": str(campaign.target_amount),
            "summary": campaign.summary,
            "story": campaign.story,
        }
        return BrowserResult(status="ok", reason="filled", draft_snapshot=self.snapshot)

    async def fill_rewards(self, campaign):
        self.reward_fill_calls += 1
        self.rewards_snapshot = [
            {
                "title": reward.title,
                "amount": str(reward.amount),
                "description": reward.description,
                "physical": reward.physical,
            }
            for reward in campaign.rewards
        ]
        return BrowserResult(
            status="ok",
            reason="rewards filled",
            draft_snapshot={"rewards": self.rewards_snapshot},
        )

    async def read_draft(self):
        return BrowserResult(status="ok", reason="read", draft_snapshot=self.snapshot)

    async def read_rewards(self):
        self.reward_read_calls += 1
        return BrowserResult(
            status="ok",
            reason="rewards read",
            draft_snapshot={"rewards": self.rewards_snapshot},
        )

    async def submit_for_moderation(self):
        self.submit_calls += 1
        return self.submit_result


@pytest.fixture
def campaign():
    return default_argos_reboot_campaign()


@pytest.fixture
def service(tmp_path):
    return PlanetaCampaignService(
        store=CampaignStore(tmp_path / "campaign.json"),
        browser=FakeBrowser(),
        approval_gate=ApprovalGate(b"test-secret", ttl_seconds=300),
        audit=AuditLogger(tmp_path / "audit.jsonl"),
    )


@pytest.mark.asyncio
async def test_fill_and_sync_include_rewards(service, campaign):
    await service.prepare_campaign(campaign)

    filled = await service.fill_draft()
    synced = await service.sync_draft()

    assert filled.status == "ok"
    assert service.browser.fill_calls == 1
    assert service.browser.reward_fill_calls == 1
    assert service.browser.reward_read_calls == 1
    assert synced["status"] == "ok"
    assert synced["differences"] == {}


@pytest.mark.asyncio
async def test_sync_reports_reward_difference(service, campaign):
    await service.prepare_campaign(campaign)
    await service.fill_draft()
    service.browser.rewards_snapshot[0]["amount"] = "999"

    synced = await service.sync_draft()

    assert "rewards" in synced["differences"]


@pytest.mark.asyncio
async def test_submit_requires_prior_human_confirmation(service, campaign):
    await service.prepare_campaign(campaign)
    request = await service.request_submit_approval()

    with pytest.raises(ApprovalError, match="human confirmation"):
        await service.submit_for_moderation(request.request_id)
    assert service.browser.submit_calls == 0

    challenge = service.get_submit_approval_challenge(request.request_id)
    service.confirm_submit_approval(request.request_id, challenge.csrf_token)
    result = await service.submit_for_moderation(request.request_id)
    assert result.status == "ok"
    assert service.browser.submit_calls == 1


@pytest.mark.asyncio
async def test_prepare_invalidates_prior_approval_request(service, campaign):
    await service.prepare_campaign(campaign)
    request = await service.request_submit_approval()
    challenge = service.get_submit_approval_challenge(request.request_id)
    service.confirm_submit_approval(request.request_id, challenge.csrf_token)
    await service.prepare_campaign(campaign.model_copy(update={"target_amount": 199999}))
    with pytest.raises(ApprovalError, match="Unknown approval request"):
        await service.submit_for_moderation(request.request_id)
    assert service.browser.submit_calls == 0


@pytest.mark.asyncio
async def test_failed_browser_submit_still_consumes_confirmed_request(service, campaign):
    await service.prepare_campaign(campaign)
    request = await service.request_submit_approval()
    challenge = service.get_submit_approval_challenge(request.request_id)
    service.confirm_submit_approval(request.request_id, challenge.csrf_token)
    service.browser.submit_result = BrowserResult(status="captcha_required", reason="human")
    result = await service.submit_for_moderation(request.request_id)
    assert result.status == "captcha_required"
    with pytest.raises(ApprovalError, match="already been used"):
        await service.submit_for_moderation(request.request_id)
    assert service.browser.submit_calls == 1


@pytest.mark.asyncio
async def test_fill_validates_before_browser_mutation(service, campaign):
    bad = campaign.model_copy(update={"rewards": []})
    await service.prepare_campaign(bad)
    result = await service.fill_draft()
    assert result.status == "validation_failed"
    assert service.browser.fill_calls == 0
    assert service.browser.reward_fill_calls == 0


@pytest.mark.asyncio
async def test_request_approval_rejects_invalid_campaign(service, campaign):
    await service.prepare_campaign(campaign.model_copy(update={"evidence_links": []}))
    with pytest.raises(CampaignValidationError):
        await service.request_submit_approval()
