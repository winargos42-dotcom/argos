---
argos_import: project_file
source_path: llama.cpp/ci/README-MUSA.md
source_abs: F:\debug\argoss\llama.cpp\ci\README-MUSA.md
source_ext: .md
source_sha256: 849af38a85ce863f7b6776e00c4a90d24432bc37c9d40202246bbef2064e7a64
text_sha256: ade57e9c5e86c06c3abcce281d583d1a4c5468f818c4f6959b57e071ec8e738c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# README-MUSA.md

- Source: `llama.cpp/ci/README-MUSA.md`
- Extract: `text`
- SHA256: `849af38a85ce863f7b6776e00c4a90d24432bc37c9d40202246bbef2064e7a64`

## Content

## Running MUSA CI in a Docker Container

Assuming `$PWD` is the root of the `llama.cpp` repository, follow these steps to set up and run MUSA CI in a Docker container:

### 1. Create a local directory to store cached models, configuration files and venv:

```bash
mkdir -p $HOME/llama.cpp/ci-cache
```

### 2. Create a local directory to store CI run results:

```bash
mkdir -p $HOME/llama.cpp/ci-results
```

### 3. Start a Docker container and run the CI:

```bash
docker run --privileged -it \
    -v $HOME/llama.cpp/ci-cache:/ci-cache \
    -v $HOME/llama.cpp/ci-results:/ci-results \
    -v $PWD:/ws -w /ws \
    mthreads/musa:rc4.3.0-devel-ubuntu22.04-amd64
```

Inside the container, execute the following commands:

```bash
apt update -y && apt install -y bc cmake ccache git python3.10-venv time unzip wget
git config --global --add safe.directory /ws
GG_BUILD_MUSA=1 bash ./ci/run.sh /ci-results /ci-cache
```

This setup ensures that the CI runs within an isolated Docker environment while maintaining cached files and results across runs.

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
