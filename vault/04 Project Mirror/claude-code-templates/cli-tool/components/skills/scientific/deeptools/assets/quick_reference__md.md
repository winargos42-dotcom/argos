---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/deeptools/assets/quick_reference.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\deeptools\assets\quick_reference.md
source_ext: .md
source_sha256: fa42d3f9f713c61c17dc6a26cbf7b8dd566a16a6e7a7be393984cd7bb93a8b99
text_sha256: 879ce94280160a8197871cbe64bfde41591cd716300b569e50151980ea807274
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:49
---

# quick_reference.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/deeptools/assets/quick_reference.md`
- Extract: `text`
- SHA256: `fa42d3f9f713c61c17dc6a26cbf7b8dd566a16a6e7a7be393984cd7bb93a8b99`

## Content

# deepTools Quick Reference

## Most Common Commands

### BAM to bigWig (normalized)
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing RPGC --effectiveGenomeSize 2913022398 \
    --binSize 10 --numberOfProcessors 8
```

### Compare two BAM files
```bash
bamCompare -b1 treatment.bam -b2 control.bam -o ratio.bw \
    --operation log2 --scaleFactorsMethod readCount
```

### Correlation heatmap
```bash
multiBamSummary bins --bamfiles *.bam -o counts.npz
plotCorrelation -in counts.npz --corMethod pearson \
    --whatToShow heatmap -o correlation.png
```

### Heatmap around TSS
```bash
computeMatrix reference-point -S signal.bw -R genes.bed \
    -b 3000 -a 3000 --referencePoint TSS -o matrix.gz

plotHeatmap -m matrix.gz -o heatmap.png
```

### ChIP enrichment check
```bash
plotFingerprint -b input.bam chip.bam -o fingerprint.png \
    --extendReads 200 --ignoreDuplicates
```

## Effective Genome Sizes

| Organism | Assembly | Size |
|----------|----------|------|
| Human | hg38 | 2913022398 |
| Mouse | mm10 | 2652783500 |
| Fly | dm6 | 142573017 |

## Common Normalization Methods

- **RPGC**: 1× genome coverage (requires --effectiveGenomeSize)
- **CPM**: Counts per million (for fixed bins)
- **RPKM**: Reads per kb per million (for genes)

## Typical Workflow

1. **QC**: plotFingerprint, plotCorrelation
2. **Coverage**: bamCoverage with normalization
3. **Comparison**: bamCompare for treatment vs control
4. **Visualization**: computeMatrix → plotHeatmap/plotProfile

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
