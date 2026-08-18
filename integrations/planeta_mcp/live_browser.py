from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from playwright.async_api import BrowserContext, Page, Playwright, async_playwright


def _serialized_origin(url: str) -> str:
    parsed = urlsplit(url)
    scheme = parsed.scheme.casefold()
    host = (parsed.hostname or "").casefold()
    port = parsed.port
    if not scheme or not host:
        return ""
    if (
        port is None
        or (scheme == "https" and port == 443)
        or (scheme == "http" and port == 80)
    ):
        return f"{scheme}://{host}"
    return f"{scheme}://{host}:{port}"


class LiveBrowserRuntime:
    """Own the local-only graphical browser stack used for human Planeta.ru login.

    X11, VNC and CDP are deliberately bound to loopback. Public access is
    mediated by the token-gated FastAPI WebSocket route, which relays directly
    to the loopback x11vnc TCP socket.
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
        self.websockify_port = websockify_port  # retained for backwards-compatible construction
        self.cdp_url = f"http://127.0.0.1:{self.cdp_port}"
        self.websockify_url = f"tcp://{self.vnc_host}:{self.vnc_port}"

        self._processes: list[asyncio.subprocess.Process] = []
        self._playwright: Playwright | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._storage_state: dict[str, Any] | None = None

    @property
    def page(self) -> Page | None:
        return self._page

    @property
    def started(self) -> bool:
        return self._context is not None

    def set_storage_state(self, storage_state: dict[str, Any] | None) -> None:
        self._storage_state = storage_state

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

    async def _rehydrate_context(self) -> None:
        state = self._storage_state
        if state is None or self._context is None:
            return

        cookies = state.get("cookies", [])
        if cookies:
            await self._context.add_cookies(cookies)

        if not self.draft_url:
            return
        draft_origin = _serialized_origin(self.draft_url)
        if not draft_origin:
            return
        matching = next(
            (
                item
                for item in state.get("origins", [])
                if _serialized_origin(str(item.get("origin", ""))) == draft_origin
            ),
            None,
        )
        if not matching or not matching.get("localStorage"):
            return

        payload = json.dumps(
            {"origin": draft_origin, "items": matching["localStorage"]},
            ensure_ascii=True,
            separators=(",", ":"),
        )
        await self._context.add_init_script(
            script=(
                f"(() => {{ const payload={payload};"
                "if(window.location.origin===payload.origin){"
                "for(const item of payload.items){"
                "localStorage.setItem(item.name,item.value);}}})();"
            )
        )

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

            self._playwright = await async_playwright().start()
            self._context = await self._playwright.chromium.launch_persistent_context(
                str(self.profile_dir),
                headless=False,
                env=display_env,
                args=self.chromium_args(),
                viewport={"width": 1365, "height": 768},
            )
            self._page = self._context.pages[0] if self._context.pages else await self._context.new_page()
            await self._rehydrate_context()

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
