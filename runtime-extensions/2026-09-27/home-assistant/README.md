# Home Assistant ↔ ARGOS

The ARGOS **Дом** tab reads actual Home Assistant states, with search, domain and availability filters, refresh timestamps, and links to HA. Unknown and unavailable readings remain separate from off/zero. The authenticated `/api/ha` response includes only selected metadata; tokens, camera URLs, location attributes and arbitrary attributes are not returned.

The HA dashboard generator builds a separate **ARGOS · Дом** dashboard from the current entity catalog. Electricity, node telemetry, lights/switches, climate and ARGOS automations use `simple-entity` rows with all interaction actions disabled. It preserves existing dashboards. No devices are created or toggled.

The transport reads the current runtime registry on each request. The legacy `HomeAssistantBridge` now also follows verified URL changes without reconstructing its instance. Once the registry exists, stale addresses cannot silently fall back to a hardcoded endpoint.

Power units preserve W versus VA; kW/kVA are scaled to their matching units. Climate temperature units come from HA `/api/config`. Missing/invalid units are labeled unconfirmed, and nonnumeric/nonfinite temperatures are not shown as measurements. A newer HA request supersedes older responses, including errors; a delayed response cannot restore stale data after an offline result or logout.

## Contents and installation

- `runtime-ha.patch`: four source changes relative to the previously deployed ARGOS runtime. `manifest.json` records baseline and final SHA-256 values. Apply only to matching source, preserving any concurrent changes.
- `candidate/src/ha_dashboard.py` and `candidate/src/interface/control_panel.html`: the final generic snapshot module and panel for inspection/tests.
- `dashboard_builder.py`: pure generator; takes actual HA REST state objects. It emits no invented device IDs. `BRIDGE_HTML` provides a same-host LAN link to HTTP port 8080; the hostname follows the browser URL. This static bridge does **not** discover the port or provide external proxy routing.
- `tests`: synthetic unit and Chromium browser regressions. No household data or credentials are included.
- `proof.json`: sanitized live verification result. Screenshots and household inventory remain private.

Check/apply the patch from the intended ARGOS application root, then restart ARGOS only when the task queue is idle. Keep the existing bearer-auth middleware for `/api/ha`. Runtime dependencies are the application's existing `requests` and FastAPI packages; browser tests use pytest, Playwright and an existing Chromium.

```sh
git apply --check /path/to/runtime-ha.patch
git apply /path/to/runtime-ha.patch
ARGOS_PANEL_HTML=/path/to/bundle/candidate/src/interface/control_panel.html \
ARGOS_RUNTIME_SOURCE=/path/to/patched/argos \
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python -m pytest /path/to/bundle/tests -q -p no:cacheprovider
```

`ARGOS_RUNTIME_SOURCE` enables the bridge integration test against the patched runtime. Without it, only that test is explicitly skipped. The other tests run against the supplied snapshot/panel. Set `ARGOS_CHROMIUM` if the browser executable is not named `chromium`.

To install the native dashboard, use the authenticated HA WebSocket API to create a new `argos-home` storage dashboard and save `dashboard_builder.build(states)` as its configuration. Refuse to overwrite an existing dashboard at that path. Save the existing dashboard list/configurations and verify them after creation. Write `BRIDGE_HTML` to the HA config's `www/argos.html` only if it does not already exist. When `www` did not exist at HA startup, one administrative HA restart is required before `/local/argos.html` is served. Inspect startup automations before any restart.

## Verified behavior

Live ARGOS and HA APIs agreed on 91 entity IDs and state counts. At the recorded check: 45 available, 30 unavailable, 16 unknown. The native dashboard displayed 52 existing entities in 6 cards. API authentication, search/filter/refresh, unavailable rendering, logout, the HA→ARGOS link and desktop/mobile layouts passed. Native entity cards exposed zero switches/sliders/select controls; the browser made zero device-service calls. The deployment used one administrative container restart of HA to activate its static directory.

Unavailable telemetry is not a claim that all devices were repaired. At inventory time, 26 Tuya entities were unavailable; their physical cause was not established. Four old MQTT Coral status entities had a separate collector configuration problem. That collector is an independent follow-up and does not alter this snapshot evidence. Other unknown states include scene and backup metadata, which do not by themselves prove a disconnected device.

Follow-up read-only [Tuya diagnostics](tuya-diagnosis-aggregate.json) confirmed that the integration is loaded and cloud MQTT connected. The cloud reports 12 of 14 devices offline; all 26 unavailable entities belong to those offline devices. The other two devices account for 14 available entities. This does not indicate HA authentication/setup failure; the physical cause of the device outages is still unknown. Check those devices and their hub in the Tuya app, power and network before considering any reconfiguration. No pairing, reset, reauthentication or device action was performed.

The separate [node collector repair](../ha-node-collector/README.md) subsequently restored the four Coral diagnostics using the verified signed accelerator API. Its live API→MQTT→HA check measured **49 available, 26 unavailable and 16 unknown out of 91 entities**. The original dashboard proof above remains the unmodified earlier observation.

## Rollback

1. Check current source hashes against `manifest.json`; restore the saved source copies (or reverse this patch only when its hunks still match), remove only the newly introduced snapshot module, then restart ARGOS at an idle queue.
2. In HA Settings → Dashboards, remove only the newly created `ARGOS · Дом` dashboard. Existing dashboards and device/entity registrations were never changed. Keep the saved pre-deployment configurations for comparison.
3. Remove only the bridge file whose SHA matches the deployment receipt. Do not remove other `www` content. No device states or history need restoration.

Actual rollback was not executed because the verified implementation remains active. Hash-guarded private backups exist on the deployment machine.

References: [HA read-only entity rows](https://www.home-assistant.io/dashboards/entities/), [HA dashboard actions](https://www.home-assistant.io/dashboards/actions/).
