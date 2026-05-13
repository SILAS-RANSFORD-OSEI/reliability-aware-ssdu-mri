# Experiment 010: Real fastMRI CNN Forward Pass

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Input Pipeline](#input-pipeline)
- [Model](#model)
- [Results](#results)
- [Interpretation](#interpretation)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Conclusion](#conclusion)

---

## Objective

Verify that the simple CNN reconstruction baseline can process a **real fastMRI-derived image input**.

---

## Motivation

[Experiment 009](EXP_009_SIMPLE_CNN_FORWARD_PASS.md) confirmed the model's structural validity using a random dummy tensor. This experiment connects the model to real MRI data by passing a zero-filled reconstruction derived from actual fastMRI brain k-space through the CNN — a necessary checkpoint before SSDU training begins.

---

## Input Pipeline

The input was generated from real fastMRI multicoil brain k-space through the following steps:

| Step | Action |
|------|--------|
| 1 | Load real fastMRI brain k-space |
| 2 | Split acquired mask into $\Theta$ and $\Lambda$ |
| 3 | Apply $\Theta$ mask to measured k-space |
| 4 | Zero-filled reconstruction from $\Theta$-only k-space |
| 5 | Root-sum-of-squares coil combination |
| 6 | Normalise image to $[0, 1]$ |
| 7 | Centre-crop to $320 \times 320$ |
| 8 | Convert to PyTorch tensor |

**Final input tensor shape:**

$$x \in \mathbb{R}^{1 \times 1 \times 320 \times 320}$$

| Dimension | Size |
|-----------|------|
| Batch size | 1 |
| Channels | 1 |
| Height | 320 |
| Width | 320 |

---

## Model

**Model:** `SimpleCNNReconstructor`

The model follows a residual formulation:

$$\hat{x} = x + g_{\theta}(x)$$

| Term | Description |
|------|-------------|
| $x$ | $\Theta$-only zero-filled input image |
| $g_{\theta}(x)$ | CNN-predicted correction |
| $\hat{x}$ | Model output |
| $\theta$ | Learnable network parameters |

---

## Results

| Quantity | Value |
|----------|-------|
| Input tensor shape | `1 × 1 × 320 × 320` |
| Output tensor shape | `1 × 1 × 320 × 320` |
| Spatial dimensions preserved | ✅ `True` |
| Forward pass successful | ✅ `True` |

---

## Interpretation

The CNN successfully processed a real fastMRI-derived image and returned an output with identical spatial dimensions, confirming that the model can be connected to the real MRI preprocessing pipeline.

> **Note:** The model is untrained at this stage. The output is not expected to be meaningful until SSDU training is applied.

---

## Importance for the Proposed Method

This experiment closes the gap between the individual components verified in earlier experiments:

| Component | Experiment |
|-----------|-----------|
| Physics operators (FFT, RSS) | Exp 001–002 |
| SSDU mask splitting | Exp 003 |
| Held-out residual computation | Exp 004–005 |
| Backprojected residual energy | Exp 006 |
| Uncertainty utilities | Exp 007–008 |
| CNN forward pass (dummy input) | Exp 009 |
| **CNN forward pass (real input)** | **Exp 010 — this experiment** |

**Next step:** transform the CNN output $\hat{x}$ back into k-space and compute the SSDU held-out k-space consistency loss on $\Lambda$.

---

## Conclusion

The first learning-based reconstruction model can process real fastMRI-derived input through the full preprocessing pipeline.

**Next step:** connect the CNN output to the SSDU held-out k-space loss on $\Lambda$ to enable end-to-end self-supervised training.
