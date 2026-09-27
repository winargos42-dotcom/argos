# ARGOS panel: current provenance and session-safe HA status

This bounded patch fixes the existing control panel. It labels discovery results as the current system map, omits nonexistent fact IDs, and ties Home Assistant status and its link to the current authenticated browser session. Logged-out pages do not poll the authenticated HA endpoint. Logout clears the link immediately; late success and 401 responses from an old session cannot restore the link or terminate a newer login. A current-session 401 still logs out.

## Apply

Use a compatible ARGOS runtime with `src/interface/control_panel.html` and the existing `/api/status`, `/api/tasks`, `/api/memory/search`, and `/api/ha` contracts. The patch includes no server changes. Check the baseline SHA-256 in `manifest.json`, inspect `panel-ui.patch`, and apply it relative to that runtime root. Refuse application if the baseline differs until the change is reviewed against that version. The runtime reads the HTML for each `/ui` request, so this HTML change does not require restarting the core.

## Test

Requirements: Python, pytest, Playwright Python, and an already installed Chromium. No browser installation, real credentials, network services, hardware, messaging, or training is used by these six rendered tests. Every browser route is intercepted with fixture data.

```sh
ARGOS_PANEL_HTML=/path/to/runtime/src/interface/control_panel.html \
ARGOS_CHROMIUM=/usr/bin/chromium \
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python -m pytest tests/test_panel_ui.py -q -p no:cacheprovider
```

Without a compatible HTML file, Playwright, or Chromium, the tests skip explicitly; skipping is not passing validation. Tests cover current-map provenance, no unauthenticated HA polling, immediate logout cleanup, late-success isolation, old-401/new-login isolation, and current-401 logout. Five bug reproductions were red before their respective fixes; the patched HTML passed all six tests.

The package contains the generic patch and mocked tests only. Live authentication helpers, runtime environment files, browser receipts, screenshots, and machine inventories are deliberately excluded.
