from __future__ import annotations

import contextlib
import hmac
import html
import os
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

from .audit import AuditLogger
from .browser import PlanetaBrowser
from .config import PlanetaConfig
from .security import ApprovalError, ApprovalGate
from .service import PlanetaCampaignService
from .session_store import SessionStore
from .store import CampaignStore

try:  # Production dependency; optional only so lightweight unit tests can import this module.
    from mcp.server import MCPServer
    from mcp.server.transport_security import TransportSecuritySettings
except ImportError:  # pragma: no cover - exercised only without the production SDK.
    MCPServer = None  # type: ignore[assignment]
    TransportSecuritySettings = None  # type: ignore[assignment]


REGISTERED_TOOL_NAMES = (
    "planeta_campaign_status",
    "planeta_campaign_preview",
    "planeta_validate_campaign",
    "planeta_prepare_campaign",
    "planeta_fill_draft",
    "planeta_sync_draft",
    "planeta_request_submit_approval",
    "planeta_submit_for_moderation",
)

_LIVE_COOKIE = "__Host-planeta_live"


def _public_base_url() -> str:
    explicit = os.getenv("PLANETA_PUBLIC_URL", "").strip().rstrip("/")
    if explicit:
        return explicit
    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "").strip().rstrip("/")
    if domain:
        if domain.startswith(("https://", "http://")):
            return domain
        return f"https://{domain}"
    return ""


def _approval_location(request_id: str) -> tuple[str, str]:
    path = f"/approve/{request_id}"
    base = _public_base_url()
    return path, f"{base}{path}" if base else path


def build_default_service() -> PlanetaCampaignService:
    config = PlanetaConfig.from_env()
    approval_secret = os.environ.get("PLANETA_APPROVAL_SECRET")
    session_key = os.environ.get("PLANETA_SESSION_KEY")
    if not approval_secret:
        raise RuntimeError("PLANETA_APPROVAL_SECRET is required")
    if not session_key:
        raise RuntimeError("PLANETA_SESSION_KEY is required")

    data_dir = config.state_path.parent
    session_store = SessionStore(data_dir / "session.enc", session_key)
    storage_state = session_store.load_storage_state()
    browser = PlanetaBrowser(
        base_url=config.base_url,
        draft_url=config.draft_url,
        headless=config.headless,
        storage_state=storage_state,
    )
    return PlanetaCampaignService(
        store=CampaignStore(config.state_path),
        browser=browser,
        approval_gate=ApprovalGate(
            approval_secret,
            ttl_seconds=config.submit_ttl_seconds,
        ),
        audit=AuditLogger(data_dir / "audit.jsonl"),
    )


