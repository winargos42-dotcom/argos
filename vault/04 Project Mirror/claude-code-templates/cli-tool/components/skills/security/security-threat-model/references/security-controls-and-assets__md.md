---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/security/security-threat-model/references/security-controls-and-assets.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\security\security-threat-model\references\security-controls-and-assets.md
source_ext: .md
source_sha256: 7edce42cefb303056801ecfb4d5319b1df089c6e84d05c320857f4ff22cd1668
text_sha256: d536cfa9acad2523dc39134bcf33b9566c29dd9a57b407cbc9901637230c6b98
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:52
---

# security-controls-and-assets.md

- Source: `claude-code-templates/cli-tool/components/skills/security/security-threat-model/references/security-controls-and-assets.md`
- Extract: `text`
- SHA256: `7edce42cefb303056801ecfb4d5319b1df089c6e84d05c320857f4ff22cd1668`

## Content

# Security Controls and Asset Categories

Use this as a lightweight checklist to keep outputs consistent across teams. Prefer concrete, system-specific items over generic text.

## Asset categories (pick only what applies)
- User data (PII, content, uploads)
- Authentication artifacts (passwords, tokens, sessions, cookies)
- Authorization state (roles, policies, ACLs)
- Secrets and keys (API keys, signing keys, encryption keys)
- Configuration and feature flags
- Models and weights (if ML systems)
- Source code and build artifacts
- Audit logs and telemetry
- Availability-critical resources (queues, caches, rate limits, compute budgets)
- Tenant isolation boundaries and metadata

## Security control categories
- Identity and access: authN, authZ, session handling, mTLS, key rotation
- Input protection: schema validation, parsing hardening, upload scanning, sandboxing
- Network safeguards: TLS, network policies, WAF, rate limiting, DoS controls
- Data protection: encryption at rest/in transit, tokenization, redaction
- Isolation: process sandboxing, container boundaries, tenant isolation, seccomp
- Observability: audit logs, alerting, anomaly detection, tamper resistance
- Supply chain: dependency pinning, SBOMs, provenance, signing
- Change control: CI checks, deployment approvals, config guardrails

## Mitigation phrasing patterns
- "Enforce schema at <boundary> for <payload> before <component>."
- "Require authZ check for <action> on <resource> in <service>."
- "Isolate <parser/component> in a sandbox with <resource limits>."
- "Rate limit <endpoint> by <key> and apply burst caps."
- "Encrypt <data> at rest using <key management> and rotate <keys>."

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Training Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Training Hub]]
