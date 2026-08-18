from pathlib import Path
from urllib.parse import urlsplit

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


@pytest.mark.asyncio
async def test_classifies_planeta_forbidden_login_page_as_authentication_required():
    class Locator:
        async def inner_text(self):
            return "Войти 403 Доступ запрещен!"

        async def count(self):
            return 0

    class ForbiddenLoginPage:
        url = "https://planeta.ru/campaigns/251138/edit/about"

        def locator(self, _selector):
            return Locator()

    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)

    state = await browser.classify_page(ForbiddenLoginPage())

    assert state.value == "authentication_required"


def test_live_browser_rejects_off_domain_draft_url():
    with pytest.raises(ValueError, match="same origin"):
        PlanetaBrowser(
            base_url="https://planeta.ru",
            draft_url="https://example.com/fake-draft",
            headless=True,
        )


@pytest.mark.parametrize("unsafe_step", ["agreement", "review", "moderation", "submit"])
def test_live_browser_rejects_unsafe_configured_editor_step(unsafe_step):
    with pytest.raises(ValueError, match="safe about"):
        PlanetaBrowser(
            base_url="https://planeta.ru",
            draft_url=f"https://planeta.ru/campaigns/251138/edit/{unsafe_step}",
        )


def test_multistep_navigation_is_restricted_to_exact_editor_allowlist():
    browser = PlanetaBrowser(
        base_url="https://planeta.ru",
        draft_url="https://planeta.ru/campaigns/251138/edit/about?private=value#fragment",
    )

    assert browser._editor_step_url("assets") == (
        "https://planeta.ru/campaigns/251138/edit/assets"
    )
    assert browser._editor_step_url("goal") == (
        "https://planeta.ru/campaigns/251138/edit/goal"
    )
    assert browser._editor_step_url("rewards") == (
        "https://planeta.ru/campaigns/251138/edit/rewards"
    )
    for forbidden in ("agreement", "review", "moderation", "publication", "submit"):
        assert browser._editor_step_url(forbidden) is None


def test_campaign_media_upload_rejects_arbitrary_local_paths():
    campaign = default_argos_reboot_campaign().model_copy(
        update={"cover_image_path": "/etc/passwd"}
    )

    assert PlanetaBrowser._campaign_media_paths(campaign) is None


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
async def test_multistep_about_editor_is_recognized_without_goal_on_same_step(browser):
    await browser.open_fixture("multistep_editor.html")

    result = await browser.inspect()

    assert result.status == "ok"


@pytest.mark.asyncio
async def test_multistep_fill_saves_only_about_assets_and_goal(browser):
    campaign = default_argos_reboot_campaign()
    await browser.open_fixture("multistep_editor.html")

    result = await browser.fill_draft(campaign)

    assert result.status == "ok"
    assert result.draft_snapshot == {
        "title": campaign.title,
        "target_amount": str(campaign.target_amount),
        "end_date": campaign.end_date.strftime("%d.%m.%Y"),
        "summary": campaign.summary,
        "story": campaign.story,
        "cover_image": "argos-reboot-cover.jpg",
        "main_image": "argos-reboot-fire-main.jpg",
    }
    page_state = await browser._page.evaluate(
        """() => ({
            activeStep: document.body.dataset.activeStep,
            navigationLog: window.navigationLog,
            saveCounts: window.saveCounts,
            mediaFiles: window.mediaFiles,
            submitClicks: window.submitClicks,
        })"""
    )
    assert page_state == {
        "activeStep": "about",
        "navigationLog": ["about", "assets", "goal", "about"],
        "saveCounts": {"about": 1, "assets": 1, "goal": 1, "rewards": 0},
        "mediaFiles": {
            "cover": "argos-reboot-cover.jpg",
            "main": "argos-reboot-fire-main.jpg",
        },
        "submitClicks": 0,
    }


