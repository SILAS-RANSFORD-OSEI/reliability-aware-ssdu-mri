# Experiment 012: Reusable SSDU Training Utility Test

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Method](#method)
- [Results](#results)
- [Interpretation](#interpretation)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Current Limitations](#current-limitations)
- [Conclusion](#conclusion)

---

## Objective

Verify that the SSDU training logic can be moved from notebook-only code into **reusable source-code utilities**.

---

## Motivation

For a publishable reconstruction method, the training pipeline must not exist only as temporary notebook cells. This experiment confirms that the reusable module `src/training.py` reproduces the same single-coil SSDU learning behaviour observed in [Experiment 011](EXP_011_SINGLE_COIL_SSDU_TRAINING.md).

---

## Method

The reusable training utilities performed the following operations:

| Step | Action |
|------|--------|
| 1 | Prepare single-coil $\Theta$-only input image |
| 2 | Convert to PyTorch tensor |
| 3 | Forward pass through `SimpleCNNReconstructor` |
| 4 | Transform model output to k-space via differentiable FFT |
| 5 | Compute normalised SSDU loss on $\Lambda$ |
| 6 | Add image-domain consistency regularisation |
| 7 | Optimise for 50 training steps |

**Total loss:**

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{SSDU}} + \lambda_{\mathrm{img}}\,\mathcal{L}_{\mathrm{img}}, \qquad \lambda_{\mathrm{img}} = 10^7$$

---

## Results

| Quantity | Value |
|----------|------:|
| Initial SSDU loss | `10,367,565` |
| Final SSDU loss | `5,188,101.5` |
| Absolute SSDU reduction | `5,179,463.5` |
| Percentage SSDU reduction | **49.96%** |
| Initial image-consistency loss | `0.00332` |
| Final image-consistency loss | `0.01763` |

---

## Interpretation

The reusable training utilities reproduced the ~50% SSDU loss reduction observed in Experiment 011, confirming that `src/training.py` correctly implements:

| Component | Status |
|-----------|--------|
| Single-coil SSDU input preparation | ✅ |
| Differentiable Fourier-domain loss | ✅ |
| Image-consistency regularisation | ✅ |
| Gradient-based optimisation | ✅ |

The increase in image-consistency loss indicates that the model moved away from the $\Theta$-only input while reducing held-out k-space inconsistency — an expected trade-off at this stage.

---

## Importance for the Proposed Method

This experiment converts the SSDU training baseline from exploratory notebook code into **reproducible method code**, which is required for:

| Requirement | Description |
|-------------|-------------|
| Reproducibility | Consistent results across runs and environments |
| Scale | Larger multi-slice and multi-file training |
| Extensibility | Adding stochastic reconstruction and uncertainty estimation |
| Publication | Method implementation suitable for the paper |

---

## Current Limitations

This remains a single-coil-equivalent baseline. The following components are not yet included:

| Missing Component | Detail |
|-------------------|--------|
| Multicoil sensitivity modelling | No coil sensitivity maps ($S_c$) |
| Improved architecture | No U-Net or unrolled reconstruction |
| Stochastic reconstruction | No MC dropout or ensemble sampling |
| Uncertainty estimation | No voxel-wise variance map |
| Uncertainty calibration | No $\mathcal{L}_{\mathrm{cal}}$ against $E_{\mathrm{img}}$ |

---

## Conclusion

The reusable SSDU training utilities in `src/training.py` work correctly and reproduce the expected learning behaviour from Experiment 011.

**Next step:** improve the reconstruction baseline and prepare for stochastic reconstruction and uncertainty estimation.
