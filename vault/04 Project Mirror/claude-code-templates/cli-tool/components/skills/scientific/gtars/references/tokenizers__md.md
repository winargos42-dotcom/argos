---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/gtars/references/tokenizers.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\gtars\references\tokenizers.md
source_ext: .md
source_sha256: e5a86d81b28c0db63a425924c087f8972f57a30ea0653c409d927a35d586b3a9
text_sha256: 59857435cccf49c0c3c5e50d918206eadb95ec2d3ee237180a70724e4bdd3a82
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:50
---

# tokenizers.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/gtars/references/tokenizers.md`
- Extract: `text`
- SHA256: `e5a86d81b28c0db63a425924c087f8972f57a30ea0653c409d927a35d586b3a9`

## Content

# Genomic Tokenizers

Tokenizers convert genomic regions into discrete tokens for machine learning applications, particularly useful for training genomic deep learning models.

## Python API

### Creating a Tokenizer

Load tokenizer configurations from various sources:

```python
import gtars

# From BED file
tokenizer = gtars.tokenizers.TreeTokenizer.from_bed_file("regions.bed")

# From configuration file
tokenizer = gtars.tokenizers.TreeTokenizer.from_config("tokenizer_config.yaml")

# From region string
tokenizer = gtars.tokenizers.TreeTokenizer.from_region_string("chr1:1000-2000")
```

### Tokenizing Genomic Regions

Convert genomic coordinates to tokens:

```python
# Tokenize a single region
token = tokenizer.tokenize("chr1", 1000, 2000)

# Tokenize multiple regions
tokens = []
for chrom, start, end in regions:
    token = tokenizer.tokenize(chrom, start, end)
    tokens.append(token)
```

### Token Properties

Access token information:

```python
# Get token ID
token_id = token.id

# Get genomic coordinates
chrom = token.chromosome
start = token.start
end = token.end

# Get token metadata
metadata = token.metadata
```

## Use Cases

### Machine Learning Preprocessing

Tokenizers are essential for preparing genomic data for ML models:

1. **Sequence modeling**: Convert genomic intervals into discrete tokens for transformer models
2. **Position encoding**: Create consistent positional encodings across datasets
3. **Data augmentation**: Generate alternative tokenizations for training

### Integration with geniml

The tokenizers module integrates seamlessly with the geniml library for genomic ML:

```python
# Tokenize regions for geniml
from gtars.tokenizers import TreeTokenizer
import geniml

tokenizer = TreeTokenizer.from_bed_file("training_regions.bed")
tokens = [tokenizer.tokenize(r.chrom, r.start, r.end) for r in regions]

# Use tokens in geniml models
model = geniml.Model(vocab_size=tokenizer.vocab_size)
```

## Configuration Format

Tokenizer configuration files support YAML format:

```yaml
# tokenizer_config.yaml
type: tree
resolution: 1000  # Token resolution in base pairs
chromosomes:
  - chr1
  - chr2
  - chr3
options:
  overlap_handling: merge
  gap_threshold: 100
```

## Performance Considerations

- TreeTokenizer uses efficient data structures for fast tokenization
- Batch tokenization is recommended for large datasets
- Pre-loading tokenizers reduces overhead for repeated operations

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
