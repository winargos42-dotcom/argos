---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/documentation/update-docs.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\documentation\update-docs.md
source_ext: .md
source_sha256: 74aafab9cc0c8f8d6fbc607984bf330a02dbcdc55f0c48612741cc79de146b3b
text_sha256: aabfd4d3946e2a9fca6f72ffe9b0c46f42485b46716f0457f775f13aed81c020
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# update-docs.md

- Source: `claude-code-templates/cli-tool/components/commands/documentation/update-docs.md`
- Extract: `text`
- SHA256: `74aafab9cc0c8f8d6fbc607984bf330a02dbcdc55f0c48612741cc79de146b3b`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [doc-type] | --implementation | --api | --architecture | --sync | --validate
description: Systematically update project documentation with implementation status, API changes, and synchronized content
---

# Documentation Update & Synchronization

Update project documentation systematically: $ARGUMENTS

## Current Documentation State

- Documentation structure: !`find . -name "*.md" | head -10`
- Specs directory: @specs/ (if exists)
- Implementation status: !`grep -r "✅\|❌\|⚠️" docs/ specs/ 2>/dev/null | wc -l` status indicators
- Recent changes: !`git log --oneline --since="1 week ago" -- "*.md" | head -5`
- Project progress: @CLAUDE.md or @README.md (if exists)

## Task

## Documentation Analysis

1. Review current documentation status:
   - Check `specs/implementation_status.md` for overall project status
   - Review implemented phase document (`specs/phase{N}_implementation_plan.md`)
   - Review `specs/flutter_structurizr_implementation_spec.md` and `specs/flutter_structurizr_implementation_spec_updated.md`
   - Review `specs/testing_plan.md` to ensure it is current given recent test passes, failures, and changes
   - Examine `CLAUDE.md` and `README.md` for project-wide documentation
   - Check for and document any new lessons learned or best practices in CLAUDE.md

2. Analyze implementation and testing results:
   - Review what was implemented in the last phase
   - Review testing results and coverage
   - Identify new best practices discovered during implementation
   - Note any implementation challenges and solutions
   - Cross-reference updated documentation with recent implementation and test results to ensure accuracy

## Documentation Updates

1. Update phase implementation document:
   - Mark completed tasks with ✅ status
   - Update implementation percentages
   - Add detailed notes on implementation approach
   - Document any deviations from original plan with justification
   - Add new sections if needed (lessons learned, best practices)
   - Document specific implementation details for complex components
   - Include a summary of any new troubleshooting tips or workflow improvements discovered during the phase

2. Update implementation status document:
   - Update phase completion percentages
   - Add or update implementation status for components
   - Add notes on implementation approach and decisions
   - Document best practices discovered during implementation
   - Note any challenges overcome and solutions implemented

3. Update implementation specification documents:
   - Mark completed items with ✅ or strikethrough but preserve original requirements
   - Add notes on implementation details where appropriate
   - Add references to implemented files and classes
   - Update any implementation guidance based on experience

4. Update CLAUDE.md and README.md if necessary:
   - Add new best practices
   - Update project status
   - Add new implementation guidance
   - Document known issues or limitations
   - Update usage examples to include new functionality

5. Document new testing procedures:
   - Add details on test files created
   - Include test running instructions
   - Document test coverage
   - Explain testing approach for complex components

## Documentation Formatting and Structure

1. Maintain consistent documentation style:
   - Use clear headings and sections
   - Include code examples where helpful
   - Use status indicators (✅, ⚠️, ❌) consistently
   - Maintain proper Markdown formatting

2. Ensure documentation completeness:
   - Cover all implemented features
   - Include usage examples
   - Document API changes or additions
   - Include troubleshooting guidance for common issues

## Guidelines

- DO NOT CREATE new specification files
- UPDATE existing files in the `specs/` directory
- Maintain consistent documentation style
- Include practical examples where appropriate
- Cross-reference related documentation sections
- Document best practices and lessons learned
- Provide clear status updates on project progress
- Update numerical completion percentages
- Ensure documentation reflects actual implementation

Provide a summary of documentation updates after completion, including:
1. Files updated
2. Major changes to documentation
3. Updated completion percentages
4. New best practices documented
5. Status of the overall project after this phase

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
