# Self-Supervised Residual-Calibrated Reliability Learning for Accelerated Brain MRI Reconstruction

> **Methods Draft** — A self-supervised framework for estimating spatial residual-risk reliability in accelerated MRI reconstruction using held-out acquired k-space consistency.

---

## Table of Contents

1. [Study Design](#1-study-design)
2. [MRI Forward Model](#2-mri-forward-model)
3. [Four-Way K-Space Partitioning](#3-four-way-k-space-partitioning)
4. [Theta-Only Input Image](#4-theta-only-input-image)
5. [SSDU Reconstruction Training](#5-ssdu-reconstruction-training)
6. [Reconstruction CNN Architecture](#6-reconstruction-cnn-architecture)
7. [Calibration Residual Energy](#7-calibration-residual-energy)
8. [Evaluation Residual Energy](#8-evaluation-residual-energy)
9. [Magnitude-Domain Reliability Features](#9-magnitude-domain-reliability-features)
10. [Per-Slice Normalization](#10-per-slice-normalization)
11. [ReliabilityCNN Architecture](#11-reliabilitycnn-architecture)
12. [Reliability Training Loss](#12-reliability-training-loss)
13. [Baseline Reliability Maps](#13-baseline-reliability-maps)
14. [Alignment Metric](#14-alignment-metric)
15. [Experimental Protocol](#15-experimental-protocol)
16. [Implementation Details](#16-implementation-details)
17. [Formal Experiment Categories](#17-formal-experiment-categories)
18. [Methodological Scope](#18-methodological-scope)

---

## 1. Study Design

This study develops a self-supervised framework for **residual-calibrated reliability learning** in accelerated brain MRI reconstruction. The objective is **not** to produce clinically calibrated uncertainty maps or fully sampled image-domain error maps. Instead, the aim is to estimate **spatial residual-risk reliability** using held-out acquired k-space consistency.

The proposed framework partitions the acquired k-space sampling set into four disjoint subsets:

$$\Omega = \Theta \cup \Lambda_{\text{train}} \cup \Lambda_{\text{cal}} \cup \Lambda_{\text{eval}}$$

| Subset | Role |
|---|---|
| $\Theta$ | Reconstruction input |
| $\Lambda_{\text{train}}$ | Self-supervised (SSDU) reconstruction training |
| $\Lambda_{\text{cal}}$ | Residual-calibrated reliability learning |
| $\Lambda_{\text{eval}}$ | Independent held-out reliability evaluation |

The central principle is that **reconstruction learning, reliability calibration, and final reliability evaluation must not reuse the same hidden k-space samples**. This separation reduces circularity and allows the predicted reliability-risk map to be evaluated against independent acquired k-space evidence.

---

## 2. MRI Forward Model

For multicoil MRI, the acquired k-space measurement from receiver coil $c$ is:

$$y_{\Omega,c} = M_\Omega \mathcal{F}(S_c x) + \varepsilon_c$$

where:
- $x \in \mathbb{C}^{H \times W}$ — unknown complex-valued MR image
- $S_c$ — coil sensitivity profile for coil $c$
- $\mathcal{F}$ — discrete Fourier transform
- $M_\Omega$ — binary sampling operator selecting acquired k-space locations
- $y_{\Omega,c}$ — undersampled k-space measurement for coil $c$
- $\varepsilon_c$ — measurement noise

### Single-Coil Feasibility Setting

This feasibility study uses one selected coil to isolate the reliability-learning framework before extension to full multicoil sensitivity-encoded reconstruction. Under this simplified setting:

$$y_\Omega = M_\Omega \mathcal{F} x + \varepsilon$$

> **Limitation:** The single-coil setting is a limitation of the present study. The proposed four-way reliability framework is not conceptually limited to one coil, but current experiments use one selected coil to simplify validation of the reliability-learning mechanism.

---

## 3. Four-Way K-Space Partitioning

The acquired k-space sampling set $\Omega$ is partitioned into four pairwise disjoint subsets — extending the standard two-way SSDU split:

$$\Omega = \Theta \cup \Lambda_{\text{train}} \cup \Lambda_{\text{cal}} \cup \Lambda_{\text{eval}}$$

The subsets satisfy:

$$\Theta \cap \Lambda_{\text{train}} = \Theta \cap \Lambda_{\text{cal}} = \Theta \cap \Lambda_{\text{eval}} = \Lambda_{\text{train}} \cap \Lambda_{\text{cal}} = \Lambda_{\text{train}} \cap \Lambda_{\text{eval}} = \Lambda_{\text{cal}} \cap \Lambda_{\text{eval}} = \emptyset$$

### Split Fractions

| Subset | Fraction of $\vert\Omega\vert$ |
|---|---|
| $\Theta$ | 60% |
| $\Lambda_{\text{train}}$ | 20% |
| $\Lambda_{\text{cal}}$ | 10% |
| $\Lambda_{\text{eval}}$ | 10% |

> **Physical interpretation:** Acquired k-space samples are scarce measured evidence. The four-way split assigns this evidence to distinct roles — image reconstruction input, reconstruction supervision, reliability calibration, and independent reliability evaluation.

The sampling mask was treated as a **Cartesian phase-encoding mask** of length 396, broadcast across the readout dimension.

*See: Figure 1.*

---

## 4. Theta-Only Input Image

The input reconstruction is obtained from $\Theta$ via zero-filled inverse Fourier reconstruction:

$$x_\Theta = \mathcal{F}^{-1}(M_\Theta y)$$

Because the underlying MRI data are complex-valued, the **magnitude image** is used for the real-valued CNN feature stack:

$$|x_\Theta| = \left| \mathcal{F}^{-1}(M_\Theta y) \right|$$

This magnitude-domain input provides the structural information available from the reconstruction input subset before SSDU refinement.

---

## 5. SSDU Reconstruction Training

The reconstruction network receives the magnitude-domain input image derived from $\Theta$ and predicts a residual correction:

$$\hat{x}_\theta = f_\theta(x_\Theta)$$

where $f_\theta$ is the reconstruction network and $\theta$ denotes its parameters.

Predicted k-space consistency is evaluated by Fourier-transforming the reconstructed image approximation:

$$\hat{y} = \mathcal{F}\hat{x}_\theta$$

The SSDU reconstruction loss is the raw squared k-space residual on the training subset:

$$\mathcal{L}_{\text{SSDU}} = \left\| M_{\Lambda_{\text{train}}}(\hat{y} - y) \right\|_2^2$$

This trains the reconstruction network to predict acquired k-space samples withheld from the input subset $\Theta$.

> **Note:** Because the implemented SSDU loss is scale-dependent, reconstruction training behavior is interpreted using **relative loss reduction** rather than raw loss magnitude. Reliability learning and evaluation use per-slice normalized residual-energy maps.

---

## 6. Reconstruction CNN Architecture

The reconstruction backbone is a **lightweight image-domain residual CNN with dropout**. The network receives a single-channel magnitude-domain input and predicts a residual correction:

$$\hat{x}_\theta = x_\Theta + g_\theta(x_\Theta)$$

where $g_\theta$ is the CNN-predicted residual.

| Layer | Channels | Kernel | Activation |
|---|---|---|---|
| Conv1 | 1 → 16 | 3×3 | ReLU + Dropout2d |
| Conv2 | 16 → 16 | 3×3 | ReLU + Dropout2d |
| Conv3 | 16 → 16 | 3×3 | ReLU + Dropout2d |
| Conv4 | 16 → 1 | 3×3 | Linear |
| Output | 1 | — | Input + residual |

All convolutions use **zero padding** to preserve spatial dimensions. Dropout probability: $p = 0.1$.

During stochastic uncertainty estimation, dropout is kept active and multiple reconstructions are sampled to estimate voxel-wise uncertainty.

---

## 7. Calibration Residual Energy

After reconstruction, the calibration residual is computed on $\Lambda_{\text{cal}}$:

$$r_{\Lambda_{\text{cal}}} = M_{\Lambda_{\text{cal}}}(\hat{y} - y)$$

This residual is backprojected into image space:

$$e_{\Lambda_{\text{cal}}} = \mathcal{F}^{-1} r_{\Lambda_{\text{cal}}}$$

The calibration residual energy map is:

$$E_{\Lambda_{\text{cal}}} = |e_{\Lambda_{\text{cal}}}|^2 = \left| \mathcal{F}^{-1} M_{\Lambda_{\text{cal}}}(\hat{y} - y) \right|^2$$

This map serves as the **target for residual-calibrated reliability learning**.

> **Interpretation:** Because Fourier residuals are globally backprojected into image space, $E_{\Lambda_{\text{cal}}}$ should be interpreted as an **image-domain residual-consistency proxy**, not a direct voxel-wise ground-truth image error map.

---

## 8. Evaluation Residual Energy

The final evaluation residual uses the separate held-out subset $\Lambda_{\text{eval}}$:

$$r_{\Lambda_{\text{eval}}} = M_{\Lambda_{\text{eval}}}(\hat{y} - y)$$

$$E_{\Lambda_{\text{eval}}} = \left| \mathcal{F}^{-1} M_{\Lambda_{\text{eval}}}(\hat{y} - y) \right|^2$$

> **Key constraint:** $\Lambda_{\text{eval}}$ is **never used** during reconstruction input, SSDU training, or reliability calibration. It is reserved exclusively for independent reliability evaluation.

As with the calibration residual map, $E_{\Lambda_{\text{eval}}}$ is a residual-consistency proxy derived from held-out acquired k-space — not a true image-domain error map.

---

## 9. Magnitude-Domain Reliability Features

Although the MRI acquisition model is complex-valued, the ReliabilityCNN operates on **real-valued magnitude-domain feature maps**.

The final reliability feature stack is:

$$z = \left[ |x_\Theta|,\ |\hat{x}|,\ |\nabla|\hat{x}|| \right]$$

| Channel | Description |
|---|---|
| $\|x_\Theta\|$ | Magnitude image reconstructed from input subset $\Theta$ |
| $\|\hat{x}\|$ | Magnitude SSDU reconstruction |
| $\|\nabla\|\hat{x}\|\|$ | Gradient magnitude of the reconstructed magnitude image |

**Tensor shapes (per slice):**

| Tensor | Shape |
|---|---|
| Input $z$ | $\mathbb{R}^{1 \times 3 \times 768 \times 396}$ |
| Target $E_{\Lambda_{\text{cal}}}$ | $\mathbb{R}^{1 \times 1 \times 768 \times 396}$ |

---

## 10. Per-Slice Normalization

For a two-dimensional map $A$, per-slice min-max normalization is defined as:

$$\text{norm}(A) = \frac{A - \min(A)}{\max(A) - \min(A) + \varepsilon}$$

where $\varepsilon$ is a small positive constant to avoid division by zero.

Normalization is applied **independently per slice** — not globally across the full dataset. This ensures that predicted reliability maps and residual-energy targets are compared by **spatial pattern** rather than absolute scale.

Per-slice normalization is used in the reliability loss and in alignment analysis.

---

## 11. ReliabilityCNN Architecture

The ReliabilityCNN is a **lightweight fully convolutional network**:

$$R_\phi = h_\phi(z)$$

where $h_\phi$ is the reliability network, $\phi$ denotes its parameters, $z$ is the three-channel magnitude-domain feature stack, and $R_\phi$ is the predicted residual-risk reliability map.

| Layer | Channels | Kernel | Activation |
|---|---|---|---|
| Conv1 | 3 → 16 | 3×3 | ReLU |
| Conv2 | 16 → 16 | 3×3 | ReLU |
| Conv3 | 16 → 16 | 3×3 | ReLU |
| Conv4 | 16 → 1 | 3×3 | Softplus |

All convolutions use **zero padding** to preserve spatial dimensions.

The final Softplus activation constrains the predicted map to be **strictly positive**:

$$R_\phi = \text{softplus}(h_\phi(z)) + 10^{-6}$$

Output tensor shape: $R_\phi \in \mathbb{R}^{1 \times 1 \times 768 \times 396}$

> **Interpretation:** $R_\phi$ is a **residual-risk reliability map** where larger values indicate regions predicted to have higher held-out residual energy.

*See: Figure 2.*

---

## 12. Reliability Training Loss

The ReliabilityCNN is trained to approximate the calibration residual energy map $E_{\Lambda_{\text{cal}}}$:

$$\mathcal{L}_{\text{rel}} = \left\| \text{norm}(R_\phi) - \text{norm}(E_{\Lambda_{\text{cal}}}) \right\|_2^2$$

where normalization is performed per slice.

This trains the network to predict the **spatial pattern** of calibration residual energy rather than its absolute magnitude.

---

## 13. Baseline Reliability Maps

The proposed ReliabilityCNN is compared against four baselines.

### 13.1 Input Intensity

$$R_{\text{input}} = |x_\Theta|$$

Tests whether residual energy is mostly explained by the input image structure itself.

### 13.2 Mean Reconstruction Intensity

$$R_{\text{mean}} = |\hat{x}|$$

Tests whether reconstructed image magnitude is sufficient as a reliability surrogate.

### 13.3 Edge Magnitude

$$R_{\text{edge}} = |\nabla|\hat{x}||$$

Tests whether residual energy primarily follows high-gradient anatomical boundaries.

### 13.4 Dropout Uncertainty

Monte Carlo dropout generates multiple stochastic reconstructions with dropout enabled. Voxel-wise variance serves as the dropout uncertainty map:

$$R_{\text{dropout}} = \text{Var}\left(\hat{x}^{(1)}, \hat{x}^{(2)}, \ldots, \hat{x}^{(T)}\right)$$

where $T = 8$ stochastic samples are used.

> **Note:** MC dropout is treated only as a **baseline** and is not the central proposed method.

---

## 14. Alignment Metric

Reliability performance is evaluated using **Pearson correlation** between a candidate reliability map $R$ and the held-out evaluation residual energy $E_{\Lambda_{\text{eval}}}$.

For flattened image pixels indexed by $i$:

$$\rho(R, E_{\Lambda_{\text{eval}}}) = \frac{\sum_i (R_i - \bar{R})(E_i - \bar{E})}{\sqrt{\sum_i (R_i - \bar{R})^2} \sqrt{\sum_i (E_i - \bar{E})^2}}$$

Pearson correlation was chosen because the goal is to assess **spatial alignment** with held-out residual-energy structure rather than absolute probabilistic calibration.

Correlation was computed **per slice** and aggregated across slices and held-out volumes. Pixels were not treated as independent statistical samples.

Higher $\rho$ indicates stronger spatial agreement between a candidate reliability map and held-out residual-energy structure.

---

## 15. Experimental Protocol

Final validation uses **five matched fastMRI brain AXT2/R=4 volumes**.

**Per-volume specification:**

| Property | Value |
|---|---|
| k-space shape | 16 × 16 × 768 × 396 |
| Mask shape | 396 |
| Slices | 16 |
| Selected coil | 1 |

**Validation design:** Leave-one-volume-out

| Split | Volumes | Slices |
|---|---|---|
| Training | 4 | 64 |
| Held-out test | 1 | 16 |

The ReliabilityCNN is trained on calibration residual-energy targets from the four training volumes and evaluated on the held-out volume using $\Lambda_{\text{eval}}$ residual energy.

> **Scope:** Only five volumes are used. Results are interpreted as **observed feasibility trends**, not claims of statistical significance.

---

## 16. Implementation Details

Experiments were implemented in **Python / PyTorch** and executed in **Google Colab**.

| Component | Setting |
|---|---|
| Selected coil index | 0 |
| Reconstruction training steps per slice | 50 |
| Reconstruction learning rate | $1 \times 10^{-4}$ |
| Reconstruction feature width | 16 |
| Dropout probability | 0.1 |
| Monte Carlo dropout samples | 8 |
| ReliabilityCNN input channels | 3 |
| ReliabilityCNN feature width | 16 |
| ReliabilityCNN optimizer | Adam |
| ReliabilityCNN learning rate | $1 \times 10^{-3}$ |
| ReliabilityCNN training epochs | 30 |
| Split seed | 42 |
| Split fractions | 60% / 20% / 10% / 10% |
| Validation design | Leave-one-volume-out |

Fold-specific model seeds were used during leave-one-volume-out training. All image-like maps were normalized per slice before reliability loss computation and alignment analysis.

---

## 17. Formal Experiment Categories

Experiments are organized into four formal categories.

### 17.1 Reliability Model Design

Comparison of candidate reliability predictors including dropout-based uncertainty, structural features, and the ReliabilityCNN.

### 17.2 Baseline-Controlled Reliability Evaluation

Comparison of the learned reliability map against simple baselines: input intensity, reconstruction intensity, edge magnitude, and dropout uncertainty.

### 17.3 Cross-Volume Generalization

Tests whether a reliability model trained on one or more volumes transfers to unseen held-out volumes.

### 17.4 Leave-One-Volume-Out Validation

Final validation training the ReliabilityCNN on four volumes and evaluating it on the remaining held-out volume across five folds.

---

## 18. Methodological Scope

This method estimates **residual-calibrated reliability** using held-out acquired k-space residual energy.

**This method does NOT estimate:**

- Clinical diagnostic uncertainty
- Lesion probability
- Fully sampled image-domain error
- Scanner-independent generalization
- Probabilistic confidence intervals

> The predicted reliability map should be interpreted as a **self-supervised residual-consistency map** derived from acquired k-space evidence.
