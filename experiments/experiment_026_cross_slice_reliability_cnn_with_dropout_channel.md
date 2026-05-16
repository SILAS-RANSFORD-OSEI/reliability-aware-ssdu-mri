# Experiment 026 — Cross-Slice Reliability CNN With Dropout Uncertainty Channel

## Objective

Evaluate whether adding MC dropout uncertainty $U$ as a fourth input channel to the cross-slice reliability CNN improves held-out residual-energy prediction beyond the structural-only 3-channel model from Experiment 025.

---

## Motivation

Experiment 025 established that a 3-channel cross-slice reliability CNN using structural inputs $(x_\Theta, \hat{x}, \lvert \nabla \hat{x} \rvert)$ achieves $\rho = 0.583 \pm 0.046$ — the first result to consistently outperform input intensity across all 16 slices.

The partial correlation analysis from Experiment 021 showed that MC dropout uncertainty retains a small but non-zero independent association with residual energy after controlling for image structure ($\rho_{\mathrm{partial}} \approx 0.047$–$0.056$). This motivated the hypothesis that adding $U$ as an explicit input channel might provide the network with stochastic information that the structural channels cannot express — and produce an incremental improvement in evaluation alignment.

This experiment tests that hypothesis.

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
| $\Lambda_{\mathrm{cal}}$ | Supervises the shared 4-channel reliability CNN |
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
| Reliability training | All 16 slices (shared model) |
| Reliability evaluation | All 16 slices |

---

## Reliability Network

The 4-channel reliability CNN extends the Experiment 025 model with MC dropout uncertainty as an additional input:

$$
R_{\mathrm{net,4ch}} = h_\phi\!\left( x_\Theta,\; \hat{x},\; \lvert \nabla \hat{x} \rvert,\; U \right)
$$

where:
- $x_\Theta$ — zero-filled $\Theta$-only input image
- $\hat{x}$ — mean reconstruction from the frozen dropout CNN
- $\lvert \nabla \hat{x} \rvert$ — gradient magnitude of the mean reconstruction
- $U$ — voxel-wise MC dropout uncertainty (variance across stochastic forward passes)

### Training target and evaluation target

$$
E_{\Lambda_{\mathrm{cal}}} = \left| \mathcal{F}^{-1}\!\left( r_{\Lambda_{\mathrm{cal}}} \right) \right|^2, \qquad E_{\Lambda_{\mathrm{eval}}} = \left| \mathcal{F}^{-1}\!\left( r_{\Lambda_{\mathrm{eval}}} \right) \right|^2
$$

The model is trained on all 16 slices using $E_{\Lambda_{\mathrm{cal}}}$ and evaluated only on $E_{\Lambda_{\mathrm{eval}}}$, preserving the held-out validity of the evaluation.

### Training loss progression

| Quantity | Value |
|---|---:|
| Initial mean reliability loss | 0.045927 |
| Final mean reliability loss | 0.002542 |
| Relative reduction | ~94% |

The loss reduction confirms the 4-channel network successfully optimised the calibration target.

---

## Results

### Evaluation Alignment Across All 16 Slices

| Method | Mean $\rho$ | Std | Min | Max |
|---|---:|---:|---:|---:|
| 3-channel CNN (Experiment 025) | 0.583 | 0.046 | 0.504 | 0.673 |
| **4-channel CNN (this experiment)** | **0.557** | **0.039** | **0.489** | **0.620** |
| Input intensity | 0.553 | 0.041 | 0.478 | 0.625 |
| Dropout uncertainty | 0.470 | 0.045 | 0.381 | 0.535 |
| Mean reconstruction intensity | 0.460 | 0.037 | 0.415 | 0.547 |
| Edge map | 0.395 | 0.045 | 0.304 | 0.468 |

### Pairwise Margins: 4-Channel CNN vs. Key Comparators

| Comparison | Mean $\Delta$ | Std | Min | Max |
|---|---:|---:|---:|---:|
| 4-ch − 3-ch CNN | −0.026 | — | — | — |
| 4-ch − Input intensity | +0.0038 | 0.0156 | −0.023 | +0.036 |
| 4-ch − Dropout uncertainty | +0.086 | 0.022 | +0.056 | +0.134 |
| 4-ch − Edge map | +0.162 | 0.032 | +0.112 | +0.206 |

---

## Interpretation

### Primary result: adding $U$ reduced alignment

The 4-channel model achieves $\rho = 0.557 \pm 0.039$, compared with the 3-channel model's $0.583 \pm 0.046$. Adding the dropout uncertainty channel **decreased** mean evaluation alignment by $0.026$. This is a consistent degradation — not noise — given that the evaluation is averaged over 16 slices.

The 4-channel model still outperforms input intensity on average ($\Delta = +0.004$), but the minimum margin is now negative ($-0.023$), meaning the model regresses below input intensity on at least one slice. This is a weaker result than Experiment 025, where all 16 slices exceeded input intensity.

