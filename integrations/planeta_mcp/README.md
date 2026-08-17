# ARGOS Planeta MCP

`planeta-mcp` is an isolated remote MCP service for preparing the **ARGOS REBOOT** crowdfunding campaign and, only after a separate explicit human approval, submitting the already-filled Planeta.ru draft for moderation.

## Safety boundary

The connector never accepts or stores a Planeta.ru password, passport scan, INN document, identity-document contents, or CAPTCHA solution. Human login, CAPTCHA, SMS/e-mail confirmation and identity verification stay on Planeta.ru and must be completed by the owner.

The tools are split into three classes:

- Read-only: `planeta_campaign_status`, `planeta_campaign_preview`, `planeta_validate_campaign`.
- Draft operations: `planeta_prepare_campaign`, `planeta_fill_draft`, `planeta_sync_draft`.
- Final action: `planeta_request_submit_approval`, then a separate human confirmation page, then `planeta_submit_for_moderation`.

`fill`, `sync`, `validate`, and `preview` cannot submit a campaign for moderation. `planeta_request_submit_approval` also cannot submit and does not authorize submission by itself. It returns a short-lived request ID and an `/approve/...` URL. Opening that URL with GET is read-only; the owner must press **«Подтвердить отправку на модерацию»**, which sends a CSRF-protected POST and arms exactly one submission for the current campaign digest. A campaign edit invalidates pending approvals. A failed/blocked submit attempt consumes the confirmed request and requires a new explicit approval before retrying.

## Required Railway variables

```text
PLANETA_MCP_SECRET=<MCP bearer secret>
PLANETA_APPROVAL_SECRET=<separate HMAC secret for human approvals>
PLANETA_SESSION_KEY=<Fernet key stored as Railway secret>
PLANETA_BASE_URL=https://planeta.ru
PLANETA_PUBLIC_URL=https://<generated-service-domain>.up.railway.app
PLANETA_HEADLESS=true
PLANETA_SUBMIT_TTL_SECONDS=300
```

Once the owner has created/opened a Planeta.ru campaign draft, configure the **exact same-origin draft editor URL**:

```text
PLANETA_DRAFT_URL=https://planeta.ru/<owner-draft-editor-path>
```

Until `PLANETA_DRAFT_URL` is configured, live browser actions deliberately return `configuration_required`. The connector never guesses a campaign/editor URL.

For a public Railway hostname configure the generated host for MCP DNS-rebinding protection:

```text
PLANETA_ALLOWED_HOSTS=<generated-service-domain>.up.railway.app
```

Optional state path:

```text
PLANETA_STATE_PATH=/data/planeta/campaign.json
```

For a persistent authenticated browser with a separately writable campaign state:

- `PLANETA_SESSION_DIR=/data/planeta` stores `session.enc` and `browser-profile` on the Railway volume.
- `PLANETA_STATE_PATH=/tmp/planeta_campaign.json` stores the current normalized campaign in a writable runtime path.
- `PLANETA_SESSION_DURABILITY=durable` reports that the browser session is expected to survive service restarts.

If `PLANETA_SESSION_DIR` is omitted, it defaults to the parent directory of `PLANETA_STATE_PATH` for backward compatibility.

There must be **no** `PLANETA_PASSWORD`, passport, INN, identity-document, cookie, or raw browser-session environment variable.

## Authentication/session handoff

The browser adapter can reuse Playwright storage-state only **after** a human has logged into Planeta.ru. Storage state is encrypted at rest using `PLANETA_SESSION_KEY`; username/password credentials are not part of this flow.

If the stored session is absent/expired, or Planeta.ru shows login, CAPTCHA, SMS/e-mail confirmation, passport/INN verification, or an unknown editor layout, the browser action fails closed and returns a human-action-required/authentication/CAPTCHA/UI-changed status rather than guessing or bypassing the step.

The production service expects an authenticated encrypted session file at `PLANETA_SESSION_DIR/session.enc` (by default, the directory containing `PLANETA_STATE_PATH`). Establishing that human-authenticated session is an operator action and is deliberately outside MCP tool calls.

## Final-submit flow

1. `planeta_request_submit_approval` creates a pending request and returns `approval_url`.
2. The owner opens `approval_url` on a browser. GET does **not** authorize anything.
3. The owner reviews the campaign digest and presses **«Подтвердить отправку на модерацию»**.
4. The server records a short-lived, one-time human confirmation for that exact campaign digest.
5. `planeta_submit_for_moderation(request_id=...)` may now click only the exact known moderation-submit control.
6. If the request expires, campaign content changes, the UI changes, login/CAPTCHA/identity verification appears, or a submit attempt is made twice, the operation fails closed.

## Local run

```bash
export PLANETA_MCP_SECRET='generate-a-long-random-secret'
export PLANETA_APPROVAL_SECRET='generate-a-different-long-random-secret'
export PLANETA_SESSION_KEY='Fernet-key-generated-with-cryptography'
export PLANETA_BASE_URL='https://planeta.ru'
export PLANETA_PUBLIC_URL='http://127.0.0.1:8000'
export PLANETA_HEADLESS='true'
export PLANETA_SUBMIT_TTL_SECONDS='300'
uvicorn integrations.planeta_mcp.server:app --host 0.0.0.0 --port 8000
```

Health:

```bash
curl http://127.0.0.1:8000/health
```

MCP endpoint: `http://127.0.0.1:8000/mcp` and requires `Authorization: Bearer <PLANETA_MCP_SECRET>`.

## Tests

```bash
python -m pytest tests/planeta_mcp -v
python -m compileall integrations/planeta_mcp
```

Browser tests use only local HTML fixtures. They never submit a live Planeta.ru project.

## Docker

From repository root:

```bash
docker build -f integrations/planeta_mcp/Dockerfile -t argos-planeta-mcp .
docker run --rm -p 8000:8000 \
  -e PLANETA_MCP_SECRET \
  -e PLANETA_APPROVAL_SECRET \
  -e PLANETA_SESSION_KEY \
  -e PLANETA_BASE_URL=https://planeta.ru \
  -e PLANETA_PUBLIC_URL=http://127.0.0.1:8000 \
  -e PLANETA_HEADLESS=true \
  -e PLANETA_SUBMIT_TTL_SECONDS=300 \
  argos-planeta-mcp
```

## Railway smoke check

The smoke script performs only health and MCP tool discovery. It never invokes a write tool.

```bash
PLANETA_MCP_SECRET='<same service secret>' \
python scripts/smoke_planeta_mcp.py https://<planeta-mcp-domain>
```
