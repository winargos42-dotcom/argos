# Planeta Live Session Rehydration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Запускать живой Chromium из `/tmp`, восстанавливать существующую зашифрованную сессию Planeta.ru до открытия черновика и не терять рабочий результат при read-only постоянном томе.

**Architecture:** `SessionStore` остаётся постоянным источником Playwright storage state. `LiveLoginCoordinator` загружает состояние и передаёт его `LiveBrowserRuntime`, который создаёт временный persistent profile, добавляет cookies и same-origin localStorage до первой навигации. Атомарное обновление сессии остаётся предпочтительным, но `OSError` при записи становится видимым предупреждением, а не отменой заполнения черновика.

**Tech Stack:** Python 3.12, FastAPI, Playwright async API, cryptography/Fernet, pytest, pytest-asyncio, Railway Docker.

**Spec:** `docs/superpowers/specs/2026-08-17-planeta-live-session-rehydration-design.md`

## Global Constraints

- Контейнер продолжает работать от непривилегированного пользователя; root и `chown` Railway-тома запрещены.
- `PLANETA_SESSION_DIR=/data/planeta` остаётся местом зашифрованного `session.enc`.
- Живой профиль v4 размещается в `/tmp/planeta-live/browser-profile` через `config.state_path.parent`.
- Восстанавливается localStorage только точного origin настроенного URL черновика.
- Формат `session.enc` и существующий headless-путь не меняются.
- Неатомарная перезапись `session.enc` запрещена.
- Отправка на модерацию не вызывается и остаётся закрыта отдельным одноразовым подтверждением владельца.

---

### Task 1: Rehydrate the live Chromium context before navigation

**Files:**
- Modify: `integrations/planeta_mcp/live_browser.py:1-140`
- Test: `tests/planeta_mcp/test_live_browser.py`

**Interfaces:**
- Consumes: validated Playwright storage state shaped as `dict[str, Any]` with `cookies` and `origins`.
- Produces: `LiveBrowserRuntime.set_storage_state(storage_state: dict[str, Any] | None) -> None`; live startup applies cookies and exact-draft-origin localStorage before `page.goto(draft_url)`.

- [ ] **Step 1: Write a failing startup-order test**

Add lightweight fake Playwright/context/page classes to `tests/planeta_mcp/test_live_browser.py`. The fake context records `add_cookies` and `add_init_script`; the fake page records `goto`. Patch `integrations.planeta_mcp.live_browser.async_playwright` and `asyncio.sleep`, and replace `runtime._spawn` with a no-op coroutine.

Use this literal state:

```python
storage_state = {
    "cookies": [
        {"name": "sid", "value": "saved", "domain": ".planeta.ru", "path": "/"}
    ],
    "origins": [
        {
            "origin": "https://planeta.ru",
            "localStorage": [{"name": "draft-mode", "value": "restored"}],
        },
        {
            "origin": "https://id.planeta.ru",
            "localStorage": [{"name": "foreign", "value": "blocked"}],
        },
    ],
}
```

Construct `LiveBrowserRuntime(data_dir=tmp_path, draft_url=draft_url)`, call
`set_storage_state(storage_state)`, then `await runtime.start()`. Assert the
recorded event kinds are exactly `cookies`, `init_script`, `goto`; the cookie
list equals the literal input; the init script contains `draft-mode` and
`restored` but not `foreign` or `blocked`; and the final navigation target is
the configured draft URL. This test catches missing hydration, hydration after
navigation, and restoration from a different Planeta subdomain.

- [ ] **Step 2: Run the new test and verify RED**

Run:

```bash
/tmp/planeta-live-venv/bin/python -m pytest tests/planeta_mcp/test_live_browser.py::test_live_browser_rehydrates_same_origin_state_before_draft_navigation -q
```

Expected: FAIL because `LiveBrowserRuntime` has no `set_storage_state` and does not call the hydration APIs.

- [ ] **Step 3: Implement minimal runtime hydration**

In `live_browser.py`:

```python
import json
from urllib.parse import urlsplit
```

Store `_storage_state: dict[str, Any] | None`, add:

```python
def set_storage_state(self, storage_state: dict[str, Any] | None) -> None:
    self._storage_state = storage_state
```

Add a small `_serialized_origin(url: str) -> str` helper that lowercases scheme
and hostname and omits default ports 80/443. Add
`async _rehydrate_context(self) -> None` which:

```python
state = self._storage_state
if state is None or self._context is None:
    return
cookies = state.get("cookies", [])
if cookies:
    await self._context.add_cookies(cookies)
if not self.draft_url:
    return
draft_origin = _serialized_origin(self.draft_url)
matching = next(
    (item for item in state.get("origins", [])
     if _serialized_origin(str(item.get("origin", ""))) == draft_origin),
    None,
)
if matching and matching.get("localStorage"):
    payload = json.dumps(
        {"origin": draft_origin, "items": matching["localStorage"]},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    await self._context.add_init_script(
        script=(
            f"const payload={payload};"
            "if(window.location.origin===payload.origin){"
            "for(const item of payload.items){localStorage.setItem(item.name,item.value);}}"
        )
    )
```

