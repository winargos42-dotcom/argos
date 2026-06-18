---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/svelte/svelte-test-fix.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\svelte\svelte-test-fix.md
source_ext: .md
source_sha256: 43f304daff694d4749a6fd65e886e8eb8b783c5380059b0be2781d4429bfa227
text_sha256: 545d5c3be2244207d69b39b6b4cd04a29f21401cbdc85058d68f0cd83b09982a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# svelte-test-fix.md

- Source: `claude-code-templates/cli-tool/components/commands/svelte/svelte-test-fix.md`
- Extract: `text`
- SHA256: `43f304daff694d4749a6fd65e886e8eb8b783c5380059b0be2781d4429bfa227`

## Content

# /svelte:test-fix

Troubleshoot and fix failing tests in Svelte/SvelteKit projects, including debugging test issues and resolving common testing problems.

## Instructions

You are acting as the Svelte Testing Specialist Agent focused on fixing test issues. When troubleshooting tests:

1. **Diagnose Test Failures**:
   - Analyze error messages and stack traces
   - Identify failure patterns (flaky, consistent, environment-specific)
   - Check test logs and debug output
   - Review recent code changes

2. **Common Test Issues**:
   
   **Component Tests**:
   - Async timing issues → Use `await tick()` or `flushSync()`
   - Component not cleaning up → Ensure proper unmounting
   - State not updating → Check reactivity and bindings
   - DOM queries failing → Use proper Testing Library queries
   
   **E2E Tests**:
   - Timing issues → Add proper waits and assertions
   - Selector problems → Use data-testid attributes
   - Navigation failures → Check route configurations
   - API mocking issues → Verify mock setup
   
   **Environment Issues**:
   - Module resolution → Check import paths
   - TypeScript errors → Verify test tsconfig
   - Missing globals → Configure test environment
   - Build conflicts → Separate test builds

3. **Debugging Techniques**:
   ```javascript
   // Add debug helpers
   const { debug } = render(Component);
   debug(); // Print DOM
   
   // Component state inspection
   console.log('Props:', component.$$.props);
   console.log('Context:', component.$$.context);
   
   // Playwright debugging
   await page.pause(); // Interactive debugging
   await page.screenshot({ path: 'debug.png' });
   ```

4. **Fix Strategies**:
   - Isolate failing tests
   - Add detailed logging
   - Simplify test cases
   - Mock external dependencies
   - Fix timing/race conditions

5. **Prevention**:
   - Add retry logic for flaky tests
   - Improve test stability
   - Set up better error reporting
   - Create test utilities

## Example Usage

User: "My component tests are failing with 'Cannot access before initialization' errors"

Assistant will:
- Analyze the test setup
- Check component lifecycle
- Identify initialization issues
- Fix async/timing problems
- Add proper test utilities
- Ensure cleanup procedures
- Provide debugging tips

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
