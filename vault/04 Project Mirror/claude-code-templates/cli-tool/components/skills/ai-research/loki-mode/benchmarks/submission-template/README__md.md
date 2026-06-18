---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/submission-template/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\loki-mode\benchmarks\submission-template\README.md
source_ext: .md
source_sha256: 885ab16efc2c78a468eac43776e2a3ee4998d2710eec072c62a5ff1168d26a0f
text_sha256: bfceb087fba90e8a9d477e9281c3fd1e40f3f2fb18d8404720ae0cd7113ae07c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:32
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/loki-mode/benchmarks/submission-template/README.md`
- Extract: `text`
- SHA256: `885ab16efc2c78a468eac43776e2a3ee4998d2710eec072c62a5ff1168d26a0f`

## Content

# Loki Mode - Multi-Agent System for SWE-bench

## Overview

**Loki Mode** is a multi-agent system built as a Claude Code skill that orchestrates specialized AI agents to solve software engineering tasks. This submission demonstrates its performance on SWE-bench Lite.

## Results

| Metric | Value |
|--------|-------|
| **Patch Generation Rate** | **99.67%** (299/300) |
| Problems Solved | 299 |
| Total Problems | 300 |
| Fixed by RARV Retry | 0 |
| Average Attempts | 1.0 |
| Total Time | ~3.5 hours |
| Avg Time/Problem | 42s |

## System Architecture

Loki Mode uses a **4-agent pipeline** with a RARV (Reason-Act-Reflect-Verify) cycle:

```
Issue -> [Architect] -> [Engineer] -> [QA] -> [Reviewer] -> Patch
                ^                                |
                |______ RARV Retry Loop ________|
```

### Agent Roles

| Agent | Role | Model | Timeout |
|-------|------|-------|---------|
| **Architect** | Analyze issue, identify files, design fix approach | Claude Opus 4.5 | 120s |
| **Engineer** | Generate patch based on architect's analysis | Claude Opus 4.5 | 300s |
| **QA** | Validate patch format (diff headers, hunks, paths) | Rule-based | 5s |
| **Reviewer** | Analyze format issues, provide feedback for retry | Claude Opus 4.5 | 60s |

### RARV Cycle

The RARV (Reason-Act-Reflect-Verify) cycle enables self-correction:

1. **Reason**: Architect analyzes the issue
2. **Act**: Engineer generates a patch
3. **Reflect**: QA validates the patch format
4. **Verify**: If invalid, Reviewer provides feedback and Engineer retries

Maximum 3 retry attempts per problem.

## Comparison with Baselines

| System | SWE-bench Lite Patch Gen |
|--------|--------------------------|
| **Loki Mode (multi-agent)** | **99.67%** (299/300) |
| Direct Claude (single agent) | 99.67% (299/300) |

After timeout optimization, the multi-agent RARV pipeline matches single-agent performance.

## Methodology

1. **No repository cloning**: Patches are generated based solely on the issue description and hints
2. **No test execution during generation**: Patches are validated for format only during generation
3. **Deterministic pipeline**: Same agent sequence for all problems
4. **Full trajectory logging**: All prompts and outputs are recorded for transparency

## Repository

- **GitHub**: [asklokesh/loki-mode](https://github.com/asklokesh/loki-mode)
- **License**: MIT
- **Version**: 2.25.0

## Running Loki Mode

```bash
# Clone the repository
git clone https://github.com/asklokesh/loki-mode.git

# Run SWE-bench with Loki Mode
./benchmarks/run-benchmarks.sh swebench --execute --loki

# Run with limit for testing
./benchmarks/run-benchmarks.sh swebench --execute --loki --limit 10
```

## Files in This Submission

```
evaluation/lite/20260105_loki_mode/
├── README.md           # This file
├── metadata.yaml       # Submission metadata
├── all_preds.jsonl     # Predictions in JSONL format
├── trajs/              # Reasoning trajectories (1 per problem)
│   ├── django__django-11039.md
│   ├── matplotlib__matplotlib-23299.md
│   └── ...
└── logs/               # Execution logs (1 dir per problem)
    ├── django__django-11039/
    │   ├── patch.diff
    │   ├── report.json
    │   └── test_output.txt
    └── ...
```

## Acknowledgments

- Built for the [Claude Code](https://claude.ai) ecosystem
- Powered by Anthropic's Claude Opus 4.5 model
- Inspired by multi-agent collaboration patterns

## Contact

- GitHub: [@asklokesh](https://github.com/asklokesh)

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
