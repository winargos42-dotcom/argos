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


class _FakeRegionLocator:
    def __init__(self, ui, kind, *, text="", visible=True):
        self.ui = ui
        self.kind = kind
        self.text = text
        self.visible = visible

    async def count(self):
        return 1

    def nth(self, _index):
        return self

    async def is_visible(self):
        if self.kind == "listbox":
            return self.ui.menu_open
        return self.visible

    async def inner_text(self):
        return self.text

    async def evaluate(self, script):
        if "tagName" in script:
            return "BUTTON"
        return self.text

    async def get_attribute(self, name):
        if self.kind == "trigger":
            if name in {"aria-controls", "aria-owns"}:
                return self.ui.aria_controls
            if name == "aria-expanded":
                return "true" if self.ui.menu_open else "false"
        if self.kind == "listbox" and name == "id":
            return "about-region-options"
        return None

    def locator(self, selector):
        if self.kind == "label" and "following-sibling" in selector:
            return _FakeRegionCollection([self.ui.trigger])
        if self.kind == "listbox" and "role=\"option\"" in selector:
            return _FakeRegionCollection(items_factory=self.ui.available_options)
        return _FakeRegionCollection([])

    def get_by_role(self, role, **_kwargs):
        if self.kind == "listbox" and role == "option":
            return _FakeRegionCollection(items_factory=self.ui.available_options)
        return _FakeRegionCollection([])

    def get_by_text(self, _text, **_kwargs):
        if self.kind == "listbox":
            return _FakeRegionCollection(items_factory=self.ui.available_options)
        return _FakeRegionCollection([])

    async def click(self):
        if self.kind == "trigger":
            self.ui.menu_open = True
        elif self.kind == "option":
            self.ui.option_clicks += 1
            self.ui.trigger.text = self.text
            self.ui.menu_open = False
        elif self.kind == "unrelated":
            self.ui.unrelated_clicks += 1


class _FakeRegionCollection:
    def __init__(self, items=None, *, items_factory=None):
        self.items = items or []
        self.items_factory = items_factory

    def _items(self):
        return self.items_factory() if self.items_factory else self.items

    async def count(self):
        return len(self._items())

    def nth(self, index):
        return self._items()[index]


class _FakeNativeRegionSelect:
    def __init__(self, selected_text):
        self.selected_text = selected_text

    async def evaluate(self, script):
        if "tagName" in script:
            return "SELECT"
        if "selectedOptions" in script:
            return self.selected_text
        return ""


class _FakeLiveRegionScope:
    def __init__(self, native_select):
        self.native_select = native_select

    def get_by_label(self, _name):
        return _FakeRegionCollection([])

    def get_by_role(self, _role, **_kwargs):
        return _FakeRegionCollection([])

    def locator(self, selector):
        if selector == "select#about-region":
            return _FakeRegionCollection([self.native_select])
        return _FakeRegionCollection([])


class _FakeRegionScope:
    def __init__(self, ui):
        self.ui = ui

    def get_by_label(self, _name):
        return _FakeRegionCollection([])

    def get_by_role(self, _role, **_kwargs):
        return _FakeRegionCollection([])

    def locator(self, selector):
        if selector == "label":
            return _FakeRegionCollection([self.ui.label])
        return _FakeRegionCollection([])


class _FakeRegionPage:
    url = "https://planeta.ru/campaigns/251138/edit/about"

    def __init__(self, ui):
        self.ui = ui

    def locator(self, selector):
        if selector == '[role="listbox"]':
            return _FakeRegionCollection([self.ui.listbox])
        return _FakeRegionCollection([])

    def get_by_role(self, role, **_kwargs):
        if role == "option" and self.ui.menu_open:
            return _FakeRegionCollection(items_factory=self.ui.available_options)
        if role == "button" and self.ui.unrelated is not None:
            return _FakeRegionCollection([self.ui.unrelated])
        return _FakeRegionCollection([])

    def get_by_text(self, _text, **_kwargs):
        if self.ui.unrelated is not None:
            return _FakeRegionCollection([self.ui.unrelated])
        return _FakeRegionCollection([])

    async def wait_for_timeout(self, _milliseconds):
        self.ui.waits += 1


