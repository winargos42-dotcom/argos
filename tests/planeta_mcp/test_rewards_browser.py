from pathlib import Path

import pytest

from integrations.planeta_mcp.browser import PlanetaBrowser
from integrations.planeta_mcp.defaults import default_argos_reboot_campaign


FIXTURES = Path(__file__).parents[2] / "integrations" / "planeta_mcp" / "fixtures"


@pytest.mark.asyncio
async def test_fill_rewards_adds_three_digital_rewards_idempotently():
    browser = PlanetaBrowser(
        base_url="https://planeta.ru",
        headless=True,
        fixture_dir=FIXTURES,
        executable_path="/usr/bin/chromium",
    )
    campaign = default_argos_reboot_campaign()
    try:
        await browser.open_fixture("rewards_editor.html")

        first = await browser.fill_rewards(campaign)
        second = await browser.fill_rewards(campaign)
        page = browser._page
        assert page is not None

        assert first.status == "ok"
        assert second.status == "ok"
        cards = page.locator(".reward-card")
        assert await cards.count() == 3
        for reward in campaign.rewards:
            assert await page.get_by_text(reward.title, exact=True).count() == 1
        assert await page.locator("#physical-reward").is_checked() is False
    finally:
        await browser.close()
