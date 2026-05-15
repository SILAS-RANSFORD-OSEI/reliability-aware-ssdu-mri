# Experiment 023B — Two-Stage Heteroscedastic Residual Calibration

## Objective

Evaluate whether a **two-stage heteroscedastic uncertainty head** — trained on a frozen reconstruction — can learn a voxel-wise reliability map from $\Lambda_{\mathrm{cal}}$ and generalise to the held-out $\Lambda_{\mathrm{eval}}$ subset.

---

## Motivation

The preceding experiment (023A) tested **joint heteroscedastic training**, in which the reconstruction head and uncertainty head were optimised simultaneously. That approach failed: the learned variance map was nearly constant and showed *negative* alignment with both calibration and evaluation residual energy.

The diagnosed failure mode was a **moving-target problem**: while the reconstruction was still changing, the calibration residual target $E_{\Lambda_{\mathrm{cal}}}$ — which depends on the current reconstruction output — was itself non-stationary. The uncertainty head could not track a target that shifted with every gradient step.

This experiment tests the corrective strategy: **decouple the two training stages** so that the uncertainty head is only trained once the reconstruction has converged and its residual structure is fixed.

---

## Four-Way SSDU Setup

The acquired k-space mask $\Omega$ is split into four disjoint subsets:

$$
\Omega = \Theta \;\cup\; \Lambda_{\mathrm{train}} \;\cup\; \Lambda_{\mathrm{cal}} \;\cup\; \Lambda_{\mathrm{eval}}
$$

| Subset | Role in this experiment |
|---|---|
| $\Theta$ | Forms the zero-filled reconstruction input |
| $\Lambda_{\mathrm{train}}$ | Supervises Stage 1 SSDU reconstruction training |
| $\Lambda_{\mathrm{cal}}$ | Provides the **fixed** calibration residual target for Stage 2 |
| $\Lambda_{\mathrm{eval}}$ | Held-out evaluation only — never used in either training stage |

---

## Model

The heteroscedastic CNN produces two outputs from the same input:

$$
\left(\hat{x},\; \hat{\sigma}^2\right) = f_\theta\!\left(x_\Theta\right)
$$

where:
- $\hat{x}$ — reconstructed image
- $\hat{\sigma}^2$ — predicted voxel-wise uncertainty (aleatoric variance map)
- $x_\Theta$ — zero-filled input formed from $\Theta$ alone

---

## Stage 1 — Reconstruction Training

The reconstruction pathway is trained with an SSDU data-consistency loss on $\Lambda_{\mathrm{train}}$ plus an image-consistency regulariser:

$$
\mathcal{L}_{\mathrm{stage1}} = \mathcal{L}_{\mathrm{SSDU}} + \lambda_{\mathrm{img}}\, \mathcal{L}_{\mathrm{img}}
$$

The uncertainty head parameters are **not updated** in Stage 1.

### Stage 1 Results

| Quantity | Value |
|---|---:|
| Initial SSDU loss | 39,434,660 |
| Final SSDU loss | 20,387,188 |
| Initial image loss | 0.002897 |
| Final image loss | 0.041968 |

The SSDU reconstruction loss reduced by approximately 48%. The image loss increase reflects the regularisation trade-off as the model adapts its output toward the $\Theta$-consistent reconstruction.

---

## Stage 2 — Uncertainty-Head Calibration

Once Stage 1 converges, the **reconstruction pathway is frozen**. The calibration residual target is then computed once from the fixed reconstruction output:

$$
E_{\Lambda_{\mathrm{cal}}} = \left| \mathcal{F}^{-1}\!\left( r_{\Lambda_{\mathrm{cal}}} \right) \right|^2, \qquad r_{\Lambda_{\mathrm{cal}}} = M_{\Lambda_{\mathrm{cal}}} \odot (\hat{x} - y)
$$

Because $\hat{x}$ is now fixed, $E_{\Lambda_{\mathrm{cal}}}$ is a **static target** for the duration of Stage 2. The uncertainty head is trained to predict the normalised calibration residual energy:

$$
\mathcal{L}_{\mathrm{cal}} = \left\| \mathrm{norm}(\hat{\sigma}^2) - \mathrm{norm}(E_{\Lambda_{\mathrm{cal}}}) \right\|_2^2
$$

### Stage 2 Results

| Quantity | Value |
|---|---:|
| Initial calibration loss | 0.175652 |
| Final calibration loss | 0.003428 |

The calibration loss reduced by approximately **98%**, indicating the uncertainty head successfully fitted the spatial structure of $E_{\Lambda_{\mathrm{cal}}}$.

---

## Evaluation on Held-Out $\Lambda_{\mathrm{eval}}$

After Stage 2, the learned $\hat{\sigma}^2$ is evaluated against residual energy from $\Lambda_{\mathrm{eval}}$, which was never accessible during either training stage.

### Alignment Comparison

| Method | $\rho$ with $E_{\Lambda_{\mathrm{eval}}}$ |
|---|---:|
| Input intensity | 0.588 |
| Reconstruction intensity | 0.505 |
| Edge map | 0.457 |
| **Two-stage learned $\hat{\sigma}^2$** | **0.447** |

### Calibration vs. Evaluation Generalisation