@pytest.mark.asyncio
async def test_routed_multistep_fill_persists_only_safe_editor_steps():
    campaign = default_argos_reboot_campaign()
    routed_fixture = (FIXTURES / "multistep_routed_editor.html").read_text(
        encoding="utf-8"
    )
    requested_requests: list[tuple[str, str]] = []
    instance = PlanetaBrowser(
        base_url="https://planeta.ru",
        draft_url="https://planeta.ru/campaigns/251138/edit/about",
        headless=True,
        executable_path="/usr/bin/chromium",
    )
    try:
        page = await instance._ensure_page()

        async def serve_editor(route):
            requested_requests.append(
                (route.request.method, urlsplit(route.request.url).path)
            )
            await route.fulfill(
                status=200,
                content_type="text/html; charset=utf-8",
                body=routed_fixture,
            )

        await page.route(
            "https://planeta.ru/campaigns/251138/edit/**", serve_editor
        )

        result = await instance.fill_draft(campaign)
        fill_requests = requested_requests.copy()
        requested_requests.clear()
        read_result = await instance.read_draft()
        read_requests = requested_requests.copy()
        state = await page.evaluate(
            "JSON.parse(localStorage.getItem('planeta-multistep-route-state') || '{}')"
        )
        final_path = urlsplit(page.url).path
        submit_clicks = await instance.submit_click_count()
    finally:
        await instance.close()

    assert result.status == "ok"
    assert fill_requests
    assert {
        path.rsplit("/", 1)[-1] for _, path in fill_requests + read_requests
    } <= {"about", "assets", "goal"}
    assert [path for method, path in fill_requests if method == "GET"] == [
        "/campaigns/251138/edit/about",
        "/campaigns/251138/edit/about",
        "/campaigns/251138/edit/assets",
        "/campaigns/251138/edit/assets",
        "/campaigns/251138/edit/goal",
        "/campaigns/251138/edit/goal",
        "/campaigns/251138/edit/about",
    ]
    assert [path for method, path in fill_requests if method == "POST"] == [
        "/campaigns/251138/edit/about",
        "/campaigns/251138/edit/assets",
        "/campaigns/251138/edit/goal",
    ]
    assert [path for method, path in read_requests if method == "GET"] == [
        "/campaigns/251138/edit/goal",
        "/campaigns/251138/edit/assets",
        "/campaigns/251138/edit/about",
    ]
    assert all(method == "GET" for method, _ in read_requests)
    assert state == {
        "title": campaign.title,
        "summary": campaign.summary,
        "endDate": campaign.end_date.strftime("%d.%m.%Y"),
        "story": campaign.story,
        "aboutSaves": 1,
        "cover": "argos-reboot-cover.jpg",
        "main": "argos-reboot-fire-main.jpg",
        "assetSaves": 1,
        "goal": str(campaign.target_amount),
        "goalSaves": 1,
    }
    assert result.draft_snapshot == {
        "title": campaign.title,
        "target_amount": str(campaign.target_amount),
        "end_date": campaign.end_date.strftime("%d.%m.%Y"),
        "summary": campaign.summary,
        "story": campaign.story,
        "cover_image": "argos-reboot-cover.jpg",
        "main_image": "argos-reboot-fire-main.jpg",
    }
    assert read_result.status == "ok"
    assert read_result.draft_snapshot == result.draft_snapshot
    assert final_path == "/campaigns/251138/edit/about"
    assert submit_clicks == 0


@pytest.mark.asyncio
async def test_multistep_read_aggregates_about_and_normalized_goal(browser):
    campaign = default_argos_reboot_campaign()
    await browser.open_fixture("multistep_editor.html")
    filled = await browser.fill_draft(campaign)
    assert filled.status == "ok"
    await browser._page.evaluate(
        "document.querySelector('#editor-goal').value = '200\u00a0000 ₽'"
    )

    result = await browser.read_draft()

    assert result.status == "ok"
    assert result.draft_snapshot["target_amount"] == "200000"
    assert result.draft_snapshot["end_date"] == "17.10.2026"
    assert await browser.submit_click_count() == 0
    navigation_log = await browser._page.evaluate("window.navigationLog")
    assert "agreement" not in navigation_log


@pytest.mark.asyncio
async def test_multistep_fill_fails_closed_on_ambiguous_save(browser):
    await browser.open_fixture("multistep_editor.html")
    await browser._page.evaluate(
        """() => {
            const form = document.querySelector('[data-step-form="about"]');
            form.appendChild(form.querySelector('button[type="submit"]').cloneNode(true));
        }"""
    )

    result = await browser.fill_draft(default_argos_reboot_campaign())

    assert result.status == "ui_changed"
    assert await browser.submit_click_count() == 0
    assert await browser._page.evaluate("window.navigationLog") == ["about"]


@pytest.mark.asyncio
async def test_multistep_rewards_are_digital_and_never_enter_agreement(browser):
    campaign = default_argos_reboot_campaign()
    await browser.open_fixture("multistep_editor.html")

    filled = await browser.fill_rewards(campaign)
    verified = await browser.read_rewards()

    assert filled.status == "ok"
    assert verified.status == "ok"
    assert verified.draft_snapshot["rewards"] == [
        {
            "title": reward.title,
            "amount": str(reward.amount),
            "description": reward.description,
            "physical": False,
        }
        for reward in campaign.rewards
    ]
    page_state = await browser._page.evaluate(
        """() => ({
            navigationLog: window.navigationLog,
            saveCounts: window.saveCounts,
            submitClicks: window.submitClicks,
        })"""
    )
    assert page_state["saveCounts"]["rewards"] == 3
    assert "agreement" not in page_state["navigationLog"]
    assert page_state["submitClicks"] == 0


@pytest.mark.asyncio
async def test_multistep_reward_verification_rejects_persisted_physical_lot(browser):
    campaign = default_argos_reboot_campaign()
    await browser.open_fixture("multistep_editor.html")
    filled = await browser.fill_rewards(campaign)
    assert filled.status == "ok"
    await browser._page.evaluate(
        "document.querySelector('#reward-list article').dataset.physical = 'true'"
    )

    verified = await browser.read_rewards()

    assert verified.status == "ui_changed"
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
