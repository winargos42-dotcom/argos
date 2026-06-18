---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/orchestration/status.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\orchestration\status.md
source_ext: .md
source_sha256: 674c15bf4ad7c4c4f352ef00cc246436fea04956d39e763cdcf52021f249f47c
text_sha256: 9b0c0c90893fd6b09c97f102445de8b173793521a3c86e1a44ad9c905e528310
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# status.md

- Source: `claude-code-templates/cli-tool/components/commands/orchestration/status.md`
- Extract: `text`
- SHA256: `674c15bf4ad7c4c4f352ef00cc246436fea04956d39e763cdcf52021f249f47c`

## Content

# Task Status Command

Check the current status of tasks in the orchestration system with various filtering and reporting options.

## Usage

```
/task-status [options]
```

## Description

Provides comprehensive visibility into task progress, status distribution, and execution metrics across all active orchestrations.

## Command Variants

### Basic Status Overview
```
/task-status
```
Shows summary of all tasks across all active orchestrations.

### Today's Tasks
```
/task-status --today
```
Shows only tasks from today's orchestrations.

### Specific Orchestration
```
/task-status --date 03_15_2024 --project payment_integration
```
Shows tasks from a specific orchestration.

### Status Filter
```
/task-status --status in_progress
/task-status --status qa
/task-status --status on_hold
```
Shows only tasks with specified status.

### Detailed View
```
/task-status --detailed
```
Shows comprehensive information for each task.

## Output Formats

### Summary View (Default)
```
Task Orchestration Status Summary
=================================

Active Orchestrations: 3
Total Tasks: 47

Status Distribution:
┌─────────────┬───────┬────────────┐
│ Status      │ Count │ Percentage │
├─────────────┼───────┼────────────┤
│ completed   │  12   │    26%     │
│ qa          │   5   │    11%     │
│ in_progress │   3   │     6%     │
│ on_hold     │   2   │     4%     │
│ todos       │  25   │    53%     │
└─────────────┴───────┴────────────┘

Active Tasks (in_progress):
- TASK-001: Implement JWT authentication (Agent: dev-frontend)
- TASK-007: Create payment webhook handler (Agent: dev-backend)
- TASK-012: Write integration tests (Agent: test-developer)

Blocked Tasks (on_hold):
- TASK-004: User profile API (Blocked by: TASK-001)
- TASK-009: Payment confirmation UI (Blocked by: TASK-007)
```

### Detailed View
```
Task Details for: 03_15_2024/authentication_system
==================================================

TASK-001: Implement JWT authentication
Status: in_progress
Agent: dev-frontend
Started: 2024-03-15T14:30:00Z
Duration: 3.5 hours
Progress: 75% (est. 1 hour remaining)
Dependencies: None
Blocks: TASK-004, TASK-005
Location: /task-orchestration/03_15_2024/authentication_system/tasks/in_progress/

Status History:
- todos → in_progress (2024-03-15T14:30:00Z) by dev-frontend
```

### Timeline View
```
/task-status --timeline
```
Shows Gantt-style timeline of task execution.

### Velocity Report
```
/task-status --velocity
```
Shows completion rates and performance metrics.

## Filtering Options

### By Agent
```
/task-status --agent dev-frontend
```

### By Priority
```
/task-status --priority high
```

### By Type
```
/task-status --type feature
/task-status --type bugfix
```

### Multiple Filters
```
/task-status --status todos --priority high --type security
```

## Quick Actions

### Show Critical Path
```
/task-status --critical-path
```
Highlights tasks that are blocking others.

### Show Overdue
```
/task-status --overdue
```
Shows tasks exceeding estimated time.

### Show Available
```
/task-status --available
```
Shows todos tasks ready to be picked up.

## Integration Commands

### Export Status
```
/task-status --export markdown
/task-status --export csv
```

### Watch Mode
```
/task-status --watch
```
Updates status in real-time (refreshes every 30 seconds).

## Examples

### Example 1: Morning Standup View
```
/task-status --today --detailed
```

### Example 2: Find Blocked Work
```
/task-status --status on_hold --show-blockers
```

### Example 3: Agent Workload
```
/task-status --by-agent --status in_progress
```

### Example 4: Sprint Progress
```
/task-status --date 03_15_2024 --metrics
```

## Metrics and Analytics

### Completion Metrics
- Average time per task
- Tasks completed per day
- Status transition times

### Bottleneck Analysis
- Most blocking tasks
- Longest on_hold duration
- Critical path duration

### Agent Performance
- Tasks per agent
- Average completion time
- Current workload

## Best Practices

1. **Daily Check**: Run `/task-status --today` each morning
2. **Blocker Review**: Check `/task-status --status on_hold` regularly
3. **Progress Tracking**: Use `/task-status --velocity` for trends
4. **Resource Planning**: Monitor `/task-status --by-agent`

## Notes

- Status data is read from TASK-STATUS-TRACKER.yaml files
- All times are shown in local timezone
- Completed tasks are included in metrics but not in active lists
- Use `--all` flag to include historical orchestrations

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
