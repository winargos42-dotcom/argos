---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/data-processing-nemo-curator/references/filtering.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\data-processing-nemo-curator\references\filtering.md
source_ext: .md
source_sha256: f495d93b074a468ffbd3eda6a4a1ba9ded548cf966e0776f42e669667f597599
text_sha256: d02c933f79b140c65e88a5af1567aa47a6cbf8eed522d8eae5ef977daf346f0a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# filtering.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/data-processing-nemo-curator/references/filtering.md`
- Extract: `text`
- SHA256: `f495d93b074a468ffbd3eda6a4a1ba9ded548cf966e0776f42e669667f597599`

## Content

# Quality Filtering Guide

Complete guide to NeMo Curator's 30+ quality filters.

## Text-based filters

### Word count

```python
from nemo_curator.filters import WordCountFilter

# Filter by word count
dataset = dataset.filter(WordCountFilter(min_words=50, max_words=100000))
```

### Repeated content

```python
from nemo_curator.filters import RepeatedLinesFilter

# Remove documents with >30% repeated lines
dataset = dataset.filter(RepeatedLinesFilter(max_repeated_line_fraction=0.3))
```

### Symbol ratio

```python
from nemo_curator.filters import SymbolToWordRatioFilter

# Remove documents with too many symbols
dataset = dataset.filter(SymbolToWordRatioFilter(max_symbol_to_word_ratio=0.3))
```

### URL ratio

```python
from nemo_curator.filters import UrlRatioFilter

# Remove documents with many URLs
dataset = dataset.filter(UrlRatioFilter(max_url_ratio=0.2))
```

## Language filtering

```python
from nemo_curator.filters import LanguageIdentificationFilter

# Keep only English documents
dataset = dataset.filter(LanguageIdentificationFilter(target_languages=["en"]))

# Multiple languages
dataset = dataset.filter(LanguageIdentificationFilter(target_languages=["en", "es", "fr"]))
```

## Classifier-based filtering

### Quality classifier

```python
from nemo_curator.classifiers import QualityClassifier

quality_clf = QualityClassifier(
    model_path="nvidia/quality-classifier-deberta",
    batch_size=256,
    device="cuda"
)

# Filter low-quality (threshold > 0.5 = high quality)
dataset = dataset.filter(lambda doc: quality_clf(doc["text"]) > 0.5)
```

### NSFW classifier

```python
from nemo_curator.classifiers import NSFWClassifier

nsfw_clf = NSFWClassifier(threshold=0.9, device="cuda")

# Remove NSFW content
dataset = dataset.filter(lambda doc: nsfw_clf(doc["text"]) < 0.9)
```

## Heuristic filters

Full list of 30+ filters:
- WordCountFilter
- RepeatedLinesFilter
- UrlRatioFilter
- SymbolToWordRatioFilter
- NonAlphaNumericFilter
- BulletsFilter
- WhiteSpaceFilter
- ParenthesesFilter
- LongWordFilter
- And 20+ more...

## Best practices

1. **Apply cheap filters first** - Word count before GPU classifiers
2. **Tune thresholds on sample** - Test on 10k docs before full run
3. **Use GPU classifiers sparingly** - Expensive but effective
4. **Chain filters efficiently** - Order by cost (cheap → expensive)

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