class _FakeRegionUi:
    def __init__(
        self,
        *,
        option_count=1,
        trigger_text="Не\u00a0выбрано",
        option_text="Тестовый\u00a0край",
        option_delay_waits=0,
        duplicate_after_waits=None,
        unrelated=False,
        aria_controls=None,
    ):
        self.menu_open = False
        self.waits = 0
        self.option_delay_waits = option_delay_waits
        self.duplicate_after_waits = duplicate_after_waits
        self.option_clicks = 0
        self.unrelated_clicks = 0
        self.aria_controls = aria_controls
        self.label = _FakeRegionLocator(self, "label", text="Регион")
        self.trigger = _FakeRegionLocator(self, "trigger", text=trigger_text)
        self.options = [
            _FakeRegionLocator(self, "option", text=option_text)
            for _ in range(option_count)
        ]
        self.listbox = _FakeRegionLocator(self, "listbox")
        self.unrelated = (
            _FakeRegionLocator(self, "unrelated", text=option_text)
            if unrelated
            else None
        )

    def available_options(self):
        if not self.menu_open or self.waits < self.option_delay_waits:
            return []
        options = list(self.options)
        if (
            self.duplicate_after_waits is not None
            and self.waits >= self.duplicate_after_waits
            and options
        ):
            options.append(
                _FakeRegionLocator(self, "option", text=options[0].text)
            )
        return options


@pytest.mark.asyncio
async def test_custom_about_region_selects_exact_configured_option():
    ui = _FakeRegionUi()
    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)

    selected = await browser._set_about_region(
        _FakeRegionPage(ui),
        _FakeRegionScope(ui),
        "Тестовый край",
    )

    assert selected == "Тестовый край"
    assert ui.trigger.text == "Тестовый\u00a0край"


@pytest.mark.asyncio
async def test_custom_about_region_accepts_exact_planeta_location_label():
    ui = _FakeRegionUi()
    ui.label.text = "Регион, область, край"
    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)

    selected = await browser._set_about_region(
        _FakeRegionPage(ui),
        _FakeRegionScope(ui),
        "Тестовый край",
    )

    assert selected == "Тестовый край"
    assert ui.option_clicks == 1


@pytest.mark.asyncio
async def test_about_region_reads_live_hidden_native_select():
    native_select = _FakeNativeRegionSelect("Тестовый край")
    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)

    control = await browser._about_region_control(
        _FakeLiveRegionScope(native_select),
        "Тестовый край",
    )

    assert control is native_select
    assert await browser._region_control_value(control) == "Тестовый край"


@pytest.mark.asyncio
async def test_custom_about_region_refuses_ambiguous_exact_options():
    ui = _FakeRegionUi(
        option_count=2,
        trigger_text="Не выбрано",
        option_text="Тестовый край",
    )
    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)

    selected = await browser._set_about_region(
        _FakeRegionPage(ui),
        _FakeRegionScope(ui),
        "Тестовый край",
    )

    assert selected is None
    assert ui.trigger.text == "Не выбрано"
    assert ui.option_clicks == 0


@pytest.mark.asyncio
async def test_custom_about_region_never_clicks_unrelated_same_text_button():
    ui = _FakeRegionUi(
        option_count=0,
        trigger_text="Не выбрано",
        option_text="Тестовый край",
        unrelated=True,
    )
    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)

    selected = await browser._set_about_region(
        _FakeRegionPage(ui),
        _FakeRegionScope(ui),
        "Тестовый край",
    )

    assert selected is None
    assert ui.unrelated_clicks == 0


@pytest.mark.asyncio
async def test_custom_about_region_waits_for_delayed_associated_option():
    ui = _FakeRegionUi(
        trigger_text="Не выбрано",
        option_text="Тестовый край",
        option_delay_waits=1,
    )
    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)

    selected = await browser._set_about_region(
        _FakeRegionPage(ui),
        _FakeRegionScope(ui),
        "Тестовый край",
    )

    assert selected == "Тестовый край"
    assert ui.option_clicks == 1


@pytest.mark.asyncio
async def test_custom_about_region_refuses_delayed_duplicate_option():
    ui = _FakeRegionUi(
        trigger_text="Не выбрано",
        option_text="Тестовый край",
        option_delay_waits=1,
        duplicate_after_waits=2,
    )
    browser = PlanetaBrowser(base_url="https://planeta.ru", headless=True)

    selected = await browser._set_about_region(
        _FakeRegionPage(ui),
        _FakeRegionScope(ui),
        "Тестовый край",
    )

    assert selected is None
    assert ui.option_clicks == 0


def test_pristine_about_retry_skips_disabled_save():
    values = {"title": "same", "region": "Тестовый край"}

    action = PlanetaBrowser._safe_step_save_action(
        initial_values=values,
        expected_values=values,
        save_enabled=False,
    )

    assert action == "skip"


