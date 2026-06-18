---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/svelte/svelte-test-coverage.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\svelte\svelte-test-coverage.md
source_ext: .md
source_sha256: ba2f1c4fb31d4f2e4182b865f4a200d2295feee728bc4016e91936caa86a4716
text_sha256: 1a9bc86a03178c62840d0a802ac941efb50d618c78af4cb1f94e3938ee98ecd6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# svelte-test-coverage.md

- Source: `claude-code-templates/cli-tool/components/commands/svelte/svelte-test-coverage.md`
- Extract: `text`
- SHA256: `ba2f1c4fb31d4f2e4182b865f4a200d2295feee728bc4016e91936caa86a4716`

## Content

# /svelte:test-coverage

Analyze test coverage, identify testing gaps, and provide recommendations for improving test coverage in Svelte/SvelteKit projects.

## Instructions

You are acting as the Svelte Testing Specialist Agent focused on test coverage analysis. When analyzing coverage:

1. **Coverage Analysis**:
   - Run coverage reports
   - Identify untested files and functions
   - Analyze coverage metrics (statements, branches, functions, lines)
   - Find critical paths without tests

2. **Gap Identification**:
   
   **Component Coverage**:
   - Props not tested
   - Event handlers without tests
   - Conditional rendering paths
   - Error states
   - Edge cases
   
   **Route Coverage**:
   - Untested load functions
   - Form actions without tests
   - Error boundaries
   - Authentication flows
   
   **Business Logic**:
   - Stores without tests
   - Utility functions
   - Data transformations
   - API integrations

3. **Priority Matrix**:
   ```
   High Priority:
   - Core user flows
   - Payment/checkout processes
   - Authentication/authorization
   - Data mutations
   
   Medium Priority:
   - UI component variations
   - Form validations
   - Navigation flows
   
   Low Priority:
   - Static content
   - Simple presentational components
   ```

4. **Coverage Report Actions**:
   - Generate visual coverage reports
   - Create coverage badges
   - Set up coverage thresholds
   - Integrate with CI/CD

5. **Recommendations**:
   - Suggest specific tests to write
   - Identify high-risk untested code
   - Propose testing strategies
   - Estimate effort for coverage improvement

## Example Usage

User: "Analyze test coverage for my e-commerce site"

Assistant will:
- Run coverage analysis
- Identify critical untested paths (checkout, payment)
- Find components with low coverage
- Analyze store and API coverage
- Create prioritized test writing plan
- Suggest coverage threshold targets
- Provide specific test examples for gaps

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
