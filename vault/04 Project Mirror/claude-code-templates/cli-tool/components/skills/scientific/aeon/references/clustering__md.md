---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/aeon/references/clustering.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\aeon\references\clustering.md
source_ext: .md
source_sha256: f89832c5876fd34eddf99989056f8d0a5fdef36adaa92f18f6b1ace1081e11a4
text_sha256: ab2635b7d55ae727bc027c0b0f21dc65167c35b0379acbd19396db82594c2832
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# clustering.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/aeon/references/clustering.md`
- Extract: `text`
- SHA256: `f89832c5876fd34eddf99989056f8d0a5fdef36adaa92f18f6b1ace1081e11a4`

## Content

# Time Series Clustering

Aeon provides clustering algorithms adapted for temporal data with specialized distance metrics and averaging methods.

## Partitioning Algorithms

Standard k-means/k-medoids adapted for time series:

- `TimeSeriesKMeans` - K-means with temporal distance metrics (DTW, Euclidean, etc.)
- `TimeSeriesKMedoids` - Uses actual time series as cluster centers
- `TimeSeriesKShape` - Shape-based clustering algorithm
- `TimeSeriesKernelKMeans` - Kernel-based variant for nonlinear patterns

**Use when**: Known number of clusters, spherical cluster shapes expected.

## Large Dataset Methods

Efficient clustering for large collections:

- `TimeSeriesCLARA` - Clustering Large Applications with sampling
- `TimeSeriesCLARANS` - Randomized search variant of CLARA

**Use when**: Dataset too large for standard k-medoids, need scalability.

## Elastic Distance Clustering

Specialized for alignment-based similarity:

- `KASBA` - K-means with shift-invariant elastic averaging
- `ElasticSOM` - Self-organizing map using elastic distances

**Use when**: Time series have temporal shifts or warping.

## Spectral Methods

Graph-based clustering:

- `KSpectralCentroid` - Spectral clustering with centroid computation

**Use when**: Non-convex cluster shapes, need graph-based approach.

## Deep Learning Clustering

Neural network-based clustering with auto-encoders:

- `AEFCNClusterer` - Fully convolutional auto-encoder
- `AEResNetClusterer` - Residual network auto-encoder
- `AEDCNNClusterer` - Dilated CNN auto-encoder
- `AEDRNNClusterer` - Dilated RNN auto-encoder
- `AEBiGRUClusterer` - Bidirectional GRU auto-encoder
- `AEAttentionBiGRUClusterer` - Attention-enhanced BiGRU auto-encoder

**Use when**: Large datasets, need learned representations, or complex patterns.

## Feature-Based Clustering

Transform to feature space before clustering:

- `Catch22Clusterer` - Clusters on 22 canonical features
- `SummaryClusterer` - Uses summary statistics
- `TSFreshClusterer` - Automated tsfresh features

**Use when**: Raw time series not informative, need interpretable features.

## Composition

Build custom clustering pipelines:

- `ClustererPipeline` - Chain transformers with clusterers

## Averaging Methods

Compute cluster centers for time series:

- `mean_average` - Arithmetic mean
- `ba_average` - Barycentric averaging with DTW
- `kasba_average` - Shift-invariant averaging
- `shift_invariant_average` - General shift-invariant method

**Use when**: Need representative cluster centers for visualization or initialization.

## Quick Start

```python
from aeon.clustering import TimeSeriesKMeans
from aeon.datasets import load_classification

# Load data (using classification data for clustering)
X_train, _ = load_classification("GunPoint", split="train")

# Cluster time series
clusterer = TimeSeriesKMeans(
    n_clusters=3,
    distance="dtw",  # Use DTW distance
    averaging_method="ba"  # Barycentric averaging
)
labels = clusterer.fit_predict(X_train)
centers = clusterer.cluster_centers_
```

## Algorithm Selection

- **Speed priority**: TimeSeriesKMeans with Euclidean distance
- **Temporal alignment**: KASBA, TimeSeriesKMeans with DTW
- **Large datasets**: TimeSeriesCLARA, TimeSeriesCLARANS
- **Complex patterns**: Deep learning clusterers
- **Interpretability**: Catch22Clusterer, SummaryClusterer
- **Non-convex clusters**: KSpectralCentroid

## Distance Metrics

Compatible distance metrics include:
- Euclidean, Manhattan, Minkowski (lock-step)
- DTW, DDTW, WDTW (elastic with alignment)
- ERP, EDR, LCSS (edit-based)
- MSM, TWE (specialized elastic)

## Evaluation

Use clustering metrics from sklearn or aeon benchmarking:
- Silhouette score
- Davies-Bouldin index
- Calinski-Harabasz index

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
