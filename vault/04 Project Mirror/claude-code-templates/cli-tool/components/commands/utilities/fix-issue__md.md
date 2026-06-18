---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/utilities/fix-issue.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\utilities\fix-issue.md
source_ext: .md
source_sha256: cbc1fff6caf69af0ef2e8135df39ba5c2a6cc64ed0b3a13adb48070a8438a2fa
text_sha256: 07b6ab9bd79c15ea3a768e9974e6af6089d4fb3f4d3d6c55372a4736e57c7d51
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# fix-issue.md

- Source: `claude-code-templates/cli-tool/components/commands/utilities/fix-issue.md`
- Extract: `text`
- SHA256: `cbc1fff6caf69af0ef2e8135df39ba5c2a6cc64ed0b3a13adb48070a8438a2fa`

## Content

# Fix Issue Command

Identify and resolve code issues

## Instructions

Follow this structured approach to analyze and fix issues: **$ARGUMENTS**

1. **Issue Analysis**
   - Use `gh issue view $ARGUMENTS` to get complete issue details
   - Read the issue description, comments, and any attached logs/screenshots
   - Identify the type of issue (bug, feature request, enhancement, etc.)
   - Understand the expected vs actual behavior

2. **Environment Setup**
   - Ensure you're on the correct branch (usually main/master)
   - Pull latest changes: `git pull origin main`
   - Create a new feature branch: `git checkout -b fix/issue-$ARGUMENTS`

3. **Reproduce the Issue**
   - Follow the steps to reproduce described in the issue
   - Set up the development environment if needed
   - Run the application/tests to confirm the issue exists
   - Document the current behavior

4. **Root Cause Analysis**
   - Search the codebase for relevant files and functions
   - Use grep/search tools to locate the problematic code
   - Analyze the code logic and identify the root cause
   - Check for related issues or similar patterns

5. **Solution Design**
   - Design a fix that addresses the root cause, not just symptoms
   - Consider edge cases and potential side effects
   - Ensure the solution follows project conventions and patterns
   - Plan for backward compatibility if needed

6. **Implementation**
   - Implement the fix with clean, readable code
   - Follow the project's coding standards and style
   - Add appropriate error handling and logging
   - Keep changes minimal and focused

7. **Testing Strategy**
   - Write or update tests to cover the fix
   - Ensure existing tests still pass
   - Test edge cases and error conditions
   - Run the full test suite to check for regressions

8. **Code Quality Checks**
   - Run linting and formatting tools
   - Perform static analysis if available
   - Check for security implications
   - Ensure performance isn't negatively impacted

9. **Documentation Updates**
   - Update relevant documentation if needed
   - Add or update code comments for clarity
   - Update changelog if the project maintains one
   - Document any breaking changes

10. **Commit and Push**
    - Stage the changes: `git add .`
    - Create a descriptive commit message following project conventions
    - Example: `fix: resolve issue with user authentication timeout (#$ARGUMENTS)`
    - Push the branch: `git push origin fix/issue-$ARGUMENTS`

11. **Create Pull Request**
    - Use `gh pr create` to create a pull request
    - Reference the issue in the PR description: "Fixes #$ARGUMENTS"
    - Provide a clear description of the changes and testing performed
    - Add appropriate labels and reviewers

12. **Follow-up**
    - Monitor the PR for feedback and requested changes
    - Address any review comments promptly
    - Update the issue with progress and resolution
    - Ensure CI/CD checks pass

13. **Verification**
    - Once merged, verify the fix in the main branch
    - Close the issue if not automatically closed
    - Monitor for any related issues or regressions

Remember to communicate clearly in both code and comments, and always prioritize maintainable solutions over quick fixes.

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
