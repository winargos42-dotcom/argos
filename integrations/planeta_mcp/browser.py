from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
from playwright.async_api import (
    Browser,
    BrowserContext,
    Error as PlaywrightError,
    Page,
    Playwright,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)

from .models import CampaignPayload
from . import selectors


class BrowserState(StrEnum):
    OK = "ok"
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


class PlanetaBrowser:
    def __init__(
        self,
        base_url: str = "https://planeta.ru",
        headless: bool = True,
        fixture_dir: str | Path | None = None,
        executable_path: str | None = None,
        storage_state: dict[str, Any] | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.headless = headless
        self.fixture_dir = Path(fixture_dir) if fixture_dir else None
        self.executable_path = executable_path
        self.storage_state = storage_state
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def _ensure_page(self) -> Page:
        if self._page is not None:
            return self._page
        self._playwright = await async_playwright().start()
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

    async def open_fixture(self, filename: str) -> None:
        if self.fixture_dir is None:
            raise RuntimeError("fixture_dir is not configured")
        path = (self.fixture_dir / filename).resolve()
        if not path.is_file() or self.fixture_dir.resolve() not in path.parents:
            raise FileNotFoundError(filename)
        page = await self._ensure_page()
        await page.set_content(path.read_text(encoding="utf-8"), wait_until="domcontentloaded")

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
                "паспорт",
                "инн",
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

            for selector in selectors.REQUIRED_DRAFT_SELECTORS.values():
                if await page.locator(selector).count() != 1:
                    return BrowserState.UI_CHANGED
            return BrowserState.OK
        except PlaywrightTimeoutError:
            return BrowserState.NETWORK_ERROR
        except PlaywrightError:
            return BrowserState.PLANETA_ERROR

    async def inspect(self) -> BrowserResult:
        page = await self._ensure_page()
        state = await self.classify_page(page)
        reasons = {
            BrowserState.OK: "known draft editor detected",
            BrowserState.AUTHENTICATION_REQUIRED: "human Planeta.ru login is required",
            BrowserState.CAPTCHA_REQUIRED: "CAPTCHA/anti-bot step requires human action",
            BrowserState.HUMAN_ACTION_REQUIRED: "identity or verification step requires human action",
            BrowserState.UI_CHANGED: "known draft selectors are missing or ambiguous",
            BrowserState.VALIDATION_FAILED: "campaign validation failed",
            BrowserState.NETWORK_ERROR: "browser/network timeout",
            BrowserState.PLANETA_ERROR: "Planeta.ru or browser error",
        }
        return BrowserResult(status=state.value, reason=reasons[state])

    async def _read_snapshot(self, page: Page) -> dict[str, str]:
        return {
            "title": await page.locator(selectors.TITLE_INPUT).input_value(),
            "target_amount": await page.locator(selectors.TARGET_INPUT).input_value(),
            "summary": await page.locator(selectors.SUMMARY_INPUT).input_value(),
            "story": await page.locator(selectors.STORY_EDITOR).input_value(),
        }

    async def read_draft(self) -> BrowserResult:
        page = await self._ensure_page()
        inspected = await self.inspect()
        if inspected.status != BrowserState.OK.value:
            return inspected
        try:
            snapshot = await self._read_snapshot(page)
            return BrowserResult(status="ok", reason="draft read", draft_snapshot=snapshot)
        except PlaywrightTimeoutError:
            return BrowserResult(status="network_error", reason="timeout while reading draft")
        except PlaywrightError as exc:
            return BrowserResult(status="planeta_error", reason=f"browser error: {type(exc).__name__}")

    async def fill_draft(self, payload: CampaignPayload) -> BrowserResult:
        page = await self._ensure_page()
        inspected = await self.inspect()
        if inspected.status != BrowserState.OK.value:
            return inspected
        try:
            await page.locator(selectors.TITLE_INPUT).fill(payload.title)
            await page.locator(selectors.TARGET_INPUT).fill(str(payload.target_amount))
            await page.locator(selectors.SUMMARY_INPUT).fill(payload.summary)
            await page.locator(selectors.STORY_EDITOR).fill(payload.story)

            pre_save = await self.inspect()
            if pre_save.status != BrowserState.OK.value:
                return pre_save
            await page.locator(selectors.SAVE_DRAFT_BUTTON).click()
            return BrowserResult(
                status="ok",
                reason="draft fields filled and safe save control clicked",
                draft_snapshot=await self._read_snapshot(page),
            )
        except PlaywrightTimeoutError:
            return BrowserResult(status="network_error", reason="timeout while filling draft")
        except PlaywrightError as exc:
            return BrowserResult(status="planeta_error", reason=f"browser error: {type(exc).__name__}")

    async def submit_for_moderation(self) -> BrowserResult:
        page = await self._ensure_page()
        inspected = await self.inspect()
        if inspected.status != BrowserState.OK.value:
            return inspected
        try:
            snapshot = await self._read_snapshot(page)
            await page.locator(selectors.SUBMIT_MODERATION_BUTTON).click()
            return BrowserResult(
                status="ok",
                reason="exact moderation-submit control clicked",
                draft_snapshot=snapshot,
            )
        except PlaywrightTimeoutError:
            return BrowserResult(status="network_error", reason="timeout during moderation submit")
        except PlaywrightError as exc:
            return BrowserResult(status="planeta_error", reason=f"browser error: {type(exc).__name__}")

    async def submit_click_count(self) -> int:
        page = await self._ensure_page()
        return int(await page.evaluate("() => window.submitClicks || 0"))

    async def close(self) -> None:
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