Call `await self._rehydrate_context()` after context/page creation and before
the existing `page.goto(draft_url)`.

- [ ] **Step 4: Run runtime tests and verify GREEN**

Run:

```bash
/tmp/planeta-live-venv/bin/python -m pytest tests/planeta_mcp/test_live_browser.py -q
```

Expected: all tests PASS with no warnings.

- [ ] **Step 5: Commit runtime hydration**

```bash
git add integrations/planeta_mcp/live_browser.py tests/planeta_mcp/test_live_browser.py
git commit -m "fix(planeta): rehydrate live browser session"
```

### Task 2: Move the live profile to writable working storage and feed saved state

**Files:**
- Modify: `integrations/planeta_mcp/live_bridge.py:35-100`
- Test: `tests/planeta_mcp/test_live_bridge.py:65-180`

**Interfaces:**
- Consumes: `PlanetaConfig.state_path`, `SessionStore.load_storage_state()`, and `LiveBrowserRuntime.set_storage_state(...)` from Task 1.
- Produces: default live data directory `config.state_path.parent / "planeta-live"`; runtime receives saved state before `start()` while zero-argument `runtime_factory` stays compatible.

- [ ] **Step 1: Replace the old path expectation with a failing writable-path test**

Rename `test_live_bridge_default_runtime_uses_session_dir` to
`test_live_bridge_default_runtime_uses_working_dir`. Preserve distinct
`state_path` and `session_dir`, then assert:

```python
assert runtime.data_dir == state_path.parent / "planeta-live"
assert runtime.profile_dir == state_path.parent / "planeta-live" / "browser-profile"
```

- [ ] **Step 2: Add a failing saved-state-before-start test**

Extend `FakeRuntime` with `_storage_state`, `storage_state_at_start`, and:

```python
def set_storage_state(self, storage_state):
    self._storage_state = storage_state

async def start(self):
    self.started = True
    self.storage_state_at_start = self._storage_state
    return self.page
```

Create a real `SessionStore`, save a literal cookie value `persisted-cookie`,
start a coordinator using the fake runtime, wait for completion, and assert
`runtime.storage_state_at_start["cookies"][0]["value"] == "persisted-cookie"`.
The completed draft flow, rather than a call-count assertion, proves the
coordinator supplied state before runtime startup.

- [ ] **Step 3: Run the two tests and verify RED**

Run:

```bash
/tmp/planeta-live-venv/bin/python -m pytest \
  tests/planeta_mcp/test_live_bridge.py::test_live_bridge_default_runtime_uses_working_dir \
  tests/planeta_mcp/test_live_bridge.py::test_live_bridge_rehydrates_runtime_before_start -q
```

Expected: path test reports `/persistent` instead of `/work/planeta-live`; rehydration test reports `None` instead of the saved cookie.

- [ ] **Step 4: Implement coordinator wiring**

Change the default runtime construction to:

```python
LiveBrowserRuntime(
    data_dir=config.state_path.parent / "planeta-live",
    draft_url=config.draft_url,
)
```

At the beginning of `start()`, before `await runtime.start()`:

```python
storage_state = self.session_store.load_storage_state()
runtime = self._runtime_factory()
set_storage_state = getattr(runtime, "set_storage_state", None)
if set_storage_state is not None:
    set_storage_state(storage_state)
await runtime.start()
```

Do not pass new positional arguments to `runtime_factory`.

- [ ] **Step 5: Run bridge tests and verify GREEN**

Run:

```bash
/tmp/planeta-live-venv/bin/python -m pytest tests/planeta_mcp/test_live_bridge.py -q
```

Expected: all tests PASS; the existing unexpected-origin test still proves no session capture occurs.

- [ ] **Step 6: Commit coordinator rehydration**

```bash
git add integrations/planeta_mcp/live_bridge.py tests/planeta_mcp/test_live_bridge.py
git commit -m "fix(planeta): use writable live browser profile"
```

### Task 3: Preserve successful draft work when session refresh is read-only

**Files:**
- Modify: `integrations/planeta_mcp/live_bridge.py:95-230`
- Test: `tests/planeta_mcp/test_live_bridge.py`

**Interfaces:**
- Consumes: `SessionStore.save_storage_state(storage_state)` and the existing coordinator result dictionary.
- Produces: status keys `session_persisted: bool | None` and `session_persist_reason: str`; `OSError` during atomic save does not block prepare/fill/sync.

- [ ] **Step 1: Add a failing read-only persistence test**

Create `WriteDeniedSessionStore(SessionStore)` in the test module:

```python
class WriteDeniedSessionStore(SessionStore):
    def save_storage_state(self, storage_state):
        raise PermissionError("read-only test volume")
```

Use the normal successful fake runtime/browser flow. Await completion and assert:

