# Experiment 013: Trained Dropout Uncertainty and Held-Out Residual Alignment

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Method](#method)
- [Results](#results)
- [Interpretation](#interpretation)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Limitations](#limitations)
- [Conclusion](#conclusion)

---

## Objective

Evaluate whether uncertainty from a **trained dropout CNN** aligns with the image-domain residual energy derived from held-out $\Lambda$ k-space measurements.

---

## Motivation

The core direction of this project is reliability-aware self-supervised MRI reconstruction. This experiment provides the **first quantitative test** of that idea:

> **Does model-derived uncertainty indicate regions where the reconstruction is inconsistent with held-out measured k-space?**

---

## Method

A single-coil-equivalent SSDU setup was used. The acquired mask was split into disjoint subsets:

$$\Omega = \Theta \cup \Lambda, \qquad \Theta \cap \Lambda = \varnothing$$

The dropout CNN was trained using the SSDU objective on $\Lambda$. After training, dropout was kept **active at inference** to generate $T = 8$ stochastic reconstructions.

**Mean reconstruction:**

$$\bar{x} = \frac{1}{T} \sum_{t=1}^{T} \hat{x}_t$$

**Voxel-wise uncertainty map (sample variance):**

$$U = \frac{1}{T-1} \sum_{t=1}^{T} (\hat{x}_t - \bar{x})^2$$

**Project mean reconstruction to k-space:**

$$\hat{y} = \mathcal{F}(\bar{x})$$

**Compute held-out $\Lambda$ residual:**

$$r_{\Lambda} = M_{\Lambda} \odot (\hat{y} - y)$$

**Backproject residual into the image domain:**

$$E_{\mathrm{img}} = \left| \mathcal{F}^{-1}(r_{\Lambda}) \right|^2$$

**Measure spatial alignment:**

$$\rho(U,\ E_{\mathrm{img}}) \quad \text{(Pearson correlation)}$$

---

## Results

| Quantity | Value |
|----------|------:|
| Number of stochastic reconstructions | `8` |
| Stochastic output shape | `768 × 396` per sample |
| Mean reconstruction shape | `768 × 396` |
| Uncertainty map shape | `768 × 396` |
| Uncertainty minimum | `3.656774e-05` |
| Uncertainty maximum | `0.004332171` |
| **Uncertainty–residual alignment** (Pearson $r$) | **`0.7016`** |

---

## Interpretation

The trained dropout uncertainty map showed **strong positive spatial alignment** with the backprojected held-out $\Lambda$ residual energy:

$$\rho = 0.7016$$

Regions with higher model uncertainty tend to correspond to regions with higher held-out k-space inconsistency. Compare this to the random-noise baseline from [Experiments 007–008](EXP_007_ARTIFICIAL_UNCERTAINTY_UTILITY_TEST.md), where $\rho \approx 0$ — the increase to $\rho = 0.70$ is the result of the model having learned to reconstruct from $\Theta$ and expressing genuine uncertainty where k-space information was missing.

This supports the central reliability-aware direction of the project.

---

## Importance for the Proposed Method

This experiment provides the **first quantitative evidence** for the proposed idea:

> **Held-out k-space residuals can act as a self-supervised reliability signal for uncertainty calibration.**

| Comparison | Pearson $r$ |
|------------|------------|
| Artificial Gaussian noise (Exp 007–008) | ≈ 0.000 |
| **Trained dropout CNN (this experiment)** | **0.701** |

The result does not yet prove final clinical reliability, but it demonstrates that model uncertainty and held-out residual energy are **meaningfully related** in the SSDU setting — confirming that the calibration objective $\mathcal{L}_{\mathrm{cal}}$ has a physically grounded target signal.

---

## Limitations

This result is a **promising proof of concept**, not a final validation.

| Limitation | Detail |
|------------|--------|
| Training data | Single slice only |
| Coil model | Single-coil-equivalent — no sensitivity maps |
| Architecture | Simple dropout CNN |
| Reference data | No fully sampled ground truth |
| Error comparison | No true voxel-wise reconstruction error available |
| Stochastic samples | $T = 8$ — small sample size |

---

## Conclusion

The trained dropout uncertainty map aligned strongly with the backprojected held-out residual energy ($\rho = 0.70$), providing the **first strong technical evidence** supporting the reliability-aware self-supervised reconstruction direction.

**Next steps:**

| Priority | Action |
|----------|--------|
| Immediate | Convert uncertainty–alignment workflow into reusable source-code utilities |
| Follow-up | Test alignment across multiple slices and files |
| Future | Extend to multicoil setup with coil sensitivity maps and stronger architecture |
