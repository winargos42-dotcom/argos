from datetime import date
from pathlib import Path

from PIL import Image

from integrations.planeta_mcp.defaults import default_argos_reboot_campaign
from integrations.planeta_mcp.store import CampaignStore


def test_argos_reboot_defaults_are_valid(monkeypatch):
    monkeypatch.delenv("ARGOS_PLANETA_PROJECT_REGION", raising=False)
    campaign = default_argos_reboot_campaign()
    report = campaign.validate_for_planeta()
    assert campaign.title == "ARGOS REBOOT — восстановление независимой AI/FPGA-системы"
    assert campaign.target_amount == 200000
    assert campaign.currency == "RUB"
    assert campaign.end_date == date(2026, 10, 17)
    assert campaign.region is None
    assert str(campaign.direct_support_url) == "https://pay.cloudtips.ru/p/8df874d0"
    assert report.errors == []
    assert all(reward.physical is False for reward in campaign.rewards)


def test_argos_reboot_region_comes_from_private_environment(monkeypatch):
    monkeypatch.setenv("ARGOS_PLANETA_PROJECT_REGION", "  Тестовый край  ")

    campaign = default_argos_reboot_campaign()

    assert campaign.region == "Тестовый край"


def test_argos_reboot_uses_deployable_factual_media_assets():
    campaign = default_argos_reboot_campaign()
    package_root = Path(__file__).parents[2] / "integrations" / "planeta_mcp"

    assert campaign.cover_image_path == "assets/argos-reboot-cover.jpg"
    assert campaign.main_image_path == "assets/argos-reboot-fire-main.jpg"

    cover = package_root / campaign.cover_image_path
    main = package_root / campaign.main_image_path
    assert cover.is_file()
    assert main.is_file()
    with Image.open(cover) as image:
        assert image.size == (1000, 625)
        image.verify()
    with Image.open(main) as image:
        assert image.width >= 1000
        assert image.height >= 625
        image.verify()


def test_argos_reboot_story_contains_fire_evidence_budget_and_recovery_plan():
    campaign = default_argos_reboot_campaign()
    story = campaign.story

    assert "По словам автора" in story
    assert "3 августа 2026" in story
    assert (
        "пожар уничтожил квартиру вместе с компьютером и локальной вычислительной "
        "средой проекта"
    ) in story
    assert "Сбор предназначен только для восстановления серверной инфраструктуры ARGOS" in story
    assert "ремонт квартиры не входит в бюджет кампании" in story
    for url in (
        "https://github.com/poilopr57-a11y/Argos",
        "https://github.com/winargos42-dotcom/argos",
        "https://huggingface.co/AvaSiG/argos-v1",
        "https://huggingface.co/datasets/AvaSiG/argos-canonical",
    ):
        assert url in story

    for text in (
        "85 000 ₽",
        "65 000 ₽",
        "30 000 ₽",
        "20 000 ₽",
        "200 000 ₽",
        "сервер",
        "GPU/FPGA",
        "резерв",
    ):
        assert text in story


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
