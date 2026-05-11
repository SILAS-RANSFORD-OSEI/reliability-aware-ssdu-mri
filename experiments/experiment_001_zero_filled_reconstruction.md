# Experiment 001: Zero-Filled Reconstruction

## Table of Contents

- [Objective](#objective)
- [Purpose](#purpose)
- [Research Role](#research-role)
- [Input](#input)
- [Method](#method)
- [Planned Steps](#planned-steps)
- [Expected Output](#expected-output)
- [Metrics](#metrics)
- [Notes](#notes)

---

## Objective

Implement the first MRI reconstruction baseline using **zero-filled reconstruction** from undersampled k-space.

---

## Purpose

This experiment establishes the simplest possible baseline for accelerated MRI reconstruction.

Before training any deep learning model, it is necessary to understand how undersampling affects reconstruction quality and what aliasing artifacts are introduced.

---

## Research Role

Zero-filled reconstruction is **not** the proposed method. It serves as the baseline against which all future methods will be compared.

The proposed reliability-aware model must eventually outperform this baseline on both fronts:

| Criterion | Description |
|-----------|-------------|
| Reconstruction quality | Quantitatively better NMSE, PSNR, and SSIM |
| Reliability estimation | Produces a calibrated uncertainty map — absent here |

---

## Input

The input is undersampled k-space data $y_{\Omega}$, where $\Omega$ is the set of acquired k-space locations.

Data will be sourced from fully sampled or **retrospectively undersampled** brain MRI k-space.

---

## Method

The zero-filled reconstruction inserts zeros into missing k-space locations and applies the inverse Fourier transform:

$$\hat{x}_{ZF} = E_{\Omega}^{H}\,y_{\Omega}$$

| Term | Description |
|------|-------------|
| $\hat{x}_{ZF}$ | Zero-filled reconstructed image |
| $E_{\Omega}^{H}$ | Adjoint undersampled MRI encoding operator |
| $y_{\Omega}$ | Undersampled k-space data |

For **single-coil MRI**, this simplifies to:

$$\hat{x}_{ZF} = \mathcal{F}^{-1}\!\left( M_{\Omega} \odot y \right)$$

| Term | Description |
|------|-------------|
| $\mathcal{F}^{-1}$ | Inverse Fourier transform |
| $M_{\Omega}$ | Undersampling mask |
| $\odot$ | Element-wise multiplication |
| $y$ | Fully sampled k-space data before retrospective undersampling |

---

## Planned Steps

1. Load one brain MRI k-space sample
2. Inspect the k-space dimensions
3. Apply a Cartesian undersampling mask
4. Perform inverse FFT reconstruction
5. Display the zero-filled image
6. Save the reconstruction result
7. Record observations about aliasing artifacts

---

## Expected Output

| Output | Description |
|--------|-------------|
| Reference image | Fully sampled ground truth (if available) |
| Undersampling mask | Binary mask $M_{\Omega}$ applied to k-space |
| Undersampled k-space | $M_{\Omega} \odot y$ |
| Zero-filled reconstruction | $\hat{x}_{ZF}$ |
| Visual comparison | Side-by-side display of the above |

---

## Metrics

If fully sampled reference data are available, the following reconstruction quality metrics will be computed:

| Metric | Full Name |
|--------|-----------|
| NMSE | Normalized Mean Squared Error |
| PSNR | Peak Signal-to-Noise Ratio |
| SSIM | Structural Similarity Index Measure |

---

## Notes

- This experiment is the **first engineering checkpoint** in the project.
- No uncertainty estimation is performed at this stage.
- Results from this experiment will be used as the lower-bound baseline in all future comparisons.
