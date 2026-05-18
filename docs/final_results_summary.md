# Final Results Summary

## Four-Way Self-Supervised K-Space Partitioning for Residual-Calibrated Reliability Learning in Accelerated Brain MRI

---

## 1. Problem Statement

Deep learning MRI reconstruction methods recover images from undersampled k-space, but their outputs contain spatially varying errors whose magnitude and distribution are unknown at inference time. In fully supervised settings, reconstruction reliability can be assessed against fully sampled reference images. In practice, fully sampled references are often unavailable.

This project addresses the following question:

> Can reconstruction reliability be estimated in a self-supervised MRI setting using **only the acquired undersampled k-space data** — without any fully sampled ground truth?

---

## 2. Core Methodological Idea

The central contribution is a **four-way k-space partition**:

$$
\Omega = \Theta \;\cup\; \Lambda_{\mathrm{train}} \;\cup\; \Lambda_{\mathrm{cal}} \;\cup\; \Lambda_{\mathrm{eval}}
$$

where $\Omega$ is the acquired k-space sampling set and the four subsets are disjoint by construction:

| Subset | Role |
|---|---|
| $\Theta$ | Reconstruction input (zero-filled image) |
| $\Lambda_{\mathrm{train}}$ | SSDU reconstruction training loss |
| $\Lambda_{\mathrm{cal}}$ | Reliability calibration target |
| $\Lambda_{\mathrm{eval}}$ | Held-out reliability evaluation — never used during training |

This separation is the critical design property. It prevents the circularity that arises when the same held-out k-space subset is used for both calibrating and evaluating a reliability signal. $\Lambda_{\mathrm{eval}}$ serves as a proxy for unseen measurement error: if a predicted reliability map is positively correlated with $E_{\Lambda_{\mathrm{eval}}}$, the model is predicting where reconstruction error concentrates in a truly held-out subset of k-space.

---

## 3. Final Proposed Model

### Reliability CNN

$$
R_\phi = h_\phi\!\left( x_\Theta,\; \hat{x},\; \lvert \nabla \hat{x} \rvert \right)
$$

| Input | Definition |
|---|---|
| $x_\Theta$ | Image reconstructed from the $\Theta$ input subset only |
| $\hat{x}$ | Mean reconstruction from the frozen dropout CNN |
| $\lvert \nabla \hat{x} \rvert$ | Gradient magnitude of the mean reconstruction |
| $R_\phi$ | Predicted voxel-wise reliability map |

### Calibration target

$$
E_{\Lambda_{\mathrm{cal}}} = \left| \mathcal{F}^{-1}\!\left[ M_{\Lambda_{\mathrm{cal}}} \odot (\hat{y} - y) \right] \right|^2
$$

### Held-out evaluation target

$$
E_{\Lambda_{\mathrm{eval}}} = \left| \mathcal{F}^{-1}\!\left[ M_{\Lambda_{\mathrm{eval}}} \odot (\hat{y} - y) \right] \right|^2
$$

where $y$ is measured k-space, $\hat{y}$ is the reconstruction's predicted k-space, $M_\Lambda$ is a binary mask selecting subset $\Lambda$, and $\mathcal{F}^{-1}$ is the inverse Fourier transform.

The model is trained on pooled $\Lambda_{\mathrm{cal}}$ residuals from multiple source volumes and evaluated on $\Lambda_{\mathrm{eval}}$ from a held-out volume — no test-volume data is ever used during training.

---

## 4. Experiment Progression

| Experiment | Purpose | Key Finding |
|---|---|---|
| 017 | Four-way split design and verification | Confirmed disjoint partition of $\Omega$ into all four subsets |
| 018 | Four-way reliability evaluation | Positive reliability signal survived the held-out evaluation split |
| 020 | All-slice reliability evaluation | Positive alignment across all 16 slices of one volume |
| 021 | Baseline-controlled analysis | Input intensity outperforms raw MC dropout; partial correlation $\approx 0.047$ |
| 022 | Ridge-calibrated hybrid map | Calibration improves over uncalibrated baselines; dropout coefficient small |
| 023B | Two-stage heteroscedastic uncertainty | Decoupled training resolves moving-target failure; uncertainty head still weak |
| 024 | Per-slice Reliability CNN | Beats dropout and edge map; unstable and below input intensity |
| 025 | Cross-slice Reliability CNN | Beats input intensity within one volume (all 16 slices) |
| 026 | 4-channel CNN + dropout uncertainty | Adding MC dropout degrades performance; 3-channel model remains best |
| 027 | Single-source cross-volume validation | Partial transfer; falls below input intensity cross-volume |
| 028 | Multi-volume training (4 volumes) | Near-parity with input intensity on one held-out volume |
| **029** | **Leave-one-volume-out validation** | **Beats input intensity in 4/5 held-out volumes** |

