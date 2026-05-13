# Method Development Status

## Table of Contents

- [Current Position](#current-position)
- [Completed Method Components](#completed-method-components)
  - [1. MRI Forward and Inverse Operators](#1-mri-forward-and-inverse-operators)
  - [2. fastMRI Data Loading](#2-fastmri-data-loading)
  - [3. Zero-Filled Reconstruction Baseline](#3-zero-filled-reconstruction-baseline)
  - [4. SSDU K-Space Splitting](#4-ssdu-k-space-splitting)
  - [5. Held-Out K-Space Residual](#5-held-out-k-space-residual)
  - [6. Backprojected Residual Energy](#6-backprojected-residual-energy)
  - [7. Basic Uncertainty Utilities](#7-basic-uncertainty-utilities)
- [Current Scientific Status](#current-scientific-status)
- [Next Method Step](#next-method-step)
- [Method Direction](#method-direction)

---

## Current Position

The project has completed the **first foundation stage** for reliability-aware self-supervised MRI reconstruction.

| Component | Status |
|-----------|--------|
| fastMRI brain k-space loading | ✅ Complete |
| Multicoil zero-filled reconstruction | ✅ Complete |
| SSDU-style k-space mask splitting | ✅ Complete |
| Held-out k-space residual computation | ✅ Complete |
| Backprojected residual energy mapping | ✅ Complete |
| Basic uncertainty utility testing | ✅ Complete |
| Learning-based reconstruction model | 🔲 Not yet started |

---

## Completed Method Components

### 1. MRI Forward and Inverse Operators

| Operator | Description |
|----------|-------------|
| `fft2c` | Centered 2D FFT |
| `ifft2c` | Centered 2D inverse FFT |
| Complex magnitude | $\|\cdot\|$ |
| RSS coil combination | $x_{\mathrm{RSS}} = \sqrt{\sum_c \|x_c\|^2}$ |

These support the basic MRI reconstruction pathway:

$$y \rightarrow \mathcal{F}^{-1}(y) \rightarrow x$$

---

### 2. fastMRI Data Loading

Reusable loading utilities for fastMRI HDF5 files. The pipeline currently supports:

| Data | Description |
|------|-------------|
| `kspace` | Complex-valued multicoil k-space |
| `mask` | Sampling mask |
| `ismrmrd_header` | Acquisition metadata |
| Central slice | Single-slice extraction for prototyping |

---

### 3. Zero-Filled Reconstruction Baseline

Zero-filled reconstruction from real accelerated multicoil brain MRI k-space. This is the simplest reconstruction method and establishes the lower-bound baseline before deep learning is introduced.

---

### 4. SSDU K-Space Splitting

The acquired mask $\Omega$ is split into two disjoint subsets:

$$\Omega = \Theta \cup \Lambda, \qquad \Theta \cap \Lambda = \varnothing$$

| Subset | Role |
|--------|------|
| $\Theta$ | Reconstruction input / data consistency |
| $\Lambda$ | Held out for self-supervised loss |

---

### 5. Held-Out K-Space Residual

$$r_{\Lambda} = M_{\Lambda} \odot (\hat{y} - y)$$

| Term | Description |
|------|-------------|
| $M_{\Lambda}$ | Binary held-out $\Lambda$ mask |
| $\hat{y}$ | Predicted k-space |
| $y$ | Measured k-space |

This is the core SSDU residual used to evaluate consistency on measured k-space hidden from the reconstruction input.

---

### 6. Backprojected Residual Energy

$$E_{\mathrm{img}} = \sum_{c=1}^{C} \left| \mathcal{F}^{-1}(r_{\Lambda,c}) \right|^2$$

| Term | Description |
|------|-------------|
| $C$ | Number of receiver coils |
| $r_{\Lambda,c}$ | Held-out residual for coil $c$ |
| $E_{\mathrm{img}}$ | Image-domain residual energy map |

$E_{\mathrm{img}}$ is the **bridge between SSDU and reliability-aware uncertainty calibration** — a self-supervised reliability signal requiring no ground-truth reference.

---

### 7. Basic Uncertainty Utilities

| Utility | Description |
|---------|-------------|
| Mean reconstruction | $\bar{x} = \frac{1}{T}\sum_{t=1}^{T} \hat{x}_t$ |
| Voxel-wise variance | $U = \frac{1}{T-1}\sum_{t=1}^{T}(\hat{x}_t - \bar{x})^2$ |
| Uncertainty normalisation | $\mathcal{N}(U)$ for downstream comparison |
| Uncertainty–residual alignment | Pearson correlation between $U$ and $E_{\mathrm{img}}$ |

> **Note:** The current uncertainty test used artificial Gaussian noise only. This serves as a **negative control** establishing a random baseline (Pearson $r \approx 0$), not a scientific result. Model-derived uncertainty is required for meaningful alignment.

---

## Current Scientific Status

No learned reconstruction model has been implemented yet. The work completed so far validates:

| Validated Component | Purpose |
|--------------------|---------|
| Reconstruction physics | Correct forward and inverse operators |
| SSDU residual logic | $\Theta \to \Lambda$ residual pipeline |
| Reliability-signal pathway | $r_{\Lambda} \to E_{\mathrm{img}}$ backprojection |

**The next scientific step** is to implement a learning-based SSDU reconstruction baseline.

---

## Next Method Step

> **Implement an SSDU reconstruction baseline using a simple neural network trained with held-out k-space consistency.**

This requires:

| Task | Description |
|------|-------------|
| PyTorch model | Small U-Net or CNN baseline |
| Input preparation | Zero-filled image from $\Theta$ |
| K-space conversion | Transform model output $\hat{x}$ back to k-space |
| SSDU loss | Held-out consistency loss on $\Lambda$ |
| Initial training | Single file, small number of slices |

---

## Method Direction

The final method will extend SSDU to produce:

$$(\bar{x},\ U)$$

| Output | Description |
|--------|-------------|
| $\bar{x}$ | Reconstructed brain MR image |
| $U$ | Voxel-wise uncertainty map calibrated against $E_{\mathrm{img}}$ |

The uncertainty map will be calibrated using the backprojected held-out residual energy via:

$$\mathcal{L}_{\mathrm{cal}} = \left\| \mathcal{N}(U) - \mathcal{N}(E_{\mathrm{img}}) \right\|_1$$
