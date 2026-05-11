# Implementation Roadmap

## Purpose

This document defines the engineering roadmap for implementing the reliability-aware self-supervised MRI reconstruction project.

The project will be developed in stages, moving from simple reconstruction baselines toward uncertainty-calibrated self-supervised reconstruction.

---

## Stage 1: Repository and Documentation Setup

### Goal

Create a clean research repository that clearly defines the problem, contribution, mathematical formulation, and planned implementation.

### Tasks

- Create GitHub repository
- Add folder structure
- Write README
- Add problem formulation document
- Add implementation roadmap

### Expected Output

A well-organized repository ready for coding and experimentation.

---

## Stage 2: Dataset Selection and Preparation

### Goal

Select a suitable MRI dataset and prepare k-space data for reconstruction experiments.

### Candidate Dataset

Preferred dataset:

- fastMRI Brain MRI dataset

### Why fastMRI Brain?

- It contains raw k-space MRI data.
- It is widely used in MRI reconstruction research.
- It supports accelerated MRI experiments.
- It allows comparison with existing reconstruction literature.

### Tasks

- Read fastMRI dataset documentation.
- Understand the HDF5 file structure.
- Load k-space data from HDF5 files.
- Inspect k-space tensor dimensions.
- Convert k-space to zero-filled image reconstruction.
- Save sample visualizations.

### Expected Output

A notebook that loads one brain MRI k-space file and displays:

- Fully sampled reference reconstruction, if available
- Undersampled k-space
- Zero-filled reconstruction

---

## Stage 3: MRI Forward Model Implementation

### Goal

Implement the basic MRI encoding and reconstruction operators.

### Core Operators

For single-coil MRI:

- Image to Fourier transform to k-space
- K-space to inverse Fourier transform to image

For multicoil MRI:

- Image to coil sensitivity multiplication
- Coil images to Fourier transform
- Fourier data to undersampled k-space

### Tasks

- Implement centered 2D FFT.
- Implement centered 2D inverse FFT.
- Implement undersampling mask.
- Implement k-space masking.
- Implement zero-filled reconstruction.
- Check tensor shapes carefully.

### Expected Output

Python functions for:

- `fft2c`
- `ifft2c`
- `apply_mask`
- `zero_filled_reconstruction`

---

## Stage 4: Undersampling Mask Design

### Goal

Simulate accelerated MRI acquisition by undersampling k-space.

### Mask Types

Initial mask types:

- Cartesian random mask
- Variable-density Cartesian mask
- Equally spaced acceleration mask

### Acceleration Factors

Initial acceleration factors:

- `R = 4`
- `R = 6`
- `R = 8`

### Tasks

- Implement mask generation.
- Preserve low-frequency central k-space.
- Apply mask to fully sampled k-space.
- Compare reconstruction degradation at different acceleration factors.

### Expected Output

Visual comparison of zero-filled reconstructions at different acceleration rates.

---

## Stage 5: Baseline Reconstruction

### Goal

Build baseline reconstruction methods before introducing the proposed reliability-aware model.

### Baselines

Start with:

1. Zero-filled reconstruction
2. U-Net image-domain reconstruction
3. SSDU-style self-supervised reconstruction

### Tasks

- Implement a simple U-Net.
- Train U-Net with available reference data only as a sanity check.
- Implement SSDU k-space splitting.
- Train using held-out k-space loss.

### Expected Output

Baseline reconstruction results with:

- NMSE
- PSNR
- SSIM

---

## Stage 6: Physics-Guided Reconstruction Model

### Goal

Move from image-only reconstruction to physics-guided reconstruction.

### Candidate Architecture

Initial architecture:

- Unrolled reconstruction network

Each unrolled block should contain:

1. Data consistency step
2. Learned denoising or regularization block
3. Updated image estimate

### Tasks

- Implement simple unrolled reconstruction.
- Add data consistency using acquired k-space.
- Use SSDU-style held-out loss.
- Compare against U-Net baseline.

### Expected Output

Physics-guided self-supervised reconstruction baseline.

---

## Stage 7: Stochastic Reconstruction for Uncertainty Estimation

### Goal

Generate multiple reconstructions from the same undersampled input.

### Initial Method

Start with:

- Monte Carlo dropout

Alternative methods for later:

- Deep ensemble
- Test-time augmentation
- Probabilistic latent variable reconstruction

### Tasks

- Add dropout layers to the reconstruction model.
- Keep dropout active during inference.
- Generate multiple stochastic reconstructions.
- Compute mean reconstruction.
- Compute voxel-wise variance map.

### Expected Output

For each input case, produce:

- Mean reconstruction
- Uncertainty map

---

## Stage 8: Held-Out K-Space Reliability Calibration

### Goal

Use held-out k-space inconsistency to calibrate the uncertainty map.

### Key Idea

The held-out k-space residual should provide a self-supervised reliability signal.

### Tasks

- Compute held-out k-space residual.
- Compute residual energy.
- Backproject residual into the image domain.
- Normalize uncertainty and residual maps.
- Add calibration loss.
- Train model with combined reconstruction and calibration loss.

### Expected Output

A model trained with:

- SSDU reconstruction loss
- Uncertainty calibration loss

---

## Stage 9: Evaluation

### Goal

Evaluate both image quality and reliability.

### Reconstruction Metrics

- NMSE
- PSNR
- SSIM

### Reliability Metrics

- Correlation between uncertainty and reconstruction error
- AUC for detecting high-error pixels
- Calibration curve
- Visual comparison of uncertainty and error maps

### Tasks

- Compute reconstruction error using reference image during testing.
- Compare uncertainty map with actual error map.
- Quantify whether high uncertainty corresponds to high error.
- Compare calibrated and uncalibrated uncertainty.

### Expected Output

Tables and figures suitable for a research paper.

---

## Stage 10: Paper Preparation

### Goal

Convert the project into a publishable research paper.

### Planned Paper Sections

- Introduction
- Related Work
- Method
- Experiments
- Results
- Discussion
- Limitations
- Conclusion

### Required Figures

- Overall method pipeline
- SSDU k-space splitting diagram
- Reconstruction architecture
- Uncertainty calibration pipeline
- Reconstruction and uncertainty examples
- Calibration/error correlation plots

### Expected Output

A complete manuscript draft supported by reproducible code and experiments.

---

## Current Development Priority

The immediate next technical priority is:

> Load fastMRI brain k-space data and produce a zero-filled reconstruction.
