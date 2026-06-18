---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/aeon/references/regression.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\aeon\references\regression.md
source_ext: .md
source_sha256: 019157cd54f6b146e6fa89d7f60f958edb9bfba5c8b25022483ffefcf0c0cf63
text_sha256: 39ccf444ec621c1e4c89fe4ba56db5d5b7b3c55bce12cd4035fd6451f734c294
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# regression.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/aeon/references/regression.md`
- Extract: `text`
- SHA256: `019157cd54f6b146e6fa89d7f60f958edb9bfba5c8b25022483ffefcf0c0cf63`

## Content

# Time Series Regression

Aeon provides time series regressors across 9 categories for predicting continuous values from temporal sequences.

## Convolution-Based Regressors

Apply convolutional kernels for feature extraction:

- `HydraRegressor` - Multi-resolution dilated convolutions
- `RocketRegressor` - Random convolutional kernels
- `MiniRocketRegressor` - Simplified ROCKET for speed
- `MultiRocketRegressor` - Combined ROCKET variants
- `MultiRocketHydraRegressor` - Merges ROCKET and Hydra approaches

**Use when**: Need fast regression with strong baseline performance.

## Deep Learning Regressors

Neural architectures for end-to-end temporal regression:

- `FCNRegressor` - Fully convolutional network
- `ResNetRegressor` - Residual blocks with skip connections
- `InceptionTimeRegressor` - Multi-scale inception modules
- `TimeCNNRegressor` - Standard CNN architecture
- `RecurrentRegressor` - RNN/LSTM/GRU variants
- `MLPRegressor` - Multi-layer perceptron
- `EncoderRegressor` - Generic encoder wrapper
- `LITERegressor` - Lightweight inception time ensemble
- `DisjointCNNRegressor` - Specialized CNN architecture

**Use when**: Large datasets, complex patterns, or need feature learning.

## Distance-Based Regressors

k-nearest neighbors with temporal distance metrics:

- `KNeighborsTimeSeriesRegressor` - k-NN with DTW, LCSS, ERP, or other distances

**Use when**: Small datasets, local similarity patterns, or interpretable predictions.

## Feature-Based Regressors

Extract statistical features before regression:

- `Catch22Regressor` - 22 canonical time-series characteristics
- `FreshPRINCERegressor` - Pipeline combining multiple feature extractors
- `SummaryRegressor` - Summary statistics features
- `TSFreshRegressor` - Automated tsfresh feature extraction

**Use when**: Need interpretable features or domain-specific feature engineering.

## Hybrid Regressors

Combine multiple approaches:

- `RISTRegressor` - Randomized Interval-Shapelet Transformation

**Use when**: Benefit from combining interval and shapelet methods.

## Interval-Based Regressors

Extract features from time intervals:

- `CanonicalIntervalForestRegressor` - Random intervals with decision trees
- `DrCIFRegressor` - Diverse Representation CIF
- `TimeSeriesForestRegressor` - Random interval ensemble
- `RandomIntervalRegressor` - Simple interval-based approach
- `RandomIntervalSpectralEnsembleRegressor` - Spectral interval features
- `QUANTRegressor` - Quantile-based interval features

**Use when**: Predictive patterns occur in specific time windows.

## Shapelet-Based Regressors

Use discriminative subsequences for prediction:

- `RDSTRegressor` - Random Dilated Shapelet Transform

**Use when**: Need phase-invariant discriminative patterns.

## Composition Tools

Build custom regression pipelines:

- `RegressorPipeline` - Chain transformers with regressors
- `RegressorEnsemble` - Weighted ensemble with learnable weights
- `SklearnRegressorWrapper` - Adapt sklearn regressors for time series

## Utilities

- `DummyRegressor` - Baseline strategies (mean, median)
- `BaseRegressor` - Abstract base for custom regressors
- `BaseDeepRegressor` - Base for deep learning regressors

## Quick Start

```python
from aeon.regression.convolution_based import RocketRegressor
from aeon.datasets import load_regression

# Load data
X_train, y_train = load_regression("Covid3Month", split="train")
X_test, y_test = load_regression("Covid3Month", split="test")

# Train and predict
reg = RocketRegressor()
reg.fit(X_train, y_train)
predictions = reg.predict(X_test)
```

## Algorithm Selection

- **Speed priority**: MiniRocketRegressor
- **Accuracy priority**: InceptionTimeRegressor, MultiRocketHydraRegressor
- **Interpretability**: Catch22Regressor, SummaryRegressor
- **Small data**: KNeighborsTimeSeriesRegressor
- **Large data**: Deep learning regressors, ROCKET variants
- **Interval patterns**: DrCIFRegressor, CanonicalIntervalForestRegressor

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
