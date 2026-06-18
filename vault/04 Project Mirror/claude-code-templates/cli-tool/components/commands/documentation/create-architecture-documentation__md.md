---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/documentation/create-architecture-documentation.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\documentation\create-architecture-documentation.md
source_ext: .md
source_sha256: ed1f0ca810977fbeb1103788e582d5eb1ddd301f681394c992801539761d18c8
text_sha256: 3fa4a31d7210cb023d4a0b8c5a00616154399685a7713d267473377969a10b8d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# create-architecture-documentation.md

- Source: `claude-code-templates/cli-tool/components/commands/documentation/create-architecture-documentation.md`
- Extract: `text`
- SHA256: `ed1f0ca810977fbeb1103788e582d5eb1ddd301f681394c992801539761d18c8`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: "[framework] | --c4-model | --arc42 | --adr | --plantuml | --full-suite"
description: Generate comprehensive architecture documentation with diagrams, ADRs, and interactive visualization
---

# Architecture Documentation Generator

Generate comprehensive architecture documentation: $ARGUMENTS

## Current Architecture Context

- Project structure: !`find . -type f -name "*.json" -o -name "*.yaml" -o -name "*.toml" | head -5`
- Documentation exists: @docs/ or @README.md (if exists)
- Architecture files: !`find . -name "*architecture*" -o -name "*design*" -o -name "*.puml" | head -3`
- Services/containers: @docker-compose.yml or @k8s/ (if exists)
- API definitions: !`find . -name "*api*" -o -name "*openapi*" -o -name "*swagger*" | head -3`

## Task

Generate comprehensive architecture documentation with modern tooling and best practices:

1. **Architecture Analysis and Discovery**
   - Analyze current system architecture and component relationships
   - Identify key architectural patterns and design decisions
   - Document system boundaries, interfaces, and dependencies
   - Assess data flow and communication patterns
   - Identify architectural debt and improvement opportunities

2. **Architecture Documentation Framework**
   - Choose appropriate documentation framework and tools:
     - **C4 Model**: Context, Containers, Components, Code diagrams
     - **Arc42**: Comprehensive architecture documentation template
     - **Architecture Decision Records (ADRs)**: Decision documentation
     - **PlantUML/Mermaid**: Diagram-as-code documentation
     - **Structurizr**: C4 model tooling and visualization
     - **Draw.io/Lucidchart**: Visual diagramming tools

3. **System Context Documentation**
   - Create high-level system context diagrams
   - Document external systems and integrations
   - Define system boundaries and responsibilities
   - Document user personas and stakeholders
   - Create system landscape and ecosystem overview

4. **Container and Service Architecture**
   - Document container/service architecture and deployment view
   - Create service dependency maps and communication patterns
   - Document deployment architecture and infrastructure
   - Define service boundaries and API contracts
   - Document data persistence and storage architecture

5. **Component and Module Documentation**
   - Create detailed component architecture diagrams
   - Document internal module structure and relationships
   - Define component responsibilities and interfaces
   - Document design patterns and architectural styles
   - Create code organization and package structure documentation

6. **Data Architecture Documentation**
   - Document data models and database schemas
   - Create data flow diagrams and processing pipelines
   - Document data storage strategies and technologies
   - Define data governance and lifecycle management
   - Create data integration and synchronization documentation

7. **Security and Compliance Architecture**
   - Document security architecture and threat model
   - Create authentication and authorization flow diagrams
   - Document compliance requirements and controls
   - Define security boundaries and trust zones
   - Create incident response and security monitoring documentation

8. **Quality Attributes and Cross-Cutting Concerns**
   - Document performance characteristics and scalability patterns
   - Create reliability and availability architecture documentation
   - Document monitoring and observability architecture
   - Define maintainability and evolution strategies
   - Create disaster recovery and business continuity documentation

9. **Architecture Decision Records (ADRs)**
   - Create comprehensive ADR template and process
   - Document historical architectural decisions and rationale
   - Create decision tracking and review process
   - Document trade-offs and alternatives considered
   - Set up ADR maintenance and evolution procedures

10. **Documentation Automation and Maintenance**
    - Set up automated diagram generation from code annotations
    - Configure documentation pipeline and publishing automation
    - Set up documentation validation and consistency checking
    - Create documentation review and approval process
    - Train team on architecture documentation practices and tools
    - Set up documentation versioning and change management

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
