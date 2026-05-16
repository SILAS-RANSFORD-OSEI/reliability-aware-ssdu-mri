# Experiment 025 — Cross-Slice Reliability CNN Training

## Objective

Evaluate whether training **one shared reliability CNN across all 16 slices** improves held-out residual-energy prediction compared with per-slice training (Experiment 024) and simple structural baselines — and in particular whether a learned model can finally outperform input image intensity.

---

## Motivation

Experiment 024 identified a precise failure mode: the per-slice reliability CNN underperformed input intensity ($\rho = 0.524$ vs. $0.553$) and exhibited high slice-to-slice variance (std = 0.080), while the simpler linear calibration model from Experiment 022 ($\rho = 0.560$) outperformed it. The diagnosis was a **data-limited per-slice training regime** — a small CNN has more parameters than a linear model but far fewer training samples per fit.

Cross-slice training is the most direct intervention: pooling calibration residuals from all 16 slices increases the effective training set by 16×, allowing the network to learn shared reliability structure across anatomical positions rather than overfitting to individual slice patterns.

---

## Four-Way SSDU Setup

The acquired k-space mask $\Omega$ is split into four disjoint subsets:

$$
\Omega = \Theta \;\cup\; \Lambda_{\mathrm{train}} \;\cup\; \Lambda_{\mathrm{cal}} \;\cup\; \Lambda_{\mathrm{eval}}
$$

| Subset | Role in this experiment |
|---|---|
| $\Theta$ | Forms the zero-filled reconstruction input |
| $\Lambda_{\mathrm{train}}$ | Supervises SSDU reconstruction training (per-slice) |
| $\Lambda_{\mathrm{cal}}$ | Supervises the shared reliability CNN (all 16 slices) |
| $\Lambda_{\mathrm{eval}}$ | Held-out evaluation only — never used during training |

**Key design note:** the SSDU reconstruction training remains per-slice; only the reliability network is shared across slices. This preserves the interpretability of the four-way partition while addressing the data-limitation bottleneck.

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
| Reliability training | All 16 slices (shared model) |
| Reliability evaluation | All 16 slices |

---

## Reliability Network

The shared CNN $h_\phi$ predicts a voxel-wise reliability map from three structural input channels:

$$
R_{\mathrm{net}} = h_\phi\!\left( x_\Theta,\; \hat{x},\; \lvert \nabla \hat{x} \rvert \right)
$$

where:
- $x_\Theta$ — zero-filled $\Theta$-only input image
- $\hat{x}$ — mean reconstruction from the frozen dropout CNN
- $\lvert \nabla \hat{x} \rvert$ — gradient magnitude of the mean reconstruction

Note: dropout uncertainty $U$ is still **not** an input here — this is the structural-only cross-slice variant. The effect of adding $U$ is the subject of the next experiment.

### Training target (calibration)

$$
E_{\Lambda_{\mathrm{cal}}} = \left| \mathcal{F}^{-1}\!\left( r_{\Lambda_{\mathrm{cal}}} \right) \right|^2, \qquad r_{\Lambda_{\mathrm{cal}}} = M_{\Lambda_{\mathrm{cal}}} \odot (\hat{x} - y)
$$

The shared model is trained on $\{(x_\Theta^{(s)}, \hat{x}^{(s)}, E_{\Lambda_{\mathrm{cal}}}^{(s)})\}_{s=0}^{15}$ jointly across all 16 slices over 30 epochs.

### Evaluation target (held-out)

$$
E_{\Lambda_{\mathrm{eval}}} = \left| \mathcal{F}^{-1}\!\left( r_{\Lambda_{\mathrm{eval}}} \right) \right|^2, \qquad r_{\Lambda_{\mathrm{eval}}} = M_{\Lambda_{\mathrm{eval}}} \odot (\hat{x} - y)
$$

### Training loss progression

| Quantity | Value |
|---|---:|
| Initial mean reliability loss | 0.021017 |
| Final mean reliability loss | 0.002433 |
| Relative reduction | ~88% |

The loss reduction confirms that the shared network successfully learned the calibration residual-energy structure across the full slice stack.

---

## Results

### Evaluation Alignment Across All 16 Slices

| Method | Mean $\rho$ | Std | Min | Max |
|---|---:|---:|---:|---:|
| **Cross-slice Reliability CNN** | **0.583** | **0.046** | **0.504** | **0.673** |
| Input intensity | 0.553 | 0.041 | 0.478 | 0.625 |
| Mean reconstruction intensity | 0.460 | 0.037 | 0.415 | 0.547 |
| Dropout uncertainty | 0.470 | 0.045 | 0.381 | 0.535 |
| Edge map | 0.395 | 0.045 | 0.304 | 0.468 |

### Pairwise Margins: Cross-Slice CNN vs. Key Comparators

| Comparison | Mean $\Delta$ | Std | Min | Max |
|---|---:|---:|---:|---:|
| CNN − Input intensity | +0.030 | 0.013 | +0.010 | +0.051 |
| CNN − Dropout uncertainty | +0.112 | 0.018 | +0.082 | +0.155 |
| CNN − Edge map | +0.188 | 0.033 | +0.146 | +0.269 |

