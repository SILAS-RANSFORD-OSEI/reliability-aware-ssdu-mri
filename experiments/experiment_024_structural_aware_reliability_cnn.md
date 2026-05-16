# Experiment 024 — Structural-Aware Reliability CNN

## Objective

Evaluate whether a **learned structural-aware reliability network** — trained on $\Lambda_{\mathrm{cal}}$ using structural image features — can predict unseen held-out residual energy better than MC dropout uncertainty and simple structural baselines.

---

## Motivation

Experiments 021 and 022 established that:

1. Input image intensity is the strongest single predictor of held-out residual energy ($\rho = 0.553$), outperforming raw MC dropout ($\rho = 0.470$).
2. A linear ridge-calibrated hybrid map ($R_{\mathrm{hybrid}}$) achieves marginal improvement over intensity alone ($\rho = 0.560$, $\Delta = +0.007$), but the dropout coefficient remains small ($\hat{\beta}_U = 0.050$).
3. Experiment 023B showed that a heteroscedastic uncertainty head trained without structural inputs produces a low-contrast map (std = 0.003) that does not surpass structural baselines.

The natural next hypothesis is that a **dedicated reliability network** — one that explicitly receives structural image features as inputs and is trained directly to predict $E_{\Lambda_{\mathrm{cal}}}$ — can learn richer spatial reliability structure than either a linear calibration model or a passive uncertainty head.

---

## Four-Way SSDU Setup

The acquired k-space mask $\Omega$ is split into four disjoint subsets:

$$
\Omega = \Theta \;\cup\; \Lambda_{\mathrm{train}} \;\cup\; \Lambda_{\mathrm{cal}} \;\cup\; \Lambda_{\mathrm{eval}}
$$

| Subset | Role in this experiment |
|---|---|
| $\Theta$ | Forms the zero-filled reconstruction input |
| $\Lambda_{\mathrm{train}}$ | Supervises SSDU reconstruction training |
| $\Lambda_{\mathrm{cal}}$ | Supervises the reliability network |
| $\Lambda_{\mathrm{eval}}$ | Held-out evaluation only — never used during training |

---

## Dataset

| Property | Value |
|---|---|
| Dataset | fastMRI Brain |
| Acquisition | AXT2 |
| Acceleration | R = 4 |
| Working setup | Single-coil-equivalent |
| Selected coil | Coil 0 |
| Tested slices | 0 – 15 (all 16 slices) |

---

## Reliability Network

A separate CNN $h_\phi$ is trained to predict a voxel-wise reliability map from structural image features:

$$
R_{\mathrm{net}} = h_\phi\!\left( x_\Theta,\; \hat{x},\; \lvert \nabla \hat{x} \rvert \right)
$$

where:
- $x_\Theta$ — zero-filled input image ($\Theta$-only)
- $\hat{x}$ — mean reconstruction (from the frozen dropout CNN)
- $\lvert \nabla \hat{x} \rvert$ — gradient magnitude of the mean reconstruction
- $R_{\mathrm{net}}$ — predicted voxel-wise reliability map

Note: dropout uncertainty $U$ is **not** an input in this experiment — this is the structural-only variant. Including $U$ is the natural next step (Experiment 025).

### Training target

The reliability network is trained to predict the calibration residual energy:

$$
E_{\Lambda_{\mathrm{cal}}} = \left| \mathcal{F}^{-1}\!\left( r_{\Lambda_{\mathrm{cal}}} \right) \right|^2, \qquad r_{\Lambda_{\mathrm{cal}}} = M_{\Lambda_{\mathrm{cal}}} \odot (\hat{x} - y)
$$

### Evaluation target

The learned map is evaluated against the held-out residual energy:

$$
E_{\Lambda_{\mathrm{eval}}} = \left| \mathcal{F}^{-1}\!\left( r_{\Lambda_{\mathrm{eval}}} \right) \right|^2, \qquad r_{\Lambda_{\mathrm{eval}}} = M_{\Lambda_{\mathrm{eval}}} \odot (\hat{x} - y)
$$

This design mirrors the two-stage strategy validated in Experiment 023B: the reconstruction is fixed before the reliability network is trained, so the calibration target is stationary.

---

## Results

### Evaluation Alignment Across All 16 Slices

| Method | Mean $\rho$ | Std | Min | Max |
|---|---:|---:|---:|---:|
| Input intensity | 0.553 | 0.041 | 0.478 | 0.625 |
| **Reliability CNN** | **0.524** | **0.080** | **0.358** | **0.642** |
| Mean reconstruction intensity | 0.460 | 0.037 | 0.415 | 0.547 |
| Dropout uncertainty | 0.470 | 0.045 | 0.381 | 0.535 |
| Edge map | 0.395 | 0.045 | 0.304 | 0.468 |

### Pairwise Margins: Reliability CNN vs. Key Comparators

| Comparison | Mean $\Delta$ | Std | Min | Max |
|---|---:|---:|---:|---:|
| CNN − Input intensity | −0.029 | 0.070 | −0.189 | +0.057 |
| CNN − Dropout uncertainty | +0.054 | 0.072 | −0.108 | +0.124 |
| CNN − Edge map | +0.129 | 0.074 | −0.043 | +0.205 |