def _register_tools(mcp: Any, service: PlanetaCampaignService | None) -> None:
    def require_service() -> PlanetaCampaignService:
        if service is None:
            raise RuntimeError("Planeta MCP service is not configured")
        return service

    @mcp.tool(
        name="planeta_campaign_status",
        description="READ-ONLY: Return local ARGOS REBOOT campaign status and validation state.",
    )
    async def planeta_campaign_status() -> dict[str, Any]:
        return await require_service().campaign_status()

    @mcp.tool(
        name="planeta_campaign_preview",
        description="READ-ONLY: Preview the exact normalized campaign payload without changing Planeta.ru.",
    )
    async def planeta_campaign_preview() -> dict[str, Any]:
        return await require_service().campaign_preview()

    @mcp.tool(
        name="planeta_validate_campaign",
        description="READ-ONLY: Validate the current campaign locally; performs no Planeta.ru write.",
    )
    async def planeta_validate_campaign() -> dict[str, Any]:
        report = await require_service().validate_campaign()
        return report.model_dump(mode="json")

    @mcp.tool(
        name="planeta_prepare_campaign",
        description="DRAFT WRITE (LOCAL): Create/update local normalized campaign state. Never submits for moderation.",
    )
    async def planeta_prepare_campaign(payload: dict[str, Any]) -> dict[str, Any]:
        return await require_service().prepare_campaign(payload)

    @mcp.tool(
        name="planeta_fill_draft",
        description="DRAFT WRITE: Fill known Planeta.ru draft fields and save the draft. Never submits for moderation.",
    )
    async def planeta_fill_draft() -> dict[str, Any]:
        result = await require_service().fill_draft()
        return result.safe_dict()

    @mcp.tool(
        name="planeta_sync_draft",
        description="DRAFT READ/SYNC: Read known Planeta.ru draft fields and report differences. Never submits.",
    )
    async def planeta_sync_draft() -> dict[str, Any]:
        return await require_service().sync_draft()

    @mcp.tool(
        name="planeta_request_submit_approval",
        description=(
            "FINAL-ACTION REQUEST: Create a short-lived pending moderation-submit request. "
            "This does NOT approve or submit anything; the owner must open the returned approval URL "
            "and press the confirmation button before submission can succeed."
        ),
    )
    async def planeta_request_submit_approval() -> dict[str, Any]:
        approval_request = await require_service().request_submit_approval()
        approval_path, approval_url = _approval_location(approval_request.request_id)
        return {
            "request_id": approval_request.request_id,
            "campaign_digest": approval_request.campaign_digest,
            "issued_at": approval_request.issued_at,
            "expires_at": approval_request.expires_at,
            "approval_path": approval_path,
            "approval_url": approval_url,
            "status": "pending_human_confirmation",
            "warning": (
                "No submission is authorized yet. The owner must open approval_url and explicitly "
                "press the confirmation button."
            ),
        }

    @mcp.tool(
        name="planeta_submit_for_moderation",
        description=(
            "FINAL WRITE: Submit the filled Planeta.ru project for moderation. "
            "Requires a request_id that has already been confirmed by the owner on the separate approval page."
        ),
    )
    async def planeta_submit_for_moderation(request_id: str) -> dict[str, Any]:
        result = await require_service().submit_for_moderation(request_id)
        return result.safe_dict()


def _transport_security() -> Any:
    if TransportSecuritySettings is None:
        return None
    hosts = ["127.0.0.1:*", "localhost:*"]
    origins = ["http://127.0.0.1:*", "http://localhost:*"]

    configured = os.getenv("PLANETA_ALLOWED_HOSTS", "")
    public_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
    candidates = [part.strip() for part in configured.split(",") if part.strip()]
    if public_domain.strip():
        candidates.append(public_domain.strip())

    for host in dict.fromkeys(candidates):
        clean = host.removeprefix("https://").removeprefix("http://").rstrip("/")
        if not clean:
            continue
        hosts.extend([clean, f"{clean}:*"])
        origins.extend([f"https://{clean}", f"https://{clean}:*"])

    return TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=list(dict.fromkeys(hosts)),
        allowed_origins=list(dict.fromkeys(origins)),
    )


def _approval_headers() -> dict[str, str]:
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


def _live_headers() -> dict[str, str]:
    return {
        "Cache-Control": "no-store, max-age=0",
        "Pragma": "no-cache",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "Content-Security-Policy": (
            "default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; "
            "connect-src 'self' ws: wss:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'"
        ),
    }


def _live_login_page() -> str:
    return """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>ARGOS — вход Planeta.ru</title>
<style>
html,body,#screen{width:100%;height:100%;margin:0;background:#111;color:#fff;font-family:system-ui,sans-serif}
#screen{overflow:hidden}.message{padding:18px}
</style>
</head>
<body><div id="screen"><div class="message">Подключение к защищённому браузеру Planeta.ru…</div></div>
<script type="module" src="/live-login/client.js"></script>
</body></html>"""


def _live_client_js() -> str:
    return """const screen = document.getElementById('screen');
let capability = window.location.hash.slice(1);
history.replaceState(null, '', window.location.pathname);

function show(message) {
  screen.innerHTML = '';
  const node = document.createElement('div');
  node.className = 'message';
  node.textContent = message;
  screen.appendChild(node);
}

async function start() {
  if (!capability) {
    show('Одноразовая ссылка недействительна или уже использована.');
    return;
  }

  const exchange = await fetch('/live-login/exchange', {
    method: 'POST',
    headers: {Authorization: `Bearer ${capability}`},
    credentials: 'same-origin',
    cache: 'no-store',
  });
  capability = '';
  if (!exchange.ok) {
    show('Не удалось открыть защищённую сессию. Запроси новую ссылку.');
    return;
  }

  const {default: RFB} = await import('/live-login/assets/core/rfb.js');
  const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const rfb = new RFB(screen, `${scheme}://${window.location.host}/live-login/websockify`);
  rfb.scaleViewport = true;
  rfb.resizeSession = true;
  rfb.focusOnClick = true;
}

start().catch(() => show('Не удалось подключиться к браузеру Planeta.ru.'));
"""


