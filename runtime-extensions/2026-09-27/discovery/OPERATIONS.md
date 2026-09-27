# Operation

Install `discovery_cli.py` in the runtime root and modules under `app/src`.
The CLI loads that runtime's private `argos.env` without printing credentials.
Use the Python environment already serving ARGOS.

```sh
python /path/to/runtime/discovery_cli.py refresh --summary
python /path/to/runtime/discovery_cli.py status
python /path/to/runtime/discovery_cli.py resolve argos --kind path
python /path/to/runtime/discovery_cli.py resolve coral --kind api
python /path/to/runtime/discovery_cli.py resolve argos-roach --kind path --machine KNOWN_NODE_ID
python /path/to/runtime/discovery_cli.py sync REPOSITORY_ID
python /path/to/runtime/discovery_cli.py sync REPOSITORY_ID --apply
```

`status` contains a private machine/repository map. Do not publish its output.
The first sync command is a dry run and does not fetch. `--apply` fetches the
explicit branch and rechecks identity, branch, head and cleanliness before merge.
Git ahead/behind metadata from ordinary refresh refers to locally stored tracking
refs; only a successful sync reports `remote_ref_verified=true`.

The existing bearer-authenticated ARGOS application exposes:

| Method | Path | Result |
|---|---|---|
| GET | `/api/discovery` | Current private map |
| POST | `/api/discovery/refresh` | Bounded local/known-remote refresh and fact replacement |
| GET | `/api/discovery/resolve/path/NAME` | Verified existing local project directory |
| GET | `/api/discovery/resolve/api/NAME` | Verified API URL |
| GET | `/api/discovery/resolve/api/NAME?machine_id=ID` | API on that specific verified machine |
| POST | `/api/discovery/repositories/ID/sync` | Dry run for known local repository |
| POST | `/api/discovery/repositories/ID/sync?apply=true` | Safe fetch/fast-forward |

Missing/expired resources and sync conflicts return 409. Unknown repository IDs
return 404. No caller-supplied arbitrary URL, host or filesystem path is probed.
Unauthenticated access is rejected by the application's existing middleware.

Use a user oneshot service with `WorkingDirectory=/path/to/runtime/app`,
`EnvironmentFile=/path/to/runtime/argos.env`, `UMask=0077`, `TimeoutStartSec=90`
and `ExecStart=/path/to/python /path/to/runtime/discovery_cli.py refresh --summary`.
Attach a timer with `OnBootSec=2min`, `OnUnitActiveSec=5min`,
`RandomizedDelaySec=20` and `WantedBy=timers.target`. Enable the timer only after
the initial oneshot completes successfully. Check `Result=success`, timer
`active/enabled`, and the authenticated resolve/memory endpoints.

Configuration is private. `ARGOS_DISCOVERY_CONFIG` optionally selects a JSON
file with `runtime_root`, `node_id_file`, `projects` (name to candidate paths),
`repository_roots` and `terminal_inventory`. The default is
`/etc/argos/discovery.json`. `ARGOS_RUNTIME_ROOT` locates the runtime;
`ARGOS_TERMINAL_INVENTORY` locates its existing SSH transport inventory;
`ARGOS_STATE_ROOT` locates state. `ARGOS_DISCOVERY_REGISTRY` overrides the registry
file. `ARGOS_PROJECT_NAME` supplies an explicit candidate for a named project.

Known API candidates use `ARGOS_API_URL`, `OLLAMA_HOST`, `ARGOS_HA_URL`, and
`ARGOS_CORAL_URL`. The API probe validates the actual protocol (ARGOS readiness,
Ollama model-list shape, authenticated HA API response, signed Coral status).
It uses bounded timeouts and response sizes. Listening ports alone do not mean a
working API. An unavailable remote Ollama endpoint remains unavailable and is
never silently replaced by the local provider.

The registry is atomically replaced with mode 0600; refresh is serialized by a
file lock. After 15 minutes without verification, resources are stale. Memory
rendering applies this age rule to machines, APIs, paths and repositories. A
single reserved `runtime_discovery` fact is transactionally replaced in the
separate new-facts store (`ARGOS_MEMPALACE_FACTS_PATH`); restored archives stay
unchanged. Consumers render current state rather than trusting an old serialized
discovery fact. Historical references are labelled unverified, not rewritten
into unsupported path mappings.