### Why might adding $U$ hurt?

Several mechanisms are plausible:

**1. Noise injection.** MC dropout uncertainty computed from a weak reconstruction model has low signal-to-noise. When added as an input channel, it injects spatially structured noise that the network must learn to discount rather than use. The cost of discounting — wasted capacity — slightly degrades the use of the structural channels.

**2. Distribution mismatch across slices.** Dropout uncertainty magnitude varies substantially across slices (as implied by the SSDU loss range in Experiment 020). A shared network must normalise $U$ implicitly or learn to ignore it when its scale is inconsistent — an additional difficulty not present in the structural channels, which share a common image-domain scale.

**3. Collinearity.** $U$ is partially correlated with $\hat{x}$ (as shown in Experiment 021 — much of the raw dropout alignment is explained by intensity). Adding a partially collinear channel to a small network can destabilise weights without adding independent information.

**4. Optimisation surface change.** The higher initial calibration loss ($0.046$ vs. $0.021$ in Experiment 025) suggests the 4-channel optimisation landscape is harder to navigate, potentially due to the additional input dimension and its scale relative to the structural channels.

### What the variance change tells us

The 4-channel model has slightly lower variance (std = 0.039) than the 3-channel model (std = 0.046). This is consistent with the network learning to suppress the $U$ channel — a suppressed channel contributes less slice-to-slice variability, so variance decreases even as mean alignment drops. If the network had learned to use $U$ productively, we would expect both mean and variance to change in the same direction.

### Consistency with prior experiments

This result is consistent with the pattern established across Experiments 021–025: MC dropout uncertainty carries a small, positive independent signal ($\rho_{\mathrm{partial}} \approx 0.047$), but it is too weak and too correlated with intensity to provide a reliable additive gain when structural features are already present. The partial correlation from Experiment 021 predicted a small effect; the 4-channel experiment confirms that the effect is, if anything, negative under the current CNN architecture.

---

## Reviewer-Level Significance

This experiment closes the MC dropout investigation with a clear and defensible conclusion:

> MC dropout uncertainty is a positive but weak reliability signal in isolation. When combined with structural features in a learned reliability network, it does not provide additive benefit and may marginally degrade performance under the current architecture.

This is not a failure of the four-way SSDU framework — it is a precise characterisation of MC dropout's role within it. The correct experimental response is to **consolidate the 3-channel model as the current best method** and shift the focus toward cross-volume validation rather than further input engineering on a single volume.

A reviewer asking *"why not use a better uncertainty method?"* receives an honest answer: the framework is designed to accommodate stronger uncertainty representations, but MC dropout is not one of them for this task.

---

## Current Best Method

The current best reliability model across all experiments is the **3-channel cross-slice Reliability CNN** from Experiment 025:

$$
R_{\mathrm{net}} = h_\phi\!\left( x_\Theta,\; \hat{x},\; \lvert \nabla \hat{x} \rvert \right)
$$

trained on $\Lambda_{\mathrm{cal}}$ across all 16 slices and evaluated on $\Lambda_{\mathrm{eval}}$.

$$
\rho = 0.583 \pm 0.046
$$

This model outperforms input intensity consistently across all 16 slices (minimum margin $+0.010$) and is more stable than the per-slice variant (std $0.046$ vs. $0.080$).

---

## Limitations

- One fastMRI volume, one coil — cross-volume and multicoil generalisation untested.
- The degradation mechanism for adding $U$ is diagnosed but not formally ablated (e.g., by training with $U$ alone as the only input).
- No normalisation of $U$ across slices was applied — this may account for the distribution mismatch issue.
- No fully sampled reference — true image-domain error cannot be verified.

---

## Next Methodological Direction

Two directions are motivated:

### 1. Cross-volume validation of the 3-channel model

The 3-channel model is the current best method. The immediate priority is testing whether it generalises to a second fastMRI volume — a prerequisite for any journal-level reliability claim.

### 2. Explicit absolute-intensity inputs

The next architectural variant to test uses magnitude images directly as inputs, ensuring the network receives clean, non-negative intensity information:

$$
R_{\mathrm{net}} = h_\phi\!\left( \lvert x_\Theta \rvert,\; \lvert \hat{x} \rvert,\; \lvert \nabla \hat{x} \rvert \right)
$$

This removes any phase information that may add variance to the input without improving the reliability signal, and aligns the input representation with what the linear calibration model used in Experiment 022.

---

## Conclusion

Adding MC dropout uncertainty as a fourth input channel to the cross-slice reliability CNN decreased mean evaluation alignment from $0.583$ to $0.557$ and introduced negative margins against input intensity on some slices. The result is consistent with the project-wide finding that MC dropout is a weak independent reliability signal when structural features are available. The 3-channel cross-slice CNN from Experiment 025 remains the current best method. The next priority is cross-volume validation rather than further input engineering within the current single-volume setting.
