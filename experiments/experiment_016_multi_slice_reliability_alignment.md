# Experiment 016: Multi-Slice Reliability Alignment

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Dataset](#dataset)
- [Method](#method)
- [Results](#results)
- [Interpretation](#interpretation)
- [Reviewer-Level Caution](#reviewer-level-caution)
- [Current Limitations](#current-limitations)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Conclusion](#conclusion)

---

## Objective

Evaluate whether dropout-derived uncertainty aligns with backprojected held-out k-space residual energy **across multiple brain MRI slices**.

---

## Motivation

Previous experiments ([Exp 013](EXP_013_DROPOUT_UNCERTAINTY_ALIGNMENT.md), [Exp 014](EXP_014_REUSABLE_RELIABILITY_WORKFLOW.md)) showed promising uncertainty–residual alignment on a single slice. A reviewer would ask whether this result is repeatable across different slices.

This experiment tests early repeatability by applying the same reliability workflow to **three slices** from the same fastMRI brain file.

---

## Dataset

| Property | Value |
|----------|-------|
| Dataset | fastMRI Brain |
| Data type | Multicoil source file |
| Working setup | Single-coil-equivalent baseline |
| Acquisition | AXT2 |
| Acceleration | $R = 4$ |
| Selected coil | Coil 0 |
| Tested slices | 4, 8, 12 |

---

## Method

For each slice, one coil was selected to form a single-coil-equivalent reconstruction.

The acquired k-space mask was split into two disjoint subsets:

$$\Omega = \Theta \cup \Lambda$$

with:

$$\Theta \cap \Lambda = \varnothing$$

where:

- $\Theta$ is used for reconstruction input and data consistency.
- $\Lambda$ is held out for the self-supervised loss.

The measured k-space was restricted to $\Theta$:

$$y_{\Theta} = M_{\Theta} \odot y$$

The zero-filled reconstruction from $\Theta$ was used as the model input:

$$x_{\Theta} = \mathcal{F}^{-1}(y_{\Theta})$$

A dropout CNN was trained using the SSDU held-out loss on $\Lambda$. After training, dropout was kept active during inference to generate multiple stochastic reconstructions:

$$\hat{x}_1, \hat{x}_2, \ldots, \hat{x}_T$$

with:

$$T = 8$$

The mean reconstruction was computed as:

$$\bar{x} = \frac{1}{T} \sum_{t=1}^{T} \hat{x}_t$$

The voxel-wise uncertainty map was computed as the sample variance:

$$U = \frac{1}{T-1} \sum_{t=1}^{T} \left( \hat{x}_t - \bar{x} \right)^2$$

where:

- $U$ is the voxel-wise uncertainty map.
- $\bar{x}$ is the mean reconstruction.
- High values of $U$ indicate regions where the model is less certain.

The mean reconstruction was projected back into k-space:

$$\hat{y} = \mathcal{F}(\bar{x})$$

The held-out $\Lambda$ residual was computed as:

$$r_{\Lambda} = M_{\Lambda} \odot \left( \hat{y} - y \right)$$

where:

- $r_{\Lambda}$ is the complex-valued held-out k-space residual.
- $M_{\Lambda}$ is the binary held-out $\Lambda$ mask.
- $\hat{y}$ is the predicted k-space from the mean reconstruction.
- $y$ is the measured k-space.

The residual was backprojected into the image domain:

$$E_{\Lambda} = \left| \mathcal{F}^{-1}(r_{\Lambda}) \right|^2$$

where:

- $E_{\Lambda}$ is the image-domain residual energy map.
- $\mathcal{F}^{-1}$ is the inverse Fourier transform.

The spatial alignment between the uncertainty map and the image-domain residual energy was measured using Pearson correlation:

$$\rho(U, E_{\Lambda})$$

---

## Results

### Per-Slice Results

| Slice | Initial SSDU Loss | Final SSDU Loss | SSDU Reduction (%) | Alignment ($\rho$) |
|------:|------------------:|----------------:|-------------------:|-------------------:|
| 4 | `23,658,390` | `20,539,922` | 13.18% | 0.613 |
| 8 | `10,912,285` | `9,636,117` | 11.69% | 0.661 |
| 12 | `17,030,082` | `14,746,922` | 13.41% | 0.751 |

### Summary Statistics

| Quantity | Value |
|----------|------:|
| Mean SSDU reduction | 12.76% |
| Std SSDU reduction | 0.93% |
| **Mean alignment** | **0.675** |
| Std alignment | 0.070 |
| Minimum alignment | 0.613 |
| Maximum alignment | 0.751 |

---

## Interpretation

Uncertainty–residual alignment remained **positive across all three slices**, with mean alignment:

$$\bar{\rho} = 0.675 \pm 0.070$$

Compare to the random-noise baseline from [Experiments 007–008](EXP_007_ARTIFICIAL_UNCERTAINTY_UTILITY_TEST.md) ($\rho \approx 0$) and the single-slice results from Experiments 013–014 ($\rho \approx 0.70$) — the alignment is consistent and well above chance.

This supports the feasibility of the project's central idea:

> **Held-out k-space inconsistency can provide a self-supervised reliability signal for uncertainty-aware MRI reconstruction.**

---

## Reviewer-Level Caution

This result supports **reliability alignment**, not full calibrated uncertainty. It does not yet demonstrate:

| Claim | Status |
|-------|--------|
| Clinical reliability | ❌ Not shown |
| True image-error calibration | ❌ No fully sampled reference |
| Multicoil reconstruction validity | ❌ Single-coil-equivalent only |
| Robustness across subjects | ❌ One file tested |
| Superiority over existing baselines | ❌ Not compared |

The result should be described as **early repeatability evidence**, not a validated method.

---

## Current Limitations

| Limitation | Detail |
|------------|--------|
| Training data | One fastMRI file, three slices |
| Coil model | Single-coil-equivalent — no sensitivity maps |
| Architecture | Simple dropout CNN |
| Reference data | No fully sampled ground truth |
| Error comparison | No true voxel-wise reconstruction error |
| Scale | No cross-subject or cross-acquisition validation |

---

## Importance for the Proposed Method

This is the **strongest current feasibility result** — uncertainty–residual alignment is not limited to a single slice.

The result justifies the next methodological upgrade: splitting the acquired mask into four disjoint subsets:

$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

| Subset | Role |
|--------|------|
| $\Theta$ | Reconstruction input / data consistency |
| $\Lambda_{\mathrm{train}}$ | Self-supervised reconstruction loss |
| $\Lambda_{\mathrm{cal}}$ | Uncertainty calibration signal |
| $\Lambda_{\mathrm{eval}}$ | Final reliability evaluation |

This separation will allow reconstruction training, uncertainty calibration, and evaluation to be performed on independent held-out measurements.

---

## Conclusion

Across three brain MRI slices, dropout-derived uncertainty showed moderate-to-strong positive alignment with backprojected held-out residual energy ($\bar{\rho} = 0.675 \pm 0.070$).

This supports continuing the project toward a reviewer-defensible reliability-aware SSDU framework.

**Next step:** implement the four-way mask split $(\Theta,\ \Lambda_{\mathrm{train}},\ \Lambda_{\mathrm{cal}},\ \Lambda_{\mathrm{eval}})$ and test whether dedicated calibration and evaluation subsets produce more precise reliability estimates.
