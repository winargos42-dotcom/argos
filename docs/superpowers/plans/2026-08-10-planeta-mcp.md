# Planeta MCP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy a separate Railway service `planeta-mcp` that prepares, validates, fills, previews, syncs, and—only after a separate explicit owner approval—submits the ARGOS REBOOT Planeta.ru campaign for moderation.

**Architecture:** Implement the connector as an isolated Python service under `integrations/planeta_mcp/`. Local campaign state, browser-session state, approval state, browser automation, audit logging, and MCP transport stay in separate modules. Browser automation fails closed on authentication, CAPTCHA, identity verification, or unknown UI. Submission is impossible without a one-time short-lived approval token bound to the exact campaign digest.

**Tech Stack:** Python, FastAPI, official MCP Python SDK, Pydantic, Playwright Chromium, cryptography/Fernet, pytest, Railway.

## Global Constraints

- Service name: `planeta-mcp`.
- Default campaign name: `ARGOS REBOOT — восстановление независимой AI/FPGA-системы`.
- Default target: `200000 RUB`.
- `PLANETA_BASE_URL=https://planeta.ru`.
- `PLANETA_HEADLESS=true` by default.
- `PLANETA_SUBMIT_TTL_SECONDS=300` by default.
- Secrets: `PLANETA_MCP_SECRET`, `PLANETA_SESSION_KEY`.
- Never accept or persist a Planeta.ru password, passport scan, INN document, identity-document contents, or CAPTCHA solution.
- Authentication, CAPTCHA, SMS/e-mail confirmation, passport/INN verification, and anti-bot steps must stop with a human-action-required result.
- `fill`, `sync`, `validate`, and `preview` must never submit a project for moderation.
- `planeta_submit_for_moderation` requires a one-time unexpired approval token bound to the exact current campaign digest.
- Any campaign mutation invalidates all existing approval tokens.
- Audit logs must never include browser cookies, auth tokens, passwords, document contents, passport data, INN data, or encrypted session blobs.
- Automated tests must never submit a live Planeta.ru campaign.

---

## File Structure

- `integrations/planeta_mcp/__init__.py` — package marker.
- `integrations/planeta_mcp/config.py` — environment configuration and validation.
- `integrations/planeta_mcp/models.py` — campaign, reward, budget, validation, and result models.
- `integrations/planeta_mcp/defaults.py` — ARGOS REBOOT default campaign payload.
- `integrations/planeta_mcp/store.py` — local normalized campaign-state persistence.
- `integrations/planeta_mcp/security.py` — campaign digest, approval token issue/consume, token invalidation.
- `integrations/planeta_mcp/session_store.py` — encrypted browser-state storage and deletion.
- `integrations/planeta_mcp/audit.py` — sanitized structured audit logging.
- `integrations/planeta_mcp/browser.py` — Playwright adapter and fail-closed page-state classification.
- `integrations/planeta_mcp/selectors.py` — centralized Planeta.ru selectors; no guessed fallback clicking.
- `integrations/planeta_mcp/service.py` — campaign orchestration methods used by MCP tools.
- `integrations/planeta_mcp/server.py` — FastAPI + remote MCP transport, `/health`, tool registration.
- `integrations/planeta_mcp/requirements.txt` — service-only dependencies.
- `integrations/planeta_mcp/Dockerfile` — Railway container with Playwright Chromium.
- `integrations/planeta_mcp/README.md` — operator instructions, human login flow, approval flow.
- `integrations/planeta_mcp/fixtures/*.html` — local browser test pages.
- `tests/planeta_mcp/test_models.py`
- `tests/planeta_mcp/test_security.py`
- `tests/planeta_mcp/test_session_store.py`
- `tests/planeta_mcp/test_audit.py`
- `tests/planeta_mcp/test_browser.py`
- `tests/planeta_mcp/test_service.py`
- `tests/planeta_mcp/test_server.py`

---

### Task 1: Campaign Model, Defaults, Validation, and Local Store

