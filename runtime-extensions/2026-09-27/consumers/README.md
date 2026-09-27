# Verified runtime consumers addendum — 2026-09-27

Two active skills previously read `ARGOS_HA_URL` directly, bypassing the verified
registry. `ha-consumers.patch` connects camera inventory/snapshots and lighting
requests to `api_url('home_assistant', ...)` on every request. An unavailable map
blocks the old URL. Camera transport failure now reports unavailable inventory,
rather than falsely reporting that Home Assistant has no cameras.

Apply the patch only to matching source versions after source-hash guards and a
private backup. It depends on the discovery extension's `runtime_registry.py`.
The original public discovery package is unchanged. Restart the importing core
only with an idle task queue and then use GET-only status checks.

Run the supplied tests against an isolated copy of the current runtime modules:

```sh
PYTHONPATH=/path/to/isolated/app python -m pytest tests -q
```

All tests replace HTTP transport. They verify changed endpoint routing,
unavailable-map rejection without old-address requests, and honest camera
transport errors. Production verification used only HA `/api/states` reads;
no camera frames, Coral inference, light switching or calibration were performed.

The bounded audit also identified absent legacy SNN inference artifacts on the
known remote machine. Existing trained weights alone do not establish compatible
inference tooling; no unverified path alias or model substitution was introduced.

`budding-unavailable.patch` removes the invented claim that a missing legacy
checkpoint means training is still running or will finish at a fixed step. Its
read-only preflight reports the specific missing checkpoint/entrypoint/config/
Python/service. An incomplete reply is unavailable. Even files being present do
not establish checkpoint/entrypoint compatibility; this unverified legacy path
does not launch an inference job. This does not disable or modify the separate
SNN worker integration.

`network-verified-ip.patch` prevents an old P2P row from overwriting the verified
Coral address in panel metadata and connection requests. If the current registry
marks that address unavailable, there is no fallback to a stale row or fixed IP.
The previously deployed execution-status contract remains unchanged.

`network-handler-binding.patch` fixes generic skill adapters that accept
`handle(text, core)`: the adapter now preserves the bound core. Signature binding
chooses the supported call shape before invocation. An exception inside the
handler is reported once, with no retry and no chat fallback. Explicit execution
status remains authoritative.

Apply patches in this order: `ha-consumers.patch`, `budding-unavailable.patch`,
`network-verified-ip.patch`, `network-handler-binding.patch`. The last two change
the same file in sequence. `DEPLOYED_HASH_CHAIN.json` records exact before/after
source hashes for all three guarded live installation phases. The runtime files
were backed up privately before every change; backups and deployment configuration
are deliberately excluded. Reconstruct the final code by applying these patches
to sources matching the initial hashes, after installing the discovery extension.
This is a versioned runtime extension, not a claim that an older repository's
entire source tree matches the deployed runtime.

Verification: 14 supplied regression cases cover HA routing/error truth, legacy
SNN unavailability, changed/offline node addresses, and two-argument dispatch
including an internal TypeError. The focused runtime/API/execution-truth suite
passed 52 checks before the additional standalone error-path regression was added.
A final complete isolated audit run was **77 passed, 3 failed**. Those three
unchanged historical assertions are recorded below; the complete run is not
reported as green. A fourth failure in the original baseline was the real
missing-core bug and now passes, alongside the new regressions.

| Historical assertion | Expected | Actual current contract | Reason retained as a documented mismatch |
| --- | --- | --- | --- |
| `test_single_argument_handler_and_generic_claim_remains_unverified` | Explicit `succeeded` becomes `unverified` | Explicit `succeeded` is preserved | The accepted execution-truth contract gives explicit status priority; generic prose still cannot prove success. |
| `test_unhandled_or_error_is_failed[None]` | `failed` | Selected-skill help with `unverified` | A nonmatching command returns the selected skill's usage hint, without claiming execution. |
| `test_unhandled_or_error_is_failed[False]` | `failed` | Selected-skill help with `unverified` | Same explicit hint contract as `None`; actual error results still fail. |

Production checks after the final restart verified all four deployed source
hashes, current node address resolution and HA GET-only reads (91 entities,
zero camera entities at observation time). Legacy SNN preflight returned explicit
unavailable. No physical actions, inference launches or external messages were
performed. A separate panel reviewer completed 13 read-only skill status probes;
GA4 reported unconfigured and the absent HA camera inventory was explicit.

Operational limits remain real: this addendum does not create a compatible legacy
SNN inference entrypoint, provision cameras or configure GA4. Existing training
weights must not be substituted for an unverified inference role.
