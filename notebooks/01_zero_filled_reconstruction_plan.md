# Notebook 01: Zero-Filled Reconstruction

## Table of Contents

- [Objective](#objective)
- [Why This Notebook Matters](#why-this-notebook-matters)
- [Sections](#sections)
  - [1. Import Libraries](#1-import-libraries)
  - [2. Load MRI K-Space Data](#2-load-mri-k-space-data)
  - [3. Visualize Raw K-Space](#3-visualize-raw-k-space)
  - [4. Define Centered FFT and IFFT](#4-define-centered-fft-and-ifft)
  - [5. Generate Undersampling Mask](#5-generate-undersampling-mask)
  - [6. Apply Undersampling](#6-apply-undersampling)
  - [7. Zero-Filled Reconstruction](#7-zero-filled-reconstruction)
  - [8. Visualize Results](#8-visualize-results)
  - [9. Compute Metrics](#9-compute-metrics)
  - [10. Observations](#10-observations)
- [Expected Output](#expected-output)
- [Status](#status)

---

## Objective

Implement the first MRI reconstruction baseline: **zero-filled reconstruction** from undersampled k-space.

---

## Why This Notebook Matters

Before implementing any deep learning reconstruction, the basic MRI reconstruction pipeline must be established:

1. Load k-space data
2. Apply an undersampling mask
3. Perform inverse Fourier transform
4. Visualise aliasing artifacts
5. Compare zero-filled reconstruction with a reference image (if available)

---

## Sections

### 1. Import Libraries

| Library | Purpose |
|---------|---------|
| `numpy` | Array operations |
| `h5py` | Loading MRI k-space files |
| `matplotlib` | Visualisation |
| `torch` | Tensor operations |
| `fastmri` | MRI utilities (if available) |

---

### 2. Load MRI K-Space Data

Load one brain MRI k-space file from the selected dataset and inspect the tensor shape before applying any reconstruction operation.

**Expected data formats:**

| Acquisition Type | Shape |
|-----------------|-------|
| Multicoil | `slices × coils × height × width` |
| Single-coil | `slices × height × width` |

---

### 3. Visualize Raw K-Space

Display the logarithm of k-space magnitude:

$$\log(1 + |k|)$$

where $k$ is the complex-valued k-space array. The logarithm improves visualisation because raw k-space values have a large dynamic range.

---

### 4. Define Centered FFT and IFFT

Implement the centered Fourier transform operations `fft2c` and `ifft2c`.

These are required because MRI k-space is conventionally stored with the **low-frequency region centered**.

The centered inverse Fourier transform maps k-space back to the image domain:

$$x = \mathcal{F}^{-1}(k)$$

| Term | Description |
|------|-------------|
| $k$ | K-space data |
| $x$ | Reconstructed image |
| $\mathcal{F}^{-1}$ | Inverse Fourier transform |

---

### 5. Generate Undersampling Mask

Create a Cartesian undersampling mask with acceleration factor $R = 4$.

The mask must preserve the **low-frequency central k-space region**, which contains most of the image contrast and global structure.

---

### 6. Apply Undersampling

Apply the mask to the fully sampled k-space:

$$k_{\Omega} = M_{\Omega} \odot k$$

| Term | Description |
|------|-------------|
| $k$ | Fully sampled k-space |
| $M_{\Omega}$ | Binary undersampling mask |
| $\odot$ | Element-wise multiplication |
| $k_{\Omega}$ | Undersampled k-space |

---

### 7. Zero-Filled Reconstruction

The zero-filled reconstruction applies the inverse Fourier transform directly to the undersampled k-space:

$$\hat{x}_{ZF} = \mathcal{F}^{-1}(k_{\Omega})$$

| Term | Description |
|------|-------------|
| $\hat{x}_{ZF}$ | Zero-filled reconstructed image |
| $k_{\Omega}$ | Undersampled k-space |
| $\mathcal{F}^{-1}$ | Inverse Fourier transform |

For **multicoil data**, reconstruct each coil image independently, then combine using root-sum-of-squares (RSS):

$$x_{\mathrm{RSS}} = \sqrt{\sum_{c=1}^{C} |x_c|^2}$$

| Term | Description |
|------|-------------|
| $C$ | Number of coils |
| $x_c$ | Reconstructed image from coil $c$ |
| $x_{\mathrm{RSS}}$ | Final coil-combined magnitude image |

---

### 8. Visualize Results

| Panel | Description |
|-------|-------------|
| Reference image | Fully sampled ground truth (if available) |
| Undersampling mask | Binary mask $M_{\Omega}$ |
| Undersampled k-space | $k_{\Omega}$ |
| Zero-filled reconstruction | $\hat{x}_{ZF}$ |
| Error image | $\|\hat{x}_{ZF} - x_{\mathrm{ref}}\|$ (if reference available) |

> **Expected artifact:** Cartesian undersampling produces aliasing in the image domain, typically appearing as structured overlap or ghosting.

---

### 9. Compute Metrics

If a reference image is available, compute the following reconstruction quality metrics:

| Metric | Full Name |
|--------|-----------|
| NMSE | Normalized Mean Squared Error |
| PSNR | Peak Signal-to-Noise Ratio |
| SSIM | Structural Similarity Index Measure |

**Normalized Mean Squared Error:**

$$\mathrm{NMSE} = \frac{\|\hat{x} - x_{\mathrm{ref}}\|_2^2}{\|x_{\mathrm{ref}}\|_2^2}$$

| Term | Description |
|------|-------------|
| $\hat{x}$ | Reconstructed image |
| $x_{\mathrm{ref}}$ | Reference image |

Lower NMSE indicates better reconstruction quality.

---

### 10. Observations

Record the following after running the notebook:

- Type of artifacts observed
- Effect of acceleration factor on image quality
- Difference between fully sampled and zero-filled reconstruction
- Whether the artifact pattern matches the structure of the k-space mask
- Lessons to carry forward into future reconstruction models

---

## Expected Output

By the end of this notebook, a working zero-filled MRI reconstruction baseline should be in place.

| Output | Description |
|--------|-------------|
| K-space sample | Loaded and inspected |
| K-space visualisation | Log-magnitude display |
| Undersampling mask | Cartesian mask at $R = 4$ |
| Zero-filled reconstruction | $\hat{x}_{ZF}$ with visible aliasing |
| Reconstruction metrics | NMSE, PSNR, SSIM (if reference available) |

---

## Status

> **Planned — not yet implemented.**
