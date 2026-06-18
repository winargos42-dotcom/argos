---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/azure/azure-role-selector.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\azure\azure-role-selector.md
source_ext: .md
source_sha256: 7ecc50308d31b1a4b33442441d9a6ab136453af610cc04148e064d89158d20b8
text_sha256: 2ac45fdb92cc1b201ad43cda4a3544056180b992689233fdd6ea67a02dde6e6a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# azure-role-selector.md

- Source: `claude-code-templates/cli-tool/components/commands/azure/azure-role-selector.md`
- Extract: `text`
- SHA256: `7ecc50308d31b1a4b33442441d9a6ab136453af610cc04148e064d89158d20b8`

## Content

---
allowed-tools: Azure MCP/documentation, Azure MCP/bicepschema, Azure MCP/extension_cli_generate, Azure MCP/get_bestpractices
description: When user is asking for guidance for which role to assign to an identity given desired permissions, this agent helps them understand the role that will meet the requirements with least privilege access and how to apply that role.
---

Use 'Azure MCP/documentation' tool to find the minimal role definition that matches the desired permissions the user wants to assign to an identity (If no built-in role matches the desired permissions, use 'Azure MCP/extension_cli_generate' tool to create a custom role definition with the desired permissions). Use 'Azure MCP/extension_cli_generate' tool to generate the CLI commands needed to assign that role to the identity and use the 'Azure MCP/bicepschema' and the 'Azure MCP/get_bestpractices' tool to provide a Bicep code snippet for adding the role assignment.

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
