---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/fluidsim/references/installation.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\fluidsim\references\installation.md
source_ext: .md
source_sha256: 34f25240d29f41c177d13c3ce883f877d607d968e6e1f7e92373d2edc6e01766
text_sha256: a2f971b5a24d489723d3aa36a40f6ce51058ea853f6f034615b9285dfebaadee
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:49
---

# installation.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/fluidsim/references/installation.md`
- Extract: `text`
- SHA256: `34f25240d29f41c177d13c3ce883f877d607d968e6e1f7e92373d2edc6e01766`

## Content

# FluidSim Installation

## Requirements

- Python >= 3.9
- Virtual environment recommended

## Installation Methods

### Basic Installation

Install fluidsim using uv:

```bash
uv pip install fluidsim
```

### With FFT Support (Required for Pseudospectral Solvers)

Most fluidsim solvers use Fourier-based methods and require FFT libraries:

```bash
uv pip install "fluidsim[fft]"
```

This installs fluidfft and pyfftw dependencies.

### With MPI and FFT (For Parallel Simulations)

For high-performance parallel computing:

```bash
uv pip install "fluidsim[fft,mpi]"
```

Note: This triggers local compilation of mpi4py.

## Environment Configuration

### Output Directories

Set environment variables to control where simulation data is stored:

```bash
export FLUIDSIM_PATH=/path/to/simulation/outputs
export FLUIDDYN_PATH_SCRATCH=/path/to/working/directory
```

### FFT Method Selection

Specify FFT implementation (optional):

```bash
export FLUIDSIM_TYPE_FFT2D=fft2d.with_fftw
export FLUIDSIM_TYPE_FFT3D=fft3d.with_fftw
```

## Verification

Test the installation:

```bash
pytest --pyargs fluidsim
```

## No Authentication Required

FluidSim does not require API keys or authentication tokens.

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
