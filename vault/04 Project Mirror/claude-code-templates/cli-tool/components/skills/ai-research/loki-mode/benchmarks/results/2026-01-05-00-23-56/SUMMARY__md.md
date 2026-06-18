---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/results/2026-01-05-00-23-56/SUMMARY.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\loki-mode\benchmarks\results\2026-01-05-00-23-56\SUMMARY.md
source_ext: .md
source_sha256: ed6ee749ca45c885a8638f45ce3dc2e304727634b0248cb8af3df96308aae5bf
text_sha256: 9e9858486e42121f96dc1e3f58a994b37b37d0b90740f7f6c357962d2e22730d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# SUMMARY.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/results/2026-01-05-00-23-56/SUMMARY.md`
- Extract: `text`
- SHA256: `ed6ee749ca45c885a8638f45ce3dc2e304727634b0248cb8af3df96308aae5bf`

## Content

# Loki Mode Benchmark Results

## Overview

This directory contains benchmark results for Loki Mode multi-agent system.

## Benchmarks Available

### HumanEval
- **Problems:** 164 Python programming problems
- **Metric:** Pass@1 (percentage of problems solved on first attempt)
- **Competitor Baseline:** MetaGPT achieves 85.9-87.7%

### SWE-bench Lite
- **Problems:** 300 real-world GitHub issues
- **Metric:** Resolution rate
- **Competitor Baseline:** Top agents achieve 45-77%

## Running Benchmarks

```bash
# Run all benchmarks
./benchmarks/run-benchmarks.sh all

# Run specific benchmark
./benchmarks/run-benchmarks.sh humaneval --execute
./benchmarks/run-benchmarks.sh swebench --execute
```

## Results Format

Results are saved as JSON files with:
- Timestamp
- Problem count
- Pass rate
- Individual problem results
- Token usage
- Execution time

## Methodology

Loki Mode uses its multi-agent architecture to solve each problem:
1. **Architect Agent** analyzes the problem
2. **Engineer Agent** implements the solution
3. **QA Agent** validates with test cases
4. **Review Agent** checks code quality

This mirrors real-world software development more accurately than single-agent approaches.

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