```python
assert status["state"] == "draft_ready"
assert status["fill_status"] == "ok"
assert status["sync_status"] == "ok"
assert status["session_persisted"] is False
assert status["session_persist_reason"] == "PermissionError"
assert shared_browser.submit_calls == 0
```

This catches the current bug where the exception changes the session to
`network_error` before campaign preparation.

- [ ] **Step 2: Extend the existing successful-capture test**

In `test_live_bridge_captures_session_fills_syncs_and_never_submits`, assert:

```python
assert status["session_persisted"] is True
assert status["session_persist_reason"] == ""
```

- [ ] **Step 3: Run persistence tests and verify RED**

Run:

```bash
/tmp/planeta-live-venv/bin/python -m pytest \
  tests/planeta_mcp/test_live_bridge.py::test_live_bridge_continues_when_session_refresh_is_read_only \
  tests/planeta_mcp/test_live_bridge.py::test_live_bridge_captures_session_fills_syncs_and_never_submits -q
```

Expected: read-only case ends as `network_error`, and the status keys are absent.

- [ ] **Step 4: Implement bounded persistence reporting**

Initialize each result with:

```python
"session_persisted": None,
"session_persist_reason": "",
```

Return both keys from `status()`. Replace the direct save in the `state == "ok"`
branch with:

```python
try:
    self.session_store.save_storage_state(await runtime.storage_state())
except OSError as exc:
    self._results[token]["session_persisted"] = False
    self._results[token]["session_persist_reason"] = type(exc).__name__
else:
    self._results[token]["session_persisted"] = True
    self._results[token]["session_persist_reason"] = ""
```

Catch only `OSError`; validation, decryption, and programmer errors retain the
existing safe failure behavior.

- [ ] **Step 5: Run bridge and session-store tests and verify GREEN**

Run:

```bash
/tmp/planeta-live-venv/bin/python -m pytest \
  tests/planeta_mcp/test_live_bridge.py \
  tests/planeta_mcp/test_session_store.py -q
```

Expected: all tests PASS; encrypted state remains unreadable as plaintext and atomic store tests remain unchanged.

- [ ] **Step 6: Commit read-only fallback**

```bash
git add integrations/planeta_mcp/live_bridge.py tests/planeta_mcp/test_live_bridge.py
git commit -m "fix(planeta): tolerate read-only session refresh"
```

### Task 4: Document, verify, review, and publish

**Files:**
- Modify: `integrations/planeta_mcp/README.md`
- Modify: `docs/superpowers/specs/2026-08-17-planeta-live-session-rehydration-design.md`
- Create: `docs/superpowers/plans/2026-08-17-planeta-live-session-rehydration.md`

**Interfaces:**
- Consumes: completed runtime/coordinator behavior from Tasks 1-3.
- Produces: operator documentation, green Planeta test suite, buildable Railway image, reviewable branch ready for PR/deployment.

- [ ] **Step 1: Update operator documentation**

In the session-storage section of `integrations/planeta_mcp/README.md`, document
that `PLANETA_SESSION_DIR` stores encrypted authorization, while graphical live
Chromium uses `<PLANETA_STATE_PATH parent>/planeta-live`. State that a read-only
refresh reports `session_persisted=false` without overwriting the old encrypted
file, and that expired platform cookies can still require a real Planeta login.

- [ ] **Step 2: Run formatting and focused verification**

```bash
git diff --check
/tmp/planeta-live-venv/bin/python -m pytest tests/planeta_mcp/test_live_browser.py tests/planeta_mcp/test_live_bridge.py tests/planeta_mcp/test_session_store.py -q
```

Expected: no whitespace errors and all focused tests PASS.

- [ ] **Step 3: Run full Planeta verification**

```bash
/tmp/planeta-live-venv/bin/python -m pytest tests/planeta_mcp -q
/tmp/planeta-live-venv/bin/python -m compileall -q integrations/planeta_mcp tests/planeta_mcp
docker build -f integrations/planeta_mcp/Dockerfile.railway integrations/planeta_mcp
```

Expected: all Planeta tests PASS, compileall exits 0, and Docker build exits 0.

- [ ] **Step 4: Commit documentation and plan alignment**

```bash
git add integrations/planeta_mcp/README.md docs/superpowers/specs/2026-08-17-planeta-live-session-rehydration-design.md docs/superpowers/plans/2026-08-17-planeta-live-session-rehydration.md
git commit -m "docs(planeta): explain live session rehydration"
```

- [ ] **Step 5: Review the complete branch**

Review `git diff <branch-base>...HEAD` for correctness, security boundaries,
unrelated changes, secrets, and any path that could call moderation submission.
Run the final verification commands again after review fixes.

- [ ] **Step 6: Publish and verify v4**

Publish branch `codex/planeta-live-session-rehydration`, open a PR, wait for
`Planeta MCP CI`, merge only when green, and deploy the fresh merged commit to
Railway service `planeta-mcp-v4`. Verify `/health`, invoke live start, confirm
the `/data/planeta/browser-profile` permission error is gone, then run campaign
fill/sync. Stop before any moderation action.
