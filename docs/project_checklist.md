# Project Checklist

This checklist tracks the development progress of the reliability-aware self-supervised MRI reconstruction project.

---

## Completed

- [x] Create GitHub repository
- [x] Add repository folder structure
- [x] Write project README
- [x] Add problem formulation document
- [x] Add implementation roadmap
- [x] Add zero-filled reconstruction experiment plan
- [x] Add zero-filled reconstruction notebook plan
- [x] Add source-code structure plan
- [x] Add MRI Fourier transform utilities
- [x] Add undersampling mask utilities
- [x] Add reconstruction metrics
- [x] Add zero-filled reconstruction utilities
- [x] Add package initializer
- [x] Add zero-filled R4 experiment config

---

## Next Immediate Tasks

- [ ] Create first Colab notebook
- [ ] Connect Colab to GitHub repository
- [ ] Test `fft2c` and `ifft2c`
- [ ] Test Cartesian undersampling mask
- [ ] Test zero-filled reconstruction on synthetic k-space
- [ ] Download or access fastMRI brain data
- [ ] Run zero-filled reconstruction on real brain MRI k-space

---

## Research Milestones

### Milestone 1: Basic MRI Physics Pipeline

- [ ] Load k-space
- [ ] Visualize k-space
- [ ] Apply undersampling mask
- [ ] Reconstruct using inverse FFT
- [ ] Save zero-filled reconstruction

### Milestone 2: Baseline Reconstruction

- [ ] Implement U-Net baseline
- [ ] Implement SSDU k-space split
- [ ] Train SSDU baseline
- [ ] Compare against zero-filled reconstruction

### Milestone 3: Reliability-Aware Reconstruction

- [ ] Add stochastic reconstruction
- [ ] Generate multiple reconstructions
- [ ] Compute mean reconstruction
- [ ] Compute voxel-wise uncertainty map
- [ ] Compute held-out k-space residual
- [ ] Add uncertainty calibration loss

### Milestone 4: Evaluation

- [ ] Compute NMSE
- [ ] Compute PSNR
- [ ] Add SSIM
- [ ] Compute uncertainty-error correlation
- [ ] Compute error-detection AUC
- [ ] Produce reliability visualizations

### Milestone 5: Paper Preparation

- [ ] Write related work notes
- [ ] Prepare method diagram
- [ ] Prepare experiment tables
- [ ] Draft method section
- [ ] Draft results section
- [ ] Draft discussion and limitations

---

## Current Status

The project is currently at:

> Stage 1 complete: repository and documentation setup.

The next practical target is:

> Test the basic MRI reconstruction utilities in Google Colab.