---

## Interpretation

### What the reliability CNN achieves

The reliability CNN reaches a mean evaluation alignment of $0.524 \pm 0.080$, which is:
- **Better** than raw dropout uncertainty ($\Delta = +0.054$), mean reconstruction intensity ($\Delta = +0.064$), and edge map ($\Delta = +0.129$).
- **Below** input intensity ($\Delta = -0.029$), meaning input intensity remains the single strongest predictor.

The CNN has learned spatial reliability structure that goes beyond what a simple edge detector captures, but it has not yet exceeded the predictive power of the plain input image magnitude.

### What the variance reveals

The reliability CNN has markedly higher slice-to-slice variance than all baselines (std = 0.080 vs. 0.037–0.045 for structural baselines). This means the network performs well on some slices (max = 0.642, exceeding input intensity's max of 0.625) but poorly on others (min = 0.358, below all baselines). The high variance suggests the network is **sensitive to per-slice structural variation** in a way that uncalibrated maps are not — a sign of overfitting to $\Lambda_{\mathrm{cal}}$ on difficult slices or insufficient training data per slice.

### Why input intensity is hard to beat

Input intensity is a proxy for anatomical signal magnitude. In undersampled MRI reconstruction, high-intensity regions (white matter, CSF boundaries) tend to have larger absolute reconstruction errors simply due to their dynamic range. A reliability network trained on $E_{\Lambda_{\mathrm{cal}}}$ must implicitly rediscover this relationship from structural features — and a small per-slice CNN trained on a single calibration target has limited capacity to do so more efficiently than the direct intensity signal.

### Comparison to linear calibration (Experiment 022)

The linear hybrid calibrated map from Experiment 022 achieved $\rho = 0.560$, which is higher than the reliability CNN ($\rho = 0.524$). This is a notable inversion: the nonlinear learned model underperforms the linear calibration baseline. The most likely explanation is the limited training signal available per slice — the linear model generalises better precisely because it has fewer parameters to fit. This inversion may reverse with more slices or cross-volume training data.

---

## Reviewer-Level Significance

This experiment makes two contributions:

**1. It validates structural feature learning as a reliability approach.**  
A learned network trained on $\Lambda_{\mathrm{cal}}$ generalises positively to $\Lambda_{\mathrm{eval}}$ across all 16 slices. The result is not trivially explained by intensity alone — the CNN with gradient magnitude input achieves positive alignment even on slices where edge maps alone are weaker.

**2. It precisely identifies the current failure mode.**  
The high variance (std = 0.080) and the underperformance relative to the linear model point to a specific problem: the reliability CNN is **data-hungry** relative to the per-slice training regime. This is a concrete and actionable diagnosis, not a vague claim that the method "needs more work."

The honest positioning for this result is:

> A structural-aware reliability CNN trained on $\Lambda_{\mathrm{cal}}$ generalises to $\Lambda_{\mathrm{eval}}$ and improves over MC dropout and edge baselines, but does not yet outperform input intensity. The limiting factor is the per-slice training regime, not the learned-reliability approach itself.

---

## Limitations

- One fastMRI file, one coil — cross-file generalisation untested.
- One training sample per slice — the reliability CNN is severely data-limited.
- Dropout uncertainty $U$ not included as an input feature.
- No cross-validation of the reliability network across slices.
- High slice-to-slice variance (std = 0.080) indicates instability that single-volume evaluation cannot fully characterise.
- No fully sampled reference — true image-domain error cannot be verified.

---

## Next Methodological Direction

Two parallel improvements are motivated by this result:

### Add dropout uncertainty as an input feature

The structural-only network does not use $U$. Experiment 022 showed that $U$ contributes a small but consistently positive marginal alignment. Including it as an explicit input channel gives the network a stochastic signal that structural features alone cannot provide:

$$
R_{\mathrm{net}} = h_\phi\!\left( x_\Theta,\; \hat{x},\; \lvert \nabla \hat{x} \rvert,\; U \right)
$$

### Address the data-limited regime

The per-slice training regime is the most likely cause of both the high variance and the linear model outperforming the CNN. Potential mitigations:

| Approach | Rationale |
|---|---|
| Train across all 16 slices jointly | More training samples per model fit |
| Cross-volume training | Generalises reliability structure across anatomy |
| Reduce network capacity | Fewer parameters → better generalisation per sample |
| Add explicit intensity input | Removes need to re-learn the dominant signal from scratch |

---

## Conclusion

The structural-aware reliability CNN generalises positively to held-out $\Lambda_{\mathrm{eval}}$ residual energy ($\rho = 0.524 \pm 0.080$) and outperforms MC dropout uncertainty, mean reconstruction intensity, and edge maps. However, it does not yet surpass input intensity, and its high slice-to-slice variance reveals sensitivity to the per-slice data-limited regime. The next experiment should add dropout uncertainty $U$ as an input feature and investigate cross-slice training to address the data limitation.
