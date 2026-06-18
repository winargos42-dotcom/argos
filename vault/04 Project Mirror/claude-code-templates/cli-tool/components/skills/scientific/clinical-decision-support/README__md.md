---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/clinical-decision-support/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\clinical-decision-support\README.md
source_ext: .md
source_sha256: 79adcc4a8f8628eec4811fcda41c1dcaa21775569d75cc43288d33b42abaa93c
text_sha256: 217ce0755db19a6a3cca9571ec17e0ef6aeb759dc1010a0377b7495efd501a83
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:49
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/clinical-decision-support/README.md`
- Extract: `text`
- SHA256: `79adcc4a8f8628eec4811fcda41c1dcaa21775569d75cc43288d33b42abaa93c`

## Content

# Clinical Decision Support Skill

Professional clinical decision support documents for medical professionals in pharmaceutical and clinical research settings.

## Quick Start

This skill enables generation of three types of clinical documents:

1. **Individual Patient Treatment Plans** - Personalized protocols for specific patients
2. **Patient Cohort Analysis** - Biomarker-stratified group analyses with outcomes
3. **Treatment Recommendation Reports** - Evidence-based clinical guidelines

All documents are generated as compact, professional LaTeX/PDF files.

## Directory Structure

```
clinical-decision-support/
├── SKILL.md                     # Main skill definition
├── README.md                    # This file
│
├── references/                  # Clinical guidance documents
│   ├── patient_cohort_analysis.md
│   ├── treatment_recommendations.md
│   ├── clinical_decision_algorithms.md
│   ├── biomarker_classification.md
│   ├── outcome_analysis.md
│   └── evidence_synthesis.md
│
├── assets/                      # Templates and examples
│   ├── cohort_analysis_template.tex
│   ├── treatment_recommendation_template.tex
│   ├── clinical_pathway_template.tex
│   ├── biomarker_report_template.tex
│   ├── example_gbm_cohort.md
│   ├── recommendation_strength_guide.md
│   └── color_schemes.tex
│
└── scripts/                     # Analysis and generation tools
    ├── generate_survival_analysis.py
    ├── create_cohort_tables.py
    ├── build_decision_tree.py
    ├── biomarker_classifier.py
    └── validate_cds_document.py
```

## Example Use Cases

### Create a Patient Cohort Analysis
```
> Analyze a cohort of 45 NSCLC patients stratified by PD-L1 expression 
  (<1%, 1-49%, ≥50%) including ORR, PFS, and OS outcomes
```

### Generate Treatment Recommendations
```
> Create evidence-based treatment recommendations for HER2-positive 
  metastatic breast cancer with GRADE methodology
```

### Build Clinical Pathway
```
> Generate a clinical decision algorithm for acute chest pain 
  management with TIMI risk score
```

## Key Features

- **GRADE Methodology**: Evidence quality grading (High/Moderate/Low/Very Low)
- **Recommendation Strength**: Strong (Grade 1) vs Conditional (Grade 2)
- **Biomarker Integration**: Genomic, expression, and molecular subtype classification
- **Statistical Analysis**: Kaplan-Meier, Cox regression, log-rank tests
- **Guideline Concordance**: NCCN, ASCO, ESMO, AHA/ACC integration
- **Professional Output**: 0.5in margins, color-coded boxes, publication-ready

## Dependencies

Python scripts require:
- `pandas`, `numpy`, `scipy`: Data analysis and statistics
- `lifelines`: Survival analysis (Kaplan-Meier, Cox regression)
- `matplotlib`: Visualization
- `pyyaml` (optional): YAML input for decision trees

Install with:
```bash
pip install pandas numpy scipy lifelines matplotlib pyyaml
```

## References Included

1. **Patient Cohort Analysis**: Stratification methods, biomarker correlations, statistical comparisons
2. **Treatment Recommendations**: Evidence grading, treatment sequencing, special populations
3. **Clinical Decision Algorithms**: Risk scores, decision trees, TikZ flowcharts
4. **Biomarker Classification**: Genomic alterations, molecular subtypes, companion diagnostics
5. **Outcome Analysis**: Survival methods, response criteria (RECIST), effect sizes
6. **Evidence Synthesis**: Guideline integration, systematic reviews, meta-analysis

## Templates Provided

1. **Cohort Analysis**: Demographics table, biomarker profile, outcomes, statistics, recommendations
2. **Treatment Recommendations**: Evidence review, GRADE-graded options, monitoring, decision algorithm
3. **Clinical Pathway**: TikZ flowchart with risk stratification and urgency-coded actions
4. **Biomarker Report**: Genomic profiling with tier-based actionability and therapy matching

## Scripts Included

1. **`generate_survival_analysis.py`**: Create Kaplan-Meier curves with hazard ratios
2. **`create_cohort_tables.py`**: Generate baseline, efficacy, and safety tables
3. **`build_decision_tree.py`**: Convert text/JSON to TikZ flowcharts
4. **`biomarker_classifier.py`**: Stratify patients by PD-L1, HER2, molecular subtypes
5. **`validate_cds_document.py`**: Quality checks for completeness and compliance

## Integration

Integrates with existing skills:
- **scientific-writing**: Citation management, statistical reporting
- **clinical-reports**: Medical terminology, HIPAA compliance
- **scientific-schematics**: TikZ flowcharts

## Version

Version 1.0 - Initial release
Created: November 2024
Last Updated: November 5, 2024

## Questions or Feedback

This skill was designed for pharmaceutical and clinical research professionals creating clinical decision support documents. For questions about usage or suggestions for improvements, contact the Scientific Writer development team.

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
