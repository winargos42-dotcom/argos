from pathlib import Path

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

from integrations.planeta_mcp.browser import PlanetaBrowser
from integrations.planeta_mcp.defaults import default_argos_reboot_campaign


FIXTURES = Path(__file__).parents[2] / "integrations" / "planeta_mcp" / "fixtures"


@pytest_asyncio.fixture
async def browser():
    instance = PlanetaBrowser(
        base_url="https://planeta.ru",
        headless=True,
        fixture_dir=FIXTURES,
        executable_path="/usr/bin/chromium",
    )
    yield instance
    await instance.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("fixture", "expected"),
    [
        ("login.html", "authentication_required"),
        ("captcha.html", "captcha_required"),
        ("identity.html", "human_action_required"),
        ("ui_changed.html", "ui_changed"),
    ],
)
async def test_classifies_blocking_pages(browser, fixture, expected):
    await browser.open_fixture(fixture)
    result = await browser.inspect()
    assert result.status == expected


@pytest.mark.asyncio
async def test_about_editor_does_not_require_submit_control(browser):
    await browser.open_fixture("about_without_submit.html")
    result = await browser.inspect()
    assert result.status == "ok"


@pytest.mark.asyncio
async def test_live_browser_requires_explicit_draft_url():
    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)
    try:
        result = await browser.inspect()
    finally:
        await browser.close()
    assert result.status == "configuration_required"


@pytest.mark.asyncio
async def test_classifies_planeta_forbidden_page_as_service_error():
    class Locator:
        async def inner_text(self):
            return "403 Доступ запрещен!"

        async def count(self):
            return 0

    class ForbiddenPage:
        url = "https://planeta.ru/campaigns/251138/edit/about"

        def locator(self, _selector):
            return Locator()

    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)

    state = await browser.classify_page(ForbiddenPage())

    assert state.value == "planeta_error"


def test_live_browser_rejects_off_domain_draft_url():
    with pytest.raises(ValueError, match="same origin"):
        PlanetaBrowser(
            base_url="https://planeta.ru",
            draft_url="https://example.com/fake-draft",
            headless=True,
        )


@pytest.mark.asyncio
async def test_fill_draft_never_submits(browser):
    campaign = default_argos_reboot_campaign()
    await browser.open_fixture("draft.html")
    result = await browser.fill_draft(campaign)
    assert result.status == "ok"
    assert await browser.submit_click_count() == 0
    assert result.draft_snapshot["title"] == campaign.title
    assert result.draft_snapshot["target_amount"] == str(campaign.target_amount)


@pytest.mark.asyncio
async def test_fill_draft_supports_semantic_accessible_controls(browser):
    campaign = default_argos_reboot_campaign()
    await browser.open_fixture("semantic_draft.html")

    result = await browser.fill_draft(campaign)

    assert result.status == "ok"
    assert result.draft_snapshot["title"] == campaign.title
    assert result.draft_snapshot["target_amount"] == str(campaign.target_amount)
    assert result.draft_snapshot["summary"] == campaign.summary
    assert result.draft_snapshot["story"] == campaign.story
    assert await browser.submit_click_count() == 0


@pytest.mark.asyncio
async def test_read_draft_returns_snapshot(browser):
    await browser.open_fixture("draft.html")
    result = await browser.read_draft()
    assert result.status == "ok"
    assert result.draft_snapshot["title"] == ""


@pytest.mark.asyncio
async def test_submit_uses_only_exact_moderation_control(browser):
    await browser.open_fixture("draft.html")
    result = await browser.submit_for_moderation()
    assert result.status == "ok"
    assert await browser.submit_click_count() == 1


@pytest.mark.asyncio
async def test_submit_navigates_exact_review_step_before_moderation(browser):
    await browser.open_fixture("moderation_nav.html")

    result = await browser.submit_for_moderation()

    assert result.status == "ok"
    assert await browser.submit_click_count() == 1


@pytest.mark.asyncio
async def test_browser_attaches_to_existing_cdp_context(tmp_path):
    async with async_playwright() as playwright:
        context = await playwright.chromium.launch_persistent_context(
            str(tmp_path / "shared-profile"),
            headless=True,
            args=[
                "--remote-debugging-port=9333",
                "--remote-debugging-address=127.0.0.1",
            ],
        )
        try:
            page = context.pages[0]
            await page.set_content("<title>shared</title><body>same-context</body>")
            adapter = PlanetaBrowser(cdp_url="http://127.0.0.1:9333")
            attached = await adapter._ensure_page()
            assert await attached.title() == "shared"
            assert await attached.locator("body").inner_text() == "same-context"
            await adapter.close()
            assert await page.title() == "shared"
        finally:
            await context.close()


@pytest.mark.asyncio
async def test_cdp_mode_never_redirects_human_login_page_back_to_draft():
    class HumanPage:
        url = "https://planeta.ru/nuborn_session"

        async def goto(self, *_args, **_kwargs):
            raise AssertionError("shared human browser must not be redirected by watcher")

    adapter = PlanetaBrowser(
        base_url="https://planeta.ru",
        draft_url="https://planeta.ru/campaigns/251138/edit/about",
        cdp_url="http://127.0.0.1:9222",
    )
    adapter._page = HumanPage()
    page, early = await adapter._prepare_page()

    assert early is None
    assert page.url == "https://planeta.ru/nuborn_session"


@pytest.mark.asyncio
async def test_ui_diagnostic_excludes_values_and_url_query():
    class DiagnosticLocator:
        async def evaluate_all(self, _script):
            return [
                {
                    "tag": "input",
                    "type": "text",
                    "name": "campaign_name",
                    "id": "campaign-name",
                    "placeholder": "Название",
                    "ariaLabel": "",
                    "testId": "",
                    "text": "",
                }
            ]

    class BodyLocator:
        async def inner_text(self):
            return "Проверка страницы"

    class DiagnosticPage:
        url = "https://planeta.ru/campaigns/251138/edit/about?private=secret#fragment"

        async def title(self):
            return "Редактор проекта"

        def locator(self, selector):
            if selector == "body":
                return BodyLocator()
            assert selector == "input, textarea, button, [contenteditable='true']"
            return DiagnosticLocator()

    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)
    browser._page = DiagnosticPage()

    diagnostic = await browser.ui_diagnostic_snapshot()

    assert diagnostic == {
        "url": "https://planeta.ru/campaigns/251138/edit/about",
        "title": "Редактор проекта",
        "bodyText": "Проверка страницы",
        "controls": [
            {
                "tag": "input",
                "type": "text",
                "name": "campaign_name",
                "id": "campaign-name",
                "placeholder": "Название",
                "ariaLabel": "",
                "testId": "",
                "text": "",
            }
        ],
    }