---

## 5. Key Result: Experiment 029 — Leave-One-Volume-Out Validation

Five matched AXT2/R=4 fastMRI brain volumes. Each fold trains on four volumes and evaluates on the fifth.

### Per-Fold Results

| Fold | Held-Out Volume | CNN Mean $\rho$ | Intensity Mean $\rho$ | $\Delta$ (CNN − Intensity) |
|---:|---|---:|---:|---:|
| 1 | `file_brain_AXT2_200_6002495.h5` | 0.5657 | 0.5529 | **+0.0128** |
| 2 | `file_brain_AXT2_200_6002623.h5` | 0.5733 | 0.5546 | **+0.0187** |
| 3 | `file_brain_AXT2_200_6002398.h5` | 0.5449 | 0.5364 | **+0.0085** |
| 4 | `file_brain_AXT2_200_2000341.h5` | 0.5916 | 0.5641 | **+0.0275** |
| 5 | `file_brain_AXT2_200_2000271.h5` | 0.5808 | 0.5821 | −0.0013 |

CNN beats input intensity in **4/5 held-out volumes**. The single exception (Fold 5) corresponds to the volume with the highest input intensity baseline across all experiments ($\rho = 0.582$) and has a negligible margin ($-0.001$).

### Overall Summary

| Method | Mean $\rho$ across held-out volumes | Std |
|---|---:|---:|
| **Reliability CNN** | **0.5713** | **0.0176** |
| Input intensity | 0.5580 | 0.0167 |
| Mean reconstruction intensity | 0.4980 | 0.0351 |
| Dropout uncertainty | 0.4900 | 0.0326 |
| Edge map | 0.4005 | 0.0337 |

**Mean CNN − Input Intensity margin:** $+0.0132 \pm 0.0108$

---

## 6. Interpretation

### What the result establishes

The multi-volume Reliability CNN produces a learned reliability map that:

1. **Generalises across subjects** under matched AXT2/R=4 acquisition conditions — 4/5 held-out volumes show positive margins over input intensity.
2. **Consistently outperforms all stochastic and gradient-based baselines** — dropout uncertainty, mean reconstruction intensity, and edge maps are clearly below in all folds.
3. **Has lower slice-to-slice variance than input intensity** in most folds — important for clinical interpretability, where a reliability map must be stable across the full scan volume.

### What the result does not establish

The margin over input intensity is modest ($+0.013$ on average) and is negative in Fold 5. The method does not yet demonstrate:

- superiority over input intensity on every subject,
- generalisation to other acquisition types, acceleration factors, or coil configurations,
- clinical-grade reconstruction error prediction,
- multicoil or scanner-independent reliability estimation.

### Mechanistic summary

The dominant signal for predicting reconstruction residual energy in undersampled MRI is anatomical intensity — high-intensity regions produce larger absolute reconstruction errors due to signal dynamic range. The Reliability CNN, trained on $\Lambda_{\mathrm{cal}}$ residuals from multiple subjects, learns to approximate and modestly improve upon this relationship using structural image features. The improvement is genuine but incremental: the network adds value beyond what raw intensity provides, but intensity remains a strong competing baseline.

---

## 7. Safe Manuscript Claim

> We propose a four-way self-supervised k-space partitioning framework for residual-calibrated reliability learning in accelerated brain MRI reconstruction. A multi-volume Reliability CNN trained on calibration-subset residuals from multiple subjects modestly but consistently improved held-out residual-energy prediction over input intensity in leave-one-volume-out validation across matched AXT2/R=4 fastMRI brain volumes, while clearly outperforming MC dropout uncertainty, edge-based, and reconstruction-intensity baselines. The framework requires no fully sampled reference images and operates within a standard self-supervised reconstruction pipeline.

