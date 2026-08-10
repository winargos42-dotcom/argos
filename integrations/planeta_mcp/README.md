# ARGOS Planeta MCP

`planeta-mcp` is an isolated remote MCP service for preparing the **ARGOS REBOOT** crowdfunding campaign and, only after a separate explicit approval, submitting the already-filled Planeta.ru draft for moderation.

## Safety boundary

The connector never accepts or stores a Planeta.ru password, passport scan, INN document, identity-document contents, or CAPTCHA solution. Human login, CAPTCHA, SMS/e-mail confirmation and identity verification stay on Planeta.ru and must be completed by the owner.

The tools are split into three classes:

- Read-only: `planeta_campaign_status`, `planeta_campaign_preview`, `planeta_validate_campaign`.
- Draft operations: `planeta_prepare_campaign`, `planeta_fill_draft`, `planeta_sync_draft`.
- Final action: `planeta_request_submit_approval`, then `planeta_submit_for_moderation` with the returned one-time token.

`fill`, `sync`, `validate`, and `preview` cannot submit a campaign for moderation. A campaign edit invalidates all outstanding submit approvals. A failed/blocked submit attempt consumes its approval token and requires a new explicit approval before retrying.

## Required Railway variables

```text
PLANETA_MCP_SECRET=<Railway secret>
PLANETA_SESSION_KEY=<Fernet key stored as Railway secret>
PLANETA_BASE_URL=https://planeta.ru
PLANETA_HEADLESS=true
PLANETA_SUBMIT_TTL_SECONDS=300
```

For a public Railway hostname also configure the generated host for MCP DNS-rebinding protection:

```text
PLANETA_ALLOWED_HOSTS=<generated-service-domain>.up.railway.app
```

Optional state path:

```text
PLANETA_STATE_PATH=/data/planeta/campaign.json
```

There must be **no** `PLANETA_PASSWORD`, passport, INN, identity-document, cookie, or raw browser-session environment variable.

## Authentication/session handoff

The browser adapter can reuse Playwright storage-state only **after** a human has logged into Planeta.ru. Storage state is encrypted at rest using `PLANETA_SESSION_KEY`; username/password credentials are not part of this flow.

If the stored session is absent/expired, or Planeta.ru shows login, CAPTCHA, SMS/e-mail confirmation, passport/INN verification, or an unknown editor layout, the browser action fails closed and returns a human-action-required/authentication/CAPTCHA/UI-changed status rather than guessing or bypassing the step.

The current production service expects an authenticated encrypted session file at `/data/planeta/session.enc` (or the directory containing `PLANETA_STATE_PATH`). Establishing that human-authenticated session is an operator action and is deliberately outside MCP tool calls.

## Local run

```bash
export PLANETA_MCP_SECRET='generate-a-long-random-secret'
export PLANETA_SESSION_KEY='Fernet-key-generated-with-cryptography'
export PLANETA_BASE_URL='https://planeta.ru'
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
pytest tests/planeta_mcp -v
python -m compileall integrations/planeta_mcp
```

Browser tests use only local HTML fixtures. They never submit a live Planeta.ru project.

## Docker

From repository root:

```bash
docker build -f integrations/planeta_mcp/Dockerfile -t argos-planeta-mcp .
docker run --rm -p 8000:8000 \
  -e PLANETA_MCP_SECRET \
  -e PLANETA_SESSION_KEY \
  -e PLANETA_BASE_URL=https://planeta.ru \
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
