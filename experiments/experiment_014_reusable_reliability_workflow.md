# Experiment 014: Reusable Reliability Workflow

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

Verify that the reliability-aware uncertainty workflow can be reproduced using **reusable source-code utilities** (`src/reliability.py`) rather than notebook-only code.

---

## Motivation

The proposed method depends on the following reliability pathway:

| Step | Action |
|------|--------|
| 1 | Generate stochastic reconstructions |
| 2 | Compute mean reconstruction $\bar{x}$ |
| 3 | Compute voxel-wise uncertainty map $U$ |
| 4 | Compute held-out $\Lambda$ residual energy $E_{\mathrm{img}}$ |
| 5 | Measure spatial alignment $\rho(U, E_{\mathrm{img}})$ |

This experiment confirms that `src/reliability.py` correctly implements each step.

---

## Method

A trained dropout CNN generated $T = 8$ stochastic reconstructions from the same SSDU $\Theta$-only input.

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
| Stochastic outputs shape | `8 × 768 × 396` |
| Mean reconstruction shape | `768 × 396` |
| Uncertainty map shape | `768 × 396` |
| Residual energy shape | `768 × 396` |
| **Uncertainty–residual alignment** (Pearson $r$) | **`0.7033`** |

---

## Interpretation

The reusable reliability utilities successfully reproduced the notebook-based result from [Experiment 013](EXP_013_DROPOUT_UNCERTAINTY_ALIGNMENT.md):

| Implementation | Pearson $r$ |
|----------------|------------|
| Notebook-only (Exp 013) | `0.7016` |
| **Reusable `src/reliability.py` (this experiment)** | **`0.7033`** |

The small difference is expected — dropout inference is stochastic, so alignment values will vary slightly across runs. The result confirms that `src/reliability.py` correctly implements the full reliability-aware pathway.

---

## Importance for the Proposed Method

This experiment converts the central reliability-aware mechanism into **reproducible, extensible source code**.

The project can now compute the full pipeline from a single reusable module:

| Component | Status |
|-----------|--------|
| Stochastic reconstructions | ✅ |
| Mean reconstruction $\bar{x}$ | ✅ |
| Voxel-wise uncertainty $U$ | ✅ |
| Backprojected residual energy $E_{\mathrm{img}}$ | ✅ |
| Uncertainty–residual alignment $\rho$ | ✅ |

---

## Current Limitations

This experiment remains preliminary:

| Limitation | Detail |
|------------|--------|
| Training data | Single slice, single coil |
| Architecture | Simple dropout CNN |
| Reference data | No fully sampled ground truth |
| Coil model | No sensitivity maps ($S_c$) |
| Scale | No multi-slice or multi-file validation |

---

## Conclusion

The reusable reliability workflow in `src/reliability.py` works correctly and reproduces the alignment result from Experiment 013 ($\rho \approx 0.70$).

**Next step:** test this workflow across multiple slices and files to determine whether the uncertainty–residual alignment remains stable at scale.
