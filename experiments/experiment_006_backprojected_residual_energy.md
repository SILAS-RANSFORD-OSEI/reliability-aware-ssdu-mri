# Experiment 006: Backprojected Held-Out Residual Energy

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Method](#method)
- [Results](#results)
- [Interpretation](#interpretation)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Conclusion](#conclusion)

---

## Objective

Compute and visualise the **image-domain reliability signal** obtained by backprojecting the held-out k-space residual from the $\Lambda$ subset.

---

## Motivation

The proposed reliability-aware reconstruction method requires an image-domain signal that can be compared with, or used to calibrate, a voxel-wise uncertainty map.

| Domain | Signal |
|--------|--------|
| K-space | Held-out residual $r_{\Lambda}$ — naturally defined here |
| Image | Uncertainty map $U$ — defined here |

Because these two signals live in different domains, the residual must be **backprojected into the image domain** before any comparison or calibration can take place.

---

## Method

The acquired mask $\Omega$ was split into disjoint subsets:

$$\Omega = \Theta \cup \Lambda, \qquad \Theta \cap \Lambda = \varnothing$$

**Step 1 — Restrict measured k-space to $\Theta$:**

$$y_{\Theta} = M_{\Theta} \odot y$$

**Step 2 — Zero-filled reconstruction from $\Theta$ only:**

$$x_{\Theta} = \mathcal{F}^{-1}(y_{\Theta})$$

**Step 3 — Predict k-space from the reconstruction:**

$$\hat{y} = \mathcal{F}(x_{\Theta})$$

**Step 4 — Compute held-out residual on $\Lambda$:**

$$r_{\Lambda} = M_{\Lambda} \odot (\hat{y} - y)$$

**Step 5 — Backproject residual into the image domain:**

$$e_{\mathrm{img}} = \left| \mathcal{F}^{-1}(r_{\Lambda}) \right|^2$$

**Step 6 — Sum across coils for multicoil data:**

$$E_{\mathrm{img}} = \sum_{c=1}^{C} \left| \mathcal{F}^{-1}(r_{\Lambda,c}) \right|^2$$

| Term | Description |
|------|-------------|
| $C$ | Number of receiver coils |
| $r_{\Lambda,c}$ | Held-out residual for coil $c$ |
| $E_{\mathrm{img}}$ | Image-domain residual energy map |

---

## Results

The backprojected residual energy produced an **image-domain map** highlighting spatial regions influenced by inconsistency on the held-out k-space samples.

The output showed higher residual energy around anatomical structures and edges — regions where missing k-space information has the strongest image-domain effect.

---

## Interpretation

$E_{\mathrm{img}}$ is not yet a learned uncertainty map. It is a **self-supervised reliability signal** derived entirely from measured k-space data, requiring no ground-truth reference.

This signal answers the question:

> **Where does the reconstruction disagree with measured k-space that was hidden from the reconstruction input?**

---

## Importance for the Proposed Method

This experiment provides the **bridge between SSDU and uncertainty calibration**.

| Framework | Role of the held-out residual |
|-----------|-------------------------------|
| Standard SSDU | Reconstruction loss only |
| **This project** | Reconstruction loss **+** self-supervised calibration signal for image-domain uncertainty |

The future uncertainty calibration objective will compare the predicted uncertainty map $U$ directly against the image-domain residual signal $E_{\mathrm{img}}$:

$$\mathcal{L}_{\mathrm{cal}} = \left\| \mathcal{N}(U) - \mathcal{N}(E_{\mathrm{img}}) \right\|_1$$

---

## Conclusion

The held-out k-space residual can be backprojected into the image domain to produce a spatial reliability signal — without any ground-truth reference data.

This supports the core direction of the project:

> **Using held-out k-space consistency not only for reconstruction learning, but also for uncertainty calibration.**

**Next step:** connect $E_{\mathrm{img}}$ to a predicted uncertainty map $U$ from a stochastic reconstruction model and evaluate whether the two signals are spatially correlated.
