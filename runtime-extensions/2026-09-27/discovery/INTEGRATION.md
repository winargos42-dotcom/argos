# Integrating into an existing runtime

The files in `app/src` are a versioned extension snapshot. Inspect the target
runtime first; do not replace an unrelated historical checkout's whole `src`
directory. `memory_index.py`, `network_coral.py` and `cloud_auth.py` are generic
dependencies bundled for reproducible tests. An existing runtime may already
have them; merge their narrow integration points instead of blindly overwriting
newer code.

1. Record SHA-256 hashes of each target source. Keep a private source backup.
   Verify those hashes again immediately before replacing files. Compile the
   staged Python sources and run the supplied tests before deployment.
2. Add `runtime_registry.py`, `runtime_discovery.py`, `discovery_api.py` and the
   runtime-root CLI. Mount `create_discovery_router()` before any catch-all ASGI
   mount, under the existing bearer-auth middleware. Never mount it unauthenticated.
3. Add `memory_index.replace_source_fact`. It permits only the reserved
   `runtime_discovery` source and only the separate writable fact store. Publish
   one current map; do not modify restored historical databases.
4. In memory search, remove serialized `runtime_discovery` hits, render
   `memory_context(query)` from the current registry, and place it first for
   infrastructure queries or when a serialized map hit was found. Mark remaining
   historical infrastructure hits `historical_unverified`. Keep this current-map
   priority when combining core facts with the search results. Add the current
   map to the prompt context instead of fixed IP assertions.
5. Resolve Home Assistant and Coral endpoints using `api_url`. Resolve remote
   Ollama with `remote_api_url('coral', 'ollama', configured_url)` so an offline
   remote API never selects the local provider. Resolve project directories with
   `resolve_path`; do not reuse a missing/stale path when a registry exists.
6. Long-lived clients must resolve on each operation. The bundled Coral client
   demonstrates configured offline-to-online recovery without sending requests
   to an unverified old URL. Panel file/backups actions should resolve their
   directory on each request, including availability checks.
7. Use `machine_host` and `ssh_command` for known-machine SSH consumers. For the
   existing finite network terminal, preserve its strict inventory validation and
   verified remote UUID check; update its target host from the fresh registry,
   pin `HostKeyAlias` to the existing trusted host identity, and include the
   resolved host in its catalog revision. An unavailable remote entry must not
   disable an otherwise valid local terminal.
8. Generate the first registry/fact via the oneshot service, then enable the
   timer. Check the live queue for queued/running/cancelling tasks before
   restarting only the core process that imports changed modules. Verify health,
   authenticated API, missing-resource 409, memory priority, exactly one current
   fact after repeat refresh, and read-only HA/signed Coral status.

All source replacements need guards against concurrent runtime edits. A rollback
must restore only files whose current hash still matches this deployment, and
must not overwrite another process's later edits. Keep source backups and machine
registries private; publish only generic code, tests and these instructions.

Current limits: Linux/systemd and Git are expected. Project and protocol
candidates are intentionally bounded; unknown hosts or protocols require an
explicit trusted inventory/configuration update. Manual repository sync applies
to known local checkouts. Remote repository metadata is read over verified SSH;
remote working trees are never mutated by automatic refresh. Missing DNS and
unreachable pinned SSH lead to `unavailable`, not broad subnet scans.
