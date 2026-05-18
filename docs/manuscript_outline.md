# Four-Way Self-Supervised K-Space Partitioning for Residual-Calibrated Reliability Learning in Accelerated Brain MRI

> **Paper Type:** Methods / Feasibility Study

---

## Overview

This paper proposes a **four-way self-supervised k-space partitioning framework** for residual-calibrated reliability learning in accelerated brain MRI.

The method separates acquired k-space into four disjoint subsets — reconstruction input, reconstruction training loss, reliability calibration, and independent reliability evaluation:

$$
\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}
$$

A `ReliabilityCNN` trained on calibration residual energy modestly improves held-out residual-energy prediction over input intensity in leave-one-volume-out validation, and clearly outperforms dropout uncertainty, edge maps, and reconstruction-intensity baselines.

---

## Table of Contents

- [Abstract](#abstract)
- [Introduction](#introduction)
- [Related Work](#related-work)
- [Methods](#methods)
- [Experiments](#experiments)
- [Results](#results)
- [Discussion](#discussion)
- [Limitations](#limitations)
- [Conclusion](#conclusion)
- [Target Journal Positioning](#target-journal-positioning)

---

## Abstract

1. **Background:** Accelerated MRI reconstruction can produce spatially unreliable outputs.
2. **Gap:** Self-supervised reconstruction methods such as SSDU do not directly provide independently calibrated reliability maps.
3. **Method:** We propose four-way k-space partitioning and a residual-calibrated `ReliabilityCNN`.
4. **Experiments:** fastMRI brain AXT2 / R=4, five-volume leave-one-volume-out validation.
5. **Results:** `ReliabilityCNN` outperformed input intensity in 4/5 held-out volumes.
6. **Conclusion:** Four-way SSDU partitioning enables feasible self-supervised residual reliability learning without fully sampled ground truth.

---

## Introduction

### Clinical and Engineering Motivation

Accelerated MRI reduces scan time but increases reconstruction difficulty because images are recovered from undersampled k-space. Deep learning reconstruction can suppress aliasing artifacts, but reconstructed images may contain spatially varying errors.

In clinical settings, a visually plausible reconstruction is not sufficient — a reconstruction method should also indicate **where the output may be unreliable**.

### Problem With Fully Supervised Reliability Estimation

Fully sampled reference images are often unavailable in realistic accelerated MRI settings. This limits the ability to train or validate reliability maps using image-domain ground-truth errors.

### Existing Self-Supervised Reconstruction Methods

Self-supervised methods such as **SSDU** split acquired k-space into an input subset and a loss subset, allowing reconstruction training without fully sampled targets. However, standard SSDU-style partitioning is primarily designed for reconstruction learning — not for separately training and independently evaluating reliability maps.

### Gap

Existing self-supervised MRI reconstruction pipelines do not clearly separate:

- Reconstruction input
- Reconstruction training loss
- Reliability calibration
- Final reliability evaluation

This creates a risk of **circularity** when the same hidden k-space evidence is used for multiple roles.

### Proposed Solution

We propose a four-way k-space partitioning framework:

$$
\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}
$$

This enables residual-calibrated reliability learning using **acquired k-space only**.

### Contributions

1. A four-way self-supervised k-space partitioning framework for reliability learning.
2. A residual-energy calibration target derived from held-out acquired k-space.
3. A structural `ReliabilityCNN` defined as:

$$
R_{\phi} = h_{\phi}(x_{\Theta},\ \hat{x},\ |\nabla \hat{x}|)
$$

4. Leave-one-volume-out validation across five matched AXT2 / R=4 fastMRI brain volumes.
5. Empirical comparison against input intensity, dropout uncertainty, reconstruction intensity, and edge-map baselines.

---

## Related Work

### Accelerated MRI Reconstruction

The MRI acquisition problem is:

$$
y_{\Omega} = M_{\Omega} F x + \varepsilon
$$

| Symbol | Description |
|--------|-------------|
| $x \in \mathbb{C}^{N}$ | Unknown MR image |
| $F$ | Fourier transform |
| $M_{\Omega}$ | Undersampling mask |
| $y_{\Omega}$ | Acquired k-space |
| $\varepsilon$ | Measurement noise |

Classical reconstruction methods include compressed sensing and parallel imaging. More recent methods use deep learning, including CNN-based, unrolled, and physics-guided reconstruction networks.

### Self-Supervised MRI Reconstruction

SSDU and related strategies train reconstruction networks using only acquired undersampled k-space by splitting it into an **input subset** and a **loss subset**, enabling learning without fully sampled reference images.

### Uncertainty and Reliability in MRI Reconstruction

Uncertainty and reliability estimation are important because deep reconstruction models may produce visually plausible but spatially unreliable images. Existing strategies include:

- MC dropout
- Bayesian approximations
- Ensemble methods
- Residual consistency checks
- Calibration-based approaches

> This paper focuses on **residual-calibrated reliability**, not full clinical uncertainty calibration.

### Gap in Current Literature

Existing approaches often evaluate reconstruction quality, but fewer methods independently calibrate and evaluate spatial reliability using held-out acquired k-space residuals. This motivates a partitioning framework that **separates** reconstruction training, reliability calibration, and reliability evaluation.

---

## Methods

### Forward Model

$$
y_{\Omega} = M_{\Omega} F x + \varepsilon
$$

where $x \in \mathbb{C}^{H \times W}$ is the unknown complex-valued MR image. For the current feasibility study, one selected coil is used, producing a **single-coil-equivalent** reconstruction setting.

---

### Four-Way K-Space Partitioning

$$
\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}
$$

All subsets are **pairwise disjoint**.

| Subset | Role |
|--------|------|
| $\Theta$ | Reconstruction input and data-consistency subset |
| $\Lambda_{\mathrm{train}}$ | SSDU reconstruction training-loss subset |
| $\Lambda_{\mathrm{cal}}$ | Reliability calibration subset |
| $\Lambda_{\mathrm{eval}}$ | Independent reliability evaluation subset |

This design prevents the same acquired k-space samples from being reused for reconstruction training, reliability calibration, and final reliability evaluation.

> See **Figure 1**.

---

### SSDU Reconstruction Training

The reconstruction network receives $y_{\Theta}$ and estimates:

$$
\hat{x}_{\theta} = f_{\theta}(y_{\Theta})
$$

The predicted k-space is:

$$
\hat{y} = F \hat{x}_{\theta}
$$

The SSDU reconstruction loss is:

$$
\mathcal{L}_{\mathrm{SSDU}} = \left\| M_{\Lambda_{\mathrm{train}}} (\hat{y} - y) \right\|_2^2
$$

---

### Calibration Residual Energy

The calibration residual:

$$
r_{\Lambda_{\mathrm{cal}}} = M_{\Lambda_{\mathrm{cal}}} (\hat{y} - y)
$$

The backprojected calibration residual energy (reliability learning target):

$$
E_{\Lambda_{\mathrm{cal}}} = \left| F^{-1} r_{\Lambda_{\mathrm{cal}}} \right|^2
$$

---

### Evaluation Residual Energy

The held-out evaluation residual:

$$
r_{\Lambda_{\mathrm{eval}}} = M_{\Lambda_{\mathrm{eval}}} (\hat{y} - y)
$$

The evaluation residual energy:

$$
E_{\Lambda_{\mathrm{eval}}} = \left| F^{-1} r_{\Lambda_{\mathrm{eval}}} \right|^2
$$

> $E_{\Lambda_{\mathrm{eval}}}$ is **never used** during reconstruction training or reliability calibration — it is reserved only for final reliability evaluation.

---

### ReliabilityCNN

**Input:**

$$
z = \left[ x_{\Theta},\ \hat{x},\ |\nabla \hat{x}| \right]
$$

| Component | Description |
|-----------|-------------|
| $x_{\Theta}$ | Input image reconstructed from $\Theta$ |
| $\hat{x}$ | SSDU reconstruction |
| $\|\nabla \hat{x}\|$ | Reconstruction gradient magnitude |

**Tensor shape:**

$$
z \in \mathbb{R}^{1 \times 3 \times 768 \times 396}
$$

*(batch=1, channels=3, height=768, width=396)*

**Output:**

$$
R_{\phi} = h_{\phi}(z) \in \mathbb{R}^{1 \times 1 \times 768 \times 396}
$$

**Training loss:**

$$
\mathcal{L}_{\mathrm{rel}} = \left\| \mathrm{norm}(R_{\phi}) - \mathrm{norm}(E_{\Lambda_{\mathrm{cal}}}) \right\|_2^2
$$

where $\mathrm{norm}(\cdot)$ denotes min-max normalization.

> See **Figure 2**.

---

### Alignment Metric

Reliability quality is measured by alignment between a candidate map and the held-out residual energy:

$$
\rho(R,\ E_{\Lambda_{\mathrm{eval}}})
$$

**Evaluated maps:**

- `ReliabilityCNN` prediction
- Input intensity
- Mean reconstruction intensity
- Edge map
- Dropout uncertainty

---

## Experiments

### Dataset

| Property | Value |
|----------|-------|
| Source | fastMRI brain multicoil test data |
| Acquisition | AXT2 |
| Acceleration | R = 4 |
| K-space shape | $16 \times 16 \times 768 \times 396$ |
| Mask shape | $396$ |
| Volumes | 5 matched |
| Coils | 1 selected |

### Experiment Progression

| Experiment | Purpose | Main Finding |
|------------|---------|--------------|
| 017 | Four-way split verification | Confirmed disjoint partitioning |
| 018 | Four-way reliability evaluation | Independent reliability signal survived |
| 024 | Per-slice ReliabilityCNN | Beat dropout and edge, not input intensity |
| 025 | Cross-slice ReliabilityCNN | Beat input intensity within one volume |
| 026 | Dropout channel test | Dropout channel degraded performance |
| 027 | One-volume cross-volume test | Partial transfer only |
| 028 | Multi-volume training | Reached input-intensity parity |
| 029 | Leave-one-volume-out validation | Beat input intensity in 4/5 held-out volumes |

### Leave-One-Volume-Out Validation (Experiment 029)

$$
4\ \text{volumes train} \rightarrow 1\ \text{volume test}
$$

| Split | Slices |
|-------|--------|
| Training per fold | 64 slices |
| Held-out test per fold | 16 slices |

---

## Results

### Experiment 029 — Main Result

| Method | Mean Alignment |
|--------|---------------|
| **ReliabilityCNN** | **0.5713** |
| Input intensity | 0.5580 |
| Mean reconstruction intensity | 0.4980 |
| Dropout uncertainty | 0.4900 |
| Edge map | 0.4005 |

**Margins over baselines:**

$$
R_{\mathrm{net}} - I_{\mathrm{input}} = +0.0132
$$

$$
R_{\mathrm{net}} - U_{\mathrm{dropout}} = +0.0813
$$

$$
R_{\mathrm{net}} - E_{\mathrm{edge}} = +0.1708
$$

> See **Figures 3 and 4**.

### Volume-Level Results

`ReliabilityCNN` beat input intensity in **4 out of 5** held-out volumes.

> See **Figure 4**.

### Representative Visual Example

**Fold 4, Volume V4, Slice 15:**

| Map | Alignment |
|-----|----------:|
| **ReliabilityCNN** | **0.5749** |
| Input intensity | 0.4595 |
| Mean reconstruction | 0.4553 |
| Dropout uncertainty | 0.3617 |
| Edge map | 0.2614 |

> See **Figure 5**.

---

## Discussion

### Main Finding

The four-way SSDU framework enables residual-calibrated reliability learning **without fully sampled ground truth**.

### Why Four-Way Partitioning Matters

The four-way split prevents the same acquired k-space subset from being reused for reconstruction training, reliability calibration, and final reliability evaluation. This makes the reliability evaluation more independent than standard two-way reconstruction-oriented SSDU partitioning.

### Interpretation of ReliabilityCNN Behavior

The model learns a structural reliability map from input intensity, reconstruction intensity, and edge information. Its improvement over input intensity is modest — raw anatomical and intensity structure remains a strong baseline — but `ReliabilityCNN` **consistently outperforms** dropout uncertainty and edge maps.

### Clinical Interpretation Caution

> ⚠️ The predicted reliability maps should be interpreted as **residual-energy reliability maps**, not lesion probability maps or fully calibrated diagnostic uncertainty maps. The held-out residual energy is a physics-derived consistency signal, not a direct clinical ground-truth error map.

---

## Limitations

- Five volumes only
- One selected coil (single-coil-equivalent setup)
- One acquisition type (AXT2)
- One acceleration factor (R = 4)
- No fully sampled image-domain reference
- No multicoil sensitivity encoding (SENSE/ESPIRiT)
- No radiologist reader study
- No external scanner or protocol validation

---

## Conclusion

This work proposes a **four-way self-supervised k-space partitioning framework** for residual-calibrated reliability learning in accelerated brain MRI.

Leave-one-volume-out validation shows that multi-volume `ReliabilityCNN` training modestly improves held-out residual-energy prediction over input intensity and **clearly outperforms** dropout uncertainty and edge-based baselines.

The method is best interpreted as a **self-supervised feasibility framework** for reliability learning without fully sampled reference images.

---

## Target Journal Positioning

**Suitable as:**
- A Scopus-indexed methods paper
- A biomedical signal or image processing paper
- A medical imaging engineering feasibility paper

**Not yet suitable as:**
- A full clinical validation paper
- An IEEE TMI-level benchmark paper
- A clinically calibrated uncertainty paper
