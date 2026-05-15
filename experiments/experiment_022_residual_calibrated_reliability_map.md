# Experiment 022 — Residual-Calibrated Reliability Map

## Objective

Evaluate whether a **residual-calibrated reliability map** — fitted using the calibration subset $\Lambda_{\mathrm{cal}}$ — can predict unseen held-out residual energy better than raw dropout uncertainty or structural image baselines.

---

## Motivation

Experiment 021 established two findings:

1. Raw MC dropout uncertainty is positively aligned with held-out evaluation residual energy ($\rho = 0.470 \pm 0.045$).
2. However, input image intensity is a stronger predictor ($\rho = 0.553 \pm 0.041$), and partial correlation analysis showed that dropout uncertainty retains only a small independent contribution ($\rho_{\mathrm{partial}} \approx 0.047$) after controlling for image structure.

This raises a natural question:

> *If $\Lambda_{\mathrm{cal}}$ is available as a calibration signal, can it be used to learn a weighted combination of uncertainty and structural predictors that outperforms any single map?*

This experiment converts $\Lambda_{\mathrm{cal}}$ from a **passive analysis tool** into an **active calibration mechanism** by fitting a linear reliability model on calibration residuals and evaluating strictly on $\Lambda_{\mathrm{eval}}$.

---

## Four-Way SSDU Setup

The acquired k-space mask $\Omega$ is split into four disjoint subsets:

$$
\Omega = \Theta \;\cup\; \Lambda_{\mathrm{train}} \;\cup\; \Lambda_{\mathrm{cal}} \;\cup\; \Lambda_{\mathrm{eval}}
$$

| Subset | Role in this experiment |
|---|---|
| $\Theta$ | Forms the zero-filled reconstruction input |
| $\Lambda_{\mathrm{train}}$ | Provides the SSDU training loss |
| $\Lambda_{\mathrm{cal}}$ | **Fits the calibrated reliability model** |
| $\Lambda_{\mathrm{eval}}$ | Held-out evaluation only — never seen during fitting |

---

## Predictor Maps

| Symbol | Definition |
|---|---|
| $U$ | Voxel-wise variance across MC dropout reconstructions |
| $I$ | Absolute value of the $\Theta$-only zero-filled input $\lvert x_\Theta \rvert$ |
| $G$ | Gradient magnitude of the mean reconstruction $\lVert \nabla \hat{y} \rVert$ |

---

## Calibrated Reliability Models

### Structural calibrated map

Uses only image-derived predictors — no uncertainty:

$$
R_{\mathrm{struct}} = \beta_0 + \beta_1 I + \beta_2 G
$$

This is the appropriate ablation baseline: it tests whether the calibration procedure itself (ridge regression on $\Lambda_{\mathrm{cal}}$) improves over uncalibrated intensity, independent of any dropout signal.

### Hybrid calibrated map

Adds dropout uncertainty as an additional predictor:

$$
R_{\mathrm{hybrid}} = \beta_0 + \beta_1 U + \beta_2 I + \beta_3 G
$$

### Calibration target and evaluation target

Coefficients $\{\beta_i\}$ are fitted by **ridge regression** on the calibration residual energy:

$$
E_{\Lambda_{\mathrm{cal}}} = \left| \mathcal{F}^{-1}\!\left( r_{\Lambda_{\mathrm{cal}}} \right) \right|^2, \qquad r_{\Lambda_{\mathrm{cal}}} = M_{\Lambda_{\mathrm{cal}}} \odot (\hat{y} - y)
$$

The fitted map is then evaluated against the **held-out** evaluation residual energy:

$$
E_{\Lambda_{\mathrm{eval}}} = \left| \mathcal{F}^{-1}\!\left( r_{\Lambda_{\mathrm{eval}}} \right) \right|^2, \qquad r_{\Lambda_{\mathrm{eval}}} = M_{\Lambda_{\mathrm{eval}}} \odot (\hat{y} - y)
$$

The strict separation between fitting (on $\Lambda_{\mathrm{cal}}$) and evaluation (on $\Lambda_{\mathrm{eval}}$) is the core validity guarantee of this analysis.

---

## Results

### Evaluation Alignment Across All 16 Slices

| Method | Mean $\rho$ | Std | Min | Max |
|---|---:|---:|---:|---:|
| Raw dropout uncertainty | 0.470 | 0.045 | 0.381 | 0.535 |
| Input intensity | 0.553 | 0.041 | 0.478 | 0.625 |
| Mean reconstruction intensity | 0.460 | 0.037 | 0.415 | 0.547 |
| Edge map | 0.395 | 0.045 | 0.304 | 0.468 |
| Structural calibrated map | 0.558 | 0.042 | 0.482 | 0.636 |
| **Hybrid calibrated map** | **0.560** | **0.041** | **0.486** | **0.639** |

### Pairwise Margins: Hybrid vs. Key Comparators

| Comparison | Mean Difference | Std | Min | Max |
|---|---:|---:|---:|---:|
| Hybrid − Raw dropout | +0.089 | 0.015 | +0.065 | +0.121 |
| Hybrid − Input intensity | +0.0067 | 0.0041 | −0.0003 | +0.0141 |
| Hybrid − Structural calibrated | +0.0017 | 0.0011 | +0.0004 | +0.0039 |

