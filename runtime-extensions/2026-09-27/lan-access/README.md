# ARGOS restricted LAN access

The existing application remains on IPv4 loopback port 8080. A native
systemd-socket-proxyd relay exposes that same application on port 8081 of one
explicitly trusted LAN interface. It does not initialize a second ARGOS instance,
change bearer authentication, configure a public tunnel or modify router NAT.

The socket accepts only the configured trusted subnet through BindToDevice and
systemd IPAddressDeny/Allow. The relay service can connect only to localhost.
Before starting, lan_bpf_check verifies that the socket cgroup has directly
attached ingress and egress filters (ancestor filters do not satisfy it). This
proves filter presence, not filter policy. The separate native allow/deny test
proves that an allowed source passes and the same disallowed source that passes
an unfiltered control cannot pass the filtered relay. Both checks are required
on the destination host. Native connection count is bounded to 64.

`candidate/lan_discovery.py` reads private `/etc/argos/lan-access.json`, selects
only a current IPv4 address on the named interface within the trusted RFC1918
subnet, and makes an interface-bound, size/deadline-bounded GET /health. Only
literal `ok: true` and `ready: true` mark `argos_lan` available. Address changes
within that trusted network are picked up by the existing refresh timer; moving
to a different network requires a deliberate policy update. No old address or
open-port fallback marks an endpoint available. Existing registry TTL applies.

The HA bridge selects port 8080 for localhost/127.0.0.1 and normalizes ::1 to the
IPv4 backend. Other hostnames use LAN port 8081. Actual served links, not an
assumed external proxy route, must be checked after installation.

## Installation into an existing reviewed runtime

1. Preserve private source backups and compare hashes before every replacement.
   Copy `candidate/lan_discovery.py` to app/src and apply runtime-discovery.patch
   to the matching runtime_discovery source. Keep all other runtime changes.
2. Render units/argos-lan.socket.in and lan-access.json.in with an explicit
   trusted interface/subnet. The placeholders deliberately do not contain a
   machine inventory. Install policy mode0600 and units mode0644. Install the BPF
   guard as `/usr/local/libexec/argos/lan_bpf_check.py` and the service under
   `/etc/systemd/system`. Check port8081 is free and systemd validates both units.
3. Run `sudo python preflight_native.py` to complete the native allow/deny
   preflight before enabling argos-lan.socket. It creates only temporary localhost
   units, removes them in a finally block, and records the tested guard SHA/time.
   Keep rollback limited to these new units/files; do not overwrite later edits.
4. Update active HA dashboard_builder sources with ha-bridge-port.patch, write
   BRIDGE_HTML to the existing HA config www/argos.html under a hash guard, and
   replace its active package README with home-assistant-README.md. Do not change
   HA dashboards, entities, devices, tokens or historical proof files.
5. At an idle task queue, restart the existing core once so authenticated manual
   discovery refresh uses the new function. Require /health readiness. Run a
   manual refresh and confirm argos_lan in resolver and current memory, then let
   the existing discovery timer continue periodic verification.

The checked source hashes are in REVIEWED_SOURCE_HASHES.json. They identify the
actual reviewed snapshot; the public socket template substitutes private policy
values. SHA256SUMS.json identifies this portable public bundle. Neither contains
credentials, a machine inventory, private deployed policy or raw entity data.

## Verification and routing limits

Run `PYTHONDONTWRITEBYTECODE=1 ARGOS_RUNTIME_SOURCE=/path/to/runtime/app python -m pytest tests -q -p no:cacheprovider` with
pytest, Playwright, an existing Chromium, and the runtime's ASGI dependencies.
Without ARGOS_RUNTIME_SOURCE, only the four explicit runtime integration cases
are skipped. Fixtures use synthetic identities/addresses and never mutate
hardware. Browser fixture cases cover localhost, IPv4/IPv6 loopback and LAN names.

Verify from a different known LAN machine: /ui and /health return200, protected
API requests without a key return401. Keep the valid key on its original machine;
check authenticated access using an interface-bound local request. Unauthorized
POST /api/tasks with an empty body must return401 before validation/handler and
must not create a job. Preserve 127.0.0.1:8080 access.

The recorded deployment also accepted an ordinary self-connection to its LAN
address. A real desktop browser followed the served LAN HA bridge to ARGOS,
authenticated, rendered the Home tab, verified the HA return link and logged out.
The localhost route passed the same checks on a mobile viewport. On hosts where
self-LAN routing is excluded by BindToDevice, retain the policy and use localhost
on that host; do not weaken the ACL to make a browser check pass.

## Recorded live acceptance

Root executed the deployment and the post-restart verification scripts. The
sanitized evidence under `evidence/` records:

- `activation.json`: native socket active, existing core ready, and zero active
  jobs immediately before the one core restart.
- `live.json`: authenticated manual discovery refresh retained a fresh
  `argos_lan` entry, its resolver and current memory; all ten installed file
  hashes matched. Localhost and interface-bound LAN public GETs returned 200,
  protected GETs and unauthorized POSTs returned 401, and authenticated HA GETs
  returned 200. The job count did not change. The installed direct BPF guard and
  both native units passed.
- `peer.json`: a separate known Coral machine reached LAN /ui and /health with
  200 responses, while no-token and wrong-token protected requests returned 401.
  The valid bearer remained on X230. Fresh registry verification and the
  installed BPF guard SHA were checked independently.
- `browser.json`: actual localhost mobile and LAN desktop authenticated browser
  paths passed, both served bridge links selected the correct port, HA return
  links matched the browser origin, logout cleared the links, and neither
  viewport overflowed. No browser errors occurred.

These are protocol, authentication and navigation checks. They do not claim to
repair unavailable physical devices or change any device state. Native allow/deny
policy evidence remains in `native-preflight.json`; portable test evidence is in
`test-proof.json`.

Rollback: stop/disable only argos-lan.socket, stop argos-lan.service, restore
matching backed-up sources/bridge/policy, remove only unchanged new files, reload
systemd and restart the existing core at an idle queue. No router, firewall table,
cloud tunnel, second core or HA restart is needed.
