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
_REWARD_TITLE = re.compile(r"^\s*название\s+вознаграждения\s*\*?\s*$", re.I)
_REWARD_AMOUNT = re.compile(r"^\s*(?:стоимость|сумма)\s+вознаграждения\s*\*?\s*$", re.I)
_REWARD_DESCRIPTION = re.compile(r"^\s*описание\s+вознаграждения\s*\*?\s*$", re.I)
_REWARD_PHYSICAL = re.compile(r"^\s*(?:физическое\s+вознаграждение|требуется\s+доставка)\s*$", re.I)
_SAVE_REWARD = re.compile(r"^\s*сохранить\s+вознаграждение\s*$", re.I)


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
            if "ошибка модерации" in body_text or "ошибка сервиса" in body_text:
                return BrowserState.PLANETA_ERROR
            if await self._resolve_required_controls(page) is None:
                return BrowserState.UI_CHANGED
            return BrowserState.OK
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

    async def read_draft(self) -> BrowserResult:
        inspected = await self.inspect()
        if inspected.status != "ok":
            return inspected
        assert self._page is not None
        try:
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
            add_button = await self._open_rewards_editor(page)
            if add_button is None:
                return BrowserResult(status="ui_changed", reason="rewards navigation or add control is missing or ambiguous")
            snapshot: list[dict[str, Any]] = []
            for reward in payload.rewards:
                existing = page.get_by_text(reward.title, exact=True)
                count = await existing.count()
                if count > 1:
                    return BrowserResult(status="ui_changed", reason="reward title is duplicated or ambiguous")
                if count == 0:
                    await add_button.click()
                    title = page.get_by_label(_REWARD_TITLE)
                    amount = page.get_by_label(_REWARD_AMOUNT)
                    description = page.get_by_label(_REWARD_DESCRIPTION)
                    save = page.get_by_role("button", name=_SAVE_REWARD)
                    if any(await locator.count() != 1 for locator in (title, amount, description, save)):
                        return BrowserResult(status="ui_changed", reason="reward editor controls are missing or ambiguous")
                    await title.fill(reward.title)
                    await amount.fill(str(reward.amount))
                    await description.fill(reward.description)
                    physical = page.get_by_role("checkbox", name=_REWARD_PHYSICAL)
                    physical_count = await physical.count()
                    if physical_count > 1:
                        return BrowserResult(status="ui_changed", reason="physical reward control is ambiguous")
                    if physical_count == 1 and await physical.is_checked():
                        await physical.uncheck()
                    await save.click()
                    if await page.get_by_text(reward.title, exact=True).count() != 1:
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
            if self.draft_url and not self._fixture_loaded:
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
                            const amountOk = dataAmount
                                ? String(dataAmount) === amount
                                : text.includes(amount) || text.includes(grouped);
                            const descriptionOk = dataDescription
                                ? norm(dataDescription) === norm(expected.description)
                                : text.includes(norm(expected.description));
                            const checkbox = current.querySelector ? current.querySelector('input[type="checkbox"]') : null;
                            const physicalOk = expected.physical ? true : !(checkbox && checkbox.checked);
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
            if self.draft_url and not self._fixture_loaded:
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
