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


def test_approval_token_is_one_time_and_bound_to_digest():
    campaign = default_argos_reboot_campaign()
    gate = ApprovalGate(b"test-secret", ttl_seconds=300)
    grant = gate.issue(campaign)
    gate.consume(grant.token, campaign)
    with pytest.raises(ApprovalError):
        gate.consume(grant.token, campaign)


def test_campaign_edit_invalidates_approval():
    campaign = default_argos_reboot_campaign()
    gate = ApprovalGate(b"test-secret", ttl_seconds=300)
    grant = gate.issue(campaign)
    changed = campaign.model_copy(update={"target_amount": campaign.target_amount + 1})
    with pytest.raises(ApprovalError):
        gate.consume(grant.token, changed)


def test_approval_expires():
    campaign = default_argos_reboot_campaign()
    clock = FakeClock()
    gate = ApprovalGate(b"test-secret", ttl_seconds=5, clock=clock)
    grant = gate.issue(campaign)
    clock.value += 6
    with pytest.raises(ApprovalError):
        gate.consume(grant.token, campaign)


def test_invalidate_all_revokes_grants():
    campaign = default_argos_reboot_campaign()
    gate = ApprovalGate(b"test-secret", ttl_seconds=300)
    grant = gate.issue(campaign)
    gate.invalidate_all()
    with pytest.raises(ApprovalError):
        gate.consume(grant.token, campaign)