**Files:**
- Create: `integrations/planeta_mcp/__init__.py`
- Create: `integrations/planeta_mcp/config.py`
- Create: `integrations/planeta_mcp/models.py`
- Create: `integrations/planeta_mcp/defaults.py`
- Create: `integrations/planeta_mcp/store.py`
- Test: `tests/planeta_mcp/test_models.py`

**Interfaces:**
- Produces: `CampaignPayload`, `Reward`, `BudgetItem`, `ValidationReport`, `CampaignStore`, `default_argos_reboot_campaign()`.
- `CampaignPayload.canonical_dict() -> dict[str, object]` must be deterministic and exclude volatile timestamps.
- `CampaignPayload.validate_for_planeta() -> ValidationReport` returns errors/warnings without external calls.
- `CampaignStore.load() -> CampaignPayload | None`, `CampaignStore.save(payload: CampaignPayload) -> None`.

- [ ] **Step 1: Write failing validation/default tests**

```python
from integrations.planeta_mcp.defaults import default_argos_reboot_campaign


def test_argos_reboot_defaults_are_valid():
    campaign = default_argos_reboot_campaign()
    report = campaign.validate_for_planeta()
    assert campaign.title == "ARGOS REBOOT — восстановление независимой AI/FPGA-системы"
    assert campaign.target_amount == 200000
    assert campaign.currency == "RUB"
    assert report.errors == []


def test_campaign_rejects_missing_evidence_and_empty_rewards():
    campaign = default_argos_reboot_campaign().model_copy(
        update={"evidence_links": [], "rewards": []}
    )
    report = campaign.validate_for_planeta()
    assert "evidence_links" in report.error_fields
    assert "rewards" in report.error_fields
```

- [ ] **Step 2: Run tests and verify failure**

Run: `pytest tests/planeta_mcp/test_models.py -v`

Expected: FAIL because the package/models/defaults do not exist.

- [ ] **Step 3: Implement typed models and local validation**

Use explicit models similar to:

```python
class Reward(BaseModel):
    title: str
    amount: int = Field(gt=0)
    description: str
    physical: bool = False


class BudgetItem(BaseModel):
    title: str
    amount: int = Field(gt=0)


class ValidationReport(BaseModel):
    errors: list[str] = []
    warnings: list[str] = []
    error_fields: list[str] = []


class CampaignPayload(BaseModel):
    title: str
    target_amount: int = Field(gt=0)
    currency: Literal["RUB"] = "RUB"
    summary: str
    story: str
    evidence_links: list[HttpUrl]
    rewards: list[Reward]
    budget: list[BudgetItem]

    def canonical_dict(self) -> dict[str, object]:
        return self.model_dump(mode="json", exclude_none=True)

    def validate_for_planeta(self) -> ValidationReport:
        ...
```

The defaults module must clearly separate public/verifiable surviving artifacts, owner testimony, and future recovery goals. Default rewards must be non-physical.

- [ ] **Step 4: Implement atomic local persistence**

`CampaignStore.save()` writes JSON to a temp file then `os.replace()` to the configured state path. It must store campaign copy only—never session/auth material.

- [ ] **Step 5: Run tests**

Run: `pytest tests/planeta_mcp/test_models.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add integrations/planeta_mcp tests/planeta_mcp/test_models.py
git commit -m "feat(planeta): add campaign model and validation"
```

---

### Task 2: Sanitized Audit Log and Approval Gate

**Files:**
- Create: `integrations/planeta_mcp/audit.py`
- Create: `integrations/planeta_mcp/security.py`
- Test: `tests/planeta_mcp/test_audit.py`
- Test: `tests/planeta_mcp/test_security.py`

**Interfaces:**
- Produces: `campaign_digest(payload) -> str`.
- Produces: `ApprovalGate.issue(payload) -> ApprovalGrant`.
- Produces: `ApprovalGate.consume(token: str, payload) -> ApprovalGrant`.
- Produces: `ApprovalGate.invalidate_all() -> None`.
- Produces: `AuditLogger.record(tool: str, campaign_id: str, status: str, result: dict) -> None`.