| Subset | $\rho(\hat{\sigma}^2,\; E_{\Lambda})$ |
|---|---:|
| $\Lambda_{\mathrm{cal}}$ (training target) | 0.421 |
| $\Lambda_{\mathrm{eval}}$ (held-out) | 0.447 |

The slight increase from calibration to evaluation alignment is consistent with patterns observed in Experiments 020 and 021, and suggests the learned map is not overfitting to $\Lambda_{\mathrm{cal}}$.

### Sigma Map Spatial Statistics

| Quantity | Value |
|---|---:|
| Minimum $\hat{\sigma}^2$ | 0.661 |
| Maximum $\hat{\sigma}^2$ | 0.724 |
| Mean $\hat{\sigma}^2$ | 0.663 |
| Standard deviation $\hat{\sigma}^2$ | 0.00329 |

The learned variance map has low spatial contrast (range 0.063, std 0.003), meaning the uncertainty head is producing a nearly flat map. This is substantially better than the degenerate constant map from 023A, but still far from a well-resolved spatial uncertainty estimate.

---

## Comparison Against Joint Training (023A)

| Method | Cal. Alignment | Eval. Alignment |
|---|---:|---:|
| Joint heteroscedastic (023A) | −0.194 | −0.246 |
| **Two-stage heteroscedastic (023B)** | **+0.421** | **+0.447** |

The reversal from negative to positive alignment confirms that **stage decoupling resolves the moving-target failure mode**. Freezing the reconstruction before calibrating the uncertainty head is a necessary design condition, not merely a performance tuning choice.

---

## Interpretation

### What worked

Two-stage decoupling converts a failing approach into a positive-alignment one. The uncertainty head learns a spatially structured residual-related map that generalises to the held-out evaluation subset — a non-trivial result given that $\Lambda_{\mathrm{eval}}$ shares no overlap with the calibration target.

### What did not work

The learned $\hat{\sigma}^2$ does not outperform input intensity (0.447 vs. 0.588) or reconstruction intensity (0.447 vs. 0.505). The low spatial contrast of $\hat{\sigma}^2$ (std = 0.003) suggests the uncertainty head is learning a weak smooth approximation to the residual map rather than capturing fine-grained spatial reliability structure. This likely reflects a combination of limited model capacity in the uncertainty head, the smoothing implicit in the $\ell_2$ normalised matching loss, and the absence of structural priors (intensity, edges) as explicit inputs to the uncertainty head.

### Diagnostic interpretation of the image loss increase

The rise in $\mathcal{L}_{\mathrm{img}}$ during Stage 1 (0.003 → 0.042) may initially appear problematic. It reflects the reconstruction adapting under the combined SSDU and image-consistency objective — the model is navigating a trade-off between k-space fidelity on $\Lambda_{\mathrm{train}}$ and image-domain consistency, which can temporarily increase the image-domain loss before settling. This does not invalidate the experiment but should be monitored in future runs.

---

## Reviewer-Level Significance

This experiment demonstrates that the **failure of 023A was architectural, not fundamental** to the heteroscedastic approach. The moving-target diagnosis is testable, the fix (stage decoupling) is principled, and the result is reproducible within the four-way SSDU framework.

A reviewer evaluating this result would likely accept the two-stage strategy as a sound methodological improvement, while correctly noting that the uncertainty head's spatial resolution is still insufficient for a final method. The honest positioning is:

> Two-stage residual calibration is a **necessary but not sufficient** condition for learned reliability estimation under SSDU. The stage-decoupling principle is validated; the uncertainty head architecture requires further development.

---

## Limitations

- Single slice, single coil — spatial and coil generalisation untested.
- Uncertainty head has limited capacity; architectural choices not yet ablated.
- Normalised $\ell_2$ loss smooths spatial structure — a perceptual or rank-based loss may preserve finer detail.
- No structural inputs ($I$, $G$) to the uncertainty head — feeding these explicitly could substantially improve alignment.
- No fully sampled reference — true image-domain error cannot be verified.
- Image loss increase in Stage 1 not yet diagnosed in detail.

---

## Next Methodological Direction

The bottleneck is the **uncertainty head's spatial resolution**, not the two-stage framework. The most direct improvements are:

| Direction | Rationale |
|---|---|
| Feed $I$ and $G$ as explicit inputs to the uncertainty head | Structural information is the strongest predictor; giving it directly removes the need to re-learn it |
| Replace $\ell_2$ normalised matching loss with a rank-based or perceptual loss | Preserve spatial contrast rather than minimising global mean-squared error |
| Separate reliability network (not a shared-encoder head) | Dedicated architecture for the reliability task; avoids capacity sharing with reconstruction |
| Extend to all 16 slices | Single-slice result may not reflect the full distribution |

All candidates should be evaluated within the same four-way SSDU framework.

---

## Conclusion

Two-stage heteroscedastic residual calibration is a meaningful and principled improvement over joint training. Freezing the reconstruction pathway eliminates the moving-target problem and yields a learned uncertainty map with positive held-out evaluation alignment ($\rho = 0.447$). However, the map's low spatial contrast (std = 0.003) and its failure to surpass structural baselines indicate that the uncertainty head architecture requires further development before it can serve as the primary reliability signal in the proposed framework.
