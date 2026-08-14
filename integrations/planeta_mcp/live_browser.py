from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from playwright.async_api import BrowserContext, Page, Playwright, async_playwright


class LiveBrowserRuntime:
    """Own the local-only graphical browser stack used for human Planeta.ru login.

    X11, VNC, websockify and CDP are deliberately bound to loopback. Public access
    is expected to be mediated by the token-gated FastAPI routes, never by Railway
    networking directly.
    """

    def __init__(
        self,
        data_dir: str | Path = "/data/planeta",
        *,
        draft_url: str | None = None,
        display: str = ":99",
        cdp_port: int = 9222,
        vnc_port: int = 5900,
        websockify_port: int = 6080,
    ):
        self.data_dir = Path(data_dir)
        self.profile_dir = self.data_dir / "browser-profile"
        self.draft_url = draft_url.strip() if draft_url else None
        self.display = display
        self.cdp_port = cdp_port
        self.vnc_host = "127.0.0.1"
        self.vnc_port = vnc_port
        self.websockify_port = websockify_port
        self.cdp_url = f"http://127.0.0.1:{self.cdp_port}"
        self.websockify_url = f"ws://127.0.0.1:{self.websockify_port}"

        self._processes: list[asyncio.subprocess.Process] = []
        self._playwright: Playwright | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    @property
    def page(self) -> Page | None:
        return self._page

    @property
    def started(self) -> bool:
        return self._context is not None

    def xvfb_command(self) -> list[str]:
        return [
            "Xvfb",
            self.display,
            "-screen",
            "0",
            "1365x768x24",
            "-nolisten",
            "tcp",
        ]

    def vnc_command(self) -> list[str]:
        return [
            "x11vnc",
            "-display",
            self.display,
            "-localhost",
            "-forever",
            "-shared",
            "-rfbport",
            str(self.vnc_port),
            "-nopw",
        ]

    def websockify_command(self) -> list[str]:
        return [
            "websockify",
            f"127.0.0.1:{self.websockify_port}",
            f"127.0.0.1:{self.vnc_port}",
        ]

    def chromium_args(self) -> list[str]:
        return [
            "--remote-debugging-address=127.0.0.1",
            f"--remote-debugging-port={self.cdp_port}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-dev-shm-usage",
        ]

    async def _spawn(self, command: list[str], *, env: dict[str, str] | None = None) -> None:
        process = await asyncio.create_subprocess_exec(
            *command,
            env=env,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        self._processes.append(process)

    async def start(self) -> Page:
        if self._context is not None:
            assert self._page is not None
            return self._page

        self.profile_dir.mkdir(parents=True, exist_ok=True)
        display_env = os.environ.copy()
        display_env["DISPLAY"] = self.display

        try:
            await self._spawn(self.xvfb_command(), env=display_env)
            await asyncio.sleep(0.25)
            await self._spawn(self.vnc_command(), env=display_env)
            await asyncio.sleep(0.15)
            await self._spawn(self.websockify_command(), env=display_env)

            self._playwright = await async_playwright().start()
            self._context = await self._playwright.chromium.launch_persistent_context(
                str(self.profile_dir),
                headless=False,
                env=display_env,
                args=self.chromium_args(),
                viewport={"width": 1365, "height": 768},
            )
            self._page = self._context.pages[0] if self._context.pages else await self._context.new_page()

            if self.draft_url:
                await self._page.goto(
                    self.draft_url,
                    wait_until="domcontentloaded",
                    timeout=30000,
                )
            return self._page
        except Exception:
            await self.stop()
            raise

    async def storage_state(self) -> dict[str, Any]:
        if self._context is None:
            raise RuntimeError("live browser is not started")
        return await self._context.storage_state()

    async def stop(self) -> None:
        context, self._context = self._context, None
        self._page = None
        if context is not None:
            try:
                await context.close()
            except Exception:
                pass

        playwright, self._playwright = self._playwright, None
        if playwright is not None:
            try:
                await playwright.stop()
            except Exception:
                pass

        processes, self._processes = self._processes, []
        for process in reversed(processes):
            if process.returncode is None:
                try:
                    process.terminate()
                except ProcessLookupError:
                    continue
        for process in reversed(processes):
            if process.returncode is not None:
                continue
            try:
                await asyncio.wait_for(process.wait(), timeout=2.0)
            except asyncio.TimeoutError:
                try:
                    process.kill()
                except ProcessLookupError:
                    continue
                await process.wait()
