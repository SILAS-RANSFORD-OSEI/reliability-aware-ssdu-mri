# Experiment 021 — Baseline-Controlled Reliability Analysis

## Objective

Evaluate whether dropout-derived uncertainty predicts unseen held-out residual energy **better than trivial reliability maps** — establishing whether the uncertainty signal is genuinely reconstruction-specific or simply a proxy for anatomical image structure.

---

## Motivation

Experiment 020 demonstrated that dropout uncertainty is positively aligned with evaluation residual energy under a four-way SSDU split across all 16 slices. However, a positive raw correlation is not sufficient evidence of a useful uncertainty signal.

A reviewer may ask:

> *Is the uncertainty–residual alignment uncertainty-specific, or is it simply driven by anatomical intensity, image edges, or random spatial structure?*

This experiment answers that question by benchmarking dropout uncertainty against four simple reliability baselines on the same evaluation target.

---

## Dataset

| Property | Value |
|---|---|
| Dataset | fastMRI Brain |
| Acquisition | AXT2 |
| Acceleration | R = 4 |
| Working setup | Single-coil-equivalent |
| Tested slices | 0 – 15 (all 16 slices) |
| Evaluation subset | $\Lambda_{\mathrm{eval}}$ |

---

## Four-Way SSDU Setup

The acquired k-space mask $\Omega$ is split into four disjoint subsets:

$$
\Omega = \Theta \;\cup\; \Lambda_{\mathrm{train}} \;\cup\; \Lambda_{\mathrm{cal}} \;\cup\; \Lambda_{\mathrm{eval}}
$$

| Subset | Role |
|---|---|
| $\Theta$ | Forms the zero-filled reconstruction input |
| $\Lambda_{\mathrm{train}}$ | Provides the SSDU training loss |
| $\Lambda_{\mathrm{cal}}$ | Reserved for calibration-style reliability analysis |
| $\Lambda_{\mathrm{eval}}$ | Held-out subset for final reliability evaluation only |

The model was trained exclusively on $\Lambda_{\mathrm{train}}$. The evaluation target $E_{\Lambda_{\mathrm{eval}}}$ was never accessible during training.

---

## Reliability Maps Compared

| Reliability Map | Description |
|---|---|
| Random map | Spatially random values — sanity check lower bound |
| Input intensity | $\lvert x_\Theta \rvert$: absolute value of the $\Theta$-only zero-filled input |
| Mean reconstruction intensity | $\lvert \hat{y} \rvert$: absolute value of the mean dropout reconstruction |
| Edge map | $G = \lVert \nabla \hat{y} \rVert$: gradient magnitude of the mean reconstruction |
| Dropout uncertainty | $U$: voxel-wise variance across stochastic MC dropout reconstructions |

---

## Evaluation Target

The held-out k-space residual on $\Lambda_{\mathrm{eval}}$ is:

$$
r_{\Lambda_{\mathrm{eval}}} = M_{\Lambda_{\mathrm{eval}}} \odot (\hat{y} - y)
$$

where $M_{\Lambda_{\mathrm{eval}}}$ is the binary mask selecting only $\Lambda_{\mathrm{eval}}$ frequencies. The corresponding image-domain residual energy is obtained by backprojecting through the inverse Fourier transform:

$$
E_{\Lambda_{\mathrm{eval}}} = \left| \mathcal{F}^{-1}\!\left( r_{\Lambda_{\mathrm{eval}}} \right) \right|^2
$$

Each reliability map was compared with $E_{\Lambda_{\mathrm{eval}}}$ using **Pearson correlation**, averaged over all 16 slices.

---

## Results

### Alignment of Each Reliability Map vs. $E_{\Lambda_{\mathrm{eval}}}$

| Reliability Map | Mean $\rho$ | Std | Min | Max |
|---|---:|---:|---:|---:|
| Random map | 0.000 | 0.002 | −0.002 | 0.004 |
| Input intensity | 0.553 | 0.041 | 0.478 | 0.625 |
| Mean reconstruction intensity | 0.460 | 0.037 | 0.415 | 0.547 |
| Edge map | 0.395 | 0.045 | 0.304 | 0.468 |
| **Dropout uncertainty** | **0.470** | **0.045** | **0.381** | **0.535** |

### Pairwise Margin: Dropout Uncertainty vs. Each Baseline

| Comparison | Mean Difference | Std | Min | Max |
|---|---:|---:|---:|---:|
| Dropout − Random | +0.470 | 0.045 | +0.382 | +0.534 |
| Dropout − Input intensity | −0.083 | 0.015 | −0.107 | −0.058 |
| Dropout − Mean intensity | +0.010 | 0.028 | −0.034 | +0.055 |
| Dropout − Edge map | +0.076 | 0.021 | +0.044 | +0.114 |

---

## Partial Correlation Analysis

To isolate the **independent contribution** of dropout uncertainty beyond shared image structure, partial correlations were computed by regressing out intensity and edge information.

**Raw alignment (no control):**

