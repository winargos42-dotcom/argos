# Planeta.ru MCP Connector — Design

## Goal

Create a dedicated remote MCP service `planeta-mcp` for ARGOS REBOOT that can prepare, validate, populate, preview, and—only after explicit owner confirmation—submit a Planeta.ru crowdfunding campaign for moderation.

## Scope

The connector will automate campaign preparation and browser-driven interaction with Planeta.ru. It will not bypass authentication, CAPTCHA, identity verification, anti-bot controls, or Planeta.ru moderation. It will not store the user's password, passport scans, INN documents, or other identity documents in GitHub, ARGOS memory, logs, or source code.

## Architecture

`planeta-mcp` is a separate Railway service, isolated from the ARGOS core runtime. It exposes MCP-over-HTTP tools and keeps campaign state separate from authentication state.

Components:

1. `campaign` — typed ARGOS REBOOT campaign model, budget, rewards, evidence links, and validation rules.
2. `planeta_browser` — Playwright adapter for Planeta.ru draft pages. Browser automation is best-effort and must stop whenever human authentication, CAPTCHA, identity verification, or unexpected UI is encountered.
3. `session_store` — encrypted/ephemeral authenticated browser state supplied after a human login. No username/password persistence.
4. `approval_gate` — creates a short-lived approval token for destructive/final actions. Submission for moderation requires a separate explicit approval immediately before execution.
5. `audit` — records tool name, timestamp, campaign id, status, and sanitized result; never logs cookies, tokens, passwords, document contents, passport data, or INN data.
6. `mcp_server` — remote MCP HTTP endpoint, health endpoint, and tool registration.

## MCP Tools

### Read-only

- `planeta_campaign_status()` — returns known draft status, last successful sync, validation state, and whether human login is required.
- `planeta_campaign_preview()` — returns normalized campaign text, budget, rewards, evidence links, and pending fields without changing Planeta.ru.
- `planeta_validate_campaign()` — validates locally against required ARGOS REBOOT fields and known Planeta.ru constraints.

### Draft write actions

- `planeta_prepare_campaign(payload)` — creates/updates the local campaign payload only.
- `planeta_fill_draft()` — uses the current authenticated browser session to populate a Planeta.ru draft, but does not submit it for moderation.
- `planeta_sync_draft()` — re-reads the draft and reports any differences between Planeta.ru and the local normalized payload.

### Final action

- `planeta_request_submit_approval()` — performs final validation and returns a short-lived one-time approval token plus a human-readable summary of exactly what will be submitted.
- `planeta_submit_for_moderation(approval_token)` — submits the already-filled project for moderation only when the approval token is valid, unused, unexpired, and matches the current campaign digest.

The connector must never auto-submit as a side effect of `fill`, `sync`, `validate`, or `preview`.

## ARGOS REBOOT Campaign Defaults

Default campaign name: `ARGOS REBOOT — восстановление независимой AI/FPGA-системы`.

Default target: `200000 RUB`.

Campaign text must clearly separate:

- public/verifiable surviving artifacts (GitHub repositories, model/data assets, documentation/logs),
- owner testimony about lost local state,
- future recovery goals.

Draft rewards should default to non-physical options to avoid shipping obligations unless explicitly changed by the owner.

## Authentication and Identity

Human login remains mandatory. The connector may reuse browser session state only after the owner has completed login in a Planeta.ru browser flow.

The connector must not:

- ask ARGOS to collect or persist the user's Planeta.ru password;
- upload passport/INN documents from chat or repository storage;
- solve CAPTCHA or bypass anti-bot controls;
- scrape or infer identity-document values;
- submit identity documents without the owner directly completing Planeta.ru's own flow.

If Planeta.ru requests re-authentication, CAPTCHA, SMS/e-mail confirmation, passport verification, INN, or another identity step, the MCP tool returns `human_action_required` with a concise reason.

## Data Storage

Campaign copy and non-secret configuration may be stored in repository-controlled JSON/YAML.

Secrets and browser state are stored only in Railway environment/volume state and never committed. Any persistent browser state must be encrypted with a Railway secret key and support explicit deletion.

Approval tokens are one-time, short-lived, and contain or bind to a digest of the exact campaign payload. Any campaign edit invalidates existing approval tokens.

## Error Handling

Every browser action must classify failures into one of:

- `human_action_required`
- `authentication_required`
- `captcha_required`
- `ui_changed`
- `validation_failed`
- `network_error`
- `planeta_error`

Unexpected selectors or page structure must fail closed instead of guessing or clicking a nearby control.

## Testing

Unit tests cover campaign validation, sanitization, digest/approval logic, token expiry/reuse, and error classification.

Browser adapter tests use saved local HTML fixtures/mocks for successful draft filling, missing selectors, CAPTCHA/auth prompts, and submit gating. No automated test submits a real Planeta.ru campaign.

A Railway smoke test must verify `/health` and MCP tool discovery without requiring a live Planeta.ru account.

## Deployment

Deploy as a separate Railway service named `planeta-mcp` in the existing ARGOS Railway project unless isolation or service limits require a dedicated project.

Expected environment variables:

- `PLANETA_MCP_SECRET`
- `PLANETA_SESSION_KEY`
- `PLANETA_BASE_URL=https://planeta.ru`
- `PLANETA_HEADLESS=true`
- `PLANETA_SUBMIT_TTL_SECONDS=300`

No Planeta.ru password or identity-document fields are accepted as environment variables.

## Success Criteria

The feature is complete when:

1. MCP discovery exposes all specified tools.
2. ARGOS REBOOT campaign payload validates locally.
3. An authenticated owner session can fill/update a Planeta.ru draft without submitting it.
4. Authentication/CAPTCHA/identity steps stop safely and report required human action.
5. Submission requires a separate one-time approval token tied to the exact campaign payload.
6. Secrets and personal identity documents are absent from Git history and sanitized logs.
7. Railway `/health` is healthy and the MCP endpoint is reachable.
