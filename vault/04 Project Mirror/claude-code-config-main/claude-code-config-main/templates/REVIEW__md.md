---
argos_import: project_file
source_path: claude-code-config-main/claude-code-config-main/templates/REVIEW.md
source_abs: F:\debug\argoss\claude-code-config-main\claude-code-config-main\templates\REVIEW.md
source_ext: .md
source_sha256: 7278012a2a6e5f9f8c93877cd26728a3f4bd39d5ed0195d6027275c004405ede
text_sha256: 7278012a2a6e5f9f8c93877cd26728a3f4bd39d5ed0195d6027275c004405ede
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:27
---

# REVIEW.md

- Source: `claude-code-config-main/claude-code-config-main/templates/REVIEW.md`
- Extract: `text`
- SHA256: `7278012a2a6e5f9f8c93877cd26728a3f4bd39d5ed0195d6027275c004405ede`

## Content

# Code Review Guidelines

This file is read ONLY during code review (not during regular Claude Code sessions).
Drop it into your project root and Claude Code will use it when reviewing PRs.

Source: code.claude.com/docs/en/code-review

---

## Always Check

- [ ] New API endpoints have integration tests
- [ ] DB migrations are backward-compatible (can roll back without data loss)
- [ ] Error messages do not leak internal details (stack traces, file paths, SQL)
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] Environment-specific values come from config, not code
- [ ] New dependencies are justified and not duplicating existing ones

## Security

- [ ] User input is validated at system boundaries
- [ ] SQL queries use parameterized statements, not string interpolation
- [ ] File paths are sanitized (no path traversal: `../../../etc/passwd`)
- [ ] Authentication/authorization checks are present on new endpoints
- [ ] CORS headers are restrictive, not `*`

## Performance

- [ ] No N+1 queries introduced
- [ ] Large collections are paginated
- [ ] Expensive operations have appropriate caching or are async
- [ ] No unbounded loops or recursion on user-controlled input

## Style

- [ ] Code follows existing project conventions (not introducing new patterns)
- [ ] Variable/function names are descriptive (not `data`, `result`, `tmp`)
- [ ] No commented-out code or TODO without a ticket reference
- [ ] Import order follows project convention

## Skip

- Generated files under `src/gen/`, `*.generated.*`
- Formatting-only changes in lock files (`package-lock.json`, `poetry.lock`)
- Auto-generated migration files (check SQL content, not file structure)
- Dependency version bumps without code changes

## Severity Markers

When reviewing, use these markers:

| Marker | Level | Meaning |
|--------|-------|---------|
| :red_circle: | Important | Blocker - must fix before merge |
| :yellow_circle: | Nit | Worth fixing, not blocking |
| :purple_circle: | Pre-existing | Bug predates this PR |

## Bidirectional Check

If this PR makes any of the following outdated, flag it:
- CLAUDE.md
- REVIEW.md (this file)
- AGENTS.md
- README.md
- API documentation

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