$$
\rho\!\left(U,\; E_{\Lambda_{\mathrm{eval}}}\right) = 0.470 \pm 0.045
$$

**Controlling for input intensity and edge magnitude:**

$$
\rho\!\left(U,\; E_{\Lambda_{\mathrm{eval}}} \;\middle|\; I_{\mathrm{input}},\; G\right) = 0.056 \pm 0.014
$$

**Controlling for input intensity, mean reconstruction intensity, and edge magnitude:**

$$
\rho\!\left(U,\; E_{\Lambda_{\mathrm{eval}}} \;\middle|\; I_{\mathrm{input}},\; I_{\mathrm{mean}},\; G\right) = 0.047 \pm 0.018
$$

The partial correlation drops from **0.470** to approximately **0.047–0.056** after conditioning on basic image structure. This means the vast majority of the raw uncertainty–residual alignment is explained by shared anatomical intensity and gradient structure, not by reconstruction-specific uncertainty.

---

## Interpretation

The results present a nuanced picture:

**What dropout uncertainty does well:**
- Substantially outperforms a random map ($\Delta = +0.470$), confirming it carries non-trivial spatial information.
- Outperforms the edge map ($\Delta = +0.076$) and is approximately on par with mean reconstruction intensity ($\Delta = +0.010$).

**Where dropout uncertainty falls short:**
- Input intensity alone achieves stronger alignment (0.553) than dropout uncertainty (0.470), despite being a strictly simpler signal.
- After removing the variance explained by intensity and edges, dropout uncertainty retains only a small independent association ($\rho_{\mathrm{partial}} \approx 0.047$–$0.056$) with held-out residual energy.

**Mechanistic interpretation:**  
MC dropout uncertainty in a CNN trained on undersampled MRI tends to be spatially correlated with image brightness — high-intensity anatomical regions produce larger absolute reconstruction errors, which in turn drive both the residual energy and the uncertainty estimate. The partial correlation analysis reveals that this covariance with image intensity is the dominant driver of the raw alignment, not a genuine model-based uncertainty signal about reconstruction fidelity.

---

## Reviewer-Level Significance

This experiment prevents overclaiming and defines the honest scope of MC dropout uncertainty as a reliability tool within the SSDU framework.

A reviewer could reasonably argue:

> *Dropout uncertainty is largely a proxy for image intensity, which is a trivial baseline. The claimed uncertainty–residual alignment does not demonstrate a fundamentally new reliability signal.*

This experiment **validates that concern** and reframes the contribution accordingly. The conclusion is not that dropout uncertainty is uninformative — it is that **uncalibrated MC dropout is an insufficient final method** for a high-quality reliability claim.

The correct framing for the proposed method is therefore:

> A **four-way SSDU reliability framework** that exposes the limitations of uncalibrated stochastic uncertainty and motivates the transition to **residual-calibrated uncertainty learning** using $\Lambda_{\mathrm{cal}}$.

---

## Next Methodological Direction

The calibration subset $\Lambda_{\mathrm{cal}}$ should be used as an **active calibration mechanism**, not merely a passive analysis tool. A natural next step is to fit a linear combination of available reliability signals on $\Lambda_{\mathrm{cal}}$ and evaluate only on $\Lambda_{\mathrm{eval}}$:

$$
U_{\mathrm{hybrid}} = \beta_1\, U + \beta_2\, I + \beta_3\, G
$$

where:
- $U$ — dropout uncertainty
- $I$ — image intensity ($\lvert \hat{y} \rvert$)
- $G$ — edge magnitude ($\lVert \nabla \hat{y} \rVert$)
- $\beta_1, \beta_2, \beta_3$ — coefficients fitted by regression on $\Lambda_{\mathrm{cal}}$

This hybrid map is evaluated only on $\Lambda_{\mathrm{eval}}$, preserving the held-out validity of the evaluation. The question of interest is whether a calibrated linear combination can outperform input intensity alone — and whether dropout uncertainty contributes incremental value beyond the intensity and edge components.

---

## Limitations

- One fastMRI file, one coil — cross-file and multicoil generalization untested.
- Linear partial correlation may underestimate nonlinear shared structure.
- No conformal or distribution-free calibration has been applied.
- The hybrid model $U_{\mathrm{hybrid}}$ is proposed but not yet evaluated.

---

## Conclusion

Baseline-controlled analysis reveals that raw MC dropout uncertainty achieves positive alignment with held-out evaluation residual energy, but its independent contribution beyond anatomical intensity and edge structure is weak ($\rho_{\mathrm{partial}} \approx 0.047$–$0.056$). Input intensity is a stronger reliability baseline.

This result is **not a failure** — it is a precise characterisation of what uncalibrated MC dropout can and cannot provide. It motivates the next methodological step: fitting a calibrated reliability model on $\Lambda_{\mathrm{cal}}$ that combines uncertainty, intensity, and edge signals to maximise alignment on the held-out $\Lambda_{\mathrm{eval}}$ subset.
