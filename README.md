# Reliability-Aware Self-Supervised MRI Reconstruction

This project investigates reliability-aware self-supervised reconstruction for accelerated brain MRI.

The central idea is to reconstruct an MR image from undersampled k-space while also estimating a voxel-wise uncertainty map that indicates where the reconstruction may be unreliable.

Unlike conventional self-supervised MRI reconstruction methods that mainly produce a reconstructed image, this project aims to produce both:

\[
\hat{x}
\]

and

\[
U
\]

where:

- \(\hat{x}\) is the reconstructed MR image.
- \(U\) is a calibrated voxel-wise uncertainty or reliability map.

## Research Motivation

Accelerated MRI reduces scan time by acquiring only a subset of k-space measurements. However, undersampling creates an ill-posed inverse problem, meaning multiple possible images may be consistent with incomplete measurements.

Deep learning reconstruction methods can produce visually sharp images, but they may also hallucinate structures or hide reconstruction errors. In clinical imaging, this is risky because a realistic-looking reconstruction is not necessarily reliable.

This project focuses on the question:

> Can a self-supervised MRI reconstruction model estimate not only the reconstructed image, but also where that reconstruction should not be fully trusted?

## Core Contribution

The core contribution is a reliability-aware self-supervised k-space reconstruction framework that uses held-out k-space consistency not only to train the reconstruction model, but also to calibrate voxel-wise uncertainty.

The project builds on three ideas:

1. Physics-guided MRI reconstruction
2. SSDU-style self-supervised k-space splitting
3. Uncertainty calibration using held-out k-space residuals

## Mathematical Setup

Let the measured undersampled k-space data be:

\[
y_{\Omega}
\]

where \(\Omega\) is the set of acquired k-space locations.

In SSDU-style training, the acquired k-space locations are split into two disjoint sets:

\[
\Omega = \Theta \cup \Lambda,
\qquad
\Theta \cap \Lambda = \emptyset
\]

where:

- \(\Theta\) is used inside the reconstruction model for data consistency.
- \(\Lambda\) is held out for the self-supervised loss.

The self-supervised reconstruction loss is:

\[
\mathcal{L}_{SSDU}
=
\left\|
E_{\Lambda}\hat{x}
-
y_{\Lambda}
\right\|_2^2
\]

where:

- \(E_{\Lambda}\) is the MRI encoding operator restricted to the held-out k-space locations.
- \(\hat{x}\) is the reconstructed image.
- \(y_{\Lambda}\) is the measured held-out k-space data.

## Uncertainty Estimation

The model will generate multiple stochastic reconstructions:

\[
\hat{x}_1, \hat{x}_2, \dots, \hat{x}_T
\]

The mean reconstruction is:

\[
\bar{x}
=
\frac{1}{T}
\sum_{t=1}^{T}
\hat{x}_t
\]

The voxel-wise uncertainty map is:

\[
U
=
\frac{1}{T-1}
\sum_{t=1}^{T}
(\hat{x}_t-\bar{x})^2
\]

The uncertainty will be calibrated using held-out k-space inconsistency:

\[
e_{\Lambda}
=
\left|
E_{\Lambda}\bar{x}
-
y_{\Lambda}
\right|^2
\]

A possible calibration loss is:

\[
\mathcal{L}_{cal}
=
\left\|
U_{\Lambda}
-
e_{\Lambda}
\right\|_1
\]

## Project Objective

The objective is to develop and evaluate a reconstruction framework that outputs:

\[
(\bar{x}, U)
\]

where:

- \(\bar{x}\) is the final reconstructed brain MR image.
- \(U\) is a calibrated uncertainty map indicating spatial reconstruction reliability.

## Planned Evaluation

The project will evaluate both reconstruction quality and reliability.

Reconstruction metrics:

- NMSE
- PSNR
- SSIM

Reliability metrics:

- Correlation between uncertainty and reconstruction error
- Error detection performance
- Calibration analysis
- Reliability maps for visual inspection

## Repository Structure

```text
data/
notebooks/
src/
configs/
experiments/
results/
docs/
tests/
