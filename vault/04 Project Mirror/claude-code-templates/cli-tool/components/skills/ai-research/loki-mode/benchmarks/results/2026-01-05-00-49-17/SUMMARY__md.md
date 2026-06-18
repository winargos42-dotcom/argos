---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/results/2026-01-05-00-49-17/SUMMARY.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\loki-mode\benchmarks\results\2026-01-05-00-49-17\SUMMARY.md
source_ext: .md
source_sha256: 4257ac70fb1fe3807ce297d2f0783955d28599f92f11bd93e4f62be987f0cdb9
text_sha256: 522d9abf735bc78a47164d7e73eeb610ff8486d10ca20a24ca277cbd9177c1f2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# SUMMARY.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/results/2026-01-05-00-49-17/SUMMARY.md`
- Extract: `text`
- SHA256: `4257ac70fb1fe3807ce297d2f0783955d28599f92f11bd93e4f62be987f0cdb9`

## Content

# Loki Mode Benchmark Results

**Generated:** 2026-01-05 01:10:21

## Overview

This directory contains benchmark results for Loki Mode multi-agent system.

## HumanEval Results

| Metric | Value |
|--------|-------|
| Problems | 164 |
| Passed | 161 |
| Failed | 3 |
| **Pass Rate** | **98.17%** |
| Model | opus |
| Time | 1263.46s |

### Competitor Comparison

| System | Pass@1 |
|--------|--------|
| MetaGPT | 85.9-87.7% |
| **Loki Mode** | **98.17%** |

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
