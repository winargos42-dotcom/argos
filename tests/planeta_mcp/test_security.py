import pytest

from integrations.planeta_mcp.defaults import default_argos_reboot_campaign
from integrations.planeta_mcp.security import ApprovalError, ApprovalGate, campaign_digest


class FakeClock:
    def __init__(self, value: float = 1000.0):
        self.value = value

    def __call__(self) -> float:
        return self.value


def test_campaign_digest_is_stable():
    campaign = default_argos_reboot_campaign()
    assert campaign_digest(campaign) == campaign_digest(campaign)


def test_request_cannot_be_consumed_until_human_confirmation():
    campaign = default_argos_reboot_campaign()
    gate = ApprovalGate(b"test-secret", ttl_seconds=300)
    request = gate.request(campaign)

    with pytest.raises(ApprovalError, match="human confirmation"):
        gate.consume(request.request_id, campaign)

    challenge = gate.challenge(request.request_id)
    gate.confirm(request.request_id, challenge.csrf_token)
    gate.consume(request.request_id, campaign)

    with pytest.raises(ApprovalError, match="already been used"):
        gate.consume(request.request_id, campaign)


def test_invalid_confirmation_token_does_not_arm_submit():
    campaign = default_argos_reboot_campaign()
    gate = ApprovalGate(b"test-secret", ttl_seconds=300)
    request = gate.request(campaign)

    with pytest.raises(ApprovalError, match="Invalid human confirmation"):
        gate.confirm(request.request_id, "wrong-csrf")
    with pytest.raises(ApprovalError, match="human confirmation"):
        gate.consume(request.request_id, campaign)


def test_campaign_edit_invalidates_approval_request():
    campaign = default_argos_reboot_campaign()
    gate = ApprovalGate(b"test-secret", ttl_seconds=300)
    request = gate.request(campaign)
    challenge = gate.challenge(request.request_id)
    gate.confirm(request.request_id, challenge.csrf_token)
    changed = campaign.model_copy(update={"target_amount": campaign.target_amount + 1})
    with pytest.raises(ApprovalError, match="does not match current campaign"):
        gate.consume(request.request_id, changed)


def test_approval_request_expires_before_confirmation():
    campaign = default_argos_reboot_campaign()
    clock = FakeClock()
    gate = ApprovalGate(b"test-secret", ttl_seconds=5, clock=clock)
    request = gate.request(campaign)
    clock.value += 6
    with pytest.raises(ApprovalError, match="expired"):
        gate.challenge(request.request_id)


def test_invalidate_all_revokes_requests():
    campaign = default_argos_reboot_campaign()
    gate = ApprovalGate(b"test-secret", ttl_seconds=300)
    request = gate.request(campaign)
    gate.invalidate_all()
    with pytest.raises(ApprovalError, match="Unknown approval request"):
        gate.challenge(request.request_id)