---

## 8. Claims to Avoid

The following claims are **not supported** by the current experimental evidence:

| Claim | Reason |
|---|---|
| Clinically calibrated uncertainty | No clinical reader study or diagnostic outcome validation |
| Generalisation across MRI protocols | Single acquisition type (AXT2) and acceleration factor (R=4) tested |
| State-of-the-art reconstruction quality | Reconstruction quality was not the evaluation target |
| Voxel-wise clinical error prediction | Evaluated against k-space residual energy, not image-domain ground-truth error |
| Scanner-independent reliability | Single scanner/coil setup; no multi-site data |
| Replacement of multicoil reconstruction | Single-coil-equivalent baseline only |

---

## 9. Proposed Paper Structure

### Recommended title
**Four-Way Self-Supervised K-Space Partitioning for Residual-Calibrated Reliability Learning in Accelerated Brain MRI**

### Recommended paper type
Methods / feasibility study

### Target venue
Realistic Scopus-indexed journal in medical imaging, biomedical signal processing, or engineering (e.g. *Magnetic Resonance Imaging*, *Computerized Medical Imaging and Graphics*, *Biomedical Signal Processing and Control*). Not yet at IEEE TMI-level full clinical validation scope.

---

## 10. Proposed Figures

| Figure | Content |
|---|---|
| Fig. 1 | Four-way k-space split diagram: $\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$ |
| Fig. 2 | Full pipeline: undersampled k-space → SSDU reconstruction → residual maps → Reliability CNN → held-out evaluation |
| Fig. 3 | LOVO result plot: CNN vs. input intensity vs. dropout vs. edge vs. reconstruction intensity, across 5 folds |
| Fig. 4 | Example visual maps for one slice: $x_\Theta$, $\hat{x}$, $\lvert \nabla \hat{x} \rvert$, $E_{\Lambda_{\mathrm{eval}}}$, $R_\phi$ |
| Fig. 5 | Borderline or failure case: a fold or slice where input intensity is comparable to or exceeds the CNN |

---

## 11. Proposed Tables

| Table | Content |
|---|---|
| Table 1 | Experiment timeline (Experiments 017–029): purpose and key finding |
| Table 2 | LOVO per-fold results (Experiment 029): CNN vs. baselines across 5 held-out volumes |
| Table 3 | Overall baseline comparison: mean $\rho$, std, and pairwise margins |

---

## 12. Current Limitations

| Limitation | Impact |
|---|---|
| Five AXT2/R=4 volumes | Low statistical power across subjects |
| Single coil, single-coil-equivalent setup | No multicoil sensitivity modelling |
| One acquisition type, one acceleration factor | Cross-protocol generalisation unverified |
| No fully sampled reference | True image-domain error unverifiable |
| No clinical reader validation | Perceptual reliability unvalidated |
| Residual energy proxy, not direct error | Evaluation metric is a k-space surrogate, not ground-truth reconstruction error |

---

## 13. Next Actions

- [ ] Freeze the current method (3-channel cross-slice multi-volume Reliability CNN)
- [ ] Clean and document the GitHub repository structure
- [ ] Generate final paper figures (Figs. 1–5 above)
- [ ] Draft manuscript outline and Introduction
- [ ] Write Methods section with four-way partition formalism
- [ ] Choose target Scopus-indexed journal and review submission guidelines
- [ ] Extend to additional acquisition types (AXT1, AXFLAIR) as future work

---

## 14. Final Project Status

The project has progressed from a single-slice feasibility test to a coherent multi-volume validated methods paper candidate.

**The primary contribution is not MC dropout uncertainty.** The primary contribution is:

> The **four-way SSDU k-space partition** — a framework that generates a calibration signal and a held-out evaluation target from the acquired undersampled k-space alone, enabling learned residual-calibrated reliability estimation without fully sampled reference data.

**The strongest result is:**

> Leave-one-volume-out validation showing modest but repeatable improvement over input intensity in 4/5 held-out AXT2/R=4 brain volumes, with consistent superiority over all stochastic and gradient-based baselines.
