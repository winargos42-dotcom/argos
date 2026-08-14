# Planeta.ru Live Browser Bridge — Design

## Goal

Connect the already deployed `planeta-mcp-v4` service to the owner's authenticated Planeta.ru session so the connector can fill and save draft campaign `251138` from the same browser context the owner uses for login/CAPTCHA. Submission for moderation remains a separate explicit owner-approved action.

## Root Cause

The existing connector works in Railway, but Planeta.ru challenges the server-side headless Chromium with CAPTCHA. The owner's phone browser is already authenticated, but its cookies are isolated from Railway. Copying credentials into chat, GitHub, Railway variables, or ARGOS is forbidden, and automated CAPTCHA solving is out of scope.

## Chosen Architecture

Use one browser context shared by the human and the connector.

1. `planeta-mcp-v4` starts a non-headless Chromium under a virtual display.
2. A browser-view gateway exposes only that Chromium UI through HTTPS to a short-lived one-time session URL.
3. The owner opens that URL from the phone and completes Planeta.ru login/CAPTCHA directly inside the live browser.
4. The connector attaches to the same Chromium context through a local-only CDP endpoint.
5. After the draft editor is detected, the connector saves only Playwright storage state through the existing encrypted `SessionStore`, prepares the ARGOS REBOOT payload, fills known draft fields, clicks only the safe draft-save control, and re-reads the draft for verification.
6. The moderation-submit control remains protected by the existing digest-bound one-time approval gate and is never clicked as part of login, fill, sync, or verification.

## Components

### Live Chromium

Runs inside the Railway service using the same Chromium installation already shipped for Playwright. It runs with a dedicated user-data directory under `/data/planeta/browser-profile` and a local CDP port bound to loopback only.

### Virtual Display and Browser View

A minimal X virtual framebuffer plus VNC/noVNC-compatible web client exposes the actual Chromium window. The public browser-view path is gated by a cryptographically random session token with a short TTL. The token is generated at runtime and never committed. Direct VNC and CDP ports are never exposed publicly.

### Session Controller

A small controller coordinates four states: `waiting_for_human`, `human_login_in_progress`, `authenticated_draft_ready`, and `expired`.

It validates that the current page origin is `https://planeta.ru`, refuses unrelated origins, and marks the session ready only when the configured draft URL can be opened without a login/password field or CAPTCHA challenge and the editor is recognizable.

### MCP Integration

`PlanetaBrowser` gains an optional CDP attachment mode. When enabled, it connects to the already-running Chromium instead of launching a separate browser. All existing fail-closed classification rules remain active.

### Persistence

The existing encrypted `SessionStore` continues to store only Playwright `cookies` and `origins`. Passwords, CAPTCHA text, passport/INN data, screenshots of identity documents, and raw credentials are never written by the connector.

A Railway volume mounted at `/data/planeta` is required before the live session is treated as durable. If no volume is attached, the connector may complete the current draft operation but must report the session as ephemeral and not claim durable authorization.

## Public Endpoints

- `/health` — unchanged.
- `/mcp` — unchanged and protected by the existing bearer secret.
- `/live-login/start` — owner-authenticated control that creates a short-lived browser session and returns the one-time browser-view URL.
- `/live-login/{token}/` — token-gated browser-view page. Token expires after a short configurable TTL and becomes invalid after successful session capture.
- `/live-login/status/{token}` — returns sanitized state only; never returns cookies, credentials, URLs containing secrets, or page content.

The live-login endpoints use `Cache-Control: no-store`, deny framing, use a strict Content Security Policy, and must not log query strings or form contents.

## Data Flow

1. Owner requests live login.
2. Service creates one-time token and starts/reuses the dedicated Chromium profile.
3. Owner opens browser view on the phone and performs Planeta.ru login/CAPTCHA directly.
4. Session controller detects the configured draft editor.
5. Connector captures encrypted storage state and invalidates the live-login token.
6. Connector prepares the canonical ARGOS REBOOT campaign payload.
7. `planeta_fill_draft` fills only known fields and saves the draft.
8. `planeta_sync_draft` verifies saved values and reports differences.
9. Service stops at `draft_ready`; moderation submission requires a new explicit approval request and human confirmation.

## Security Rules

- Never accept or store Planeta.ru passwords in application forms, environment variables, Git history, ARGOS memory, or audit logs.
- Never automate CAPTCHA solving or bypass Planeta.ru anti-bot checks.
- Never expose CDP or VNC directly to the public network.
- Browser-view URLs are random, one-time, short-lived, no-store, and invalidated after use.
- Live browser is restricted to Planeta.ru navigation; unexpected origins fail closed.
- Identity verification, passport, INN, SMS/e-mail codes, and legal acceptance flows remain human actions on Planeta.ru.
- Final moderation submission remains protected by the existing separate approval gate.

## Error Handling

The bridge returns only sanitized states:

- `waiting_for_human`
- `authentication_required`
- `captcha_required`
- `human_action_required`
- `draft_ready`
- `ui_changed`
- `network_error`
- `expired`

Unexpected UI never triggers guessed clicks.

## Testing

Tests are written before production changes and cover:

1. one-time token creation, expiry, invalidation, and no-store headers;
2. rejection of wrong-origin navigation;
3. CDP attachment using a local test Chromium instance;
4. session capture stores encrypted state only;
5. password/credential fields never enter `SessionStore` or audit logs;
6. live-login completion transitions to `draft_ready` only after the known draft editor is detected;
7. fill/sync works through the attached browser context;
8. no path from live login can call moderation submission;
9. existing Planeta MCP test suite remains green.

## Deployment

Extend the existing `integrations/planeta_mcp/Dockerfile.railway` with only the packages required for the virtual display and browser view. Keep `planeta-mcp-v4` on port 8000; the browser-view transport and CDP listeners are loopback-only and proxied through the application.

Before persisting authorization, attach a Railway volume at `/data/planeta`. If the available Railway connector cannot create a volume directly, report that operational gap explicitly rather than claiming durability.

## Success Criteria

The bridge is complete when:

1. Owner opens a one-time HTTPS browser-view URL from the phone.
2. Owner completes Planeta.ru login/CAPTCHA inside that live Chromium.
3. `planeta-mcp-v4` detects authenticated access to `https://planeta.ru/campaigns/251138/edit/about` in the same browser context.
4. The connector saves only encrypted session state.
5. ARGOS REBOOT campaign payload is prepared, filled, saved, and synced against the real draft.
6. No moderation submission occurs without a separate explicit owner confirmation.
7. `/health` remains healthy and the full Planeta MCP test suite passes.