- [ ] **Step 1: Write failing approval tests**

```python
def test_approval_token_is_one_time_and_bound_to_digest(gate, campaign):
    grant = gate.issue(campaign)
    gate.consume(grant.token, campaign)
    with pytest.raises(ApprovalError):
        gate.consume(grant.token, campaign)


def test_campaign_edit_invalidates_approval(gate, campaign):
    grant = gate.issue(campaign)
    changed = campaign.model_copy(update={"target_amount": campaign.target_amount + 1})
    with pytest.raises(ApprovalError):
        gate.consume(grant.token, changed)
```

- [ ] **Step 2: Write failing audit-redaction test**

```python
def test_audit_never_logs_secret_material(tmp_path):
    logger = AuditLogger(tmp_path / "audit.jsonl")
    logger.record("fill", "argos-reboot", "ok", {
        "cookie": "secret-cookie",
        "password": "secret-password",
        "passport": "1234 567890",
        "safe": "ok",
    })
    text = (tmp_path / "audit.jsonl").read_text()
    assert "secret-cookie" not in text
    assert "secret-password" not in text
    assert "1234 567890" not in text
    assert '"safe": "ok"' in text
```

- [ ] **Step 3: Run tests and verify failure**

Run: `pytest tests/planeta_mcp/test_security.py tests/planeta_mcp/test_audit.py -v`

Expected: FAIL because security/audit modules do not exist.

- [ ] **Step 4: Implement SHA-256 campaign digest and HMAC-backed approval tokens**

Approval records must contain token hash, campaign digest, issued-at, expires-at, and used flag. The raw token is returned once and never logged. TTL comes from `PLANETA_SUBMIT_TTL_SECONDS`, default 300 seconds.

- [ ] **Step 5: Implement recursive audit sanitizer**

Redact keys matching at least: `password`, `cookie`, `cookies`, `authorization`, `token`, `secret`, `passport`, `inn`, `document`, `session`, `storage_state`. Preserve non-sensitive status metadata.

- [ ] **Step 6: Run tests**

Run: `pytest tests/planeta_mcp/test_security.py tests/planeta_mcp/test_audit.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add integrations/planeta_mcp/audit.py integrations/planeta_mcp/security.py tests/planeta_mcp
git commit -m "feat(planeta): add approval gate and sanitized audit"
```

---

### Task 3: Encrypted Human-Authenticated Browser Session Store

**Files:**
- Create: `integrations/planeta_mcp/session_store.py`
- Test: `tests/planeta_mcp/test_session_store.py`

**Interfaces:**
- Produces: `SessionStore.save_storage_state(storage_state: dict) -> None`.
- Produces: `SessionStore.load_storage_state() -> dict | None`.
- Produces: `SessionStore.clear() -> None`.
- The module accepts only Playwright storage-state JSON, never username/password credentials.

- [ ] **Step 1: Write failing encrypted-store tests**

```python
def test_session_state_is_encrypted_at_rest(tmp_path, fernet_key):
    store = SessionStore(tmp_path / "session.enc", fernet_key)
    state = {"cookies": [{"name": "sid", "value": "sensitive"}], "origins": []}
    store.save_storage_state(state)
    raw = (tmp_path / "session.enc").read_bytes()
    assert b"sensitive" not in raw
    assert store.load_storage_state() == state


def test_clear_removes_browser_state(tmp_path, fernet_key):
    store = SessionStore(tmp_path / "session.enc", fernet_key)
    store.save_storage_state({"cookies": [], "origins": []})
    store.clear()
    assert store.load_storage_state() is None
```

- [ ] **Step 2: Run test and verify failure**

Run: `pytest tests/planeta_mcp/test_session_store.py -v`

Expected: FAIL because `SessionStore` does not exist.

- [ ] **Step 3: Implement Fernet encrypted persistence**

`PLANETA_SESSION_KEY` is required when persistent session storage is enabled. Reject malformed keys at startup. Restrict file permissions where the platform allows it.

