# ARGOS runtime discovery extension — 2026-09-27

This is a versioned extension for the running ARGOS Python service. It does not
replace the repository's older `src` tree. The package contains portable discovery
modules, the exact generic transport/auth/fact-store dependencies used by their
tests, and integration instructions. No machine inventory, registry, credential,
environment file, restored memory, or production database is included.

The registry separates stable node identity from changing addresses. It records
verified project paths, API protocol health, Git remote/branch/head/dirty state,
provenance and verification timestamps. Local candidates come from the runtime,
known local account homes, bounded repository roots and known service working
directories. Existing valid project overrides have priority.

Run the isolated tests:

```sh
python -m pip install fastapi python-dotenv pytest httpx
python -m pytest -q
```

Read [INTEGRATION.md](INTEGRATION.md) before installation and
[OPERATIONS.md](OPERATIONS.md) for CLI/API/timer use. `SHA256SUMS.json` records this
public package's file hashes. Production deployment additionally used source hash
guards, private source backups, an empty command queue and live API/memory checks.

This extension does not scan unknown hosts. Remote discovery requires an existing
SSH inventory, a pinned host key and matching stable node UUID. It can try the
configured address, last verified address, DNS for the known hostname, then a
bounded number of previously observed interfaces. If none works, the node stays
unavailable. DNS by itself never establishes machine identity.

Refresh does not synchronize repositories. Manual synchronization fetches only
the configured matching branch and fast-forwards a clean worktree. It rejects a
changed registry repository identity, detached/mismatched branch, dirty worktree,
divergence or local commits ahead of the remote. It never resets, stashes, pushes,
force-updates a tracking ref or discards changes. A missing narrow fetch refspec
may be added for the already configured tracking branch after the checks pass.
