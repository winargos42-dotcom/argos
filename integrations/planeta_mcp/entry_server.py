from __future__ import annotations

import asyncio
import hmac
import html
import json
import os
from typing import Any, Awaitable, Callable
from urllib.parse import parse_qs, urlsplit

from starlette.responses import HTMLResponse, JSONResponse

from . import server as server_module
from .direct_vnc import direct_vnc_relay
from .security import ApprovalError
from .service import CampaignValidationError, PlanetaCampaignService


# Production-only transport override: keep the core MCP/FastAPI routes intact,
# but relay the noVNC WebSocket directly to loopback x11vnc TCP instead of
# chaining through a second local WebSocket/websockify process.
server_module._default_live_ws_relay = direct_vnc_relay
core_app = server_module.app


ASGIApp = Callable[
    [
        dict[str, Any],
        Callable[[], Awaitable[dict[str, Any]]],
        Callable[[dict[str, Any]], Awaitable[None]],
    ],
    Awaitable[None],
]


def _authorization(scope: dict[str, Any]) -> str:
    for name, value in scope.get("headers", []):
        if name.lower() == b"authorization":
            return value.decode("latin-1")
    return ""


def _safe_headers() -> dict[str, str]:
    return {
        "Cache-Control": "no-store, max-age=0",
        "Pragma": "no-cache",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "Content-Security-Policy": (
            "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; "
            "frame-ancestors 'none'; base-uri 'none'"
        ),
    }


