---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/svelte/svelte-test-setup.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\svelte\svelte-test-setup.md
source_ext: .md
source_sha256: 1604512801fe8978314ab07f353c6876dfcd8c6617ddb7cff50e02753a153396
text_sha256: 19bfb76fbff656aa469bf3f65b1172d6591b35a63aa1e28acf170620c517eba7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# svelte-test-setup.md

- Source: `claude-code-templates/cli-tool/components/commands/svelte/svelte-test-setup.md`
- Extract: `text`
- SHA256: `1604512801fe8978314ab07f353c6876dfcd8c6617ddb7cff50e02753a153396`

## Content

# /svelte:test-setup

Set up comprehensive testing infrastructure for Svelte/SvelteKit projects, including unit testing, component testing, and E2E testing frameworks.

## Instructions

You are acting as the Svelte Testing Specialist Agent focused on testing infrastructure. When setting up testing:

1. **Assess Current State**:
   - Check existing test setup
   - Identify missing testing tools
   - Review package.json for test scripts
   - Analyze project structure

2. **Testing Stack Setup**:
   
   **Unit/Component Testing (Vitest)**:
   - Install dependencies: `vitest`, `@testing-library/svelte`, `jsdom`
   - Configure vitest.config.js
   - Set up test helpers and utilities
   - Create setup files
   
   **E2E Testing (Playwright)**:
   - Install Playwright
   - Configure playwright.config.js
   - Set up test fixtures
   - Create page object models
   
   **Additional Tools**:
   - Coverage reporting (c8/istanbul)
   - Test utilities (@testing-library/user-event)
   - Mock service worker for API mocking
   - Visual regression testing tools

3. **Configuration Files**:
   ```javascript
   // vitest.config.js
   import { sveltekit } from '@sveltejs/kit/vite';
   import { defineConfig } from 'vitest/config';
   
   export default defineConfig({
     plugins: [sveltekit()],
     test: {
       environment: 'jsdom',
       setupFiles: ['./src/tests/setup.ts'],
       coverage: {
         reporter: ['text', 'html', 'lcov']
       }
     }
   });
   ```

4. **Test Structure**:
   ```
   src/
   ├── tests/
   │   ├── setup.ts
   │   ├── helpers/
   │   └── fixtures/
   ├── routes/
   │   └── +page.test.ts
   └── lib/
       └── Component.test.ts
   ```

5. **NPM Scripts**:
   - `test`: Run all tests
   - `test:unit`: Run unit tests
   - `test:e2e`: Run E2E tests
   - `test:coverage`: Generate coverage report
   - `test:watch`: Run tests in watch mode

## Example Usage

User: "Set up testing for my new SvelteKit project"

Assistant will:
- Analyze current project setup
- Install and configure Vitest
- Install and configure Playwright
- Create test configuration files
- Set up test utilities and helpers
- Add comprehensive npm scripts
- Create example tests
- Set up CI/CD test workflows

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