- [ ] **Step 4: Add explicit input guard**

Reject mappings containing keys such as `username`, `email_password`, `password`, `passport`, `inn`, or arbitrary document blobs. The only accepted top-level storage-state keys are Playwright-compatible `cookies` and `origins`.

- [ ] **Step 5: Run tests**

Run: `pytest tests/planeta_mcp/test_session_store.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add integrations/planeta_mcp/session_store.py tests/planeta_mcp/test_session_store.py
git commit -m "feat(planeta): encrypt browser session state"
```

---

### Task 4: Fail-Closed Playwright Adapter

**Files:**
- Create: `integrations/planeta_mcp/selectors.py`
- Create: `integrations/planeta_mcp/browser.py`
- Create: `integrations/planeta_mcp/fixtures/draft.html`
- Create: `integrations/planeta_mcp/fixtures/login.html`
- Create: `integrations/planeta_mcp/fixtures/captcha.html`
- Create: `integrations/planeta_mcp/fixtures/identity.html`
- Create: `integrations/planeta_mcp/fixtures/ui_changed.html`
- Test: `tests/planeta_mcp/test_browser.py`

**Interfaces:**
- Produces: `BrowserResult(status, reason, draft_snapshot)`.
- Produces: `PlanetaBrowser.classify_page(page) -> BrowserState`.
- Produces: `PlanetaBrowser.fill_draft(payload) -> BrowserResult`.
- Produces: `PlanetaBrowser.read_draft() -> BrowserResult`.
- Produces: `PlanetaBrowser.submit_for_moderation() -> BrowserResult`.
- Error statuses: `human_action_required`, `authentication_required`, `captcha_required`, `ui_changed`, `validation_failed`, `network_error`, `planeta_error`.

- [ ] **Step 1: Write fixture-based page classification tests**

```python
@pytest.mark.parametrize(
    ("fixture", "expected"),
    [
        ("login.html", "authentication_required"),
        ("captcha.html", "captcha_required"),
        ("identity.html", "human_action_required"),
        ("ui_changed.html", "ui_changed"),
    ],
)
async def test_classifies_blocking_pages(browser, fixture, expected):
    await browser.open_fixture(fixture)
    result = await browser.inspect()
    assert result.status == expected
```

- [ ] **Step 2: Write test proving fill never presses moderation submit**

```python
async def test_fill_draft_never_submits(browser, campaign):
    await browser.open_fixture("draft.html")
    result = await browser.fill_draft(campaign)
    assert result.status == "ok"
    assert await browser.submit_click_count() == 0
```

- [ ] **Step 3: Run tests and verify failure**

Run: `pytest tests/planeta_mcp/test_browser.py -v`

Expected: FAIL because browser adapter and fixtures do not exist.

- [ ] **Step 4: Implement centralized selectors**

Every selector must have a semantic name such as `TITLE_INPUT`, `TARGET_INPUT`, `STORY_EDITOR`, `SAVE_DRAFT_BUTTON`, `SUBMIT_MODERATION_BUTTON`. Missing required selectors return `ui_changed`; do not use proximity clicking, text guessing, or generic `button:nth-child(...)` fallbacks.

- [ ] **Step 5: Implement blocker detection before every mutation**

Detect login forms, CAPTCHA widgets/text, SMS/e-mail verification prompts, passport/INN/identity wording, moderation errors, and unexpected redirect paths before entering data or clicking Save/Submit.

- [ ] **Step 6: Implement fill/read/submit primitives**

`fill_draft()` fills only known draft fields and saves the draft if a known safe save control is present. `submit_for_moderation()` only clicks the exact known moderation control; it does no approval logic itself.

- [ ] **Step 7: Run browser tests**

Run: `pytest tests/planeta_mcp/test_browser.py -v`

Expected: PASS entirely against local HTML fixtures; no live submission.

- [ ] **Step 8: Commit**

```bash
git add integrations/planeta_mcp/browser.py integrations/planeta_mcp/selectors.py integrations/planeta_mcp/fixtures tests/planeta_mcp/test_browser.py
git commit -m "feat(planeta): add fail-closed browser adapter"
```

