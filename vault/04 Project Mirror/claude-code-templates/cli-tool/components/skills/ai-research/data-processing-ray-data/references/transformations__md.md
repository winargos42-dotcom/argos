---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/data-processing-ray-data/references/transformations.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\data-processing-ray-data\references\transformations.md
source_ext: .md
source_sha256: 9087b47440bde4e044018ee4dab71254338ec02a68415c380cec1ad79fefe3d5
text_sha256: afc01ade53bc95de6dec6de614b52c6f92eb4a0b141740d937b5dd1855de380d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# transformations.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/data-processing-ray-data/references/transformations.md`
- Extract: `text`
- SHA256: `9087b47440bde4e044018ee4dab71254338ec02a68415c380cec1ad79fefe3d5`

## Content

# Ray Data Transformations

Complete guide to data transformations in Ray Data.

## Core operations

### Map batches (vectorized)

```python
# Recommended for performance
def process_batch(batch):
    # batch is dict of numpy arrays or pandas Series
    batch["doubled"] = batch["value"] * 2
    return batch

ds = ds.map_batches(process_batch, batch_size=1000)
```

**Performance**: 10-100× faster than row-by-row

### Map (row-by-row)

```python
# Use only when vectorization not possible
def process_row(row):
    row["squared"] = row["value"] ** 2
    return row

ds = ds.map(process_row)
```

### Filter

```python
# Remove rows
ds = ds.filter(lambda row: row["score"] > 0.5)
```

### Flat map

```python
# One row → multiple rows
def expand_row(row):
    return [{"value": row["value"] + i} for i in range(3)]

ds = ds.flat_map(expand_row)
```

## GPU-accelerated transforms

```python
def gpu_transform(batch):
    import torch
    data = torch.tensor(batch["data"]).cuda()
    # GPU processing
    result = data * 2
    return {"processed": result.cpu().numpy()}

ds = ds.map_batches(gpu_transform, num_gpus=1, batch_size=64)
```

## Groupby operations

```python
# Group by column
grouped = ds.groupby("category")

# Aggregate
result = grouped.count()

# Custom aggregation
result = grouped.map_groups(lambda group: {
    "sum": group["value"].sum(),
    "mean": group["value"].mean()
})
```

## Best practices

1. **Use map_batches over map** - 10-100× faster
2. **Tune batch_size** - Larger = faster (balance with memory)
3. **Use GPUs for heavy compute** - Image/audio preprocessing
4. **Stream large datasets** - Use iter_batches for >memory data

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
