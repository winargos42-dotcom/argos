---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/modal/references/getting-started.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\modal\references\getting-started.md
source_ext: .md
source_sha256: b46420d733f86a000139984f0ec76b7b0bbaedd4aa8d680c0b12825fb3550207
text_sha256: 5def976716dffa732990438cbe6f3fba0333d6c505dd1377fd0b759dc3a122bb
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:50
---

# getting-started.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/modal/references/getting-started.md`
- Extract: `text`
- SHA256: `b46420d733f86a000139984f0ec76b7b0bbaedd4aa8d680c0b12825fb3550207`

## Content

# Getting Started with Modal

## Sign Up

Sign up for free at https://modal.com and get $30/month of credits.

## Authentication

Set up authentication using the Modal CLI:

```bash
modal token new
```

This creates credentials in `~/.modal.toml`. Alternatively, set environment variables:
- `MODAL_TOKEN_ID`
- `MODAL_TOKEN_SECRET`

## Basic Concepts

### Modal is Serverless

Modal is a serverless platform - only pay for resources used and spin up containers on demand in seconds.

### Core Components

**App**: Represents an application running on Modal, grouping one or more Functions for atomic deployment.

**Function**: Acts as an independent unit that scales up and down independently. No containers run (and no charges) when there are no live inputs.

**Image**: The environment code runs in - a container snapshot with dependencies installed.

## First Modal App

Create a file `hello_modal.py`:

```python
import modal

app = modal.App(name="hello-modal")

@app.function()
def hello():
    print("Hello from Modal!")
    return "success"

@app.local_entrypoint()
def main():
    hello.remote()
```

Run with:
```bash
modal run hello_modal.py
```

## Running Apps

### Ephemeral Apps (Development)

Run temporarily with `modal run`:
```bash
modal run script.py
```

The app stops when the script exits. Use `--detach` to keep running after client exits.

### Deployed Apps (Production)

Deploy persistently with `modal deploy`:
```bash
modal deploy script.py
```

View deployed apps at https://modal.com/apps or with:
```bash
modal app list
```

Stop deployed apps:
```bash
modal app stop app-name
```

## Key Features

- **Fast prototyping**: Write Python, run on GPUs in seconds
- **Serverless APIs**: Create web endpoints with a decorator
- **Scheduled jobs**: Run cron jobs in the cloud
- **GPU inference**: Access T4, L4, A10, A100, H100, H200, B200 GPUs
- **Distributed volumes**: Persistent storage for ML models
- **Sandboxes**: Secure containers for untrusted code

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
