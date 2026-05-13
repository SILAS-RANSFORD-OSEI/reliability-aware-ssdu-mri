# Notebook 02: SSDU Reconstruction Baseline

## Table of Contents

- [Objective](#objective)
- [Purpose](#purpose)
- [Core Idea](#core-idea)
- [Planned Model](#planned-model)
- [Planned Sections](#planned-sections)
- [Expected Output](#expected-output)
- [Status](#status)

---

## Objective

Implement the first **learning-based self-supervised MRI reconstruction baseline** using SSDU-style k-space splitting.

---

## Purpose

[Notebook 01](NOTEBOOK_01_ZERO_FILLED_RECONSTRUCTION.md) verified the full MRI physics pipeline:

| Component | Description |
|-----------|-------------|
| K-space loading | fastMRI HDF5 data |
| Reconstruction | Inverse FFT + RSS coil combination |
| Mask splitting | SSDU $\Theta$ / $\Lambda$ partition |
| Residual | Held-out k-space residual computation |
| Backprojection | Image-domain residual energy $E_{\mathrm{img}}$ |
| Uncertainty | Voxel-wise variance utility testing |

Notebook 02 moves from **physics-only reconstruction** to a **learning-based SSDU reconstruction baseline**.

---

## Core Idea

The acquired k-space mask is split into two disjoint subsets:

$$\Omega = \Theta \cup \Lambda, \qquad \Theta \cap \Lambda = \varnothing$$

The model receives data from $\Theta$ and is trained to match held-out measurements on $\Lambda$ via the self-supervised loss:

$$\mathcal{L}_{\mathrm{SSDU}} = \left\| E_{\Lambda}\hat{x} - y_{\Lambda} \right\|_2^2$$

| Term | Description |
|------|-------------|
| $E_{\Lambda}$ | MRI encoding operator restricted to $\Lambda$ |
| $\hat{x}$ | Model reconstruction |
| $y_{\Lambda}$ | Measured held-out k-space data |

---

## Planned Model

The first baseline model will be deliberately simple.

| Property | Choice |
|----------|--------|
| Architecture | Image-domain U-Net refinement |
| Input | Zero-filled reconstruction from $\Theta$ |
| Output | Refined reconstructed image |
| Loss | Held-out k-space consistency on $\Lambda$ |

---

## Planned Sections

### 1. Environment Setup

- Mount Google Drive
- Clone GitHub repository
- Import project modules
- Select fastMRI brain file

### 2. Load fastMRI Data

- Load one multicoil fastMRI brain file
- Extract central k-space slice
- Inspect acquisition type and acceleration factor

### 3. SSDU Mask Split

- Split acquired mask into $\Theta$ and $\Lambda$
- Visualise original mask, $\Theta$ mask, and $\Lambda$ mask

### 4. Create Theta-Only Input

- Apply $\Theta$ mask to measured k-space
- Reconstruct zero-filled image from $\Theta$
- Use as model input

### 5. Define Simple Reconstruction Network

- Implement small U-Net or CNN baseline
- Input: zero-filled image from $\Theta$
- Output: refined reconstruction $\hat{x}$

### 6. Define SSDU Loss

- Transform model output $\hat{x}$ to k-space
- Compare predicted k-space with measured data on $\Lambda$ only
- Compute held-out k-space consistency loss

### 7. Train on a Small Number of Slices

- Start with one file
- Expand to multiple slices
- Monitor SSDU loss curve

### 8. Visualise Results

| Panel | Description |
|-------|-------------|
| $\Theta$-only zero-filled reconstruction | Model input |
| Model reconstruction | $\hat{x}$ after training |
| Held-out residual energy | $\|r_{\Lambda}\|^2$ |
| Backprojected residual energy | $E_{\mathrm{img}}$ |

### 9. Save Observations

- Does the SSDU loss decrease during training?
- Does the reconstruction visually improve over the zero-filled baseline?
- What limitations appear at this stage?

---

## Expected Output

| Output | Description |
|--------|-------------|
| SSDU learning baseline | Model trained without fully sampled reference images |
| Loss curves | Held-out k-space loss over training |
| Visual comparison | Zero-filled vs. model reconstruction |
| Residual maps | Held-out residual and backprojected energy |

---

## Status

> **Planned — not yet implemented.**