### Per-Slice vs. Cross-Slice Training Comparison

| Training regime | Mean $\rho$ | Std | Min | Max |
|---|---:|---:|---:|---:|
| Per-slice CNN (Experiment 024) | 0.524 | 0.080 | 0.358 | 0.642 |
| **Cross-slice CNN (Experiment 025)** | **0.583** | **0.046** | **0.504** | **0.673** |
| Input intensity (reference) | 0.553 | 0.041 | 0.478 | 0.625 |

---

## Interpretation

### Primary result

The cross-slice reliability CNN is the **first learned model in this project to outperform input intensity across all 16 slices**, achieving $\rho = 0.583 \pm 0.046$ against input intensity's $0.553 \pm 0.041$. The minimum improvement margin is $+0.010$, meaning no slice regresses below input intensity — a qualitative change from the per-slice result where some slices fell as low as 0.358.

### The data-limitation diagnosis is confirmed

The per-slice → cross-slice transition produces a simultaneous improvement in both mean ($+0.059$) and variance ($0.080 \rightarrow 0.046$). This is the signature of a data-limited model: more training data raises the floor, reduces variance, and improves generalisation. The diagnosis from Experiment 024 is validated.

### Why cross-slice generalisation is non-trivial

The shared model must generalise across slices with substantially different anatomical content and signal energy — recall from Experiment 020 that SSDU losses varied by an order of magnitude across slices (from ~20M for slices 8–10 to ~376M for slice 15). The fact that a shared network achieves consistent improvement across this range indicates it is learning a transferable reliability-to-residual mapping, not merely interpolating within a narrow distribution.

### Relationship to Experiment 022 (linear calibration)

The linear hybrid model from Experiment 022 achieved $\rho = 0.560$. The cross-slice CNN now achieves $\rho = 0.583$, reversing the earlier inversion where the linear model outperformed the nonlinear one. This confirms that the linear model's earlier advantage was purely a function of data availability, not architectural superiority.

### Remaining gap relative to input intensity

The mean improvement over input intensity is modest ($+0.030$). The network is still dominated by the intensity signal, which is expected given that the three input channels all carry strong intensity information ($x_\Theta$, $\hat{x}$, and $\lvert \nabla \hat{x} \rvert$ all co-vary with image magnitude). Adding dropout uncertainty $U$ as a fourth input channel is the next logical step — $U$ is the only available signal that is structurally decoupled from image magnitude.

---

## Reviewer-Level Significance

This result directly addresses two prior reviewer-level concerns:

**1.** *"The learned reliability model cannot beat input intensity."*  
— Resolved. Cross-slice CNN exceeds input intensity consistently (min $\Delta = +0.010$ across all slices).

**2.** *"The per-slice CNN is too unstable to be a reliable method."*  
— Resolved. Cross-slice training reduces std from 0.080 to 0.046, comparable to structural baselines (0.037–0.045).

The central contribution of this project can now be stated more precisely:

> **Four-way self-supervised k-space partitioning for residual-calibrated reliability learning in accelerated MRI reconstruction** — a framework in which the calibration subset $\Lambda_{\mathrm{cal}}$ trains a shared reliability network that generalises to unseen held-out residual energy, outperforming all simple structural and stochastic baselines.

MC dropout is correctly positioned as a **baseline uncertainty feature** in this framework, not the primary contribution.

---

## Limitations

- One fastMRI volume, one coil — cross-volume and multicoil generalisation untested.
- Dropout uncertainty $U$ not yet included as an input feature.
- No cross-volume validation — the shared model is trained and tested within the same volume.
- No fully sampled reference — true image-domain reconstruction error cannot be verified.
- The improvement over input intensity ($+0.030$) is modest; replication across multiple files is needed to establish robustness.

---

## Next Methodological Direction

Two experiments follow directly from this result:

### Add dropout uncertainty as an input feature (Experiment 026)

$$
R_{\mathrm{net}} = h_\phi\!\left( x_\Theta,\; \hat{x},\; \lvert \nabla \hat{x} \rvert,\; U \right)
$$

If $U$ carries independent information beyond structural features — as suggested by the partial correlation analysis in Experiment 021 ($\rho_{\mathrm{partial}} \approx 0.047$–$0.056$) — adding it as an explicit channel should produce an incremental improvement in evaluation alignment.

### Cross-volume validation

The current model is trained and evaluated within one fastMRI volume. Testing on a second held-out volume would establish whether the learned reliability structure transfers across subjects — a prerequisite for any journal-level reliability claim.

---

## Conclusion

Cross-slice reliability CNN training resolves the data-limitation problem identified in Experiment 024. The shared model achieves $\rho = 0.583 \pm 0.046$ on held-out $\Lambda_{\mathrm{eval}}$ residual energy — the first result in this project to consistently outperform input intensity across all 16 slices, with minimum margin $+0.010$. The simultaneous improvement in mean and variance confirms the data-limited diagnosis. The framework is now mature enough to support the project's central reliability-learning claim, contingent on further validation with dropout uncertainty as an added input feature and cross-volume testing.
