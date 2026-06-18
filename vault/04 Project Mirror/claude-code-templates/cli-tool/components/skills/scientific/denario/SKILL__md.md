---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/denario/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\denario\SKILL.md
source_ext: .md
source_sha256: 21e0dd7fa8327fdd576ad01742c8d384ef8932269974e74101b70fdb08858153
text_sha256: b01a3a658ec892c727790e954e7df37d2b60cdf1ab3d100df5326a40c2c8af2a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:49
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/denario/SKILL.md`
- Extract: `text`
- SHA256: `21e0dd7fa8327fdd576ad01742c8d384ef8932269974e74101b70fdb08858153`

## Content

---
name: denario
description: Multiagent AI system for scientific research assistance that automates research workflows from data analysis to publication. This skill should be used when generating research ideas from datasets, developing research methodologies, executing computational experiments, performing literature searches, or generating publication-ready papers in LaTeX format. Supports end-to-end research pipelines with customizable agent orchestration.
---

# Denario

## Overview

Denario is a multiagent AI system designed to automate scientific research workflows from initial data analysis through publication-ready manuscripts. Built on AG2 and LangGraph frameworks, it orchestrates multiple specialized agents to handle hypothesis generation, methodology development, computational analysis, and paper writing.

## When to Use This Skill

Use this skill when:
- Analyzing datasets to generate novel research hypotheses
- Developing structured research methodologies
- Executing computational experiments and generating visualizations
- Conducting literature searches for research context
- Writing journal-formatted LaTeX papers from research results
- Automating the complete research pipeline from data to publication

## Installation

Install denario using uv (recommended):

```bash
uv init
uv add "denario[app]"
```

Or using pip:

```bash
uv pip install "denario[app]"
```

For Docker deployment or building from source, see `references/installation.md`.

## LLM API Configuration

Denario requires API keys from supported LLM providers. Supported providers include:
- Google Vertex AI
- OpenAI
- Other LLM services compatible with AG2/LangGraph

Store API keys securely using environment variables or `.env` files. For detailed configuration instructions including Vertex AI setup, see `references/llm_configuration.md`.

## Core Research Workflow

Denario follows a structured four-stage research pipeline:

### 1. Data Description

Define the research context by specifying available data and tools:

```python
from denario import Denario

den = Denario(project_dir="./my_research")
den.set_data_description("""
Available datasets: time-series data on X and Y
Tools: pandas, sklearn, matplotlib
Research domain: [specify domain]
""")
```

### 2. Idea Generation

Generate research hypotheses from the data description:

```python
den.get_idea()
```

This produces a research question or hypothesis based on the described data. Alternatively, provide a custom idea:

```python
den.set_idea("Custom research hypothesis")
```

### 3. Methodology Development

Develop the research methodology:

```python
den.get_method()
```

This creates a structured approach for investigating the hypothesis. Can also accept markdown files with custom methodologies:

```python
den.set_method("path/to/methodology.md")
```

### 4. Results Generation

Execute computational experiments and generate analysis:

```python
den.get_results()
```

This runs the methodology, performs computations, creates visualizations, and produces findings. Can also provide pre-computed results:

```python
den.set_results("path/to/results.md")
```

### 5. Paper Generation

Create a publication-ready LaTeX paper:

```python
from denario import Journal

den.get_paper(journal=Journal.APS)
```

The generated paper includes proper formatting for the specified journal, integrated figures, and complete LaTeX source.

## Available Journals

Denario supports multiple journal formatting styles:
- `Journal.APS` - American Physical Society format
- Additional journals may be available; check `references/research_pipeline.md` for the complete list

## Launching the GUI

Run the graphical user interface:

```bash
denario run
```

This launches a web-based interface for interactive research workflow management.

## Common Workflows

### End-to-End Research Pipeline

```python
from denario import Denario, Journal

# Initialize project
den = Denario(project_dir="./research_project")

# Define research context
den.set_data_description("""
Dataset: Time-series measurements of [phenomenon]
Available tools: pandas, sklearn, scipy
Research goal: Investigate [research question]
""")

# Generate research idea
den.get_idea()

# Develop methodology
den.get_method()

# Execute analysis
den.get_results()

# Create publication
den.get_paper(journal=Journal.APS)
```

### Hybrid Workflow (Custom + Automated)

```python
# Provide custom research idea
den.set_idea("Investigate the correlation between X and Y using time-series analysis")

# Auto-generate methodology
den.get_method()

# Auto-generate results
den.get_results()

# Generate paper
den.get_paper(journal=Journal.APS)
```

### Literature Search Integration

For literature search functionality and additional workflow examples, see `references/examples.md`.

## Advanced Features

- **Multiagent orchestration**: AG2 and LangGraph coordinate specialized agents for different research tasks
- **Reproducible research**: All stages produce structured outputs that can be version-controlled
- **Journal integration**: Automatic formatting for target publication venues
- **Flexible input**: Manual or automated at each pipeline stage
- **Docker deployment**: Containerized environment with LaTeX and all dependencies

## Detailed References

For comprehensive documentation:
- **Installation options**: `references/installation.md`
- **LLM configuration**: `references/llm_configuration.md`
- **Complete API reference**: `references/research_pipeline.md`
- **Example workflows**: `references/examples.md`

## Troubleshooting

Common issues and solutions:
- **API key errors**: Ensure environment variables are set correctly (see `references/llm_configuration.md`)
- **LaTeX compilation**: Install TeX distribution or use Docker image with pre-installed LaTeX
- **Package conflicts**: Use virtual environments or Docker for isolation
- **Python version**: Requires Python 3.12 or higher

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
