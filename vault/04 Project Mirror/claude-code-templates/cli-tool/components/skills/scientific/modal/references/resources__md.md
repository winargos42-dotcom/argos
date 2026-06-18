---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/modal/references/resources.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\modal\references\resources.md
source_ext: .md
source_sha256: 742a55603d67251ab645502b124fed87fb3e553b9c5f4e52b56198d89f417c2f
text_sha256: eeb8922013b3b4434f47d93bcdc87a5776bef3bdbce2cac91a85b7ff23e93b6b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:50
---

# resources.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/modal/references/resources.md`
- Extract: `text`
- SHA256: `742a55603d67251ab645502b124fed87fb3e553b9c5f4e52b56198d89f417c2f`

## Content

# CPU, Memory, and Disk Resources

## Default Resources

Each Modal container has default reservations:
- **CPU**: 0.125 cores
- **Memory**: 128 MiB

Containers can exceed minimum if worker has available resources.

## CPU Cores

Request CPU cores as floating-point number:

```python
@app.function(cpu=8.0)
def my_function():
    # Guaranteed access to at least 8 physical cores
    ...
```

Values correspond to physical cores, not vCPUs.

Modal sets multi-threading environment variables based on CPU reservation:
- `OPENBLAS_NUM_THREADS`
- `OMP_NUM_THREADS`
- `MKL_NUM_THREADS`

## Memory

Request memory in megabytes (integer):

```python
@app.function(memory=32768)
def my_function():
    # Guaranteed access to at least 32 GiB RAM
    ...
```

## Resource Limits

### CPU Limits

Default soft CPU limit: request + 16 cores
- Default request: 0.125 cores → default limit: 16.125 cores
- Above limit, host throttles CPU usage

Set explicit CPU limit:

```python
cpu_request = 1.0
cpu_limit = 4.0

@app.function(cpu=(cpu_request, cpu_limit))
def f():
    ...
```

### Memory Limits

Set hard memory limit to OOM kill containers at threshold:

```python
mem_request = 1024  # MB
mem_limit = 2048    # MB

@app.function(memory=(mem_request, mem_limit))
def f():
    # Container killed if exceeds 2048 MB
    ...
```

Useful for catching memory leaks early.

### Disk Limits

Running containers have access to many GBs of SSD disk, limited by:
1. Underlying worker's SSD capacity
2. Per-container disk quota (100s of GBs)

Hitting limits causes `OSError` on disk writes.

Request larger disk with `ephemeral_disk`:

```python
@app.function(ephemeral_disk=10240)  # 10 GiB
def process_large_files():
    ...
```

Maximum disk size: 3.0 TiB (3,145,728 MiB)
Intended use: dataset processing

## Billing

Charged based on whichever is higher: reservation or actual usage.

Disk requests increase memory request at 20:1 ratio:
- Requesting 500 GiB disk → increases memory request to 25 GiB (if not already higher)

## Maximum Requests

Modal enforces maximums at Function creation time. Requests exceeding maximum will be rejected with `InvalidError`.

Contact support if you need higher limits.

## Example: Resource Configuration

```python
@app.function(
    cpu=4.0,              # 4 physical cores
    memory=16384,         # 16 GiB RAM
    ephemeral_disk=51200, # 50 GiB disk
    timeout=3600,         # 1 hour timeout
)
def process_data():
    # Heavy processing with large files
    ...
```

## Monitoring Resource Usage

View resource usage in Modal dashboard:
- CPU utilization
- Memory usage
- Disk usage
- GPU metrics (if applicable)

Access via https://modal.com/apps

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
