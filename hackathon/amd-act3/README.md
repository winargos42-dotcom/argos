# ARGOS-MUKHTAR — AMD ACT III

Reproducible hackathon track for the existing ARGOS-MUKHTAR bio-inspired edge-AI stack.

## Pipeline
AMD GPU / ROCm -> train + benchmark teacher/student -> quantize/distill -> Coral Edge TPU -> Mukhtar BioCore -> action.

## Evidence policy
Only measured runs are reported. Existing Coral results are kept separate from future AMD/ROCm measurements. No AMD result is claimed until generated on an AMD runtime.

## Success criteria
- AMD/ROCm training or inference run with captured environment metadata.
- Exported student artifact with checksum and reproducible config.
- Edge TPU inference benchmark using the same frozen evaluation inputs.
- End-to-end BioCore action output and latency report.
- Comparison JSON/Markdown generated from raw result files.

## Layout
- `configs/` frozen experiment definitions
- `scripts/` environment and benchmark runners
- `results/` raw machine-readable measurements
- `benchmarks/` generated comparisons