---

### Task 5: Orchestration Service and MCP Tools

**Files:**
- Create: `integrations/planeta_mcp/service.py`
- Create: `integrations/planeta_mcp/server.py`
- Test: `tests/planeta_mcp/test_service.py`
- Test: `tests/planeta_mcp/test_server.py`

**Interfaces:**
- Produces service methods matching all MCP tools:
  - `campaign_status()`
  - `campaign_preview()`
  - `validate_campaign()`
  - `prepare_campaign(payload)`
  - `fill_draft()`
  - `sync_draft()`
  - `request_submit_approval()`
  - `submit_for_moderation(approval_token)`
- Exposes `/health` and MCP-over-HTTP endpoint.

- [ ] **Step 1: Write failing service tests for approval sequencing**

```python
async def test_submit_requires_prior_approval(service):
    with pytest.raises(ApprovalError):
        await service.submit_for_moderation("not-valid")


async def test_prepare_invalidates_prior_approval(service, campaign):
    await service.prepare_campaign(campaign)
    grant = await service.request_submit_approval()
    await service.prepare_campaign(campaign.model_copy(update={"target_amount": 199999}))
    with pytest.raises(ApprovalError):
        await service.submit_for_moderation(grant.token)
```

- [ ] **Step 2: Write failing MCP discovery/health tests**

```python
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_tool_names_are_registered(mcp_client):
    names = {tool.name for tool in mcp_client.list_tools()}
    assert {
        "planeta_campaign_status",
        "planeta_campaign_preview",
        "planeta_validate_campaign",
        "planeta_prepare_campaign",
        "planeta_fill_draft",
        "planeta_sync_draft",
        "planeta_request_submit_approval",
        "planeta_submit_for_moderation",
    } <= names
```

- [ ] **Step 3: Run tests and verify failure**

Run: `pytest tests/planeta_mcp/test_service.py tests/planeta_mcp/test_server.py -v`

Expected: FAIL because service/server do not exist.

- [ ] **Step 4: Implement orchestration service**

For every action: load current campaign, validate where required, invoke exactly one responsibility, sanitize audit output, and return typed status. Any `prepare_campaign()` mutation calls `approval_gate.invalidate_all()`.

- [ ] **Step 5: Implement final submit order exactly**

`submit_for_moderation(token)` must execute in this order:

```python
campaign = store.load_required()
report = campaign.validate_for_planeta()
if report.errors:
    raise ValidationError(report.errors)
approval_gate.consume(token, campaign)  # validates current digest + one-time + TTL
result = await browser.submit_for_moderation()
audit.record("planeta_submit_for_moderation", campaign.id, result.status, result.safe_dict())
return result
```

If browser submission returns a blocker/error, the consumed token stays consumed. A fresh explicit approval is required for any retry.

- [ ] **Step 6: Register MCP tools and `/health`**

Tool descriptions must clearly label read-only tools, draft-write tools, and the final moderation-submission tool. The final tool description must state that it requires an approval token generated immediately beforehand.

- [ ] **Step 7: Run tests**

Run: `pytest tests/planeta_mcp/test_service.py tests/planeta_mcp/test_server.py -v`

Expected: PASS.

- [ ] **Step 8: Run complete connector suite**

Run: `pytest tests/planeta_mcp -v`

Expected: PASS with zero live Planeta.ru submissions.

- [ ] **Step 9: Commit**

```bash
git add integrations/planeta_mcp/service.py integrations/planeta_mcp/server.py tests/planeta_mcp
git commit -m "feat(planeta): expose guarded MCP campaign tools"
```

---

### Task 6: Container, Railway Deployment, Smoke Test, and Operator Docs

**Files:**
- Create: `integrations/planeta_mcp/requirements.txt`
- Create: `integrations/planeta_mcp/Dockerfile`
- Create: `integrations/planeta_mcp/README.md`
- Create: `scripts/smoke_planeta_mcp.py`
- Modify only if needed: root Railway/deployment documentation; do not alter the existing ARGOS Core service command.

