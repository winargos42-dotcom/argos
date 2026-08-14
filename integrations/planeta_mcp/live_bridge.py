from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any
from urllib.parse import urlsplit

from .browser import PlanetaBrowser
from .config import PlanetaConfig
from .defaults import default_argos_reboot_campaign
from .live_browser import LiveBrowserRuntime
from .live_login import LiveLoginController, LiveLoginSession, LiveLoginState
from .service import PlanetaCampaignService
from .session_store import SessionStore


def _origin(url: str) -> tuple[str, str, int | None]:
    parsed = urlsplit(url)
    return parsed.scheme.casefold(), (parsed.hostname or "").casefold(), parsed.port


class LiveLoginCoordinator:
    """Bridge a human-visible Chromium session to the existing Planeta MCP service."""

    def __init__(
        self,
        *,
        service: PlanetaCampaignService,
        config: PlanetaConfig,
        session_store: SessionStore,
        controller: LiveLoginController | None = None,
        runtime_factory: Callable[[], Any] | None = None,
        browser_factory: Callable[[Any], Any] | None = None,
        poll_interval: float = 1.0,
        durability: str = "ephemeral",
    ):
        if not config.draft_url:
            raise ValueError("PLANETA_DRAFT_URL is required for live login")
        if _origin(config.draft_url) != _origin(config.base_url):
            raise ValueError("draft_url must use the same origin as base_url")
        if poll_interval <= 0:
            raise ValueError("poll_interval must be positive")

        self.service = service
        self.config = config
        self.session_store = session_store
        self.controller = controller or LiveLoginController()
        self.poll_interval = poll_interval
        self.durability = durability

        self._runtime_factory = runtime_factory or (
            lambda: LiveBrowserRuntime(
                data_dir=config.state_path.parent,
                draft_url=config.draft_url,
            )
        )
        self._browser_factory = browser_factory or (
            lambda runtime: PlanetaBrowser(
                base_url=config.base_url,
                draft_url=config.draft_url,
                headless=False,
                cdp_url=runtime.cdp_url,
            )
        )
        self._runtime: Any | None = None
        self._active_token: str | None = None
        self._tasks: dict[str, asyncio.Task[None]] = {}
        self._results: dict[str, dict[str, Any]] = {}

    async def start(self) -> LiveLoginSession:
        if self._active_token:
            active = self.controller.get(self._active_token)
            task = self._tasks.get(self._active_token)
            if active is not None and task is not None and not task.done():
                raise RuntimeError("a live login session is already active")

        session = self.controller.start()
        runtime = self._runtime_factory()
        await runtime.start()
        shared_browser = self._browser_factory(runtime)

        old_browser = self.service.browser
        close = getattr(old_browser, "close", None)
        if close is not None:
            await close()
        self.service.browser = shared_browser

        self._runtime = runtime
        self._active_token = session.token
        self._results[session.token] = {
            "reason": "waiting_for_human",
            "fill_status": None,
            "sync_status": None,
            "differences": [],
        }
        self._tasks[session.token] = asyncio.create_task(
            self._watch(session.token, runtime, shared_browser)
        )
        return session

    def exchange(self, token: str) -> LiveLoginSession:
        return self.controller.exchange(token)

    def status(self, token: str) -> dict[str, Any] | None:
        session = self.controller.get(token)
        if session is None:
            return None
        result = self._results.get(token, {})
        return {
            "state": session.state.value,
            "expires_at": session.expires_at,
            "durability": self.durability,
            "reason": result.get("reason", ""),
            "fill_status": result.get("fill_status"),
            "sync_status": result.get("sync_status"),
            "differences": list(result.get("differences", [])),
        }

    def websockify_url(self, token: str) -> str | None:
        session = self.controller.get(token)
        if (
            session is None
            or not session.exchanged
            or not session.view_active
            or token != self._active_token
            or self._runtime is None
        ):
            return None
        return str(self._runtime.websockify_url)

    async def wait(self, token: str, timeout: float | None = None) -> None:
        task = self._tasks.get(token)
        if task is None:
            raise KeyError("live login task not found")
        if timeout is None:
            await task
        else:
            await asyncio.wait_for(asyncio.shield(task), timeout=timeout)

    async def _restore_headless_browser(self) -> None:
        storage_state = self.session_store.load_storage_state()
        self.service.browser = PlanetaBrowser(
            base_url=self.config.base_url,
            draft_url=self.config.draft_url,
            headless=self.config.headless,
            storage_state=storage_state,
        )

    async def _finish_runtime(self, runtime: Any, shared_browser: Any) -> None:
        close = getattr(shared_browser, "close", None)
        if close is not None:
            try:
                await close()
            except Exception:
                pass
        try:
            await runtime.stop()
        finally:
            if runtime is self._runtime:
                self._runtime = None
                self._active_token = None
            await self._restore_headless_browser()

    async def _watch(self, token: str, runtime: Any, shared_browser: Any) -> None:
        terminal = False
        try:
            while self.controller.get(token) is not None:
                page = getattr(runtime, "page", None)
                page_url = str(getattr(page, "url", ""))
                if page_url and _origin(page_url) != _origin(self.config.base_url):
                    self.controller.set_state(token, LiveLoginState.HUMAN_ACTION_REQUIRED)
                    self._results[token]["reason"] = "unexpected_origin"
                    terminal = True
                    return

                inspected = await shared_browser.inspect()
                state = inspected.status
                self._results[token]["reason"] = inspected.reason

                if state == "ok":
                    self.session_store.save_storage_state(await runtime.storage_state())
                    await self.service.prepare_campaign(default_argos_reboot_campaign())

                    fill = await self.service.fill_draft()
                    self._results[token]["fill_status"] = fill.status
                    if fill.status != "ok":
                        self._set_from_browser_status(token, fill.status)
                        self._results[token]["reason"] = fill.reason
                        terminal = fill.status not in {
                            "authentication_required",
                            "captcha_required",
                            "human_action_required",
                            "ui_changed",
                        }
                        if terminal:
                            return
                        await asyncio.sleep(self.poll_interval)
                        continue

                    sync = await self.service.sync_draft()
                    self._results[token]["sync_status"] = sync.get("status")
                    differences = list(sync.get("differences", {}).keys())
                    self._results[token]["differences"] = differences
                    self._results[token]["reason"] = str(sync.get("reason", ""))
                    if sync.get("status") == "ok" and not differences:
                        self.controller.mark_ready(token)
                        terminal = True
                        return

                    self._set_from_browser_status(token, str(sync.get("status", "ui_changed")))
                    await asyncio.sleep(self.poll_interval)
                    continue

                self._set_from_browser_status(token, state)
                if state in {
                    "authentication_required",
                    "captcha_required",
                    "human_action_required",
                    "ui_changed",
                }:
                    await asyncio.sleep(self.poll_interval)
                    continue

                terminal = True
                return
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            if self.controller.get(token) is not None:
                self.controller.set_state(token, LiveLoginState.NETWORK_ERROR)
                self._results[token]["reason"] = type(exc).__name__
            terminal = True
        finally:
            session = self.controller.get(token)
            if session is None or terminal or session.state == LiveLoginState.DRAFT_READY:
                await self._finish_runtime(runtime, shared_browser)

    def _set_from_browser_status(self, token: str, status: str) -> None:
        mapping = {
            "authentication_required": LiveLoginState.AUTHENTICATION_REQUIRED,
            "captcha_required": LiveLoginState.CAPTCHA_REQUIRED,
            "human_action_required": LiveLoginState.HUMAN_ACTION_REQUIRED,
            "ui_changed": LiveLoginState.UI_CHANGED,
            "network_error": LiveLoginState.NETWORK_ERROR,
        }
        self.controller.set_state(token, mapping.get(status, LiveLoginState.NETWORK_ERROR))
