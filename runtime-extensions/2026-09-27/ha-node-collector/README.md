# Verified Coral status in the Home Assistant node collector

The old node collector still queried a fixed legacy P2P endpoint and reported
`not_configured`, while the current signed accelerator API was available. This
patch routes Coral diagnostics through the current verified registry and the
existing bounded `network_coral.CoralClient.status()` implementation.

The live repair was installed with source hash guards and backups. Only
`argos-ha-nodes.service` was restarted. Existing node/discovery identities and
the X230 probe remain unchanged; `publisher.py` is byte-identical. No inference,
device commands, HA service calls, ACL changes or synthetic MQTT states were
performed. The collector's actual received messages were inspected read-only.

## Truthful scope and fail-closed behavior

The Coral device label now says accelerator API. Its readiness diagnostic says
**Signed status ready**, with HA/MQTT attributes:

```json
{"status_source":"coral_accelerator_api","readiness_scope":"signed_status","inference_verified":false,"authenticated":true}
```

The value means a successful authenticated `GET /v1/status`, not legacy P2P
readiness or newly tested TPU inference. Uptime is the accelerator API process
uptime (`uptime_s`), not host uptime. Model metadata and historical calls do not
authorize an inference-success claim.

The registry machine identity must match the existing diagnostic identity and
carry the Coral role. Both machine and API entries must be available and fresh
under the existing registry's 900-second TTL. Their status and URL are checked
again after the response; invalidation or address changes discard the result.
There is no old-address fallback. Missing configuration yields `not_configured`,
invalid/stale registry evidence yields `stale`, malformed returned data yields
`invalid_response`, and the existing client's combined transport/auth/HTTP
failure yields `service_unavailable`. Only an actual propagated `TimeoutError`
is classified as `timeout`; exception text and private addresses are not emitted.

The existing client performs response HMAC verification, strict JSON/schema
validation, a 3-second global network deadline and a 1 MiB response cap. It does
not use proxies, redirects or retries. The adapter calls only `status()`.

MQTT still polls every 20 seconds, rejects results older than 60 seconds or from
a previous connection generation, and starts/reconnects offline. HA entities
retain their 90-second expiry and require bridge, source and field availability.
The bridge last will remains unchanged. Negative freshness/HMAC cases use test
fixtures; the real service was not stopped to manufacture failure evidence.

## Configuration

The collector remains standalone. It loads only the trusted registry and Coral
transport source files, without initializing the core `src` package. It reads
three allowlisted settings from the runtime's existing `argos.env` or explicit
environment overrides: `ARGOS_CORAL_SECRET_FILE`, `ARGOS_STATE_ROOT`, and
`ARGOS_DISCOVERY_REGISTRY`. Configuration values are not published and process
environment is not mutated. No full `EnvironmentFile` was added to the unit.

The normal runtime root is derived from `integrations/ha_nodes`; staging can set
`ARGOS_NODE_RUNTIME_ROOT` or pass a test root. The private key must be an owned
regular file with restrictive permissions; symlinks, FIFOs and weak keys are
rejected. Runtime modules/configuration must be root-owned and not group/world
writable. The live collector interpreter already had `python-dotenv` and Paho.

## Actual evidence

`evidence/live-chain-proof.json` contains sanitized aliases for the eight owned
diagnostic sensors, not a household entity inventory. The final chain measured:

- Signed GET uptime before: **87,626 s**.
- Fresh, non-retained MQTT state: **87,631 s**.
- HA uptime sensor: **87,631 s**.
- Signed GET after: **87,631 s**.

A real retained Coral state was also received. Coral connectivity/readiness were
on, role was accelerator, and signed-status source attributes reached HA. X230
connectivity/readiness stayed on, and a separate actual ARGOS `/health` probe
confirmed readiness. Source hashes and the deployment receipt accompany proof.

Measured HA totals after the fix were **91 entities: 49 available, 26 unavailable,
16 unknown**. Those are aggregate observations, not claims that this repair
addresses other devices. The four Coral diagnostics recovered independently.

The original faulty `main.observe()` was reproduced calling legacy P2P in RED.
Then 69 new/existing tests passed, with existing tests copied next to the actual
candidate sources. Independent review found no material defects and added three
real-HMAC/expiry integration cases: **72 checks** in the complete local suite.
The self-contained public suite contains the 25 new tests plus those three
independent integration cases. Historical/source literals in the patch are
retained so it applies exactly; no credentials or private inventories are bundled.

## Apply and verify

`patch.diff` applies relative to the ARGOS runtime repository root:

```bash
git apply --check /path/to/patch.diff
git apply /path/to/patch.diff
```

For an existing installation, first compare live source hashes to the deployment
receipt and retain backups; do not overwrite concurrent edits. Verify a fresh
signed GET and restart only the collector service. The actual installation used
those guards; its private transport/deployment helpers are not in this bundle.

Portable tests from this bundle directory:

```bash
python -m pip install -r requirements-test.txt
python -m pytest -q
```

Trusted-file ownership tests assume the root service account, as in the deployed
unit. `reference/` freezes the existing transport/registry sources used as
evidence; the patch does not replace those core modules. `MANIFEST.json` records
every bundled file hash. Full core/runtime and Home Assistant deployments are
outside this patch.
