# Reliability-Aware Self-Supervised MRI Reconstruction

> Reconstructing accelerated brain MRI while estimating a voxel-wise uncertainty map that indicates where the reconstruction may be unreliable.

---

## Table of Contents

- [Overview](#overview)
- [Research Motivation](#research-motivation)
- [Core Contribution](#core-contribution)
- [What This Project Is Not Claiming](#what-this-project-is-not-claiming)
- [Mathematical Setup](#mathematical-setup)
  - [Self-Supervised Reconstruction Loss](#self-supervised-reconstruction-loss)
  - [Uncertainty Estimation](#uncertainty-estimation)
  - [Held-Out K-Space Reliability Signal](#held-out-k-space-reliability-signal)
  - [Uncertainty Calibration Loss](#uncertainty-calibration-loss)
- [Project Objective](#project-objective)
- [Planned Evaluation](#planned-evaluation)
- [Repository Structure](#repository-structure)
- [Planned Development Stages](#planned-development-stages)
- [Current Status](#current-status)

---

## Overview

This project investigates **reliability-aware self-supervised reconstruction** for accelerated brain MRI.

The goal is to reconstruct an MR image from undersampled k-space while simultaneously estimating a **voxel-wise uncertainty map** that indicates where the reconstruction may be unreliable.

Unlike conventional self-supervised MRI reconstruction methods that produce only a reconstructed image, this project aims to output:

$$\left(\bar{x},\ U\right)$$

| Symbol | Description |
|--------|-------------|
| $\bar{x}$ | Mean reconstructed MR image |
| $U$ | Voxel-wise uncertainty / reliability map |

---

## Research Motivation

Accelerated MRI reduces scan time by acquiring only a **subset of k-space measurements**. However, undersampling creates an ill-posed inverse problem — multiple possible images may be consistent with incomplete measurements.

Deep learning reconstruction methods can produce visually sharp images, but they may also **hallucinate structures** or **hide reconstruction errors**. In clinical imaging, this is risky because a realistic-looking reconstruction is not necessarily reliable.

This project focuses on the question:

> **Can a self-supervised MRI reconstruction model estimate not only the reconstructed image, but also where that reconstruction should not be fully trusted?**

---

## Core Contribution

A **reliability-aware self-supervised k-space reconstruction framework** that uses held-out k-space consistency not only to train the reconstruction model, but also to calibrate voxel-wise uncertainty.

The project builds on three main ideas:

1. **Physics-guided MRI reconstruction**
2. **SSDU-style self-supervised k-space splitting**
3. **Uncertainty calibration using held-out k-space residuals**

---

## What This Project Is Not Claiming

This project does **not** claim to introduce:

- The first physics-informed MRI reconstruction method
- The first self-supervised MRI reconstruction method
- The first uncertainty estimation method for MRI reconstruction
- A clinically validated AI reconstruction system

Instead, the specific research direction is:

> **Using held-out k-space residuals as a self-supervised signal for calibrating spatial uncertainty in accelerated brain MRI reconstruction.**

---

## Mathematical Setup

Let the measured undersampled k-space data be $y_{\Omega}$, where $\Omega$ is the set of acquired k-space locations.

In SSDU-style training, the acquired k-space locations are split into two **disjoint** sets:

$$\Omega = \Theta \cup \Lambda, \qquad \Theta \cap \Lambda = \varnothing$$

| Set | Role |
|-----|------|
| $\Theta$ | Used inside the reconstruction model for data consistency |
| $\Lambda$ | Held out for the self-supervised loss |
| $\Omega$ | Full acquired undersampled k-space |

The reconstruction model receives data from $\Theta$ and produces an image estimate:

$$\hat{x} = f_{\theta}\!\left(y_{\Theta}\right)$$

where $f_{\theta}$ is the reconstruction network with learnable parameters $\theta$.

---

### Self-Supervised Reconstruction Loss

The held-out k-space prediction is obtained by applying the MRI encoding operator to the reconstructed image, evaluated only on $\Lambda$:

$$\mathcal{L}_{\mathrm{SSDU}} = \left\| E_{\Lambda}\hat{x} - y_{\Lambda} \right\|_{2}^{2}$$

| Term | Description |
|------|-------------|
| $E_{\Lambda}$ | MRI encoding operator restricted to held-out k-space locations |
| $\hat{x}$ | Reconstructed image |
| $y_{\Lambda}$ | Measured held-out k-space data |

This loss penalises inconsistency between predicted and measured held-out k-space.

---

### Uncertainty Estimation

The model generates $T$ stochastic reconstructions:

$$\hat{x}_{1},\ \hat{x}_{2},\ \ldots,\ \hat{x}_{T}$$

**Mean reconstruction:**

$$\bar{x} = \frac{1}{T} \sum_{t=1}^{T} \hat{x}_{t}$$

**Voxel-wise uncertainty map (sample variance):**

$$U = \frac{1}{T-1} \sum_{t=1}^{T} \left( \hat{x}_{t} - \bar{x} \right)^{2}$$

High values of $U$ indicate regions where the model is less certain.

---

### Held-Out K-Space Reliability Signal

**K-space residual:**

$$r_{\Lambda} = E_{\Lambda}\bar{x} - y_{\Lambda}$$

**Residual energy:**

$$e_{\Lambda} = \left| r_{\Lambda} \right|^{2} = \left| E_{\Lambda}\bar{x} - y_{\Lambda} \right|^{2}$$

Large values of $e_{\Lambda}$ indicate poor consistency with measured held-out k-space.

Because $U$ is an image-domain map while $e_{\Lambda}$ is a k-space-domain residual, the held-out residual is **backprojected into the image domain** for a meaningful calibration signal:

$$e_{\mathrm{img}} = \left| E_{\Lambda}^{H}\!\left( E_{\Lambda}\bar{x} - y_{\Lambda} \right) \right|^{2}$$

where $E_{\Lambda}^{H}$ is the adjoint MRI encoding operator restricted to $\Lambda$.

---

### Uncertainty Calibration Loss

$$\mathcal{L}_{\mathrm{cal}} = \left\| \mathcal{N}(U) - \mathcal{N}(e_{\mathrm{img}}) \right\|_{1}$$

| Term | Description |
|------|-------------|
| $\mathcal{N}(\cdot)$ | Normalisation operation |
| $U$ | Predicted voxel-wise uncertainty map |
| $e_{\mathrm{img}}$ | Image-domain residual from held-out k-space |

This encourages uncertainty to increase where held-out k-space inconsistency suggests unreliability.

**Total training objective:**

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{SSDU}} + \lambda_{\mathrm{cal}}\,\mathcal{L}_{\mathrm{cal}}$$

where $\lambda_{\mathrm{cal}}$ controls the strength of uncertainty calibration.

---

## Project Objective

Develop and evaluate a reconstruction framework that outputs $(\bar{x},\ U)$:

| Output | Description |
|--------|-------------|
| $\bar{x}$ | Reconstructed brain MR image |
| $U$ | Calibrated uncertainty map showing where the reconstruction may be unreliable |

**Key research question:**

> **Can held-out k-space consistency be used not only for self-supervised reconstruction, but also for uncertainty calibration and reliability failure detection?**

---

## Planned Evaluation

### Reconstruction Quality

| Metric | Description |
|--------|-------------|
| **NMSE** | Normalized Mean Squared Error |
| **PSNR** | Peak Signal-to-Noise Ratio |
| **SSIM** | Structural Similarity Index Measure |

### Reliability and Uncertainty

- Correlation between uncertainty and reconstruction error
- Error detection performance
- Calibration analysis
- Reliability map visualisation
- Comparison between high-uncertainty regions and actual reconstruction error

When fully sampled reference data are available, reconstruction error is:

$$\mathrm{Error}(r) = \left| \bar{x}(r) - x_{\mathrm{ref}}(r) \right|$$

**Reliability hypothesis:**

$$U(r) \uparrow \quad \Longrightarrow \quad \mathrm{Error}(r) \uparrow$$

Regions with higher uncertainty should generally correspond to regions with higher reconstruction error.

---

## Repository Structure

```
.
├── data/           # Dataset instructions and download notes (no raw data committed)
├── notebooks/      # Google Colab notebooks for exploration and prototyping
├── src/            # Source code: models, masking, losses, training, evaluation
├── configs/        # Experiment configs (acceleration factor, mask type, model settings)
├── experiments/    # Experiment logs, run descriptions, reproducibility notes
├── results/        # Saved reconstructions, uncertainty maps, figures, evaluation summaries
├── docs/           # Research notes, derivations, literature summaries, paper planning
└── tests/          # Unit tests for code correctness
```

---

## Planned Development Stages

| Stage | Title | Key Tasks |
|-------|-------|-----------|
| 1 | **Project Setup** | Repository structure, research README, problem formulation, mathematical assumptions |
| 2 | **Data Preparation** | Select brain MRI dataset, implement k-space loading, implement undersampling masks, simulate accelerated acquisition |
| 3 | **Baseline Reconstruction** | Zero-filled reconstruction, supervised baseline (if available), SSDU-style self-supervised baseline |
| 4 | **Physics-Guided Reconstruction** | Implement reconstruction network, add data consistency, train with held-out k-space loss |
| 5 | **Uncertainty Estimation** | Stochastic forward passes, compute mean reconstruction, compute voxel-wise variance map |
| 6 | **Uncertainty Calibration** | Compute held-out k-space residual, add calibration loss, evaluate uncertainty-error correspondence |
| 7 | **Evaluation & Paper Prep** | Compare reconstruction quality, analyse reliability maps, prepare figures, draft paper |

