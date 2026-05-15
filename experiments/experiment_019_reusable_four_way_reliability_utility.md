# Experiment 019: Reusable Four-Way Reliability Utility

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Reusable Function](#reusable-function)
- [Dataset](#dataset)
- [Method](#method)
- [Results](#results)
- [Interpretation](#interpretation)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Current Limitations](#current-limitations)
- [Conclusion](#conclusion)

---

## Objective

Verify that the four-way SSDU reliability workflow can be reproduced using reusable source-code utilities in `src/four_way_reliability.py` rather than notebook-only code.

---

## Motivation

The reviewer-defensible reliability workflow separates the acquired k-space into four disjoint subsets:

$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

where:

- $\Theta$ is used for reconstruction input and data consistency.
- $\Lambda_{\mathrm{train}}$ is used for SSDU reconstruction training loss.
- $\Lambda_{\mathrm{cal}}$ is used for calibration-style reliability analysis.
- $\Lambda_{\mathrm{eval}}$ is reserved for final held-out reliability evaluation.

This separation reduces circularity by assigning independent roles to training, calibration, and evaluation. The purpose of this experiment is to confirm that this workflow is correctly implemented in `src/four_way_reliability.py`.

---

## Reusable Function

The function tested was `run_four_way_reliability_experiment()`, which performs the following steps:

| Step | Action |
|------|--------|
| 1 | Select one slice and one coil from real fastMRI brain k-space |
| 2 | Split the acquired mask into four disjoint subsets |
| 3 | Form reconstruction input from $\Theta$ |
| 4 | Train the dropout CNN only on $\Lambda_{\mathrm{train}}$ |
| 5 | Generate stochastic reconstructions using dropout at inference |
| 6 | Compute the mean reconstruction $\bar{x}$ |
| 7 | Compute the voxel-wise uncertainty map $U$ |
| 8 | Compute residual energy on $\Lambda_{\mathrm{cal}}$ |
| 9 | Compute residual energy on $\Lambda_{\mathrm{eval}}$ |
| 10 | Measure uncertainty–residual alignment on both subsets |

---

## Dataset

| Property | Value |
|----------|-------|
| Dataset | fastMRI Brain |
| Acquisition | AXT2 |
| Acceleration | $R = 4$ |
| Working setup | Single-coil-equivalent |
| Slice index | 8 |
| Coil index | 0 |

---

## Method

The acquired mask was partitioned into four disjoint subsets:

$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

The model received only the reconstruction input subset $\Theta$ and was trained using the SSDU loss computed on $\Lambda_{\mathrm{train}}$ only:

$$\mathcal{L}_{\mathrm{train}} = \frac{\left\| M_{\Lambda_{\mathrm{train}}} \odot (\hat{y} - y) \right\|_2^2}{\left\| M_{\Lambda_{\mathrm{train}}} \odot y \right\|_2^2}$$

where:

- $\hat{y}$ is the predicted k-space from the model output.
- $y$ is the measured k-space.
- $M_{\Lambda_{\mathrm{train}}}$ is the binary training subset mask.

After training, dropout was kept active during inference to generate multiple stochastic reconstructions:

$$\hat{x}_1, \hat{x}_2, \ldots, \hat{x}_T$$

The mean reconstruction was computed as:

$$\bar{x} = \frac{1}{T} \sum_{t=1}^{T} \hat{x}_t$$

The voxel-wise uncertainty map was computed as the sample variance:

$$U = \frac{1}{T-1} \sum_{t=1}^{T} \left( \hat{x}_t - \bar{x} \right)^2$$

The held-out residual was computed separately for $\Lambda_{\mathrm{cal}}$ and $\Lambda_{\mathrm{eval}}$:

$$r_{\Lambda} = M_{\Lambda} \odot (\hat{y} - y)$$

where:

- $M_{\Lambda}$ is the binary mask for the relevant subset.
- $r_{\Lambda}$ is the complex-valued held-out k-space residual.

The image-domain residual energy was computed as:

$$E_{\Lambda} = \left| \mathcal{F}^{-1}(r_{\Lambda}) \right|^2$$

where:

- $E_{\Lambda}$ is the image-domain residual energy map.
- $\mathcal{F}^{-1}$ is the inverse Fourier transform.

The spatial alignment between the uncertainty map and each residual energy map was measured using Pearson correlation:

$$\rho(U, E_{\Lambda})$$

---

## Results

| Quantity | Value |
|----------|------:|
| Initial train SSDU loss | `34,236,328` |
| Final train SSDU loss | `20,935,760` |
| Training SSDU reduction | **38.85%** |
| Calibration alignment ($\rho$) | 0.4238 |
| **Evaluation alignment ($\rho$)** | **0.5122** |

---

## Interpretation

The reusable source-code function `run_four_way_reliability_experiment()` reproduced the notebook-based four-way experiment result from [Experiment 018](EXP_018_FOUR_WAY_RELIABILITY_ALIGNMENT.md).

| Implementation | Eval. Alignment ($\rho$) |
|----------------|-------------------------:|
| Notebook-only (Exp 018, slice 8) | 0.512 |
| **Reusable `src/four_way_reliability.py` (this experiment)** | **0.512** |

The positive evaluation alignment is important because $\Lambda_{\mathrm{eval}}$ was not used during model training.

---

## Importance for the Proposed Method

This experiment converts the reviewer-defensible four-way reliability workflow from a notebook demonstration into **reproducible, extensible source code**.

| Component | Status |
|-----------|--------|
| Four-way mask split | ✅ |
| SSDU training on $\Lambda_{\mathrm{train}}$ only | ✅ |
| Stochastic reconstructions and uncertainty map $U$ | ✅ |
| Calibration residual energy $E_{\Lambda_{\mathrm{cal}}}$ | ✅ |
| Evaluation residual energy $E_{\Lambda_{\mathrm{eval}}}$ | ✅ |
| Alignment $\rho(U, E_{\Lambda_{\mathrm{eval}}})$ on held-out samples | ✅ |

The reusable function is now ready for larger-scale experiments across multiple slices and files.

---

## Current Limitations

| Limitation | Detail |
|------------|--------|
| Training data | One file, one slice, one coil |
| Architecture | Simple dropout CNN |
| Reference data | No fully sampled ground truth |
| Coil model | No sensitivity maps |
| Error comparison | No true voxel-wise reconstruction error |
| Scale | No multi-slice or multi-file validation |

---

## Conclusion

The reusable four-way reliability utility in `src/four_way_reliability.py` works correctly and reproduces the expected reliability-alignment result.

**Next step:** use `run_four_way_reliability_experiment()` to run larger slice-level and file-level experiments.
