from __future__ import annotations

import asyncio
import json
import os
from urllib.parse import urlsplit

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from .browser import BrowserState, PlanetaBrowser
from .config import PlanetaConfig
from .defaults import default_argos_reboot_campaign
from .server import build_default_service
from .session_store import SessionStore


def _origin(url: str) -> tuple[str, str, int | None]:
    parsed = urlsplit(url)
    return parsed.scheme.casefold(), (parsed.hostname or "").casefold(), parsed.port


async def _safe_form_schema(page) -> list[dict[str, str]]:
    return await page.evaluate(
        """() => Array.from(document.querySelectorAll('input,textarea,select,button,[contenteditable="true"]'))
          .filter(el => {
            const s = getComputedStyle(el);
            return s.display !== 'none' && s.visibility !== 'hidden';
          })
          .slice(0, 120)
          .map(el => ({
            tag: (el.tagName || '').toLowerCase(),
            type: el.getAttribute('type') || '',
            name: el.getAttribute('name') || '',
            id: el.id || '',
            placeholder: el.getAttribute('placeholder') || '',
            aria_label: el.getAttribute('aria-label') || '',
            data_testid: el.getAttribute('data-testid') || '',
            role: el.getAttribute('role') || '',
            text: (el.tagName === 'BUTTON' ? (el.innerText || '').trim().slice(0, 120) : '')
          }))"""
    )


async def run() -> int:
    bootstrap_url = os.getenv("PLANETA_BOOTSTRAP_URL", "").strip()
    if not bootstrap_url:
        print("PLANETA_BOOTSTRAP status=skipped reason=no_bootstrap_url", flush=True)
        return 0

    config = PlanetaConfig.from_env()
    if not config.draft_url:
        print("PLANETA_BOOTSTRAP status=configuration_required reason=no_draft_url", flush=True)
        return 0
    if _origin(bootstrap_url) != _origin(config.base_url):
        print("PLANETA_BOOTSTRAP status=configuration_required reason=bootstrap_origin_mismatch", flush=True)
        return 0

    session_key = os.getenv("PLANETA_SESSION_KEY", "").strip()
    if not session_key:
        print("PLANETA_BOOTSTRAP status=configuration_required reason=no_session_key", flush=True)
        return 0

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            try:
                await page.goto(bootstrap_url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(1200)
                await page.goto(config.draft_url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(1000)

                classifier = PlanetaBrowser(
                    base_url=config.base_url,
                    draft_url=config.draft_url,
                    headless=True,
                )
                state = await classifier.classify_page(page)
                schema = await _safe_form_schema(page)
                print(
                    "PLANETA_BOOTSTRAP_INSPECT "
                    + json.dumps({"state": state.value, "schema": schema}, ensure_ascii=False),
                    flush=True,
                )

                if state in {
                    BrowserState.AUTHENTICATION_REQUIRED,
                    BrowserState.CAPTCHA_REQUIRED,
                    BrowserState.NETWORK_ERROR,
                    BrowserState.PLANETA_ERROR,
                }:
                    print(f"PLANETA_BOOTSTRAP status={state.value}", flush=True)
                    return 0

                storage_state = await context.storage_state()
                store = SessionStore(config.state_path.parent / "session.enc", session_key)
                store.save_storage_state(storage_state)
                print(f"PLANETA_BOOTSTRAP status=session_saved page_state={state.value}", flush=True)
            finally:
                await browser.close()

        service = build_default_service()
        try:
            await service.prepare_campaign(default_argos_reboot_campaign())
            fill_result = await service.fill_draft()
            print(
                "PLANETA_BOOTSTRAP_FILL "
                + json.dumps(
                    {"status": fill_result.status, "reason": fill_result.reason},
                    ensure_ascii=False,
                ),
                flush=True,
            )
            if fill_result.status == "ok":
                sync_result = await service.sync_draft()
                print(
                    "PLANETA_BOOTSTRAP_SYNC "
                    + json.dumps(
                        {
                            "status": sync_result.get("status"),
                            "reason": sync_result.get("reason"),
                            "differences": list(sync_result.get("differences", {}).keys()),
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
        finally:
            close = getattr(service.browser, "close", None)
            if close is not None:
                await close()
        return 0
    except PlaywrightTimeoutError:
        print("PLANETA_BOOTSTRAP status=network_error reason=timeout", flush=True)
        return 0
    except PlaywrightError as exc:
        print(f"PLANETA_BOOTSTRAP status=planeta_error reason={type(exc).__name__}", flush=True)
        return 0
    except Exception as exc:
        print(f"PLANETA_BOOTSTRAP status=planeta_error reason={type(exc).__name__}", flush=True)
        return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run()))
