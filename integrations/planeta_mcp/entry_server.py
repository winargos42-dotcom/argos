from __future__ import annotations

import asyncio
import hmac
import json
import os
from typing import Any, Awaitable, Callable
from urllib.parse import urlsplit

from starlette.responses import HTMLResponse, JSONResponse

from .server import app as core_app


ASGIApp = Callable[[dict[str, Any], Callable[[], Awaitable[dict[str, Any]]], Callable[[dict[str, Any]], Awaitable[None]]], Awaitable[None]]


def _authorization(scope: dict[str, Any]) -> str:
    for name, value in scope.get("headers", []):
        if name.lower() == b"authorization":
            return value.decode("latin-1")
    return ""


def _mobile_launcher() -> str:
    return """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,viewport-fit=cover">
<title>ARGOS — Planeta mobile login</title>
<style>
html,body{margin:0;min-height:100%;background:#111;color:#fff;font:16px system-ui,sans-serif}
main{max-width:620px;margin:0 auto;padding:32px 20px}.card{border:1px solid #444;border-radius:18px;padding:22px;background:#181818}
h1{font-size:1.3rem;margin:0 0 12px}.muted{color:#aaa}.error{color:#ffb4b4}button{font-size:1rem;padding:12px 16px}
</style>
</head>
<body><main><div class="card"><h1>ARGOS — вход Planeta.ru</h1><p id="status">Открываю защищённый браузер…</p><p class="muted">После подключения используй кнопку клавиатуры в панели noVNC. Экран можно прокручивать и масштабировать пальцами.</p></div></main>
<script>
(async()=>{
  const status=document.getElementById('status');
  const token=location.hash.slice(1);
  if(!token){status.className='error';status.textContent='Нет токена сессии. Запроси новую ссылку.';return;}
  history.replaceState(null,'',location.pathname);
  try{
    const r=await fetch('/live-login/exchange',{
      method:'POST',
      headers:{Authorization:`Bearer ${token}`},
      credentials:'same-origin',
      cache:'no-store'
    });
    if(!r.ok){
      status.className='error';
      status.textContent=r.status===401?'Сессия истекла. Запроси новую ссылку.':'Не удалось открыть сессию: HTTP '+r.status;
      return;
    }
    status.textContent='Подключено. Открываю мобильный экран…';
    location.replace('/live-login/assets/vnc.html?autoconnect=true&resize=scale&view_clip=true&reconnect=true');
  }catch(e){status.className='error';status.textContent='Ошибка сети при открытии защищённой сессии.';}
})();
</script></body></html>"""


