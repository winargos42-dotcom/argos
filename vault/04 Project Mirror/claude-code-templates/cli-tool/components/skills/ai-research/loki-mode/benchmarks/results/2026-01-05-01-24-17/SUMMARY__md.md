---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/results/2026-01-05-01-24-17/SUMMARY.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\loki-mode\benchmarks\results\2026-01-05-01-24-17\SUMMARY.md
source_ext: .md
source_sha256: c3b707a400ba1d30449eb301a92bf1f352aa852774aef05e9581969dccb729d9
text_sha256: 0d0f35436306dc4add09e6eb9ba96969203932a3a507f5d84124bb43ffc198af
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# SUMMARY.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/results/2026-01-05-01-24-17/SUMMARY.md`
- Extract: `text`
- SHA256: `c3b707a400ba1d30449eb301a92bf1f352aa852774aef05e9581969dccb729d9`

## Content

# Loki Mode Benchmark Results

**Generated:** 2026-01-05 07:34:38

## Overview

This directory contains benchmark results for Loki Mode multi-agent system.

## SWE-bench Lite Results

| Metric | Value |
|--------|-------|
| Problems | 300 |
| Patches Generated | 299 |
| Errors | 1 |
| Model | opus |
| Time | 22218.33s |

**Next Step:** Run the SWE-bench evaluator to validate patches:

```bash
python -m swebench.harness.run_evaluation     --predictions /Users/lokesh/git/loki-mode/benchmarks/results/2026-01-05-01-24-17/swebench-predictions.json     --max_workers 4
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
