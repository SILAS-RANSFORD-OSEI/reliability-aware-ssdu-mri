# Experiment 011: Single-Coil SSDU Training Baseline

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Dataset](#dataset)
- [Method](#method)
- [Model](#model)
- [Results](#results)
- [Interpretation](#interpretation)
- [Limitations](#limitations)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Conclusion](#conclusion)

---

## Objective

Test whether a simple CNN reconstruction model can **reduce held-out k-space inconsistency** using an SSDU-style self-supervised training objective.

---

## Motivation

Previous experiments verified the MRI physics pipeline, SSDU mask splitting, held-out residual computation, and basic model forward passes. This experiment is the **first learning-based SSDU reconstruction baseline**.

The goal is not to produce a final high-quality reconstruction, but to confirm that the model can learn from the held-out k-space objective.

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
| Selected slice | Central slice |

A single coil was selected to avoid the need for coil sensitivity estimation at this stage (see [Multicoil SSDU Limitation Note](MULTICOIL_SSDU_LIMITATION_NOTE.md)).

---

## Method

The acquired mask $\Omega$ was split into disjoint subsets:

$$\Omega = \Theta \cup \Lambda, \qquad \Theta \cap \Lambda = \varnothing$$

**Step 1 — Restrict k-space to $\Theta$:**

$$y_{\Theta} = M_{\Theta} \odot y$$

**Step 2 — Zero-filled reconstruction from $\Theta$:**

$$x_{\Theta} = \mathcal{F}^{-1}(y_{\Theta})$$

**Step 3 — CNN reconstruction from normalised magnitude input:**

$$\hat{x} = f_{\theta}(x_{\Theta})$$

**Step 4 — Transform model output back to k-space:**

$$\hat{y} = \mathcal{F}(\hat{x})$$

**Step 5 — Compute normalised SSDU loss on $\Lambda$:**

$$\mathcal{L}_{\mathrm{SSDU}} = \frac{\left\| M_{\Lambda} \odot (\hat{y} - y) \right\|_2^2}{\left\| M_{\Lambda} \odot y \right\|_2^2}$$

**Step 6 — Regularised variant with image-consistency term:**

$$\mathcal{L}_{\mathrm{img}} = \|\hat{x} - x_{\Theta}\|_1$$

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{SSDU}} + \lambda_{\mathrm{img}}\,\mathcal{L}_{\mathrm{img}}, \qquad \lambda_{\mathrm{img}} = 10^7$$

---

## Model

**Model:** `SimpleCNNReconstructor`

Residual learning formulation:

$$\hat{x} = x_{\Theta} + g_{\theta}(x_{\Theta})$$

where $g_{\theta}$ is a small CNN that predicts a correction to the $\Theta$-only zero-filled input.

---

## Results

### Unregularised SSDU Training

| Quantity | Value |
|----------|------:|
| Initial SSDU loss | `10,282,251` |
| Final SSDU loss | `5,179,808.5` |
| Absolute reduction | `5,102,442.5` |
| Percentage reduction | **49.62%** |

### Regularised SSDU Training

| Quantity | Value |
|----------|------:|
| Initial SSDU loss | `10,226,644` |
| Final SSDU loss | `4,972,892.5` |
| Absolute SSDU reduction | `5,253,751.5` |
| Percentage SSDU reduction | **51.37%** |
| Initial image-consistency loss | `0.0585` |
| Final image-consistency loss | `0.0462` |

---

## Interpretation

The SSDU loss decreased by approximately **50%** in both variants, confirming that the CNN successfully optimised the held-out k-space consistency objective. The regularised model reduced the SSDU loss while also constraining the output to remain close to the $\Theta$-only input.

Visual inspection showed that the model preserved gross brain structure, but the correction map remained broad and noisy — the training loop works, but the simple CNN is not yet a reliable reconstruction model.

---

## Limitations

This experiment is a **proof-of-training-baseline**, not the final proposed method.

| Limitation | Detail |
|------------|--------|
| Training data | Single slice, single coil |
| Model | Simple CNN — no physics-based data consistency |
| Coil model | No coil sensitivity maps |
| Reference data | No fully sampled ground truth |
| Metrics | NMSE, PSNR, SSIM not evaluated |
| Uncertainty | Not yet estimated |

---

## Importance for the Proposed Method

This experiment verifies the full end-to-end SSDU training pipeline for the first time:

| Step | Component |
|------|-----------|
| 1 | Real fastMRI k-space loading |
| 2 | SSDU $\Theta$ / $\Lambda$ mask split |
| 3 | $\Theta$-only zero-filled reconstruction input |
| 4 | CNN reconstruction model |
| 5 | Fourier transform of model output |
| 6 | Held-out $\Lambda$ consistency loss |
| 7 | Decreasing self-supervised training objective ✅ |

This pipeline is the **foundation** before adding stochastic reconstruction and uncertainty calibration.

---

## Conclusion

The single-coil-equivalent SSDU baseline successfully reduced held-out k-space loss by ~50%, confirming the end-to-end self-supervised training loop.

**Next steps:**

| Priority | Action |
|----------|--------|
| Immediate | Build a stable, reusable multi-slice training pipeline |
| Follow-up | Extend toward stochastic reconstruction and voxel-wise uncertainty estimation |
| Future | Add coil sensitivity maps for full multicoil SSDU |