class LiveEntryBootstrap:
    """One-time fragment capability bootstrap for the existing live-login API.

    The public browser sends the high-entropy entry capability only in the
    Authorization header to /live-login/exchange. This wrapper converts that
    capability into the core app's normal generated live session without ever
    placing the entry capability in a URL path/query or log message.
    """

    def __init__(self, app: ASGIApp, *, entry_token: str, control_secret: str):
        self.app = app
        self._entry_token = entry_token
        self._control_secret = control_secret
        self._entry_used = False
        self._lock = asyncio.Lock()

    async def __call__(self, scope, receive, send):
        # One-link mobile launcher: exchange the fragment token in JS and then
        # redirect into noVNC's full touch-friendly UI in the same browser.
        if (
            scope.get("type") == "http"
            and scope.get("method") == "GET"
            and scope.get("path") == "/live-login/mobile"
        ):
            await HTMLResponse(
                _mobile_launcher(),
                headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"},
            )(scope, receive, send)
            return

        # noVNC's full mobile UI resolves its default websocket endpoint
        # relative to /live-login/assets/vnc.html. Rewrite that websocket path
        # to the protected live-login relay before Starlette's StaticFiles mount
        # can see it (StaticFiles is HTTP-only and would otherwise raise 500).
        if (
            scope.get("type") == "websocket"
            and scope.get("path") == "/live-login/assets/websockify"
        ):
            rewritten = dict(scope)
            rewritten["path"] = "/live-login/websockify"
            rewritten["raw_path"] = b"/live-login/websockify"
            await self.app(rewritten, receive, send)
            return

        if (
            scope.get("type") != "http"
            or scope.get("method") != "POST"
            or scope.get("path") != "/live-login/exchange"
        ):
            await self.app(scope, receive, send)
            return

        supplied = _authorization(scope)
        expected = f"Bearer {self._entry_token}"
        if not hmac.compare_digest(supplied, expected):
            await self.app(scope, receive, send)
            return

        async with self._lock:
            if self._entry_used:
                await JSONResponse(
                    {"detail": "entry capability already used"},
                    status_code=409,
                    headers={"Cache-Control": "no-store"},
                )(scope, receive, send)
                return

            start = await self._invoke_core(
                scope,
                method="POST",
                path="/live-login/start",
                authorization=f"Bearer {self._control_secret}",
            )
            if start["status"] != 200:
                await JSONResponse(
                    {"detail": "live login could not be started"},
                    status_code=503,
                    headers={"Cache-Control": "no-store"},
                )(scope, receive, send)
                return

            try:
                payload = json.loads(start["body"].decode("utf-8"))
                session_token = urlsplit(str(payload["browser_url"])).fragment
            except (KeyError, ValueError, UnicodeDecodeError, json.JSONDecodeError):
                session_token = ""

            if not session_token:
                await JSONResponse(
                    {"detail": "live login returned an invalid session"},
                    status_code=503,
                    headers={"Cache-Control": "no-store"},
                )(scope, receive, send)
                return

            # Burn the public entry capability as soon as the core live session
            # exists. A later internal exchange failure must not permit a second
            # Chromium session to be started with the same capability.
            self._entry_used = True

            exchanged = await self._invoke_core(
                scope,
                method="POST",
                path="/live-login/exchange",
                authorization=f"Bearer {session_token}",
            )
            if exchanged["status"] != 204:
                await JSONResponse(
                    {"detail": "live login session exchange failed"},
                    status_code=503,
                    headers={"Cache-Control": "no-store"},
                )(scope, receive, send)
                return

            await self._replay(exchanged, send)

    async def _invoke_core(
        self,
        original_scope: dict[str, Any],
        *,
        method: str,
        path: str,
        authorization: str,
    ) -> dict[str, Any]:
        scope = dict(original_scope)
        scope["method"] = method
        scope["path"] = path
        scope["raw_path"] = path.encode("ascii")
        scope["query_string"] = b""
        scope["headers"] = [
            (name, value)
            for name, value in original_scope.get("headers", [])
            if name.lower() not in {b"authorization", b"content-length", b"content-type"}
        ] + [(b"authorization", authorization.encode("latin-1"))]

        sent: list[dict[str, Any]] = []
        request_consumed = False

        async def synthetic_receive() -> dict[str, Any]:
            nonlocal request_consumed
            if not request_consumed:
                request_consumed = True
                return {"type": "http.request", "body": b"", "more_body": False}
            await asyncio.sleep(0)
            return {"type": "http.disconnect"}

        async def capture(message: dict[str, Any]) -> None:
            sent.append(message)

        await self.app(scope, synthetic_receive, capture)

        start = next((m for m in sent if m.get("type") == "http.response.start"), None)
        if start is None:
            return {"status": 500, "headers": [], "body": b""}
        body = b"".join(
            m.get("body", b"") for m in sent if m.get("type") == "http.response.body"
        )
        return {
            "status": int(start.get("status", 500)),
            "headers": list(start.get("headers", [])),
            "body": body,
        }

    @staticmethod
    async def _replay(response: dict[str, Any], send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": response["status"],
                "headers": response["headers"],
            }
        )
        await send({"type": "http.response.body", "body": response["body"], "more_body": False})


def create_entry_app(
    app: ASGIApp,
    *,
    entry_token: str | None,
    control_secret: str | None,
) -> ASGIApp:
    entry_token = (entry_token or "").strip()
    control_secret = (control_secret or "").strip()
    if not entry_token or not control_secret:
        return app
    return LiveEntryBootstrap(
        app,
        entry_token=entry_token,
        control_secret=control_secret,
    )


app = create_entry_app(
    core_app,
    entry_token=os.getenv("PLANETA_LIVE_ENTRY_TOKEN"),
    control_secret=os.getenv("PLANETA_LIVE_CONTROL_SECRET"),
)
