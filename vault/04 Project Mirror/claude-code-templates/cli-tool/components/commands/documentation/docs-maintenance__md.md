---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/documentation/docs-maintenance.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\documentation\docs-maintenance.md
source_ext: .md
source_sha256: a12cfd021b46e606ea0413bfa0c9fd615fbc79f19efb565f118d85f3c71d94ad
text_sha256: 1eec80d60735f3a2e17d6b1ea38d1182151c2cbdfb7ecd5fc9734d90c4611460
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# docs-maintenance.md

- Source: `claude-code-templates/cli-tool/components/commands/documentation/docs-maintenance.md`
- Extract: `text`
- SHA256: `a12cfd021b46e606ea0413bfa0c9fd615fbc79f19efb565f118d85f3c71d94ad`

## Content

---
allowed-tools: Read, Write, Edit, Bash, Grep
argument-hint: [maintenance-type] | --audit | --update | --validate | --optimize | --comprehensive
description: Use PROACTIVELY to implement comprehensive documentation maintenance systems with quality assurance, validation, and automated updates
---

# Documentation Maintenance & Quality Assurance

Implement comprehensive documentation maintenance system: $ARGUMENTS

## Current Documentation Health

- Documentation files: !`find . -name "*.md" -o -name "*.mdx" | wc -l` files
- Last updates: !`find . -name "*.md" -exec stat -f "%m %N" {} \; | sort -n | tail -5`
- External links: !`grep -r "http" --include="*.md" . | wc -l` links to validate
- Image references: !`grep -r "!\[.*\]" --include="*.md" . | wc -l` images to check
- Documentation structure: @docs/ or detect documentation directories

## Task

Create systematic documentation maintenance framework with automated quality assurance, comprehensive validation, content optimization, and regular update procedures.

## Documentation Maintenance Framework

### 1. Content Quality Audit System
- Comprehensive file discovery and categorization
- Content freshness analysis and aging detection
- Word count, readability, and structure assessment
- Missing sections and incomplete documentation identification
- TODO/FIXME marker tracking and resolution planning

### 2. Link and Reference Validation
- External link health monitoring with retry logic
- Internal link validation and broken reference detection
- Image reference verification and missing asset identification
- Cross-reference consistency checking
- Automated link correction suggestions

### 3. Style and Consistency Checking
- Markdown syntax validation and formatting standards
- Heading hierarchy and structure consistency
- List formatting and emphasis style uniformity
- Code block formatting and language specification
- Accessibility compliance (alt text, descriptive links)

### 4. Content Optimization and Enhancement
- Table of contents generation for long documents
- Metadata updating and frontmatter management
- Common formatting issue correction
- Spelling and grammar validation
- Readability analysis and improvement suggestions

### 5. Automated Synchronization System
- Git-based change tracking and documentation updates
- Version control integration with branch management
- Automated commit generation with detailed change logs
- Merge conflict resolution strategies
- Rollback procedures for failed updates

### 6. Quality Assurance Reporting
- Comprehensive audit reports with severity classifications
- Issue categorization and prioritization systems
- Progress tracking and maintenance metrics
- Automated notification systems for critical issues
- Dashboard creation for ongoing monitoring

## Implementation Requirements

### Audit Configuration
- Configurable quality thresholds and validation rules
- Custom style guide integration and enforcement
- Platform-specific optimization settings
- Team collaboration workflow integration
- Automated scheduling and recurring maintenance

### Validation Processes
- Multi-level validation with error categorization
- Batch processing for large documentation sets
- Performance optimization for comprehensive scans
- Integration with existing CI/CD pipelines
- Real-time monitoring and alerting systems

### Reporting and Analytics
- Detailed maintenance reports with actionable insights
- Historical trend analysis and improvement tracking
- Team productivity metrics and documentation health scores
- Integration with project management tools
- Automated stakeholder communication

## Deliverables

1. **Maintenance System Architecture**
   - Automated audit and validation framework
   - Content optimization and enhancement tools
   - Quality assurance reporting infrastructure
   - Version control integration and synchronization

2. **Validation and Quality Tools**
   - Link checking and reference validation systems
   - Style consistency and accessibility compliance tools
   - Content freshness and completeness analyzers
   - Automated correction and enhancement utilities

3. **Reporting and Monitoring**
   - Comprehensive audit reports with prioritized recommendations
   - Real-time monitoring dashboards and alert systems
   - Progress tracking and maintenance history documentation
   - Integration with team communication and project tools

4. **Documentation and Procedures**
   - Implementation guidelines and configuration instructions
   - Team workflow integration and collaboration procedures
   - Troubleshooting guides and maintenance best practices
   - Automated scheduling and recurring maintenance setup

## Integration Guidelines

Implement with existing documentation platforms and development workflows. Ensure scalability for large documentation sets and team collaboration while maintaining quality standards and accessibility compliance.

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
