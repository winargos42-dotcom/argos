from __future__ import annotations

import contextlib
import hmac
import os
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .audit import AuditLogger
from .browser import PlanetaBrowser
from .config import PlanetaConfig
from .security import ApprovalGate
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


def build_default_service() -> PlanetaCampaignService:
    config = PlanetaConfig.from_env()
    secret = os.environ.get("PLANETA_MCP_SECRET")
    session_key = os.environ.get("PLANETA_SESSION_KEY")
    if not secret:
        raise RuntimeError("PLANETA_MCP_SECRET is required")
    if not session_key:
        raise RuntimeError("PLANETA_SESSION_KEY is required")

    data_dir = config.state_path.parent
    session_store = SessionStore(data_dir / "session.enc", session_key)
    storage_state = session_store.load_storage_state()
    browser = PlanetaBrowser(
        base_url=config.base_url,
        headless=config.headless,
        storage_state=storage_state,
    )
    return PlanetaCampaignService(
        store=CampaignStore(config.state_path),
        browser=browser,
        approval_gate=ApprovalGate(secret, ttl_seconds=config.submit_ttl_seconds),
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
        description="FINAL-ACTION GATE: Validate current payload and return a short-lived one-time approval token bound to its digest.",
    )
    async def planeta_request_submit_approval() -> dict[str, Any]:
        grant = await require_service().request_submit_approval()
        return {
            "approval_token": grant.token,
            "campaign_digest": grant.campaign_digest,
            "issued_at": grant.issued_at,
            "expires_at": grant.expires_at,
            "warning": "This token authorizes exactly one immediate moderation submission for this campaign digest.",
        }

    @mcp.tool(
        name="planeta_submit_for_moderation",
        description="FINAL WRITE: Submit the filled Planeta.ru project for moderation. Requires the one-time approval token generated immediately beforehand.",
    )
    async def planeta_submit_for_moderation(approval_token: str) -> dict[str, Any]:
        result = await require_service().submit_for_moderation(approval_token)
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


def create_app(
    service: PlanetaCampaignService | None = None,
    *,
    enable_mcp: bool = True,
    auth_secret: str | None = None,
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

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "ok": (service is not None) or (mcp_server is None),
            "service": "planeta-mcp",
            "mcp_enabled": mcp_server is not None,
            "configured": service is not None,
        }

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
    secret = os.environ.get("PLANETA_MCP_SECRET")
    try:
        service = build_default_service()
    except Exception:
        service = None
    return create_app(service=service, enable_mcp=MCPServer is not None, auth_secret=secret)


app = _module_app()