**Interfaces:**
- Container starts `planeta-mcp` on Railway `$PORT`.
- `/health` returns at least `{"ok": true, "service": "planeta-mcp"}`.
- Smoke script checks health and tool discovery only.

- [ ] **Step 1: Add service-only dependencies**

Include the project-compatible packages for FastAPI/ASGI, MCP SDK, Pydantic, Playwright, cryptography, and pytest test extras. Do not add browser automation dependencies to the entire ARGOS runtime unless already shared.

- [ ] **Step 2: Add Playwright-capable Dockerfile**

The image must install Chromium and required system libraries, copy only required repository content, use a non-root runtime user where compatible with Playwright, and start:

```bash
uvicorn integrations.planeta_mcp.server:app --host 0.0.0.0 --port ${PORT:-8000}
```

- [ ] **Step 3: Add Railway runtime documentation**

Document these variables exactly:

```text
PLANETA_MCP_SECRET=<Railway secret>
PLANETA_SESSION_KEY=<Fernet key stored as Railway secret>
PLANETA_BASE_URL=https://planeta.ru
PLANETA_HEADLESS=true
PLANETA_SUBMIT_TTL_SECONDS=300
```

Explicitly document that there must be no `PLANETA_PASSWORD`, passport, INN, or identity-document environment variable.

- [ ] **Step 4: Add smoke test**

`scripts/smoke_planeta_mcp.py` accepts a base URL, verifies `/health`, performs MCP initialization/tool discovery, asserts all eight tool names, and never invokes write tools.

- [ ] **Step 5: Run local verification**

Run:

```bash
pytest tests/planeta_mcp -v
python -m compileall integrations/planeta_mcp
```

Expected: all tests PASS and compileall exits 0.

- [ ] **Step 6: Build container locally or in CI**

Run:

```bash
docker build -f integrations/planeta_mcp/Dockerfile -t argos-planeta-mcp .
```

Expected: build completes successfully.

- [ ] **Step 7: Deploy a separate Railway service `planeta-mcp`**

Deploy into the existing ARGOS Railway project when possible. Do not replace or repoint the running ARGOS Core service. Configure only the Planeta MCP service with the required secrets.

- [ ] **Step 8: Verify Railway deployment**

Check latest deployment is `SUCCESS`, then run:

```bash
python scripts/smoke_planeta_mcp.py https://<planeta-mcp-domain>
```

Expected: `/health` OK and all eight tools discovered.

- [ ] **Step 9: Verify secret hygiene**

Run repository searches before declaring completion:

```bash
git grep -nEi 'PLANETA_PASSWORD|passport|паспорт|storage_state.*cookie|secret-cookie|1234 567890' -- . ':!docs/superpowers/*' ':!tests/planeta_mcp/*'
```

Expected: no credential/document values or browser-session blobs. Generic documentation terms are acceptable only where they state prohibited handling.

- [ ] **Step 10: Commit deployment artifacts**

```bash
git add integrations/planeta_mcp scripts/smoke_planeta_mcp.py
git commit -m "deploy(planeta): add Railway MCP service"
```

---

## Final Verification Checklist

- [ ] `pytest tests/planeta_mcp -v` passes.
- [ ] `/health` is healthy on Railway.
- [ ] MCP discovery exposes exactly the intended Planeta tools.
- [ ] ARGOS REBOOT default payload validates.
- [ ] `fill_draft` cannot trigger moderation submission.
- [ ] Auth/CAPTCHA/identity fixtures fail closed.
- [ ] Submission without approval fails.
- [ ] Approval expires, is one-time, and is digest-bound.
- [ ] Campaign edits invalidate approvals.
- [ ] No live automated test submits to Planeta.ru.
- [ ] No Planeta password, passport/INN document content, cookies, tokens, or encrypted session blobs are present in Git history or sanitized logs.
- [ ] Railway service is separate from ARGOS Core and does not disrupt existing `/health` or `/mcp` services.