def test_pristine_goal_retry_skips_disabled_save():
    action = PlanetaBrowser._safe_step_save_action(
        initial_values={"target_amount": "200000"},
        expected_values={"target_amount": "200000"},
        save_enabled=False,
    )

    assert action == "skip"


def test_changed_step_with_disabled_save_is_blocked():
    action = PlanetaBrowser._safe_step_save_action(
        initial_values={"target_amount": "100000"},
        expected_values={"target_amount": "200000"},
        save_enabled=False,
    )

    assert action == "blocked"


def test_pristine_step_with_enabled_save_is_not_saved():
    values = {"target_amount": "200000"}

    action = PlanetaBrowser._safe_step_save_action(
        initial_values=values,
        expected_values=values,
        save_enabled=True,
    )

    assert action == "skip"


class _FakeAboutField:
    def __init__(self, state, key, *, enabled=False):
        self.state = state
        self.key = key
        self.enabled = enabled

    async def evaluate(self, _script):
        return self.state[self.key]

    async def fill(self, value):
        self.state[self.key] = value

    async def press(self, _key):
        return None

    async def is_enabled(self):
        return self.enabled


class _PersistenceReadbackBrowser(PlanetaBrowser):
    def __init__(self, current, persisted):
        super().__init__(base_url="https://planeta.ru", headless=True)
        self.current = current
        self.persisted = persisted
        self.opened_steps = []
        self.about_scope = object()
        self.about = {
            key: _FakeAboutField(self.current, key)
            for key in ("title", "summary", "end_date", "story")
        }
        self.about["save"] = _FakeAboutField(
            self.current, "save", enabled=False
        )
        self.region_control = object()

    async def _open_editor_step(self, _page, step):
        self.opened_steps.append(step)
        if step != "about":
            raise AssertionError(f"unsafe downstream navigation to {step}")
        return self.about_scope

    async def _multistep_about_controls(self, _scope):
        return self.about

    async def _about_region_control(self, _scope, _expected_region):
        return self.region_control

    async def _region_control_value(self, _control):
        return self.current.get("region", "")

    async def _reload_safe_editor_step(self, _page, step):
        assert step == "about"
        self.current.update(self.persisted)
        if "save_enabled" in self.persisted:
            self.about["save"].enabled = self.persisted["save_enabled"]
        return self.about_scope


def _campaign_about_values(campaign, *, region=None):
    values = {
        "title": campaign.title,
        "summary": campaign.summary,
        "end_date": campaign.end_date.strftime("%d.%m.%Y"),
        "story": campaign.story,
        "save": "",
    }
    if region is not None:
        values["region"] = region
    return values


@pytest.mark.asyncio
async def test_missing_region_pristine_disabled_about_stops_before_assets():
    campaign = default_argos_reboot_campaign()
    current = _campaign_about_values(campaign)
    browser = _PersistenceReadbackBrowser(current, dict(current))

    result = await browser._fill_multistep_draft(object(), campaign)

    assert result.status == "human_action_required"
    assert browser.opened_steps == ["about"]


@pytest.mark.asyncio
async def test_missing_region_unknown_dirty_state_is_rechecked_after_reload():
    campaign = default_argos_reboot_campaign()
    current = _campaign_about_values(campaign)
    persisted = {**current, "save_enabled": False}
    browser = _PersistenceReadbackBrowser(current, persisted)
    browser.about["save"].enabled = True

    result = await browser._fill_multistep_draft(object(), campaign)

    assert result.status == "human_action_required"
    assert browser.opened_steps == ["about"]


@pytest.mark.asyncio
async def test_unsaved_equal_about_values_that_revert_on_reload_are_rejected():
    region = "Тестовый край"
    campaign = default_argos_reboot_campaign().model_copy(
        update={"region": region}
    )
    current = _campaign_about_values(campaign, region=region)
    persisted = {**current, "title": "Старое сохранённое название"}
    browser = _PersistenceReadbackBrowser(current, persisted)

    result = await browser._fill_multistep_draft(object(), campaign)

    assert result.status == "ui_changed"
    assert browser.opened_steps == ["about"]


