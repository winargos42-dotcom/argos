---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/test-detect/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\test-detect\SKILL.md
source_ext: .md
source_sha256: 804ce9497216c733ae8926c70611be52ea9f83e6c3675d3c71b7fd735c471d16
text_sha256: 6611c3d6acf8843511bb27a4be9fe22c6f8aee550b7b1e5b650c0af8cac67cc0
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/development/test-detect/SKILL.md`
- Extract: `text`
- SHA256: `804ce9497216c733ae8926c70611be52ea9f83e6c3675d3c71b7fd735c471d16`

## Content

---
name: test-detect
description: Auto-detect testing framework and run relevant tests. Identifies Jest, Vitest, Playwright, Cypress, pytest, Go test, and others. Can run all tests, specific file tests, or generate basic tests for new code. Usage - /test-detect, /test-detect src/auth/login.ts, /test-detect generate src/utils.ts
---

# Test Detect

Automatically detect the testing framework in the current project and run the right tests.

## Workflow

### Step 1: Detect the testing framework

Check for these files in order (first match wins):

| Check | Framework | Run Command |
|-------|-----------|-------------|
| `vitest.config.*` exists OR `vitest` in devDeps | **Vitest** | `npx vitest run` |
| `jest.config.*` exists OR `jest` in devDeps | **Jest** | `npx jest` |
| `playwright.config.*` exists | **Playwright** | `npx playwright test` |
| `cypress.config.*` exists | **Cypress** | `npx cypress run` |
| `pytest.ini` or `conftest.py` or `pyproject.toml` with `[tool.pytest]` | **pytest** | `python -m pytest` |
| `go.mod` exists | **Go test** | `go test ./...` |
| `Cargo.toml` exists | **Rust/cargo** | `cargo test` |
| `mix.exs` exists | **ExUnit** | `mix test` |
| `Gemfile` with `rspec` | **RSpec** | `bundle exec rspec` |
| `package.json` has `scripts.test` | **npm test** | `npm test` |

Report the detected framework before proceeding.

### Step 2: Parse arguments

Check `$ARGUMENTS` for the mode:

- **No arguments** or **"all"**: Run the full test suite (Step 3)
- **File path** (e.g., `src/auth/login.ts`): Run tests for that file (Step 4)
- **"generate" + file path** (e.g., `generate src/utils.ts`): Generate tests (Step 5)

### Step 3: Run full test suite

Run the detected test command. After completion:

- Report total tests, passed, failed, skipped
- If tests fail, show the first 3 failure messages with file:line references
- Suggest: "Run `/test-detect <failing-file>` to investigate a specific failure"

### Step 4: Run tests for a specific file

Given a source file path, find its test file:

**Search strategy** (try in order):
1. `__tests__/<filename>.test.<ext>` (Jest convention)
2. `<filename>.test.<ext>` (co-located)
3. `<filename>.spec.<ext>` (alternative convention)
4. `test/<filename>_test.<ext>` (Go/Python convention)
5. `tests/test_<filename>.<ext>` (pytest convention)
6. `<filename>_test.go` (Go convention)

Use Glob to find matches. If found, run only that test file:

| Framework | Command |
|-----------|---------|
| Vitest | `npx vitest run <test-file>` |
| Jest | `npx jest <test-file>` |
| Playwright | `npx playwright test <test-file>` |
| pytest | `python -m pytest <test-file>` |
| Go | `go test -run <TestName> ./<package>/` |
| Cargo | `cargo test <test_name>` |

If no test file found, ask: "No tests found for this file. Want me to generate them? Run `/test-detect generate <file>`"

### Step 5: Generate tests

Read the source file and analyze:
1. Identify all exported functions/classes/components
2. Determine the appropriate test patterns for the framework
3. Generate a test file with:
   - Import statements
   - `describe` block per function/class
   - `it`/`test` blocks covering: happy path, edge cases, error cases
   - Framework-appropriate assertions and mocking

**Save to the conventional location** for the detected framework:
- Jest/Vitest: `__tests__/<filename>.test.<ext>` or `<filename>.test.<ext>` (match existing convention)
- pytest: `tests/test_<filename>.py`
- Go: `<filename>_test.go` (same directory)
- RSpec: `spec/<filename>_spec.rb`

Show the generated file path and ask if the user wants to run the new tests.

## Tips

- If multiple frameworks are detected (e.g., Vitest for unit tests + Playwright for e2e), mention both and default to the unit test framework
- For monorepos, detect from the closest config file to the current directory
- If `package.json` has both `test` and `test:unit`/`test:e2e` scripts, prefer the specific one when context is clear

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
