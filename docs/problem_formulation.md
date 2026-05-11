# Problem Formulation

## Table of Contents

- [Research Problem](#research-problem)
- [Core Question](#core-question)
- [Input](#input)
- [Output](#output)
- [Forward Model](#forward-model)
- [Self-Supervised Reconstruction Objective](#self-supervised-reconstruction-objective)
- [Reliability-Aware Extension](#reliability-aware-extension)
- [Hypothesis](#hypothesis)
- [Practical Importance](#practical-importance)

---

## Research Problem

Accelerated MRI reduces scan time by acquiring only a subset of k-space measurements. This creates an inverse problem where the goal is to recover the underlying image from incomplete Fourier-domain data.

The main challenge is that undersampled MRI reconstruction is **ill-posed** — a reconstruction model may generate an image that appears visually plausible while still containing local errors or unreliable regions.

Most self-supervised MRI reconstruction methods focus solely on reconstructing the image. This project extends that objective by asking whether the model can also **estimate where the reconstruction is uncertain or unreliable**.

---

## Core Question

> **Can held-out k-space consistency be used not only to train a self-supervised MRI reconstruction model, but also to calibrate voxel-wise uncertainty for reliability-aware reconstruction?**

---

## Input

The input is undersampled k-space data $y_{\Omega}$, where $\Omega$ is the set of acquired k-space locations.

The acquired k-space is split into two disjoint subsets:

$$\Omega = \Theta \cup \Lambda, \qquad \Theta \cap \Lambda = \varnothing$$

| Subset | Role |
|--------|------|
| $\Theta$ | Data consistency inside the reconstruction model |
| $\Lambda$ | Held out for self-supervised loss and reliability calibration |

---

## Output

The model outputs a pair $(\bar{x},\ U)$:

| Symbol | Description |
|--------|-------------|
| $\bar{x}$ | Reconstructed MR image |
| $U$ | Voxel-wise uncertainty map |

---

## Forward Model

The MRI measurement process is modelled as:

$$y_{\Omega} = E_{\Omega}\,x + n$$

| Term | Description |
|------|-------------|
| $x$ | Unknown true image |
| $E_{\Omega}$ | Undersampled MRI encoding operator |
| $n$ | Measurement noise |
| $y_{\Omega}$ | Acquired undersampled k-space data |

The encoding operator $E_{\Omega}$ differs by acquisition type:

- **Single-coil MRI** — undersampled Fourier encoding
- **Multicoil MRI** — coil sensitivity encoding + Fourier transform + undersampling

---

## Self-Supervised Reconstruction Objective

The reconstruction model receives $y_{\Theta}$ and produces an image estimate:

$$\hat{x} = f_{\theta}(y_{\Theta})$$

The held-out k-space loss is:

$$\mathcal{L}_{\mathrm{SSDU}} = \left\| E_{\Lambda}\hat{x} - y_{\Lambda} \right\|_2^2$$

This forces the reconstruction to agree with acquired measurements that were **not** directly used inside the reconstruction model.

---

## Reliability-Aware Extension

Rather than using the held-out k-space residual solely as a training loss, this project repurposes it as a **reliability signal**.

**Held-out residual:**

$$r_{\Lambda} = E_{\Lambda}\bar{x} - y_{\Lambda}$$

**Residual energy:**

$$e_{\Lambda} = \left| r_{\Lambda} \right|^2$$

**Image-domain backprojection** (for comparison with image-domain uncertainty):

$$e_{\mathrm{img}} = \left| E_{\Lambda}^{H}\,r_{\Lambda} \right|^2$$

The uncertainty map $U$ is calibrated so that **high uncertainty corresponds to regions likely to have high reconstruction error**.

---

## Hypothesis

$$U(r) \uparrow \quad \Longrightarrow \quad \left|\,\bar{x}(r) - x_{\mathrm{ref}}(r)\,\right| \uparrow$$

| Term | Description |
|------|-------------|
| $r$ | Spatial pixel or voxel location |
| $U(r)$ | Predicted uncertainty at location $r$ |
| $\bar{x}(r)$ | Reconstructed image value at location $r$ |
| $x_{\mathrm{ref}}(r)$ | Reference image value (available only during evaluation) |

Regions with higher predicted uncertainty should correspond to regions with higher actual reconstruction error.

---

## Practical Importance

A reliability-aware MRI reconstruction system should do more than produce a visually plausible image — it should **indicate regions where the reconstruction may be less trustworthy**.

This matters because clinical interpretation depends not only on image quality, but also on knowing when a reconstructed region may be unreliable. Overconfident reconstructions can mask errors that are critical for diagnosis.
