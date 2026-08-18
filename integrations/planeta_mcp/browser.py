from __future__ import annotations

import re
from enum import StrEnum
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from pydantic import BaseModel, Field
from playwright.async_api import (
    Browser,
    BrowserContext,
    Error as PlaywrightError,
    Locator,
    Page,
    Playwright,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)

from . import selectors
from .models import CampaignPayload


class BrowserState(StrEnum):
    OK = "ok"
    CONFIGURATION_REQUIRED = "configuration_required"
    HUMAN_ACTION_REQUIRED = "human_action_required"
    AUTHENTICATION_REQUIRED = "authentication_required"
    CAPTCHA_REQUIRED = "captcha_required"
    UI_CHANGED = "ui_changed"
    VALIDATION_FAILED = "validation_failed"
    NETWORK_ERROR = "network_error"
    PLANETA_ERROR = "planeta_error"


class BrowserResult(BaseModel):
    status: str
    reason: str = ""
    draft_snapshot: dict[str, Any] = Field(default_factory=dict)

    def safe_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def _origin(url: str) -> tuple[str, str, int | None]:
    parsed = urlsplit(url)
    return parsed.scheme.casefold(), (parsed.hostname or "").casefold(), parsed.port


def _normalize_editor_text(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


_SEMANTIC_NAMES = {
    "title": re.compile(r"^\s*(?:название(?:\s+проекта)?|заголовок(?:\s+проекта)?)\s*\*?\s*$", re.I),
    "target": re.compile(
        r"^\s*(?:сумма\s+сбора|финансовая\s+цель|цель\s+сбора|нужно\s+собрать|сумма)\s*\*?\s*$",
        re.I,
    ),
    "summary": re.compile(
        r"^\s*(?:краткое\s+описание(?:\s+проекта)?|короткое\s+описание|анонс)\s*\*?\s*$",
        re.I,
    ),
    "story": re.compile(
        r"^\s*(?:описание\s+проекта|подробное\s+описание|история\s+проекта|о\s+проекте)\s*\*?\s*$",
        re.I,
    ),
    "save": re.compile(r"^\s*сохранить(?:\s+(?:черновик|изменения))?\s*$", re.I),
    "submit": re.compile(r"^\s*отправить(?:\s+проект)?\s+на\s+модераци(?:ю|и)\s*$", re.I),
}

_EXACT_SELECTORS = {
    "title": selectors.TITLE_INPUT,
    "target": selectors.TARGET_INPUT,
    "summary": selectors.SUMMARY_INPUT,
    "story": selectors.STORY_EDITOR,
    "save": selectors.SAVE_DRAFT_BUTTON,
    "submit": selectors.SUBMIT_MODERATION_BUTTON,
}

_DRAFT_EDITOR_KEYS = ("title", "target", "summary", "story", "save")
_REVIEW_NAV = re.compile(r"^\s*проверка\s+и\s+публикация\s*$", re.I)
_REWARDS_NAV = re.compile(r"^\s*вознаграждения\s*$", re.I)
_ADD_REWARD = re.compile(r"^\s*добавить\s+вознаграждение\s*$", re.I)
_ADD_REWARD_SHORT = re.compile(r"^\s*добавить\s*$", re.I)
_REWARD_TITLE = re.compile(r"^\s*название\s+вознаграждения\s*\*?\s*$", re.I)
_REWARD_AMOUNT = re.compile(r"^\s*(?:стоимость|сумма)\s+вознаграждения\s*\*?\s*$", re.I)
_REWARD_DESCRIPTION = re.compile(r"^\s*описание\s+вознаграждения\s*\*?\s*$", re.I)
_REWARD_PHYSICAL = re.compile(r"^\s*(?:физическое\s+вознаграждение|требуется\s+доставка)\s*$", re.I)
_SAVE_REWARD = re.compile(r"^\s*сохранить\s+вознаграждение\s*$", re.I)
_SAFE_STEP_SAVE = re.compile(r"^\s*сохранить\s*$", re.I)
_SAFE_EDITOR_STEPS = frozenset({"about", "assets", "goal", "rewards"})
_COVER_ASSET = "assets/argos-reboot-cover.jpg"
_MAIN_ASSET = "assets/argos-reboot-fire-main.jpg"
_ASSET_PREVIEW_SELECTOR = (
    '[class*="assets-module__"] img, '
    '[class*="assets-page-module__"] img'
)


class PlanetaBrowser:
    def __init__(
        self,
        base_url: str = "https://planeta.ru",
        draft_url: str | None = None,
        headless: bool = True,
        fixture_dir: str | Path | None = None,
        executable_path: str | None = None,
        storage_state: dict[str, Any] | None = None,
        cdp_url: str | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.draft_url = draft_url.strip() if draft_url else None
        if self.draft_url and _origin(self.draft_url) != _origin(self.base_url):
            raise ValueError("draft_url must use the same origin as base_url")
        if self.draft_url:
            parsed_draft = urlsplit(self.draft_url)
            editor_root, separator, configured_step = (
                parsed_draft.path.rstrip("/").rpartition("/")
            )
            if (
                not separator
                or configured_step != "about"
                or not editor_root.endswith("/edit")
            ):
                raise ValueError("draft_url must point to the safe about editor step")
        self.headless = headless
        self.fixture_dir = Path(fixture_dir) if fixture_dir else None
        self.executable_path = executable_path
        self.storage_state = storage_state
        self.cdp_url = cdp_url.strip() if cdp_url else None
        self._fixture_loaded = False
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._attached_over_cdp = False
        self._last_rewards_snapshot: list[dict[str, Any]] = []

    async def _ensure_page(self) -> Page:
        if self._page is not None:
            return self._page
        self._playwright = await async_playwright().start()
        if self.cdp_url:
            self._browser = await self._playwright.chromium.connect_over_cdp(self.cdp_url)
            self._attached_over_cdp = True
            contexts = self._browser.contexts
            if not contexts:
                raise RuntimeError("connected Chromium has no browser context")
            self._context = contexts[0]
            pages = self._context.pages
            self._page = pages[0] if pages else await self._context.new_page()
            return self._page

        launch_kwargs: dict[str, Any] = {"headless": self.headless}
        if self.executable_path:
            launch_kwargs["executable_path"] = self.executable_path
        self._browser = await self._playwright.chromium.launch(**launch_kwargs)
        context_kwargs: dict[str, Any] = {}
        if self.storage_state is not None:
            context_kwargs["storage_state"] = self.storage_state
        self._context = await self._browser.new_context(**context_kwargs)
        self._page = await self._context.new_page()
        return self._page

    async def _prepare_page(self) -> tuple[Page | None, BrowserResult | None]:
        if not self._fixture_loaded and not self.draft_url:
            return None, BrowserResult(
                status=BrowserState.CONFIGURATION_REQUIRED.value,
                reason="PLANETA_DRAFT_URL must point to the owner's Planeta.ru draft editor",
            )
        page = await self._ensure_page()
        if not self.cdp_url and not self._fixture_loaded and self.draft_url and page.url != self.draft_url:
            await page.goto(self.draft_url, wait_until="domcontentloaded", timeout=30000)
        if not self._fixture_loaded:
            current_step = self._current_editor_step(page)
            if current_step is not None:
                await self._wait_for_step_ready(page, current_step)
        return page, None

    async def open_fixture(self, filename: str) -> None:
        if self.fixture_dir is None:
            raise RuntimeError("fixture_dir is not configured")
        path = (self.fixture_dir / filename).resolve()
        if not path.is_file() or self.fixture_dir.resolve() not in path.parents:
            raise FileNotFoundError(filename)
        page = await self._ensure_page()
        await page.set_content(path.read_text(encoding="utf-8"), wait_until="domcontentloaded")
        self._fixture_loaded = True

    @staticmethod
    async def _unique_visible(locator: Locator) -> Locator | None:
        visible: list[Locator] = []
        for index in range(await locator.count()):
            candidate = locator.nth(index)
            if await candidate.is_visible():
                visible.append(candidate)
                if len(visible) > 1:
                    return None
        return visible[0] if len(visible) == 1 else None

    def _editor_step_url(self, step: str) -> str | None:
        if step not in _SAFE_EDITOR_STEPS or not self.draft_url:
            return None
        parsed = urlsplit(self.draft_url)
        editor_root, separator, configured_step = parsed.path.rstrip("/").rpartition("/")
        if (
            not separator
            or configured_step not in _SAFE_EDITOR_STEPS
            or not editor_root.endswith("/edit")
        ):
            return None
        return parsed._replace(
            path=f"{editor_root}/{step}",
            query="",
            fragment="",
        ).geturl()

    def _current_editor_step(self, page: Page) -> str | None:
        if self._fixture_loaded:
            return None
        parsed = urlsplit(page.url)
        if not self.draft_url or _origin(page.url) != _origin(self.draft_url):
            return None
        editor_root, separator, step = parsed.path.rstrip("/").rpartition("/")
        draft_root, _, _ = urlsplit(self.draft_url).path.rstrip("/").rpartition("/")
        if not separator or editor_root != draft_root or step not in _SAFE_EDITOR_STEPS:
            return None
        return step

    async def _is_multistep_editor(self, page: Page) -> bool:
        if self._fixture_loaded:
            return await page.locator("[data-step-panel]").count() > 0
        return self._current_editor_step(page) in _SAFE_EDITOR_STEPS

    async def _wait_for_step_ready(self, page: Page, step: str) -> None:
        if step == "about":
            for selector in (
                selectors.ABOUT_TITLE_INPUT,
                selectors.ABOUT_SUMMARY_INPUT,
                selectors.ABOUT_END_DATE_INPUT,
            ):
                await page.locator(selector).wait_for(state="visible", timeout=15000)
            await page.locator(selectors.ABOUT_STORY_EDITOR).first.wait_for(
                state="visible", timeout=15000
            )
            await page.get_by_role("button", name=_SAFE_STEP_SAVE).first.wait_for(
                state="visible", timeout=15000
            )
            return
        if step == "assets":
            await page.locator(selectors.ASSET_FILE_INPUTS).first.wait_for(
                state="attached", timeout=15000
            )
            await page.locator(selectors.ASSET_FILE_INPUTS).nth(1).wait_for(
                state="attached", timeout=15000
            )
            await page.get_by_role("button", name=_SAFE_STEP_SAVE).first.wait_for(
                state="visible", timeout=15000
            )
            return
        if step == "goal":
            await page.locator(selectors.GOAL_INPUT).wait_for(
                state="visible", timeout=15000
            )
            await page.get_by_role("button", name=_SAFE_STEP_SAVE).first.wait_for(
                state="visible", timeout=15000
            )
            return
        await page.get_by_role("button", name=_ADD_REWARD).first.wait_for(
            state="visible", timeout=15000
        )

    async def _open_editor_step(self, page: Page, step: str) -> Locator | None:
        if step not in _SAFE_EDITOR_STEPS:
            return None
        if self._fixture_loaded:
            scope = page.locator(f'[data-step-panel="{step}"]:not([hidden])')
            if await scope.count() != 1:
                navigation = page.locator(f'[data-editor-step="{step}"]')
                navigation = await self._unique_visible(navigation)
                if navigation is None:
                    return None
                await navigation.click()
                scope = page.locator(f'[data-step-panel="{step}"]:not([hidden])')
            return scope if await scope.count() == 1 else None

        target = self._editor_step_url(step)
        if target is None:
            return None
        current = urlsplit(page.url)
        expected = urlsplit(target)
        if _origin(page.url) != _origin(target) or current.path.rstrip("/") != expected.path.rstrip("/"):
            await page.goto(target, wait_until="domcontentloaded", timeout=30000)
        current = urlsplit(page.url)
        if _origin(page.url) != _origin(target) or current.path.rstrip("/") != expected.path.rstrip("/"):
            return None
        await self._wait_for_step_ready(page, step)
        return page.locator("body")

    async def _safe_step_save(self, scope: Locator) -> Locator | None:
        buttons = scope.locator('button[type="submit"]')
        matches: list[Locator] = []
        for index in range(await buttons.count()):
            candidate = buttons.nth(index)
            if not await candidate.is_visible():
                continue
            if _SAFE_STEP_SAVE.fullmatch((await candidate.inner_text()).strip()):
                matches.append(candidate)
                if len(matches) > 1:
                    return None
        return matches[0] if len(matches) == 1 else None

    async def _multistep_about_controls(
        self, scope: Locator
    ) -> dict[str, Locator] | None:
        candidates = {
            "title": scope.locator(selectors.ABOUT_TITLE_INPUT),
            "summary": scope.locator(selectors.ABOUT_SUMMARY_INPUT),
            "end_date": scope.locator(selectors.ABOUT_END_DATE_INPUT),
            "story": scope.locator(selectors.ABOUT_STORY_EDITOR),
        }
        resolved: dict[str, Locator] = {}
        for key, candidate in candidates.items():
            control = await self._unique_visible(candidate)
            if control is None:
                return None
            resolved[key] = control
        save = await self._safe_step_save(scope)
        if save is None:
            return None
        resolved["save"] = save
        return resolved

    async def _reward_add_button(self, scope: Locator) -> Locator | None:
        for pattern in (_ADD_REWARD, _ADD_REWARD_SHORT):
            locator = scope.get_by_role("button", name=pattern)
            visible: list[Locator] = []
            for index in range(await locator.count()):
                candidate = locator.nth(index)
                if await candidate.is_visible():
                    visible.append(candidate)
                    if len(visible) > 1:
                        return None
            if len(visible) == 1:
                return visible[0]
        return None

    async def _current_multistep_scope(
        self, page: Page
    ) -> tuple[str, Locator] | None:
        if self._fixture_loaded:
            scope = page.locator("[data-step-panel]:not([hidden])")
            if await scope.count() != 1:
                return None
            step = await scope.get_attribute("data-step-panel")
            if step not in _SAFE_EDITOR_STEPS:
                return None
            return step, scope
        step = self._current_editor_step(page)
        if step is None:
            return None
        return step, page.locator("body")

    async def _multistep_step_is_known(self, page: Page) -> bool:
        current = await self._current_multistep_scope(page)
        if current is None:
            return False
        step, scope = current
        if step == "about":
            return await self._multistep_about_controls(scope) is not None
        if step == "assets":
            files = scope.locator(selectors.ASSET_FILE_INPUTS)
            return await files.count() == 2 and await self._safe_step_save(scope) is not None
        if step == "goal":
            goal = await self._unique_visible(scope.locator(selectors.GOAL_INPUT))
            return goal is not None and await self._safe_step_save(scope) is not None
        return await self._reward_add_button(scope) is not None

    @staticmethod
    def _normalized_amount(value: str) -> str:
        return "".join(character for character in value if character.isdigit())

    @staticmethod
    def _campaign_media_paths(payload: CampaignPayload) -> tuple[Path, Path] | None:
        if payload.cover_image_path != _COVER_ASSET or payload.main_image_path != _MAIN_ASSET:
            return None
        package_root = Path(__file__).resolve().parent
        cover = package_root / _COVER_ASSET
        main = package_root / _MAIN_ASSET
        if not cover.is_file() or not main.is_file():
            return None
        return cover, main

    async def _resolve_control(self, page: Page, key: str) -> Locator | None:
        exact = page.locator(_EXACT_SELECTORS[key])
        exact_count = await exact.count()
        if exact_count == 1:
            return exact
        if exact_count > 1:
            return None

        semantic_name = _SEMANTIC_NAMES[key]
        if key in {"save", "submit"}:
            for role in ("button", "link"):
                candidate = page.get_by_role(role, name=semantic_name)
                count = await candidate.count()
                if count == 1:
                    return candidate
                if count > 1:
                    return None
            return None

        labelled = page.get_by_label(semantic_name)
        count = await labelled.count()
        if count == 1:
            return labelled
        if count > 1:
            return None

        roles = ("textbox", "spinbutton") if key == "target" else ("textbox",)
        for role in roles:
            candidate = page.get_by_role(role, name=semantic_name)
            count = await candidate.count()
            if count == 1:
                return candidate
            if count > 1:
                return None

        placeholder = page.get_by_placeholder(semantic_name)
        return placeholder if await placeholder.count() == 1 else None

    async def _resolve_required_controls(self, page: Page) -> dict[str, Locator] | None:
        resolved: dict[str, Locator] = {}
        for key in _DRAFT_EDITOR_KEYS:
            control = await self._resolve_control(page, key)
            if control is None:
                return None
            resolved[key] = control
        return resolved

    async def classify_page(self, page: Page) -> BrowserState:
        try:
            url = page.url.casefold()
            body_text = (await page.locator("body").inner_text()).casefold()
            if "login" in url or await page.locator(selectors.LOGIN_PASSWORD_INPUT).count() > 0:
                return BrowserState.AUTHENTICATION_REQUIRED
            if await page.locator(selectors.CAPTCHA_WIDGET).count() > 0 or any(
                marker in body_text for marker in ("captcha", "капча", "я не робот")
            ):
                return BrowserState.CAPTCHA_REQUIRED
            human_markers = (
                "подтвердите личность",
                "верификация личности",
                "загрузите паспорт",
                "загрузить паспорт",
                "предоставьте паспорт",
                "введите инн",
                "укажите инн",
                "загрузите инн",
                "sms-код",
                "смс-код",
                "код из письма",
                "подтвердите e-mail",
                "подтвердите email",
            )
            if any(marker in body_text for marker in human_markers):
                return BrowserState.HUMAN_ACTION_REQUIRED
            if "403" in body_text and any(
                marker in body_text for marker in ("доступ запрещен", "access denied")
            ):
                if "войти" in body_text:
                    return BrowserState.AUTHENTICATION_REQUIRED
                return BrowserState.PLANETA_ERROR
            if "ошибка модерации" in body_text or "ошибка сервиса" in body_text:
                return BrowserState.PLANETA_ERROR
            if await self._resolve_required_controls(page) is not None:
                return BrowserState.OK
            if await self._is_multistep_editor(page) and await self._multistep_step_is_known(page):
                return BrowserState.OK
            return BrowserState.UI_CHANGED
        except PlaywrightTimeoutError:
            return BrowserState.NETWORK_ERROR
        except PlaywrightError:
            return BrowserState.PLANETA_ERROR

    async def inspect(self) -> BrowserResult:
        try:
            page, early = await self._prepare_page()
            if early is not None:
                return early
            assert page is not None
            state = await self.classify_page(page)
        except PlaywrightTimeoutError:
            state = BrowserState.NETWORK_ERROR
        except PlaywrightError:
            state = BrowserState.PLANETA_ERROR
        reasons = {
            BrowserState.OK: "known draft editor detected",
            BrowserState.CONFIGURATION_REQUIRED: "Planeta.ru draft URL is not configured",
            BrowserState.AUTHENTICATION_REQUIRED: "human Planeta.ru login is required",
            BrowserState.CAPTCHA_REQUIRED: "CAPTCHA/anti-bot step requires human action",
            BrowserState.HUMAN_ACTION_REQUIRED: "identity or verification step requires human action",
            BrowserState.UI_CHANGED: "known draft selectors are missing or ambiguous",
            BrowserState.VALIDATION_FAILED: "campaign validation failed",
            BrowserState.NETWORK_ERROR: "browser/network timeout",
            BrowserState.PLANETA_ERROR: "Planeta.ru or browser error",
        }
        return BrowserResult(status=state.value, reason=reasons[state])

    async def ui_diagnostic_snapshot(self) -> dict[str, Any]:
        """Return selector metadata without field values or URL query data."""
        page = await self._ensure_page()
        parsed = urlsplit(page.url)
        safe_url = parsed._replace(query="", fragment="").geturl()
        controls = await page.locator(
            "input, textarea, button, [contenteditable='true']"
        ).evaluate_all(
            """elements => elements.slice(0, 40).map(element => ({
                tag: element.tagName.toLowerCase(),
                type: element.getAttribute('type') || '',
                name: element.getAttribute('name') || '',
                id: element.id || '',
                placeholder: element.getAttribute('placeholder') || '',
                ariaLabel: element.getAttribute('aria-label') || '',
                testId: element.getAttribute('data-testid') || '',
                text: element.tagName === 'BUTTON'
                    ? String(element.innerText || '').trim().slice(0, 80)
                    : '',
            }))"""
        )
        return {
            "url": safe_url,
            "title": (await page.title())[:160],
            "bodyText": (await page.locator("body").inner_text())[:1000],
            "controls": controls,
        }

    async def navigate_to_draft(self) -> BrowserResult:
        if not self.draft_url:
            return BrowserResult(status="configuration_required", reason="Planeta.ru draft URL is not configured")
        try:
            page = await self._ensure_page()
            if page.url != self.draft_url:
                await page.goto(self.draft_url, wait_until="domcontentloaded", timeout=30000)
            return BrowserResult(status="ok", reason="configured draft opened")
        except PlaywrightTimeoutError:
            return BrowserResult(status="network_error", reason="timeout while opening configured draft")
        except PlaywrightError as exc:
            return BrowserResult(status="planeta_error", reason=f"browser error: {type(exc).__name__}")

    @staticmethod
    async def _control_value(control: Locator) -> str:
        value = await control.evaluate(
            """(el) => {
                if ('value' in el) return String(el.value ?? '');
                return String(el.innerText ?? el.textContent ?? '');
            }"""
        )
        return _normalize_editor_text(str(value))

    async def _read_snapshot(self, page: Page) -> dict[str, str]:
        controls: dict[str, Locator] = {}
        for key in ("title", "target", "summary", "story"):
            control = await self._resolve_control(page, key)
            if control is None:
                raise LookupError(key)
            controls[key] = control
        return {
            "title": await self._control_value(controls["title"]),
            "target_amount": await self._control_value(controls["target"]),
            "summary": await self._control_value(controls["summary"]),
            "story": await self._control_value(controls["story"]),
        }

    async def _read_multistep_about(self, page: Page) -> dict[str, str]:
        scope = await self._open_editor_step(page, "about")
        if scope is None:
            raise LookupError("about")
        controls = await self._multistep_about_controls(scope)
        if controls is None:
            raise LookupError("about")
        return {
            "title": await self._control_value(controls["title"]),
            "end_date": await self._control_value(controls["end_date"]),
            "summary": await self._control_value(controls["summary"]),
            "story": await self._control_value(controls["story"]),
        }

    async def _read_multistep_snapshot(self, page: Page) -> dict[str, str]:
        snapshot = await self._read_multistep_about(page)
        goal_scope = await self._open_editor_step(page, "goal")
        if goal_scope is None:
            raise LookupError("goal")
        goal = await self._unique_visible(goal_scope.locator(selectors.GOAL_INPUT))
        if goal is None:
            raise LookupError("goal")
        snapshot["target_amount"] = self._normalized_amount(
            await self._control_value(goal)
        )
        assets_scope = await self._open_editor_step(page, "assets")
        if assets_scope is None or not await self._assets_are_persisted(
            page,
            assets_scope,
            Path(_COVER_ASSET).name,
            Path(_MAIN_ASSET).name,
        ):
            raise LookupError("assets")
        snapshot["cover_image"] = Path(_COVER_ASSET).name
        snapshot["main_image"] = Path(_MAIN_ASSET).name
        if await self._open_editor_step(page, "about") is None:
            raise LookupError("about")
        return snapshot

    async def _exact_asset_inputs(self, scope: Locator) -> list[Locator] | None:
        inputs = scope.locator(selectors.ASSET_FILE_INPUTS)
        return [inputs.nth(0), inputs.nth(1)] if await inputs.count() == 2 else None

    async def _save_and_reload_step(
        self, page: Page, step: str, current_scope: Locator, save: Locator
    ) -> Locator | None:
        if self._fixture_loaded:
            await save.click()
            return current_scope
        expected = self._editor_step_url(step)
        if expected is None:
            return None
        await save.click()
        # The current editor does not expose a stable save endpoint or success
        # marker. Use a bounded settle period and rely on the mandatory reload plus
        # exact field/media readback below as the authoritative persistence proof.
        await page.wait_for_timeout(2000)
        current = urlsplit(page.url)
        expected_url = urlsplit(expected)
        if (
            _origin(page.url) != _origin(expected)
            or current.path.rstrip("/") != expected_url.path.rstrip("/")
        ):
            return None
        await page.reload(wait_until="domcontentloaded", timeout=30000)
        return await self._open_editor_step(page, step)

    @staticmethod
    async def _asset_preview_sources(page: Page) -> set[str]:
        sources = await page.locator(_ASSET_PREVIEW_SELECTOR).evaluate_all(
            """images => images
                .filter(image => {
                    const src = String(image.currentSrc || image.src || '');
                    const rect = image.getBoundingClientRect();
                    return image.complete
                        && image.naturalWidth > 1
                        && image.naturalHeight > 1
                        && rect.width > 0
                        && rect.height > 0
                        && src
                        && !/placeholder|spinner|loader/i.test(src);
                })
                .map(image => String(image.currentSrc || image.src))"""
        )
        return set(sources)

    async def _wait_for_new_asset_preview(
        self, page: Page, existing_sources: set[str]
    ) -> set[str] | None:
        try:
            await page.wait_for_function(
                """({selector, existing}) => Array.from(
                    document.querySelectorAll(selector)
                ).some(image => {
                    const src = String(image.currentSrc || image.src || '');
                    const rect = image.getBoundingClientRect();
                    return image.complete
                        && image.naturalWidth > 1
                        && image.naturalHeight > 1
                        && rect.width > 0
                        && rect.height > 0
                        && src
                        && !existing.includes(src)
                        && !/placeholder|spinner|loader/i.test(src);
                })""",
                arg={
                    "selector": _ASSET_PREVIEW_SELECTOR,
                    "existing": sorted(existing_sources),
                },
                timeout=15000,
            )
        except PlaywrightTimeoutError:
            return None
        sources = await self._asset_preview_sources(page)
        return sources if sources - existing_sources else None

    async def _assets_are_persisted(
        self,
        page: Page,
        scope: Locator,
        cover_name: str,
        main_name: str,
        baseline_sources: set[str] | None = None,
    ) -> bool:
        if self._fixture_loaded:
            media = await page.evaluate("() => window.mediaFiles || {}")
            return media == {"cover": cover_name, "main": main_name}
        del scope, cover_name, main_name
        try:
            await page.wait_for_function(
                """({selector, baseline}) => {
                    const previews = Array.from(document.querySelectorAll(selector))
                    .map(image => {
                        const src = String(image.currentSrc || image.src || '');
                        const rect = image.getBoundingClientRect();
                        const valid = image.complete
                            && image.naturalWidth > 1
                            && image.naturalHeight > 1
                            && rect.width > 0
                            && rect.height > 0
                            && src
                            && !/placeholder|spinner|loader/i.test(src);
                        return valid ? {
                            src,
                            ratio: image.naturalWidth / image.naturalHeight,
                        } : null;
                    }).filter(Boolean);
                    const newSources = previews.filter(
                        preview => !baseline.includes(preview.src)
                    );
                    const persisted = baseline.length ? newSources : previews;
                    const cover = persisted.some(
                        preview => Math.abs(preview.ratio - 1.6) <= 0.15
                    );
                    const main = persisted.some(
                        preview => Math.abs(preview.ratio - 0.75) <= 0.12
                    );
                    return previews.length >= 2
                        && new Set(previews.map(preview => preview.src)).size >= 2
                        && new Set(
                            persisted.map(preview => preview.src)
                        ).size >= 2
                        && cover
                        && main;
                }""",
                arg={
                    "selector": _ASSET_PREVIEW_SELECTOR,
                    "baseline": sorted(baseline_sources or set()),
                },
                timeout=15000,
            )
            return True
        except PlaywrightTimeoutError:
            return False

    async def _fill_multistep_draft(
        self, page: Page, payload: CampaignPayload
    ) -> BrowserResult:
        media_paths = self._campaign_media_paths(payload)
        if media_paths is None:
            return BrowserResult(
                status=BrowserState.CONFIGURATION_REQUIRED.value,
                reason="approved campaign media assets are missing or not allowlisted",
            )
        if payload.end_date is None:
            return BrowserResult(
                status=BrowserState.CONFIGURATION_REQUIRED.value,
                reason="campaign end date is not configured",
            )
        cover_path, main_path = media_paths

        about_scope = await self._open_editor_step(page, "about")
        if about_scope is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="known about step is missing",
            )
        about = await self._multistep_about_controls(about_scope)
        if about is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="known about controls are missing or ambiguous",
            )
        await about["title"].fill(payload.title)
        await about["summary"].fill(payload.summary)
        await about["end_date"].fill(payload.end_date.strftime("%d.%m.%Y"))
        await about["end_date"].press("Tab")
        await about["story"].fill(payload.story)
        if not await about["save"].is_enabled():
            return BrowserResult(
                status=BrowserState.HUMAN_ACTION_REQUIRED.value,
                reason="Planeta requires another about field, such as the project region",
            )
        about_scope = await self._save_and_reload_step(
            page, "about", about_scope, about["save"]
        )
        if about_scope is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="about step could not be reloaded after save",
            )
        saved_about = await self._multistep_about_controls(about_scope)
        if saved_about is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="about controls changed after save",
            )
        saved_about_values = {
            "title": await self._control_value(saved_about["title"]),
            "summary": await self._control_value(saved_about["summary"]),
            "end_date": await self._control_value(saved_about["end_date"]),
            "story": await self._control_value(saved_about["story"]),
        }
        if saved_about_values != {
            "title": _normalize_editor_text(payload.title),
            "summary": _normalize_editor_text(payload.summary),
            "end_date": payload.end_date.strftime("%d.%m.%Y"),
            "story": _normalize_editor_text(payload.story),
        }:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="about values were not persisted after save",
                draft_snapshot=saved_about_values,
            )

        assets_scope = await self._open_editor_step(page, "assets")
        if assets_scope is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="known assets step is missing",
            )
        asset_inputs = await self._exact_asset_inputs(assets_scope)
        if asset_inputs is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="exactly two campaign file controls are required",
            )
        baseline_sources = (
            set()
            if self._fixture_loaded
            else await self._asset_preview_sources(page)
        )
        await asset_inputs[0].set_input_files(str(cover_path))
        cover_sources = baseline_sources
        if not self._fixture_loaded:
            observed_cover_sources = await self._wait_for_new_asset_preview(
                page, baseline_sources
            )
            if observed_cover_sources is None:
                return BrowserResult(
                    status=BrowserState.UI_CHANGED.value,
                    reason="cover uploader did not produce a distinct factual image preview",
                )
            cover_sources = observed_cover_sources
        assets_scope = await self._open_editor_step(page, "assets")
        if assets_scope is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="assets step changed after cover selection",
            )
        asset_inputs = await self._exact_asset_inputs(assets_scope)
        if asset_inputs is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="asset controls changed after cover selection",
            )
        await asset_inputs[1].set_input_files(str(main_path))
        if not self._fixture_loaded:
            main_sources = await self._wait_for_new_asset_preview(
                page, cover_sources
            )
            if main_sources is None:
                return BrowserResult(
                    status=BrowserState.UI_CHANGED.value,
                    reason="main uploader did not produce a second distinct factual image preview",
                )
        asset_save = await self._safe_step_save(assets_scope)
        if asset_save is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="safe assets save control is missing or ambiguous",
            )
        if not await asset_save.is_enabled():
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="assets save remains disabled after both factual images were selected",
            )
        assets_scope = await self._save_and_reload_step(
            page, "assets", assets_scope, asset_save
        )
        if assets_scope is None or not await self._assets_are_persisted(
            page,
            assets_scope,
            cover_path.name,
            main_path.name,
            baseline_sources,
        ):
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="two persisted campaign image previews could not be verified",
            )

        goal_scope = await self._open_editor_step(page, "goal")
        if goal_scope is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="known goal step is missing",
            )
        goal = await self._unique_visible(goal_scope.locator(selectors.GOAL_INPUT))
        goal_save = await self._safe_step_save(goal_scope)
        if goal is None or goal_save is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="known goal controls are missing or ambiguous",
            )
        await goal.fill(str(payload.target_amount))
        await goal.press("Tab")
        if not await goal_save.is_enabled():
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="goal save remains disabled after the target was filled",
            )
        goal_scope = await self._save_and_reload_step(
            page, "goal", goal_scope, goal_save
        )
        if goal_scope is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="goal step could not be reloaded after save",
            )
        goal = await self._unique_visible(goal_scope.locator(selectors.GOAL_INPUT))
        if goal is None:
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="goal control changed after save",
            )
        target_amount = self._normalized_amount(await self._control_value(goal))
        if target_amount != str(payload.target_amount):
            return BrowserResult(
                status=BrowserState.UI_CHANGED.value,
                reason="server target was not persisted after save",
                draft_snapshot={"target_amount": target_amount},
            )

        snapshot = await self._read_multistep_about(page)
        snapshot["target_amount"] = target_amount
        snapshot["cover_image"] = cover_path.name
        snapshot["main_image"] = main_path.name
        return BrowserResult(
            status=BrowserState.OK.value,
            reason="about, factual images, and server target filled and safely saved",
            draft_snapshot=snapshot,
        )

    async def read_draft(self) -> BrowserResult:
        inspected = await self.inspect()
        if inspected.status != "ok":
            return inspected
        assert self._page is not None
        try:
            if await self._is_multistep_editor(self._page):
                return BrowserResult(
                    status="ok",
                    reason="multi-step draft read",
                    draft_snapshot=await self._read_multistep_snapshot(self._page),
                )
            return BrowserResult(status="ok", reason="draft read", draft_snapshot=await self._read_snapshot(self._page))
        except LookupError:
            return BrowserResult(status="ui_changed", reason="known draft selectors are missing or ambiguous")
        except PlaywrightTimeoutError:
            return BrowserResult(status="network_error", reason="timeout while reading draft")
        except PlaywrightError as exc:
            return BrowserResult(status="planeta_error", reason=f"browser error: {type(exc).__name__}")

    async def fill_draft(self, payload: CampaignPayload) -> BrowserResult:
        inspected = await self.inspect()
        if inspected.status != "ok":
            return inspected
        assert self._page is not None
        page = self._page
        try:
            if await self._is_multistep_editor(page):
                return await self._fill_multistep_draft(page, payload)
            controls = await self._resolve_required_controls(page)
            if controls is None:
                return BrowserResult(status="ui_changed", reason="known draft selectors are missing or ambiguous")
            await controls["title"].fill(payload.title)
            await controls["target"].fill(str(payload.target_amount))
            await controls["summary"].fill(payload.summary)
            await controls["story"].fill(payload.story)
            pre_save = await self.inspect()
            if pre_save.status != "ok":
                return pre_save
            await controls["save"].click()
            return BrowserResult(
                status="ok",
                reason="draft fields filled and safe save control clicked",
                draft_snapshot=await self._read_snapshot(page),
            )
        except PlaywrightTimeoutError:
            return BrowserResult(status="network_error", reason="timeout while filling draft")
        except PlaywrightError as exc:
            return BrowserResult(status="planeta_error", reason=f"browser error: {type(exc).__name__}")

    async def _open_rewards_editor(self, page: Page) -> Locator | None:
        if await self._is_multistep_editor(page):
            scope = await self._open_editor_step(page, "rewards")
            return await self._reward_add_button(scope) if scope is not None else None
        add_button = page.get_by_role("button", name=_ADD_REWARD)
        count = await add_button.count()
        if count == 1:
            return add_button
        if count > 1:
            return None
        navigation_candidates: list[Locator] = []
        for role in ("link", "button"):
            candidate = page.get_by_role(role, name=_REWARDS_NAV)
            count = await candidate.count()
            if count == 1:
                navigation_candidates.append(candidate)
            elif count > 1:
                return None
        if len(navigation_candidates) != 1:
            return None
        await navigation_candidates[0].click()
        add_button = page.get_by_role("button", name=_ADD_REWARD)
        return add_button if await add_button.count() == 1 else None

    async def fill_rewards(self, payload: CampaignPayload) -> BrowserResult:
        page = await self._ensure_page()
        try:
            if await self._open_rewards_editor(page) is None:
                return BrowserResult(status="ui_changed", reason="rewards navigation or add control is missing or ambiguous")
            snapshot: list[dict[str, Any]] = []
            for reward in payload.rewards:
                existing = await self._unique_visible(
                    page.get_by_text(reward.title, exact=True)
                )
                existing_count = 0
                for index in range(await page.get_by_text(reward.title, exact=True).count()):
                    if await page.get_by_text(reward.title, exact=True).nth(index).is_visible():
                        existing_count += 1
                if existing_count > 1:
                    return BrowserResult(status="ui_changed", reason="reward title is duplicated or ambiguous")
                if existing is None:
                    add_button = await self._open_rewards_editor(page)
                    if add_button is None:
                        return BrowserResult(status="ui_changed", reason="reward add control changed or became ambiguous")
                    await add_button.click()
                    title = await self._unique_visible(page.get_by_label(_REWARD_TITLE))
                    amount = await self._unique_visible(page.get_by_label(_REWARD_AMOUNT))
                    description = await self._unique_visible(
                        page.get_by_label(_REWARD_DESCRIPTION)
                    )
                    save = await self._unique_visible(
                        page.get_by_role("button", name=_SAVE_REWARD)
                    )
                    if title is None or amount is None or description is None or save is None:
                        return BrowserResult(status="ui_changed", reason="reward editor controls are missing or ambiguous")
                    await title.fill(reward.title)
                    await amount.fill(str(reward.amount))
                    await description.fill(reward.description)
                    physical = await self._unique_visible(
                        page.get_by_role("checkbox", name=_REWARD_PHYSICAL)
                    )
                    physical_matches = page.get_by_role("checkbox", name=_REWARD_PHYSICAL)
                    visible_physical = 0
                    for index in range(await physical_matches.count()):
                        if await physical_matches.nth(index).is_visible():
                            visible_physical += 1
                    if visible_physical > 1:
                        return BrowserResult(status="ui_changed", reason="physical reward control is ambiguous")
                    if physical is not None and await physical.is_checked():
                        await physical.uncheck()
                    await save.click()
                    saved_title = await self._unique_visible(
                        page.get_by_text(reward.title, exact=True)
                    )
                    if saved_title is None:
                        return BrowserResult(status="ui_changed", reason="saved reward could not be verified")
                snapshot.append(
                    {
                        "title": reward.title,
                        "amount": str(reward.amount),
                        "description": reward.description,
                        "physical": False,
                    }
                )
            self._last_rewards_snapshot = [dict(item) for item in snapshot]
            if await self._is_multistep_editor(page):
                if await self._open_editor_step(page, "about") is None:
                    return BrowserResult(status="ui_changed", reason="could not return to the safe about step")
            elif self.draft_url and not self._fixture_loaded:
                returned = await self.navigate_to_draft()
                if returned.status != "ok":
                    return returned
            return BrowserResult(
                status="ok",
                reason="digital rewards created or already present",
                draft_snapshot={"rewards": snapshot},
            )
        except PlaywrightTimeoutError:
            return BrowserResult(status="network_error", reason="timeout while filling rewards")
        except PlaywrightError as exc:
            return BrowserResult(status="planeta_error", reason=f"browser error: {type(exc).__name__}")

    async def read_rewards(self) -> BrowserResult:
        if not self._last_rewards_snapshot:
            return BrowserResult(status="ui_changed", reason="no rewards snapshot is available for strict verification")
        page = await self._ensure_page()
        try:
            if await self._open_rewards_editor(page) is None:
                return BrowserResult(status="ui_changed", reason="rewards editor could not be verified")
            for expected in self._last_rewards_snapshot:
                title = page.get_by_text(str(expected["title"]), exact=True)
                if await title.count() != 1:
                    return BrowserResult(status="ui_changed", reason="saved reward title is missing or ambiguous")
                verified = await title.evaluate(
                    r"""(node, expected) => {
                        const norm = (value) => String(value ?? '')
                            .replace(/\u00a0/g, ' ')
                            .replace(/\s+/g, ' ')
                            .trim();
                        const amount = String(expected.amount);
                        const grouped = Number(amount).toLocaleString('ru-RU').replace(/\u00a0/g, ' ');
                        let current = node;
                        for (let depth = 0; current && depth < 7; depth += 1, current = current.parentElement) {
                            const text = norm(current.innerText || current.textContent || '');
                            const dataAmount = current.dataset ? current.dataset.amount : '';
                            const dataDescription = current.dataset ? current.dataset.description : '';
                            const dataPhysical = current.dataset ? current.dataset.physical : '';
                            const amountOk = dataAmount
                                ? String(dataAmount) === amount
                                : text.includes(amount) || text.includes(grouped);
                            const descriptionOk = dataDescription
                                ? norm(dataDescription) === norm(expected.description)
                                : text.includes(norm(expected.description));
                            const checkbox = current.querySelector ? current.querySelector('input[type="checkbox"]') : null;
                            const physicalOk = expected.physical
                                ? dataPhysical === 'true' || Boolean(checkbox && checkbox.checked)
                                : dataPhysical
                                    ? dataPhysical === 'false'
                                    : !(checkbox && checkbox.checked);
                            if (amountOk && descriptionOk && physicalOk) return true;
                        }
                        return false;
                    }""",
                    expected,
                )
                if not verified:
                    return BrowserResult(
                        status="ui_changed",
                        reason="saved reward amount, description, or digital type could not be verified",
                    )
            snapshot = [dict(item) for item in self._last_rewards_snapshot]
            if await self._is_multistep_editor(page):
                if await self._open_editor_step(page, "about") is None:
                    return BrowserResult(status="ui_changed", reason="could not return to the safe about step")
            elif self.draft_url and not self._fixture_loaded:
                returned = await self.navigate_to_draft()
                if returned.status != "ok":
                    return returned
            return BrowserResult(status="ok", reason="digital rewards verified", draft_snapshot={"rewards": snapshot})
        except PlaywrightTimeoutError:
            return BrowserResult(status="network_error", reason="timeout while reading rewards")
        except PlaywrightError as exc:
            return BrowserResult(status="planeta_error", reason=f"browser error: {type(exc).__name__}")

    async def _resolve_review_navigation(self, page: Page) -> Locator | None:
        candidates: list[Locator] = []
        for role in ("link", "button"):
            candidate = page.get_by_role(role, name=_REVIEW_NAV)
            count = await candidate.count()
            if count == 1:
                candidates.append(candidate)
            elif count > 1:
                return None
        return candidates[0] if len(candidates) == 1 else None

    async def submit_for_moderation(self) -> BrowserResult:
        inspected = await self.inspect()
        if inspected.status != "ok":
            return inspected
        assert self._page is not None
        page = self._page
        try:
            snapshot = await self._read_snapshot(page)
            submit = await self._resolve_control(page, "submit")
            if submit is None:
                review_navigation = await self._resolve_review_navigation(page)
                if review_navigation is None:
                    return BrowserResult(
                        status="ui_changed",
                        reason="moderation control and exact review navigation are missing or ambiguous",
                        draft_snapshot=snapshot,
                    )
                await review_navigation.click()
                submit = await self._resolve_control(page, "submit")
            if submit is None:
                return BrowserResult(
                    status="ui_changed",
                    reason="exact moderation-submit control is missing or ambiguous after review navigation",
                    draft_snapshot=snapshot,
                )
            await submit.click()
            return BrowserResult(
                status="ok",
                reason="exact moderation-submit control clicked",
                draft_snapshot=snapshot,
            )
        except LookupError:
            return BrowserResult(status="ui_changed", reason="known draft selectors are missing or ambiguous")
        except PlaywrightTimeoutError:
            return BrowserResult(status="network_error", reason="timeout during moderation submit")
        except PlaywrightError as exc:
            return BrowserResult(status="planeta_error", reason=f"browser error: {type(exc).__name__}")

    async def submit_click_count(self) -> int:
        page = await self._ensure_page()
        return int(await page.evaluate("() => window.submitClicks || 0"))

    async def close(self) -> None:
        if not self._attached_over_cdp:
            if self._context is not None:
                await self._context.close()
            if self._browser is not None:
                await self._browser.close()
        if self._playwright is not None:
            await self._playwright.stop()
        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None
        self._fixture_loaded = False
        self._attached_over_cdp = False
        self._last_rewards_snapshot = []
