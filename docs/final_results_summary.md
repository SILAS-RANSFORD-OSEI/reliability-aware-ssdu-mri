


# Figure 3 Summary — Experiment 029

## Overview
Experiment 029 evaluated the learned ReliabilityCNN across 80 slice-level experiments from 5 held-out test volumes and 5 folds.

## Main evaluation alignment results
- ReliabilityCNN: 0.571 ± 0.047
- Input intensity baseline: 0.558 ± 0.050
- Mean intensity baseline: 0.498 ± 0.055
- Edge baseline: 0.400 ± 0.057
- Dropout baseline: 0.490 ± 0.061

## Margin analysis
- Net minus input: 0.013 ± 0.027
- Net minus dropout: 0.081 ± 0.038
- Net minus edge: 0.171 ± 0.047

## Interpretation
The learned ReliabilityCNN is clearly better than the edge-based and dropout-based baselines on average, but it remains competitive with, rather than decisively better than, the strongest structural intensity baselines.
