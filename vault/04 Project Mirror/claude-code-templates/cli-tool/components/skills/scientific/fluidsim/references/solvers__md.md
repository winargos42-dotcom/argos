---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/fluidsim/references/solvers.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\fluidsim\references\solvers.md
source_ext: .md
source_sha256: b707511c1e2f771e0c1cf9b62084075ff41f85aa926d97853709873d1066f5de
text_sha256: 3abe711620b8c463e2916851985ebab1bfbbbacfa9f944e07b1e7d38c2887bb4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:49
---

# solvers.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/fluidsim/references/solvers.md`
- Extract: `text`
- SHA256: `b707511c1e2f771e0c1cf9b62084075ff41f85aa926d97853709873d1066f5de`

## Content

# FluidSim Solvers

FluidSim provides multiple solvers for different fluid dynamics equations. All solvers work on periodic domains using pseudospectral methods with FFT.

## Available Solvers

### 2D Incompressible Navier-Stokes

**Solver key**: `ns2d`

**Import**:
```python
from fluidsim.solvers.ns2d.solver import Simul
# or dynamically
Simul = fluidsim.import_simul_class_from_key("ns2d")
```

**Use for**: 2D turbulence studies, vortex dynamics, fundamental fluid flow simulations

**Key features**: Energy and enstrophy cascades, vorticity dynamics

### 3D Incompressible Navier-Stokes

**Solver key**: `ns3d`

**Import**:
```python
from fluidsim.solvers.ns3d.solver import Simul
```

**Use for**: 3D turbulence, realistic fluid flow simulations, high-resolution DNS

**Key features**: Full 3D turbulence dynamics, parallel computing support

### Stratified Flows (2D/3D)

**Solver keys**: `ns2d.strat`, `ns3d.strat`

**Import**:
```python
from fluidsim.solvers.ns2d.strat.solver import Simul  # 2D
from fluidsim.solvers.ns3d.strat.solver import Simul  # 3D
```

**Use for**: Oceanic and atmospheric flows, density-driven flows

**Key features**: Boussinesq approximation, buoyancy effects, constant Brunt-Väisälä frequency

**Parameters**: Set stratification via `params.N` (Brunt-Väisälä frequency)

### Shallow Water Equations

**Solver key**: `sw1l` (one-layer)

**Import**:
```python
from fluidsim.solvers.sw1l.solver import Simul
```

**Use for**: Geophysical flows, tsunami modeling, rotating flows

**Key features**: Rotating frame support, geostrophic balance

**Parameters**: Set rotation via `params.f` (Coriolis parameter)

### Föppl-von Kármán Equations

**Solver key**: `fvk` (elastic plate equations)

**Import**:
```python
from fluidsim.solvers.fvk.solver import Simul
```

**Use for**: Elastic plate dynamics, fluid-structure interaction studies

## Solver Selection Guide

Choose a solver based on the physical problem:

1. **2D turbulence, quick testing**: Use `ns2d`
2. **3D flows, realistic simulations**: Use `ns3d`
3. **Density-stratified flows**: Use `ns2d.strat` or `ns3d.strat`
4. **Geophysical flows, rotating systems**: Use `sw1l`
5. **Elastic plates**: Use `fvk`

## Modified Versions

Many solvers have modified versions with additional physics:
- Forcing terms
- Different boundary conditions
- Additional scalar fields

Check `fluidsim.solvers` module for complete list.

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
