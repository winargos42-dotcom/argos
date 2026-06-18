---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/geopandas/references/data-structures.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\geopandas\references\data-structures.md
source_ext: .md
source_sha256: 48db8cc01b26b234bba1f42e606bfc427bfdd32e88a0fa810e6e762e314b33d0
text_sha256: 9cd950173409b04e3c57b40b24e296646931de938ebcc86b8bf6806a97fcaab8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:49
---

# data-structures.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/geopandas/references/data-structures.md`
- Extract: `text`
- SHA256: `48db8cc01b26b234bba1f42e606bfc427bfdd32e88a0fa810e6e762e314b33d0`

## Content

# GeoPandas Data Structures

## GeoSeries

A GeoSeries is a vector where each entry is a set of shapes corresponding to one observation (similar to a pandas Series but with geometric data).

```python
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Create a GeoSeries from geometries
points = gpd.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)])

# Access geometric properties
points.area
points.length
points.bounds
```

## GeoDataFrame

A GeoDataFrame is a tabular data structure that contains a GeoSeries (similar to a pandas DataFrame but with geographic data).

```python
# Create from dictionary
gdf = gpd.GeoDataFrame({
    'name': ['Point A', 'Point B'],
    'value': [100, 200],
    'geometry': [Point(1, 1), Point(2, 2)]
})

# Create from pandas DataFrame with coordinates
import pandas as pd
df = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 2, 3], 'name': ['A', 'B', 'C']})
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x, df.y))
```

## Key Properties

- **geometry**: The active geometry column (can have multiple geometry columns)
- **crs**: Coordinate reference system
- **bounds**: Bounding box of all geometries
- **total_bounds**: Overall bounding box

## Setting Active Geometry

When a GeoDataFrame has multiple geometry columns:

```python
# Set active geometry column
gdf = gdf.set_geometry('other_geom_column')

# Check active geometry column
gdf.geometry.name
```

## Indexing and Selection

Use standard pandas indexing with spatial data:

```python
# Select by label
gdf.loc[0]

# Boolean indexing
large_areas = gdf[gdf.area > 100]

# Select columns
gdf\[\['name', 'geometry'\]\]
```

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
