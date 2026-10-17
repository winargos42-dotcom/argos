# ARGOS — Start here / С чего начать

[Main README](../README.md) · [Contributing](../CONTRIBUTING.md) · [Security](../SECURITY.md) · [Roadmap](../ROADMAP_2026_2027.md)

ARGOS Universal OS is an **experimental distributed AI/agent framework**,
not a finished operating system or a security-audited production package.

## Map of the project

| Area | Where to look | Validation boundary |
|---|---|---|
| Agent runtime and integrations | `src/`, `integrations/` | Different modules have different maturity levels |
| Automated checks | `.github/workflows/`, `tests/` | A green workflow validates only the steps it ran |
| MUKHTAR / biomimetic experiments | `experimental/` | Experimental; rely on linked artifacts for measured results |
| FPGA / Edge AI interfaces | `drivers/`, `src/connectivity/` | Simulated PCIe tests are **not** proof of physical GTI inference |
| Deployment and operations | `docker-compose*.yml`, `docs/` | Review scripts and configuration before deploying |

## Safe initial review

1. Read the main README and the relevant module's documentation.
2. Inspect scripts and dependencies before executing them.
3. For Python work, use a **new isolated virtual environment**, not the
   `venv/` or `.venv/` snapshots included in some historical commits.
4. Start with focused, non-hardware unit tests from `tests/`.
5. Do not connect real devices, production accounts, or secrets until the
   specific integration has been reviewed.

## What a CI result means

GitHub Actions checks are useful regression evidence for the tested files
and synthetic fixtures. A successful CI check does not prove that a real
FPGA, Coral TPU, robot, CAN device, or cloud deployment was exercised.
Record exact command, commit SHA, hardware, dataset and logs for physical
results.

## Security

The tracked-file secret check can catch PEM private-key headers, selected
credential-file paths and Google service-account JSON, but is not a full
history scan. See [SECURITY.md](../SECURITY.md).
