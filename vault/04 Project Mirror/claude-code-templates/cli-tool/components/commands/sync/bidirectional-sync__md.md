---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/sync/bidirectional-sync.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\sync\bidirectional-sync.md
source_ext: .md
source_sha256: 3c068cb9287886737d305a5e325eaec6cf0bdb064d0cf045279dcd4d509042e3
text_sha256: aee4ece8ff280091e1c2841be63c5a24169f893e5b62fad692b75df6c6d13e7b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# bidirectional-sync.md

- Source: `claude-code-templates/cli-tool/components/commands/sync/bidirectional-sync.md`
- Extract: `text`
- SHA256: `3c068cb9287886737d305a5e325eaec6cf0bdb064d0cf045279dcd4d509042e3`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [sync-mode] | --full | --incremental | --dry-run | --conflict-strategy
description: Enable comprehensive bidirectional GitHub-Linear synchronization with conflict resolution
---

# Bidirectional Sync

Enable comprehensive bidirectional GitHub-Linear synchronization: **$ARGUMENTS**

## Current Sync Environment

- GitHub status: !`gh api user 2>/dev/null && echo "✓ Authenticated" || echo "⚠ Not authenticated"`
- Linear MCP: Check if Linear MCP server is available and configured
- Sync state: @.sync-state.json or @sync/ (if exists)
- Webhooks: !`gh api repos/{owner}/{repo}/hooks 2>/dev/null | grep -c linear || echo "0"`

## Task

Implement robust bidirectional synchronization between GitHub Issues and Linear tasks:

**Sync Mode**: Use $ARGUMENTS to specify full sync, incremental sync, dry-run preview, or conflict resolution strategy

**Synchronization Framework**:
1. **Sync State Management** - Initialize sync database, track entity relationships, maintain sync history
2. **Conflict Detection** - Identify simultaneous changes, field-level conflicts, timing issues
3. **Resolution Strategies** - NEWER_WINS, GITHUB_WINS, LINEAR_WINS, or intelligent field-level merge
4. **Transaction Management** - Atomic operations, rollback capability, distributed locking
5. **Webhook Integration** - Real-time event handling, sync loop prevention, automated triggers
6. **Data Integrity** - Bidirectional validation, cross-reference maintenance, audit trails

**Advanced Features**: Field-level merge rules, sync loop prevention, webhook automation, performance optimization, comprehensive monitoring.

**Production Ready**: Transaction safety, conflict resolution, error recovery, performance monitoring, comprehensive logging.

**Output**: Complete bidirectional sync system with conflict resolution, webhook integration, performance metrics, and comprehensive sync reporting.

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
