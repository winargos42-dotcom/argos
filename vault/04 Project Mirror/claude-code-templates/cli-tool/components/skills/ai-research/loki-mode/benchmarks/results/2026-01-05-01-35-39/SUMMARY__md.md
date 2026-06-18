---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/results/2026-01-05-01-35-39/SUMMARY.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\loki-mode\benchmarks\results\2026-01-05-01-35-39\SUMMARY.md
source_ext: .md
source_sha256: 2932969b7077afeb60ac5d82c006f1146f77067e185a06291baf050a6561a665
text_sha256: 201bb69a7dfc24bb3a630d3e5713393423f60d1120321d9f52a7a7bb2aa59ea8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:32
---

# SUMMARY.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/results/2026-01-05-01-35-39/SUMMARY.md`
- Extract: `text`
- SHA256: `2932969b7077afeb60ac5d82c006f1146f77067e185a06291baf050a6561a665`

## Content

# Loki Mode Benchmark Results

**Generated:** 2026-01-05 02:32:40

## Overview

This directory contains benchmark results for Loki Mode multi-agent system.

## SWE-bench Lite Results

| Metric | Value |
|--------|-------|
| Problems | 50 |
| Patches Generated | 50 |
| Errors | 0 |
| Model | opus |
| Time | 3413.75s |

**Next Step:** Run the SWE-bench evaluator to validate patches:

```bash
python -m swebench.harness.run_evaluation     --predictions /Users/lokesh/git/loki-mode/benchmarks/results/2026-01-05-01-35-39/swebench-predictions.json     --max_workers 4
```

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
