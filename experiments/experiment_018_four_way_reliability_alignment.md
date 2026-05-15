# Experiment 018: Four-Way Reliability Alignment

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Dataset](#dataset)
- [Method](#method)
- [Results](#results)
- [Interpretation](#interpretation)
- [Reviewer-Level Significance](#reviewer-level-significance)
- [Current Limitations](#current-limitations)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Conclusion](#conclusion)

---

## Objective

Evaluate uncertainty–residual alignment using a four-way SSDU split that separates reconstruction input, training loss, calibration analysis, and final reliability evaluation into independent subsets.

---

## Motivation

Earlier experiments used a two-way SSDU split:

$$\Omega = \Theta \cup \Lambda$$

where:

- $\Theta$ was used for reconstruction input.
- $\Lambda$ was used for held-out loss and reliability analysis.

This was useful for feasibility testing, but the same held-out set served multiple roles simultaneously. To make the method more reviewer-defensible, the acquired k-space mask is now split into four disjoint subsets:

$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

where:

- $\Theta$ is used as reconstruction input.
- $\Lambda_{\mathrm{train}}$ is used for SSDU training loss.
- $\Lambda_{\mathrm{cal}}$ is used for calibration-style reliability analysis.
- $\Lambda_{\mathrm{eval}}$ is reserved for final reliability evaluation.

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

For each slice, a single coil was selected to form a single-coil-equivalent reconstruction.

The acquired mask was split into four disjoint subsets:

$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

The reconstruction input was formed from $\Theta$:

$$y_{\Theta} = M_{\Theta} \odot y$$

$$x_{\Theta} = \mathcal{F}^{-1}(y_{\Theta})$$

A dropout CNN was trained using only $\Lambda_{\mathrm{train}}$:

$$\mathcal{L}_{\mathrm{train}} = \frac{\left\| M_{\Lambda_{\mathrm{train}}} \odot (\hat{y} - y) \right\|_2^2}{\left\| M_{\Lambda_{\mathrm{train}}} \odot y \right\|_2^2}$$

where:

- $\hat{y}$ is the predicted k-space from the model output.
- $y$ is the measured k-space.
- $M_{\Lambda_{\mathrm{train}}}$ is the binary training subset mask.

After training, dropout was kept active during inference to generate multiple stochastic reconstructions:

$$\hat{x}_1, \hat{x}_2, \ldots, \hat{x}_T$$

with:

$$T = 8$$

The mean reconstruction was computed as:

$$\bar{x} = \frac{1}{T} \sum_{t=1}^{T} \hat{x}_t$$

The voxel-wise uncertainty map was computed as the sample variance:

$$U = \frac{1}{T-1} \sum_{t=1}^{T} \left( \hat{x}_t - \bar{x} \right)^2$$

The held-out residual was computed separately for $\Lambda_{\mathrm{cal}}$ and $\Lambda_{\mathrm{eval}}$:

$$r_{\Lambda} = M_{\Lambda} \odot (\hat{y} - y)$$

where:

- $M_{\Lambda}$ is the binary mask for the relevant subset ($\Lambda_{\mathrm{cal}}$ or $\Lambda_{\mathrm{eval}}$).
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

### Per-Slice Results

| Slice | Initial Train Loss | Final Train Loss | Train Reduction (%) | Cal. Alignment ($\rho$) | Eval. Alignment ($\rho$) |
|------:|-------------------:|-----------------:|--------------------:|------------------------:|-------------------------:|
| 4 | `77,422,928` | `40,357,816` | 47.87% | 0.393 | 0.405 |
| 8 | `34,236,328` | `20,935,760` | 38.85% | 0.424 | 0.512 |
| 12 | `55,932,464` | `35,439,100` | 36.64% | 0.433 | 0.518 |

### Summary Statistics

| Quantity | Value |
|----------|------:|
| Mean training SSDU reduction | 41.12% |
| Std training SSDU reduction | 5.95% |
| Mean calibration alignment | 0.416 |
| Std calibration alignment | 0.021 |
| **Mean evaluation alignment** | **0.478** |
| Std evaluation alignment | 0.064 |
| Minimum evaluation alignment | 0.405 |
| Maximum evaluation alignment | 0.518 |

---

## Interpretation

The model was trained only on $\Lambda_{\mathrm{train}}$. Despite this, uncertainty remained positively aligned with residual energy on $\Lambda_{\mathrm{eval}}$, which was not used during training.

The mean evaluation alignment was:

$$\bar{\rho}_{\mathrm{eval}} = 0.478 \pm 0.064$$

This is lower than the earlier two-way SSDU alignment ($\bar{\rho} = 0.675$), but it is more scientifically defensible because training and evaluation are now fully separated.

---

## Reviewer-Level Significance

This experiment directly addresses the concern that the same held-out k-space samples should not be used for training, calibration, and evaluation simultaneously.

The result supports the following cautious, defensible claim:

> **Even under a four-way SSDU split, dropout-derived uncertainty remains positively associated with held-out residual energy on evaluation samples not used during training.**

This is reliability-alignment evidence, not full uncertainty calibration.

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

This result strengthens feasibility but is not yet final journal-level validation.

---

## Importance for the Proposed Method

This experiment upgrades the project from a two-way SSDU feasibility test to a **reviewer-defensible four-way reliability framework**.

| Split | Purpose |
|-------|---------|
| Two-way $(\Theta, \Lambda)$ | Feasibility testing — Experiments 011–016 |
| **Four-way $(\Theta, \Lambda_{\mathrm{train}}, \Lambda_{\mathrm{cal}}, \Lambda_{\mathrm{eval}})$** | **Reviewer-defensible method — this experiment onward** |

The four-way split enables independent separation of reconstruction learning, uncertainty calibration, and final reliability evaluation — strengthening the path toward a publishable reliability-aware self-supervised MRI reconstruction method.

---

## Conclusion

The four-way SSDU reliability experiment produced positive evaluation alignment ($\bar{\rho}_{\mathrm{eval}} = 0.478 \pm 0.064$) across three slices, on held-out measurements not used during training.

**Next steps:**

| Priority | Action |
|----------|--------|
| Immediate | Scale testing to more slices and files |
| Follow-up | Develop stronger uncertainty calibration using $\Lambda_{\mathrm{cal}}$ explicitly |
| Future | Extend to multicoil setup with coil sensitivity maps |
