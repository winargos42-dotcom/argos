---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/team/team-knowledge-mapper.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\team\team-knowledge-mapper.md
source_ext: .md
source_sha256: 2576d1d9ff674a2c0272daa266340a3bda51d34a25bf0051e22a02836821e1a2
text_sha256: cdb2339445a285c4588ff7e29048b6b1ce5842db0265387fe55352be0d7278a6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# team-knowledge-mapper.md

- Source: `claude-code-templates/cli-tool/components/commands/team/team-knowledge-mapper.md`
- Extract: `text`
- SHA256: `2576d1d9ff674a2c0272daa266340a3bda51d34a25bf0051e22a02836821e1a2`

## Content

---
allowed-tools: Read, Bash, Glob, Grep
argument-hint: [mapping-type] | --skill-matrix | --knowledge-gaps | --expertise-areas | --learning-paths
description: Map team knowledge and expertise with skill gap analysis and learning path recommendations
---

# Team Knowledge Mapper

Map team knowledge and expertise with comprehensive skill gap analysis: **$ARGUMENTS**

## Current Knowledge Context

- Team expertise: !`git log --format='%ae' --since='3 months ago' | sort | uniq -c | sort -nr` contributor activity patterns
- Technology stack: Analysis of languages, frameworks, and tools used in codebase
- Knowledge distribution: Assessment of expertise concentration and bus factor risks
- Learning activity: Recent skill development and cross-training initiatives

## Task

Execute comprehensive knowledge mapping with skill gap analysis and learning optimization:

**Mapping Type**: Use $ARGUMENTS to focus on skill matrix creation, knowledge gap identification, expertise area analysis, or learning path recommendations

**Knowledge Mapping Framework**:
1. **Skill Matrix Creation** - Map individual expertise levels, identify core competencies, assess technology proficiencies, evaluate domain knowledge
2. **Knowledge Gap Analysis** - Identify critical skill gaps, assess team vulnerabilities, evaluate learning priorities, recommend skill development
3. **Expertise Distribution** - Analyze knowledge concentration, identify single points of failure, assess bus factor risks, recommend knowledge sharing
4. **Learning Path Planning** - Design skill development roadmaps, recommend training priorities, plan mentorship programs, optimize knowledge transfer
5. **Cross-Training Optimization** - Identify pairing opportunities, plan knowledge rotation, design shadowing programs, optimize skill redundancy
6. **Knowledge Retention** - Assess knowledge preservation, plan documentation strategies, design knowledge capture systems, prevent expertise loss

**Advanced Features**: Dynamic skill tracking, expertise prediction modeling, learning ROI analysis, knowledge graph visualization, competency gap forecasting.

**Strategic Planning**: Succession planning support, hiring decision guidance, team composition optimization, skill portfolio balancing.

**Output**: Comprehensive knowledge map with skill matrices, gap analysis, learning recommendations, and strategic knowledge management plans.

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
