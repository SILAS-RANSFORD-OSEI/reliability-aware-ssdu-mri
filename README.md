# Reliability-Aware Self-Supervised MRI Reconstruction

This project investigates reliability-aware self-supervised reconstruction for accelerated brain MRI.

The central idea is to reconstruct an MR image from undersampled k-space while also estimating a voxel-wise uncertainty map that indicates where the reconstruction may be unreliable.

Unlike conventional self-supervised MRI reconstruction methods that mainly produce only a reconstructed image, this project aims to produce both:

$$
\hat{x}
$$

and

$$
U
$$

where:

- $\hat{x}$ is the reconstructed MR image.
- $U$ is a calibrated voxel-wise uncertainty or reliability map.

---

## Research Motivation

Accelerated MRI reduces scan time by acquiring only a subset of k-space measurements. However, undersampling creates an ill-posed inverse problem, meaning that multiple possible images may be consistent with incomplete measurements.

Deep learning reconstruction methods can produce visually sharp images, but they may also hallucinate structures or hide reconstruction errors. In clinical imaging, this is risky because a realistic-looking reconstruction is not necessarily reliable.

This project focuses on the question:

> Can a self-supervised MRI reconstruction model estimate not only the reconstructed image, but also where that reconstruction should not be fully trusted?

---

## Core Contribution

The core contribution is a reliability-aware self-supervised k-space reconstruction framework that uses held-out k-space consistency not only to train the reconstruction model, but also to calibrate voxel-wise uncertainty.

The project builds on three main ideas:

1. Physics-guided MRI reconstruction
2. SSDU-style self-supervised k-space splitting
3. Uncertainty calibration using held-out k-space residuals

The intended output is:

$$
(\bar{x}, U)
$$

where:

- $\bar{x}$ is the final mean reconstructed brain MR image.
- $U$ is the calibrated uncertainty map indicating spatial reconstruction reliability.

---

## What This Project Is Not Claiming

This project does **not** claim to introduce:

- The first physics-informed MRI reconstruction method
- The first self-supervised MRI reconstruction method
- The first uncertainty estimation method for MRI reconstruction
- A clinically validated AI reconstruction system

Instead, the specific research direction is:

> Using held-out k-space residuals as a self-supervised signal for calibrating spatial uncertainty in accelerated brain MRI reconstruction.

---

## Mathematical Setup

Let the measured undersampled k-space data be:

$$
y_{\Omega}
$$

where $\Omega$ is the set of acquired k-space locations.

In SSDU-style training, the acquired k-space locations are split into two disjoint sets:

$$
\Omega = \Theta \cup \Lambda
$$

$$
\Theta \cap \Lambda = \emptyset
$$

where:

- $\Theta$ is used inside the reconstruction model for data consistency.
- $\Lambda$ is held out for the self-supervised loss.

The self-supervised reconstruction loss is:

$$
\mathcal{L}_{SSDU}
=
\left\|
E_{\Lambda}\hat{x}
-
y_{\Lambda}
\right\|_2^2
$$

where:

- $E_{\Lambda}$ is the MRI encoding operator restricted to the held-out k-space locations.
- $\hat{x}$ is the reconstructed image.
- $y_{\Lambda}$ is the measured held-out k-space data.

---

## Uncertainty Estimation

The model will generate multiple stochastic reconstructions:

$$
\hat{x}_1, \hat{x}_2, \dots, \hat{x}_T
$$

where $T$ is the number of stochastic forward passes.

The mean reconstruction is:

$$
\bar{x}
=
\frac{1}{T}
\sum_{t=1}^{T}
\hat{x}_t
$$

The voxel-wise uncertainty map is estimated as:

$$
U
=
\frac{1}{T-1}
\sum_{t=1}^{T}
(\hat{x}_t-\bar{x})^2
$$

where:

- $\bar{x}$ is the mean reconstruction.
- $U$ is the voxel-wise variance map.
- High values of $U$ indicate regions where the model is less certain.

---

## Held-Out K-Space Reliability Signal

The held-out k-space residual is defined as:

$$
e_{\Lambda}
=
\left|
E_{\Lambda}\bar{x}
-
y_{\Lambda}
\right|^2
$$

where:

- $E_{\Lambda}\bar{x}$ is the predicted k-space measurement from the reconstructed image.
- $y_{\Lambda}$ is the actually measured held-out k-space data.
- $e_{\Lambda}$ measures inconsistency between prediction and measurement.

A possible uncertainty calibration loss is:

$$
\mathcal{L}_{cal}
=
\left\|
U_{\Lambda}
-
e_{\Lambda}
\right\|_1
$$

where:

- $U_{\Lambda}$ is the uncertainty estimate projected or compared in the held-out measurement domain.
- $e_{\Lambda}$ is the held-out k-space residual.
- $\mathcal{L}_{cal}$ encourages uncertainty to increase where reconstruction inconsistency is high.

The total training objective may be written as:

$$
\mathcal{L}_{total}
=
\mathcal{L}_{SSDU}
+
\lambda_{cal}\mathcal{L}_{cal}
$$

where $\lambda_{cal}$ controls the strength of uncertainty calibration.

---

## Project Objective

The objective is to develop and evaluate a reconstruction framework that outputs:

$$
(\bar{x}, U)
$$

where:

- $\bar{x}$ is the reconstructed brain MR image.
- $U$ is a calibrated uncertainty map showing where the reconstruction may be unreliable.

The key research question is:

> Can held-out k-space consistency be used not only for self-supervised reconstruction, but also for uncertainty calibration and reliability failure detection?

---

## Planned Evaluation

The project will evaluate both reconstruction quality and reliability.

### Reconstruction Quality Metrics

- Normalized Mean Squared Error
- Peak Signal-to-Noise Ratio
- Structural Similarity Index Measure

### Reliability and Uncertainty Metrics

- Correlation between uncertainty and reconstruction error
- Error detection performance
- Calibration analysis
- Reliability map visualization
- Comparison between high-uncertainty regions and actual reconstruction error

If fully sampled reference data are available for testing, reconstruction error can be computed as:

$$
\text{Error}(r)
=
|\bar{x}(r)-x_{ref}(r)|
$$

where:

- $r$ denotes a spatial voxel or pixel location.
- $\bar{x}(r)$ is the reconstructed image value at location $r$.
- $x_{ref}(r)$ is the reference image value at location $r$.

The reliability hypothesis is:

$$
U(r) \uparrow
\quad \Rightarrow \quad
\text{Error}(r) \uparrow
$$

meaning that regions with higher uncertainty should generally correspond to regions with higher reconstruction error.

---

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
