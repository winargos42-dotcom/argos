---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/game-development/game-performance-profiler.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\game-development\game-performance-profiler.md
source_ext: .md
source_sha256: 7e7d32f4f97c63e2159b7e8f1870aa4622edc15ccab9449cac485fc651659dde
text_sha256: 334fa12683052d717c7a26b0a55f5985ea3622046337937ea47510bb664c4c7a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# game-performance-profiler.md

- Source: `claude-code-templates/cli-tool/components/commands/game-development/game-performance-profiler.md`
- Extract: `text`
- SHA256: `7e7d32f4f97c63e2159b7e8f1870aa4622edc15ccab9449cac485fc651659dde`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [profile-type] | --fps | --memory | --rendering | --comprehensive
description: Use PROACTIVELY to analyze game performance bottlenecks and generate optimization recommendations across multiple platforms
---

# Game Performance Analysis & Optimization

Analyze game performance and generate optimization recommendations: $ARGUMENTS

## Current Performance Context

- Game engine: @package.json or detect Unity/Unreal/Godot project files
- Platform targets: !`find . -name "*.pbxproj" -o -name "*.gradle" -o -name "*.vcxproj" | head -3`
- Asset pipeline: !`find . -name "*.meta" -o -name "*.asset" | wc -l` game assets
- Build configs: !`grep -r "BuildTarget\|Platform" . 2>/dev/null | wc -l` platform configurations
- Performance logs: !`find . -name "*profile*" -o -name "*perf*" | head -5`

## Task

Create comprehensive performance analysis with automated bottleneck detection, optimization suggestions, and platform-specific recommendations for game development projects.

## Performance Analysis Areas

### 1. Frame Rate & Rendering Performance
- Analyze draw calls and batching efficiency
- Identify overdraw and fillrate bottlenecks
- Review shader complexity and optimization opportunities
- Evaluate mesh and texture optimization potential
- Check lighting and shadow rendering performance

### 2. Memory Usage Analysis
- Memory allocation patterns and potential leaks
- Texture memory usage and compression opportunities
- Audio memory optimization suggestions
- Object pooling and garbage collection analysis
- Platform-specific memory constraints evaluation

### 3. CPU Performance Profiling
- Script execution bottlenecks identification
- Physics simulation optimization opportunities
- AI and pathfinding performance analysis
- Animation system efficiency review
- Threading and parallelization recommendations

### 4. Platform-Specific Optimization
- Mobile performance considerations (battery, thermal throttling)
- Console-specific optimization guidelines
- PC hardware scaling recommendations
- VR performance requirements and optimizations
- Web/WebGL specific performance considerations

## Deliverables

1. **Performance Audit Report**
   - Current performance metrics and benchmarks
   - Identified bottlenecks with severity ratings
   - Platform-specific performance analysis

2. **Optimization Recommendations**
   - Prioritized optimization suggestions
   - Implementation difficulty and impact assessment
   - Code and asset optimization guidelines

3. **Monitoring Setup**
   - Performance monitoring implementation
   - Key metrics tracking configuration
   - Automated performance regression detection

4. **Testing Strategy**
   - Performance testing procedures
   - Target device testing recommendations
   - Continuous performance monitoring setup

## Implementation Guidelines

Follow game engine best practices and target platform requirements. Generate actionable recommendations with clear implementation steps and expected performance improvements.

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
