---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/plugin-settings/examples/create-settings-command.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\plugin-settings\examples\create-settings-command.md
source_ext: .md
source_sha256: e87a80231825ca345b8c8b52b1200beee0c6101cdea59652bb8b0de87e490026
text_sha256: abf0a36bb3f6425041046f2da1ebfac5505c5b37656fdd4772cfc4d8bd2fa655
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# create-settings-command.md

- Source: `claude-code-templates/cli-tool/components/skills/development/plugin-settings/examples/create-settings-command.md`
- Extract: `text`
- SHA256: `e87a80231825ca345b8c8b52b1200beee0c6101cdea59652bb8b0de87e490026`

## Content

---
description: "Create plugin settings file with user preferences"
allowed-tools: ["Write", "AskUserQuestion"]
---

# Create Plugin Settings

This command helps users create a `.claude/my-plugin.local.md` settings file.

## Steps

### Step 1: Ask User for Preferences

Use AskUserQuestion to gather configuration:

```json
{
  "questions": [
    {
      "question": "Enable plugin for this project?",
      "header": "Enable Plugin",
      "multiSelect": false,
      "options": [
        {
          "label": "Yes",
          "description": "Plugin will be active"
        },
        {
          "label": "No",
          "description": "Plugin will be disabled"
        }
      ]
    },
    {
      "question": "Validation mode?",
      "header": "Mode",
      "multiSelect": false,
      "options": [
        {
          "label": "Strict",
          "description": "Maximum validation and security checks"
        },
        {
          "label": "Standard",
          "description": "Balanced validation (recommended)"
        },
        {
          "label": "Lenient",
          "description": "Minimal validation only"
        }
      ]
    }
  ]
}
```

### Step 2: Parse Answers

Extract answers from AskUserQuestion result:

- answers["0"]: enabled (Yes/No)
- answers["1"]: mode (Strict/Standard/Lenient)

### Step 3: Create Settings File

Use Write tool to create `.claude/my-plugin.local.md`:

```markdown
---
enabled: <true if Yes, false if No>
validation_mode: <strict, standard, or lenient>
max_file_size: 1000000
notify_on_errors: true
---

# Plugin Configuration

Your plugin is configured with <mode> validation mode.

To modify settings, edit this file and restart Claude Code.
```

### Step 4: Inform User

Tell the user:
- Settings file created at `.claude/my-plugin.local.md`
- Current configuration summary
- How to edit manually if needed
- Reminder: Restart Claude Code for changes to take effect
- Settings file is gitignored (won't be committed)

## Implementation Notes

Always validate user input before writing:
- Check mode is valid
- Validate numeric fields are numbers
- Ensure paths don't have traversal attempts
- Sanitize any free-text fields

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