### Mean Fitted Regression Coefficients

| Predictor | Mean $\hat{\beta}$ | Std | Min | Max |
|---|---:|---:|---:|---:|
| Dropout uncertainty $U$ | 0.050 | 0.021 | 0.017 | 0.092 |
| Input intensity $I$ | 0.261 | 0.063 | 0.150 | 0.387 |
| Edge magnitude $G$ | 0.081 | 0.049 | 0.012 | 0.167 |

---

## Interpretation

### What the calibration achieves

The hybrid calibrated map achieves the best overall evaluation alignment:

$$
\rho(R_{\mathrm{hybrid}},\; E_{\Lambda_{\mathrm{eval}}}) = 0.560 \pm 0.041
$$

This is a meaningful improvement over raw dropout ($+0.089$) and a modest improvement over uncalibrated input intensity ($+0.007$). The result confirms that fitting on $\Lambda_{\mathrm{cal}}$ transfers usefully to $\Lambda_{\mathrm{eval}}$ — the calibration partition is doing real work.

### What the coefficient table reveals

The fitted coefficients expose the relative predictive weight of each signal. Input intensity $I$ carries the largest coefficient ($\hat{\beta}_2 = 0.261 \pm 0.063$) and dominates the model. Edge magnitude $G$ contributes moderately ($\hat{\beta}_3 = 0.081$). Dropout uncertainty $U$ has a consistently positive but small coefficient ($\hat{\beta}_1 = 0.050 \pm 0.021$), confirming it adds marginal value but is not the primary driver.

### What the hybrid-vs-structural margin means

The improvement of the hybrid over the structural calibrated map is $+0.0017$ — small in absolute terms but strictly positive across all 16 slices (min $+0.0004$). This means dropout uncertainty is a reliably positive but weak incremental predictor. A reviewer could reasonably question whether this margin is practically significant.

### Overall picture

The dominant signal for predicting reconstruction error in undersampled MRI remains the anatomical intensity of the input image. Dropout uncertainty contributes genuine but modest additional information after intensity and edges are accounted for. Calibration via $\Lambda_{\mathrm{cal}}$ provides a principled way to combine these signals and consistently improves over any single uncalibrated map.

---

## Reviewer-Level Significance

This experiment makes two contributions to the project's reviewability:

**1. It validates the four-way partition design.**  
The fact that a model fitted on $\Lambda_{\mathrm{cal}}$ generalises to $\Lambda_{\mathrm{eval}}$ demonstrates that the two held-out subsets are exchangeable enough for calibration to transfer — a non-trivial property of the four-way split that could be highlighted in a methods paper.

**2. It precisely locates the current weakness.**  
The small hybrid-vs-structural margin and the low dropout coefficient jointly confirm that MC dropout is a weak independent uncertainty source. A reviewer asking *"why not just use image intensity?"* receives an honest answer: the calibrated combination is better, but the MC dropout contribution is currently marginal.

The corrected framing for the proposed method is:

> A **four-way SSDU residual-calibrated reliability framework** in which the calibration subset is used to learn a reliability model combining structural and stochastic uncertainty signals — with MC dropout serving as a baseline uncertainty feature pending development of stronger uncertainty representations.

---

## Limitations

- One fastMRI file, one coil — cross-file and multicoil generalization untested.
- Linear ridge calibration model — nonlinear interactions between $U$, $I$, $G$ are not captured.
- MC dropout is the only stochastic uncertainty source tested.
- No fully sampled reference image — true image-domain error cannot be verified.
- The margin of hybrid over structural calibration ($+0.0017$) is small; practical significance requires multi-file replication.

---

## Next Methodological Direction

The experiment localises the bottleneck clearly: **the uncertainty feature $U$ is too weak**. The calibration framework is sound; what needs to improve is the quality of the stochastic uncertainty signal fed into it. Candidate directions include:

| Uncertainty Method | Key Property |
|---|---|
| Deep ensemble | Independent network initializations; often stronger than MC dropout |
| Heteroscedastic variance head | Directly predicts aleatoric uncertainty per voxel |
| Residual-supervised uncertainty head | Trained explicitly to predict $E_{\Lambda_{\mathrm{cal}}}$, not just reconstruction error |
| Nonlinear calibration model | Captures interactions between $U$, $I$, $G$ via a small MLP or kernel method |

All candidates should be evaluated within the same four-way SSDU framework, fitting on $\Lambda_{\mathrm{cal}}$ and reporting only $\Lambda_{\mathrm{eval}}$ alignment.

---

## Conclusion

Residual calibration using $\Lambda_{\mathrm{cal}}$ improves reliability prediction on the held-out $\Lambda_{\mathrm{eval}}$ subset. The hybrid calibrated map achieves the best evaluation alignment ($0.560 \pm 0.041$), but the gain over structural calibration alone is small ($+0.0017$), indicating that MC dropout currently contributes only marginal independent predictive power.

The four-way SSDU calibration framework is validated as a methodology. The next priority is developing a stronger uncertainty feature to replace MC dropout as the stochastic component of the calibrated reliability model.
