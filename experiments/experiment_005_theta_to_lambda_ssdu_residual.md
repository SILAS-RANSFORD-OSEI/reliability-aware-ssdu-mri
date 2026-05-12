# Experiment 005: Theta-to-Lambda SSDU Residual

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Method](#method)
- [Results](#results)
- [Interpretation](#interpretation)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Conclusion](#conclusion)

---

## Objective

Compute a **non-zero** SSDU held-out k-space residual by reconstructing from the $\Theta$ subset only and evaluating consistency on the held-out $\Lambda$ subset.

---

## Motivation

In [Experiment 004](EXP_004_HELD_OUT_KSPACE_RESIDUAL.md), the SSDU loss was nearly zero because the reconstruction used the full measured k-space — making the round-trip lossless.

This experiment tests the **actual SSDU logic**:

| Component | Description |
|-----------|-------------|
| Reconstruction input | $\Theta$ only |
| Loss evaluation | $\Lambda$ only |

This mimics the self-supervised training setting, where the model is trained on one subset and judged on another.

---

## Method

The acquired mask $\Omega$ was split into disjoint subsets:

$$\Omega = \Theta \cup \Lambda, \qquad \Theta \cap \Lambda = \varnothing$$

**Step 1 — Restrict measured k-space to $\Theta$:**

$$y_{\Theta} = M_{\Theta} \odot y$$

**Step 2 — Zero-filled reconstruction from $\Theta$ only:**

$$x_{\Theta} = \mathcal{F}^{-1}(y_{\Theta})$$

**Step 3 — Predict k-space from the reconstruction:**

$$\hat{y} = \mathcal{F}(x_{\Theta})$$

**Step 4 — Compute held-out residual on $\Lambda$:**

$$r_{\Lambda} = M_{\Lambda} \odot (\hat{y} - y)$$

| Term | Description |
|------|-------------|
| $M_{\Lambda}$ | Binary held-out $\Lambda$ mask |
| $\hat{y}$ | Predicted k-space from $\Theta$-only reconstruction |
| $y$ | Full measured k-space |

**Step 5 — Compute normalised SSDU loss:**

$$\mathcal{L}_{\mathrm{SSDU}} = \frac{\|r_{\Lambda}\|_2^2}{\|M_{\Lambda} \odot y\|_2^2}$$

---

## Results

| Quantity | Value |
|----------|------:|
| $\Theta$-only k-space shape | `16 × 768 × 396` |
| $\Theta$-only coil images shape | `16 × 768 × 396` |
| Held-out residual shape | `16 × 768 × 396` |
| $\Theta \to \Lambda$ SSDU loss | `1.0` |

---

## Interpretation

The loss of `1.0` is the expected result. The zero-filled reconstruction from $\Theta$ does not predict the held-out $\Lambda$ measurements — the predicted k-space on $\Lambda$ is effectively zero, so:

$$r_{\Lambda} \approx -y_{\Lambda}$$

Since the loss is normalised by the energy of $y_{\Lambda}$, this gives:

$$\mathcal{L}_{\mathrm{SSDU}} \approx 1$$

A loss of `1.0` is therefore **not a failure** — it is the correct baseline behaviour of a zero-filled reconstruction in the SSDU setting.

---

## Importance for the Proposed Method

This experiment confirms the self-supervised training logic:

> **The model sees $\Theta$ but is judged on $\Lambda$.**

A learned reconstruction model should reduce this loss below `1.0` by predicting image structure that becomes more consistent with the held-out measured k-space.

For the proposed reliability-aware method, the held-out residual $r_{\Lambda}$ will later become a **calibration signal** for voxel-wise uncertainty estimation:

| Stage | Role of $r_{\Lambda}$ |
|-------|----------------------|
| Self-supervised training | Reconstruction loss on held-out $\Lambda$ |
| Uncertainty calibration | Signal for aligning $U$ with reconstruction unreliability |

---

## Conclusion

The $\Theta \to \Lambda$ SSDU residual computation works correctly on real fastMRI brain multicoil k-space.

**Next step:** visualise the residual energy and backproject the held-out residual into the image domain to produce $e_{\mathrm{img}}$ — the image-domain reliability signal.
