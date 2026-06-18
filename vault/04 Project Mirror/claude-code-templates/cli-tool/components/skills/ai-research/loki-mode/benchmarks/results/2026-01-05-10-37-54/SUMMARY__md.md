---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/results/2026-01-05-10-37-54/SUMMARY.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\loki-mode\benchmarks\results\2026-01-05-10-37-54\SUMMARY.md
source_ext: .md
source_sha256: e38334f3299ee47422224891c306b11bd7bd1168af220dbc625994a69ddc6fbd
text_sha256: 2ceaf432a64b0a33cd4b418b29192a1e9f6c750e2e2371edaa58f620a0f6d524
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:32
---

# SUMMARY.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/results/2026-01-05-10-37-54/SUMMARY.md`
- Extract: `text`
- SHA256: `e38334f3299ee47422224891c306b11bd7bd1168af220dbc625994a69ddc6fbd`

## Content

# Loki Mode Benchmark Results

**Generated:** 2026-01-05 14:15:24

## Overview

This directory contains benchmark results for Loki Mode multi-agent system.

## Methodology

Loki Mode uses its multi-agent architecture to solve each problem:
1. **Architect Agent** analyzes the problem
2. **Engineer Agent** implements the solution
3. **QA Agent** validates with test cases
4. **Review Agent** checks code quality

This mirrors real-world software development more accurately than single-agent approaches.

## Running Benchmarks

```bash
# Setup only (download datasets)
./benchmarks/run-benchmarks.sh all

# Execute with Claude
./benchmarks/run-benchmarks.sh humaneval --execute
./benchmarks/run-benchmarks.sh humaneval --execute --limit 10  # First 10 only
./benchmarks/run-benchmarks.sh swebench --execute --limit 5    # First 5 only

# Use different model
./benchmarks/run-benchmarks.sh humaneval --execute --model opus
```

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