@pytest.mark.asyncio
async def test_multistep_fill_saves_only_about_assets_and_goal(browser):
    campaign = default_argos_reboot_campaign().model_copy(
        update={"region": "Тестовый край"}
    )
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
        r"""() => ({
            activeStep: document.body.dataset.activeStep,
            navigationLog: window.navigationLog,
            saveCounts: window.saveCounts,
            mediaFiles: window.mediaFiles,
            region: document.querySelector('#about-region').selectedOptions[0]
              .textContent.replace(/\s+/g, ' ').trim(),
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
        "region": "Тестовый край",
        "submitClicks": 0,
    }


@pytest.mark.asyncio
async def test_multistep_retry_skips_pristine_disabled_about_and_goal(browser):
    campaign = default_argos_reboot_campaign().model_copy(
        update={"region": "Тестовый край"}
    )
    await browser.open_fixture("multistep_editor.html")
    first = await browser.fill_draft(campaign)
    assert first.status == "ok"
    await browser._page.evaluate(
        """() => {
            document.querySelector('[data-step-form="about"] button[type="submit"]').disabled = true;
            document.querySelector('[data-step-form="goal"] button[type="submit"]').disabled = true;
        }"""
    )

    retried = await browser.fill_draft(campaign)

    assert retried.status == "ok"
    page_state = await browser._page.evaluate(
        "({saveCounts: window.saveCounts, reloadCounts: window.reloadCounts})"
    )
    save_counts = page_state["saveCounts"]
    assert save_counts["about"] == 1
    assert save_counts["goal"] == 1
    assert page_state["reloadCounts"] == {"about": 1, "goal": 1}


@pytest.mark.asyncio
async def test_missing_region_disabled_about_never_navigates_downstream(browser):
    campaign = default_argos_reboot_campaign()
    await browser.open_fixture("multistep_editor.html")
    await browser._page.evaluate(
        """values => {
            document.querySelector('#about-name').value = values.title;
            document.querySelector('#about-project').value = values.summary;
            document.querySelector('#about-end-date').value = values.endDate;
            document.querySelector('[contenteditable="true"]').innerText = values.story;
            document.querySelector('[data-step-form="about"] button[type="submit"]').disabled = true;
        }""",
        {
            "title": campaign.title,
            "summary": campaign.summary,
            "endDate": campaign.end_date.strftime("%d.%m.%Y"),
            "story": campaign.story,
        },
    )

    result = await browser.fill_draft(campaign)

    assert result.status == "human_action_required"
    assert await browser._page.evaluate("window.navigationLog") == ["about"]


@pytest.mark.asyncio
async def test_unsaved_equal_about_dom_is_rejected_after_reload(browser):
    campaign = default_argos_reboot_campaign().model_copy(
        update={"region": "Тестовый край"}
    )
    await browser.open_fixture("multistep_editor.html")
    await browser._page.evaluate(
        """values => {
            document.querySelector('#about-name').value = values.title;
            document.querySelector('#about-project').value = values.summary;
            document.querySelector('#about-end-date').value = values.endDate;
            document.querySelector('#about-region').selectedIndex = 1;
            document.querySelector('[contenteditable="true"]').innerText = values.story;
            document.querySelector('[data-step-form="about"] button[type="submit"]').disabled = true;
        }""",
        {
            "title": campaign.title,
            "summary": campaign.summary,
            "endDate": campaign.end_date.strftime("%d.%m.%Y"),
            "story": campaign.story,
        },
    )

    result = await browser.fill_draft(campaign)

    assert result.status == "ui_changed"
    assert await browser._page.evaluate("window.navigationLog") == ["about"]


@pytest.mark.asyncio
async def test_multistep_read_reports_only_redacted_region_match(browser):
    campaign = default_argos_reboot_campaign().model_copy(
        update={"region": "Тестовый край"}
    )
    await browser.open_fixture("multistep_editor.html")
    filled = await browser.fill_draft(campaign)
    assert filled.status == "ok"

    matching = await browser.read_draft(expected_region=campaign.region)
    await browser._page.evaluate(
        "document.querySelector('#about-region').selectedIndex = 0"
    )
    mismatching = await browser.read_draft(expected_region=campaign.region)

    assert matching.draft_snapshot["region_match"] is True
    assert mismatching.draft_snapshot["region_match"] is False
    assert "region" not in matching.draft_snapshot
    assert "Тестовый край" not in str(matching.safe_dict())


@pytest.mark.asyncio
async def test_routed_multistep_fill_persists_only_safe_editor_steps():
    campaign = default_argos_reboot_campaign().model_copy(
        update={"region": "Тестовый край"}
    )
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

    assert result.status == "ok", result.reason
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
        "region": campaign.region,
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
