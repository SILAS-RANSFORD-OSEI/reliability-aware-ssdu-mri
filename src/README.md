# Source Code Structure

This folder will contain the implementation code for the reliability-aware self-supervised MRI reconstruction project.

The code will be organized into modular components so that each part of the reconstruction pipeline can be tested independently.

---

## Planned Modules

### 1. `transforms.py`

MRI Fourier transform utilities.

Planned functions:

- `fft2c`
- `ifft2c`
- `complex_abs`
- `rss_combine`

---

### 2. `masks.py`

Undersampling mask generation.

Planned functions:

- `cartesian_mask`
- `variable_density_mask`
- `apply_mask`

---

### 3. `data.py`

Dataset loading and preprocessing.

Planned functions:

- Load HDF5 k-space files
- Select slices
- Normalize k-space or image data
- Prepare training samples

---

### 4. `metrics.py`

Reconstruction quality and reliability metrics.

Planned functions:

- `nmse`
- `psnr`
- `ssim`
- uncertainty-error correlation
- error detection AUC

---

### 5. `models/`

Neural network reconstruction models.

Planned models:

- U-Net baseline
- Unrolled reconstruction network
- SSDU reconstruction model
- Dropout-enabled uncertainty model

---

### 6. `losses.py`

Training losses.

Planned losses:

- SSDU held-out k-space loss
- uncertainty calibration loss
- total reconstruction-calibration loss

---

### 7. `train.py`

Training loop.

Planned responsibilities:

- Load configuration
- Load dataset
- Initialize model
- Train model
- Save checkpoints
- Log losses

---

### 8. `evaluate.py`

Evaluation pipeline.

Planned responsibilities:

- Load trained model
- Run reconstruction
- Compute metrics
- Generate uncertainty maps
- Compare uncertainty with reconstruction error

---

## Immediate Coding Priority

The first implementation target is:

1. Centered FFT and inverse FFT
2. Cartesian undersampling mask
3. Zero-filled reconstruction
4. Basic visualization in Colab

---

## Status

Planned, not implemented yet.
