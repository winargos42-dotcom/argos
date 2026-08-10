from pathlib import Path

from integrations.planeta_mcp.defaults import default_argos_reboot_campaign
from integrations.planeta_mcp.store import CampaignStore


def test_argos_reboot_defaults_are_valid():
    campaign = default_argos_reboot_campaign()
    report = campaign.validate_for_planeta()
    assert campaign.title == "ARGOS REBOOT — восстановление независимой AI/FPGA-системы"
    assert campaign.target_amount == 200000
    assert campaign.currency == "RUB"
    assert report.errors == []
    assert all(reward.physical is False for reward in campaign.rewards)


def test_campaign_rejects_missing_evidence_and_empty_rewards():
    campaign = default_argos_reboot_campaign().model_copy(
        update={"evidence_links": [], "rewards": []}
    )
    report = campaign.validate_for_planeta()
    assert "evidence_links" in report.error_fields
    assert "rewards" in report.error_fields


def test_canonical_dict_is_stable():
    campaign = default_argos_reboot_campaign()
    assert campaign.canonical_dict() == campaign.canonical_dict()
    assert "created_at" not in campaign.canonical_dict()
    assert "updated_at" not in campaign.canonical_dict()


def test_campaign_store_round_trip(tmp_path: Path):
    path = tmp_path / "campaign.json"
    store = CampaignStore(path)
    campaign = default_argos_reboot_campaign()
    assert store.load() is None
    store.save(campaign)
    loaded = store.load()
    assert loaded is not None
    assert loaded.canonical_dict() == campaign.canonical_dict()