def _final_approval_page(
    request_id: str,
    campaign_digest: str,
    expires_at: float,
    csrf_token: str,
) -> str:
    safe_request = html.escape(request_id, quote=True)
    safe_digest = html.escape(campaign_digest, quote=True)
    safe_csrf = html.escape(csrf_token, quote=True)
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ARGOS REBOOT — финальное подтверждение</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:720px;margin:40px auto;padding:0 18px;line-height:1.5}}
.card{{border:1px solid #8885;border-radius:16px;padding:22px}}
code{{word-break:break-all}}button{{font-size:1.05rem;padding:12px 18px;margin-top:16px}}
.warn{{font-weight:700}}
</style>
</head>
<body><div class="card">
<h1>ARGOS REBOOT</h1>
<p class="warn">Черновик заполнен и сверен. Отправить кампанию на модерацию Planeta.ru?</p>
<p>Это финальное одноразовое подтверждение для текущей версии кампании.</p>
<p>Digest: <code>{safe_digest}</code></p>
<p>Истекает: <code>{expires_at:.0f}</code></p>
<form method="post" action="/live-login/moderation/{safe_request}">
<input type="hidden" name="csrf_token" value="{safe_csrf}">
<button type="submit">Подтвердить и отправить на модерацию</button>
</form>
</div></body></html>"""


def _submission_page(*, success: bool, status: str = "") -> str:
    if success:
        heading = "Кампания отправлена на модерацию"
        detail = "ARGOS REBOOT передан Planeta.ru на модерацию."
    else:
        heading = "Отправка не завершена"
        safe_status = html.escape(status or "unknown", quote=True)
        detail = (
            "Planeta.ru не подтвердила завершение отправки. "
            f"Безопасный статус: <code>{safe_status}</code>. "
            "Для повторной попытки потребуется новое подтверждение."
        )
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ARGOS REBOOT</title>
<style>body{{font-family:system-ui,sans-serif;max-width:720px;margin:40px auto;padding:0 18px;line-height:1.5}}.card{{border:1px solid #8885;border-radius:16px;padding:22px}}code{{word-break:break-all}}</style>
</head><body><div class="card"><h1>{heading}</h1><p>{detail}</p></div></body></html>"""


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
  history.replaceState(null,'',location.pathname);
  const openVnc=()=>location.replace('/live-login/assets/vnc.html?autoconnect=true&resize=scale&view_clip=true&reconnect=true');

  try{
    const existing=await fetch('/live-login/status',{credentials:'same-origin',cache:'no-store'});
    if(existing.ok){
      const state=await existing.json();
      if(state.state==='draft_ready'){
        location.replace('/live-login/moderation');
        return;
      }
      status.textContent='Активная сессия найдена. Восстанавливаю экран…';
      openVnc();
      return;
    }
  }catch(_e){}

  if(!token){status.className='error';status.textContent='Нет активной сессии и нет нового токена. Запроси новую ссылку.';return;}

  try{
    const r=await fetch('/live-login/exchange',{
      method:'POST',
      headers:{Authorization:`Bearer ${token}`},
      credentials:'same-origin',
      cache:'no-store'
    });
    if(!r.ok){
      status.className='error';
      status.textContent=r.status===409?'Эта ссылка уже использована. Открой её в той же вкладке с сохранённой сессией или запроси новую.':(r.status===401?'Сессия истекла. Запроси новую ссылку.':'Не удалось открыть сессию: HTTP '+r.status);
      return;
    }
    status.textContent='Подключено. Открываю мобильный экран…';
    openVnc();
  }catch(e){status.className='error';status.textContent='Ошибка сети при открытии защищённой сессии.';}
})();
</script></body></html>"""


class LiveEntryBootstrap:
    """One-time mobile bootstrap plus guarded final moderation handoff."""

    def __init__(self, app: ASGIApp, *, entry_token: str, control_secret: str):
        self.app = app
        self._entry_token = entry_token
        self._control_secret = control_secret
        self._entry_used = False
        self._lock = asyncio.Lock()
        self._approval_services: dict[str, PlanetaCampaignService] = {}

    async def __call__(self, scope, receive, send):
        scope_type = scope.get("type")
        method = scope.get("method")
        path = scope.get("path", "")

        if scope_type == "http" and method == "GET" and path == "/live-login/mobile":
            await HTMLResponse(
                _mobile_launcher(),
                headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"},
            )(scope, receive, send)
            return

        if scope_type == "http" and method == "GET" and path == "/live-login/moderation":
            await self._show_live_moderation(scope, receive, send)
            return

        if (
            scope_type == "http"
            and method == "POST"
            and path.startswith("/live-login/moderation/")
        ):
            await self._submit_live_moderation(scope, receive, send)
            return

        if scope_type == "websocket" and path == "/live-login/assets/websockify":
            rewritten = dict(scope)
            rewritten["path"] = "/live-login/websockify"
            rewritten["raw_path"] = b"/live-login/websockify"
            await self.app(rewritten, receive, send)
            return

        if scope_type != "http" or method != "POST" or path != "/live-login/exchange":
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

            self._entry_used = True
            await self._replay(exchanged, send)

    async def _show_live_moderation(self, scope, receive, send) -> None:
        status_response = await self._invoke_core(
            scope,
            method="GET",
            path="/live-login/status",
        )
        if status_response["status"] == 401:
            await JSONResponse(
                {"detail": "live session authorization required"},
                status_code=401,
                headers={"Cache-Control": "no-store"},
            )(scope, receive, send)
            return
        if status_response["status"] != 200:
            await JSONResponse(
                {"detail": "live login session not found"},
                status_code=404,
                headers={"Cache-Control": "no-store"},
            )(scope, receive, send)
            return

        try:
            status = json.loads(status_response["body"].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            status = {}
        if status.get("state") != "draft_ready":
            await JSONResponse(
                {"detail": "draft is not ready"},
                status_code=409,
                headers={"Cache-Control": "no-store"},
            )(scope, receive, send)
            return

        try:
            service = server_module.build_default_service()
            approval_request = await service.request_submit_approval()
            challenge = service.get_submit_approval_challenge(approval_request.request_id)
        except (RuntimeError, CampaignValidationError, ApprovalError):
            await JSONResponse(
                {"detail": "final approval could not be prepared"},
                status_code=503,
                headers={"Cache-Control": "no-store"},
            )(scope, receive, send)
            return

        self._approval_services[approval_request.request_id] = service
        await HTMLResponse(
            _final_approval_page(
                challenge.request_id,
                challenge.campaign_digest,
                challenge.expires_at,
                challenge.csrf_token,
            ),
            headers=_safe_headers(),
        )(scope, receive, send)

    async def _submit_live_moderation(self, scope, receive, send) -> None:
        request_id = str(scope.get("path", "")).rsplit("/", 1)[-1]
        service = self._approval_services.get(request_id)
        if not request_id or service is None:
            await JSONResponse(
                {"detail": "approval request not found"},
                status_code=404,
                headers={"Cache-Control": "no-store"},
            )(scope, receive, send)
            return

        body = await self._read_body(receive)
        try:
            form = parse_qs(body.decode("utf-8"), keep_blank_values=True)
            csrf_token = form.get("csrf_token", [""])[0]
        except UnicodeDecodeError:
            csrf_token = ""
        if not csrf_token:
            await JSONResponse(
                {"detail": "missing confirmation token"},
                status_code=400,
                headers={"Cache-Control": "no-store"},
            )(scope, self._empty_receive, send)
            return

        try:
            service.confirm_submit_approval(request_id, csrf_token)
        except ApprovalError:
            await JSONResponse(
                {"detail": "invalid or expired confirmation"},
                status_code=400,
                headers={"Cache-Control": "no-store"},
            )(scope, self._empty_receive, send)
            return

        try:
            result = await service.submit_for_moderation(request_id)
        except (ApprovalError, CampaignValidationError):
            self._approval_services.pop(request_id, None)
            await HTMLResponse(
                _submission_page(success=False, status="approval_error"),
                status_code=409,
                headers=_safe_headers(),
            )(scope, self._empty_receive, send)
            return

        self._approval_services.pop(request_id, None)
        if result.status == "ok":
            await HTMLResponse(
                _submission_page(success=True),
                headers=_safe_headers(),
            )(scope, self._empty_receive, send)
            return

        await HTMLResponse(
            _submission_page(success=False, status=result.status),
            status_code=409,
            headers=_safe_headers(),
        )(scope, self._empty_receive, send)

    async def _invoke_core(
        self,
        original_scope: dict[str, Any],
        *,
        method: str,
        path: str,
        authorization: str | None = None,
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
        ]
        if authorization is not None:
            scope["headers"].append((b"authorization", authorization.encode("latin-1")))

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
    async def _read_body(receive) -> bytes:
        chunks: list[bytes] = []
        while True:
            message = await receive()
            if message.get("type") == "http.disconnect":
                break
            if message.get("type") != "http.request":
                continue
            chunks.append(message.get("body", b""))
            if not message.get("more_body", False):
                break
        return b"".join(chunks)

    @staticmethod
    async def _empty_receive() -> dict[str, Any]:
        return {"type": "http.request", "body": b"", "more_body": False}

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