def _approval_page(
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
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ARGOS REBOOT — подтверждение</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:720px;margin:40px auto;padding:0 18px;line-height:1.5}}
.card{{border:1px solid #8885;border-radius:16px;padding:22px}}
code{{word-break:break-all}}button{{font-size:1.05rem;padding:12px 18px;margin-top:16px}}
.warn{{font-weight:700}}
</style>
</head>
<body><div class="card">
<h1>ARGOS REBOOT</h1>
<p class="warn">Подтвердить отправку на модерацию?</p>
<p>Это разрешение одноразовое и действует только для текущей версии кампании.</p>
<p>Digest: <code>{safe_digest}</code></p>
<p>Истекает: <code>{expires_at:.0f}</code></p>
<form method="post" action="/approve/{safe_request}">
<input type="hidden" name="csrf_token" value="{safe_csrf}">
<button type="submit">Подтвердить отправку на модерацию</button>
</form>
</div></body></html>"""


def create_app(
    service: PlanetaCampaignService | None = None,
    *,
    enable_mcp: bool = True,
    auth_secret: str | None = None,
    live_control_secret: str | None = None,
    live_coordinator: Any | None = None,
) -> FastAPI:
    mcp_server = None
    mcp_subapp = None
    if enable_mcp:
        if MCPServer is None:
            raise RuntimeError("Official MCP Python SDK v2 is required when MCP is enabled")
        mcp_server = MCPServer("ARGOS Planeta MCP")
        _register_tools(mcp_server, service)
        mcp_subapp = mcp_server.streamable_http_app(
            streamable_http_path="/mcp",
            json_response=True,
            stateless_http=True,
            transport_security=_transport_security(),
            host="0.0.0.0",
        )

    if mcp_server is not None:
        @contextlib.asynccontextmanager
        async def lifespan(_app: FastAPI):
            async with mcp_server.session_manager.run():
                yield
        app = FastAPI(title="ARGOS Planeta MCP", lifespan=lifespan)
    else:
        app = FastAPI(title="ARGOS Planeta MCP")

    app.mount(
        "/live-login/assets",
        StaticFiles(directory="/usr/share/novnc", check_dir=False),
        name="planeta-novnc",
    )

    def require_http_service() -> PlanetaCampaignService:
        if service is None:
            raise HTTPException(status_code=503, detail="Planeta MCP service is not configured")
        return service

    def require_live_coordinator() -> Any:
        if live_coordinator is None or not live_control_secret:
            raise HTTPException(status_code=503, detail="live login is not configured")
        return live_coordinator

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "ok": (service is not None) or (mcp_server is None),
            "service": "planeta-mcp",
            "mcp_enabled": mcp_server is not None,
            "configured": service is not None,
        }

    @app.post("/live-login/start")
    async def live_login_start(request: Request) -> JSONResponse:
        coordinator = require_live_coordinator()
        supplied = request.headers.get("authorization", "")
        expected = f"Bearer {live_control_secret}"
        if not hmac.compare_digest(supplied, expected):
            return JSONResponse(status_code=401, content={"detail": "unauthorized"})
        session = await coordinator.start()
        base = _public_base_url()
        path = "/live-login/"
        browser_url = f"{base}{path}#{session.token}" if base else f"{path}#{session.token}"
        return JSONResponse(
            {
                "browser_url": browser_url,
                "expires_at": session.expires_at,
                "status_url": f"{base}/live-login/status" if base else "/live-login/status",
                "durability": getattr(coordinator, "durability", "ephemeral"),
            },
            headers=_live_headers(),
        )

    @app.get("/live-login/", response_class=HTMLResponse)
    async def live_login_page() -> HTMLResponse:
        if live_coordinator is None or not live_control_secret:
            raise HTTPException(status_code=503, detail="live login is not configured")
        return HTMLResponse(_live_login_page(), headers=_live_headers())

    @app.get("/live-login/client.js", response_class=PlainTextResponse)
    async def live_login_client() -> PlainTextResponse:
        if live_coordinator is None or not live_control_secret:
            raise HTTPException(status_code=503, detail="live login is not configured")
        return PlainTextResponse(
            _live_client_js(),
            media_type="application/javascript",
            headers=_live_headers(),
        )

    @app.post("/live-login/exchange")
    async def live_login_exchange(request: Request) -> Response:
        coordinator = require_live_coordinator()
        supplied = request.headers.get("authorization", "")
        prefix = "Bearer "
        if not supplied.startswith(prefix):
            return JSONResponse(status_code=401, content={"detail": "unauthorized"})
        token = supplied[len(prefix):]
        try:
            coordinator.exchange(token)
        except KeyError:
            return JSONResponse(status_code=401, content={"detail": "invalid or expired capability"})
        except ValueError:
            return JSONResponse(status_code=409, content={"detail": "capability already exchanged"})

        response = Response(status_code=204, headers=_live_headers())
        response.set_cookie(
            _LIVE_COOKIE,
            token,
            secure=True,
            httponly=True,
            samesite="strict",
            path="/",
            max_age=None,
        )
        return response

    @app.get("/live-login/status")
    async def live_login_status(request: Request) -> JSONResponse:
        coordinator = require_live_coordinator()
        token = request.cookies.get(_LIVE_COOKIE, "")
        if not token:
            return JSONResponse(status_code=401, content={"detail": "unauthorized"})
        status = coordinator.status(token)
        if status is None:
            return JSONResponse(status_code=404, content={"detail": "live login session not found"})
        return JSONResponse(status, headers=_live_headers())

    @app.get("/approve/{request_id}", response_class=HTMLResponse)
    async def approval_form(request_id: str) -> HTMLResponse:
        svc = require_http_service()
        try:
            challenge = svc.get_submit_approval_challenge(request_id)
        except ApprovalError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return HTMLResponse(
            _approval_page(
                request_id=challenge.request_id,
                campaign_digest=challenge.campaign_digest,
                expires_at=challenge.expires_at,
                csrf_token=challenge.csrf_token,
            ),
            headers=_approval_headers(),
        )

    @app.post("/approve/{request_id}", response_class=HTMLResponse)
    async def approval_confirm(request_id: str, request: Request) -> HTMLResponse:
        svc = require_http_service()
        form = await request.form()
        csrf_token = str(form.get("csrf_token", ""))
        try:
            challenge = svc.confirm_submit_approval(request_id, csrf_token)
        except ApprovalError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        safe_digest = html.escape(challenge.campaign_digest, quote=True)
        body = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ARGOS REBOOT — подтверждено</title></head><body>
<h1>Подтверждение принято</h1>
<p>Одноразовое разрешение на отправку кампании с digest <code>{safe_digest}</code> активировано.</p>
<p>Теперь можно выполнить инструмент <code>planeta_submit_for_moderation</code> с тем же request_id.</p>
</body></html>"""
        return HTMLResponse(body, headers=_approval_headers())

    if auth_secret:
        @app.middleware("http")
        async def protect_mcp(request: Request, call_next):
            if request.url.path.startswith("/mcp"):
                supplied = request.headers.get("authorization", "")
                expected = f"Bearer {auth_secret}"
                if not hmac.compare_digest(supplied, expected):
                    return JSONResponse(status_code=401, content={"detail": "unauthorized"})
            return await call_next(request)

    if mcp_subapp is not None:
        # Mount at root so the MCPServer's own /mcp route stays publicly available as /mcp.
        app.mount("/", mcp_subapp)
    else:
        @app.api_route("/mcp", methods=["GET", "POST", "DELETE"])
        async def mcp_disabled():
            raise HTTPException(status_code=503, detail="MCP SDK not enabled")

    return app


def _module_app() -> FastAPI:
    mcp_secret = os.environ.get("PLANETA_MCP_SECRET")
    try:
        service = build_default_service()
    except Exception:
        service = None
    return create_app(
        service=service,
        enable_mcp=MCPServer is not None,
        auth_secret=mcp_secret,
    )


app = _module_app()
