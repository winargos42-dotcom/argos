---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/plugin-settings/examples/example-settings.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\plugin-settings\examples\example-settings.md
source_ext: .md
source_sha256: 664a77278fed768386153fe467f906e592fbe7750a2b8cf6809795b93a9fea4a
text_sha256: f07209b6e2fb62d443ae07d01bc1674c6c741c352a04549bfa978e1f34b9769e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# example-settings.md

- Source: `claude-code-templates/cli-tool/components/skills/development/plugin-settings/examples/example-settings.md`
- Extract: `text`
- SHA256: `664a77278fed768386153fe467f906e592fbe7750a2b8cf6809795b93a9fea4a`

## Content

# Example Plugin Settings File

## Template: Basic Configuration

**.claude/my-plugin.local.md:**

```markdown
---
enabled: true
mode: standard
---

# My Plugin Configuration

Plugin is active in standard mode.
```

## Template: Advanced Configuration

**.claude/my-plugin.local.md:**

```markdown
---
enabled: true
strict_mode: false
max_file_size: 1000000
allowed_extensions: [".js", ".ts", ".tsx"]
enable_logging: true
notification_level: info
retry_attempts: 3
timeout_seconds: 60
custom_path: "/path/to/data"
---

# My Plugin Advanced Configuration

This project uses custom plugin configuration with:
- Standard validation mode
- 1MB file size limit
- JavaScript/TypeScript files allowed
- Info-level logging
- 3 retry attempts

## Additional Notes

Contact @team-lead with questions about this configuration.
```

## Template: Agent State File

**.claude/multi-agent-swarm.local.md:**

```markdown
---
agent_name: database-implementation
task_number: 4.2
pr_number: 5678
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.5", "Task 4.1"]
additional_instructions: "Use PostgreSQL, not MySQL"
---

# Task Assignment: Database Schema Implementation

Implement the database schema for the new features module.

## Requirements

- Create migration files
- Add indexes for performance
- Write tests for constraints
- Document schema in README

## Success Criteria

- Migrations run successfully
- All tests pass
- PR created with CI green
- Schema documented

## Coordination

Depends on:
- Task 3.5: API endpoint definitions
- Task 4.1: Data model design

Report status to coordinator session 'team-leader'.
```

## Template: Feature Flag Pattern

**.claude/experimental-features.local.md:**

```markdown
---
enabled: true
features:
  - ai_suggestions
  - auto_formatting
  - advanced_refactoring
experimental_mode: false
---

# Experimental Features Configuration

Current enabled features:
- AI-powered code suggestions
- Automatic code formatting
- Advanced refactoring tools

Experimental mode is OFF (stable features only).
```

## Usage in Hooks

These templates can be read by hooks:

```bash
# Check if plugin is configured
if \[\[ ! -f ".claude/my-plugin.local.md" \]\]; then
  exit 0  # Not configured, skip hook
fi

# Read settings
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' ".claude/my-plugin.local.md")
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# Apply settings
if \[\[ "$ENABLED" == "true" \]\]; then
  # Hook is active
  # ...
fi
```

## Gitignore

Always add to project `.gitignore`:

```gitignore
# Plugin settings (user-local, not committed)
.claude/*.local.md
.claude/*.local.json
```

## Editing Settings

Users can edit settings files manually:

```bash
# Edit settings
vim .claude/my-plugin.local.md

# Changes take effect after restart
exit  # Exit Claude Code
claude  # Restart
```

Changes require Claude Code restart - hooks can't be hot-swapped.

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
