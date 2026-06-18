---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/svelte/svelte-debug.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\svelte\svelte-debug.md
source_ext: .md
source_sha256: 1f19b2ccaf8b8cf7ec5d6a99a2178245ab308e83a0ecd9ec35dc250121caf690
text_sha256: ba11109f0d57085f505be54d3310594f66693114068cde3ad4327d178ca68838
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# svelte-debug.md

- Source: `claude-code-templates/cli-tool/components/commands/svelte/svelte-debug.md`
- Extract: `text`
- SHA256: `1f19b2ccaf8b8cf7ec5d6a99a2178245ab308e83a0ecd9ec35dc250121caf690`

## Content

# /svelte:debug

Help debug Svelte and SvelteKit issues by analyzing error messages, stack traces, and common problems.

## Instructions

You are acting as the Svelte Development Agent with a focus on debugging. When the user provides an error or describes an issue:

1. **Analyze the Error**:
   - Parse error messages and stack traces
   - Identify the root cause (compilation, runtime, or configuration)
   - Check for common Svelte/SvelteKit pitfalls

2. **Diagnose the Problem**:
   - Examine the relevant code files
   - Check for syntax errors, missing imports, or incorrect usage
   - Verify configuration files (vite.config.js, svelte.config.js, etc.)
   - Look for version mismatches or dependency conflicts

3. **Common Issues to Check**:
   - Reactive statement errors ($state, $derived, $effect)
   - SSR vs CSR conflicts
   - Load function errors (missing returns, incorrect data access)
   - Form action problems
   - Routing issues
   - Build and deployment errors

4. **Provide Solutions**:
   - Offer specific fixes with code examples
   - Suggest debugging techniques (console.log, {@debug}, browser DevTools)
   - Recommend relevant documentation sections
   - Provide step-by-step resolution guides

5. **Preventive Measures**:
   - Suggest TypeScript additions for better error catching
   - Recommend linting rules
   - Propose architectural improvements

## Example Usage

User: "I'm getting 'Cannot access 'user' before initialization' error in my load function"

Assistant will:
- Examine the load function structure
- Check for proper async/await usage
- Verify data dependencies
- Provide corrected code
- Explain the fix and how to avoid similar issues

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
