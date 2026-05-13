# Experiment 009: Simple CNN Forward-Pass Test

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Model](#model)
- [Input](#input)
- [Output](#output)
- [Results](#results)
- [Interpretation](#interpretation)
- [Conclusion](#conclusion)

---

## Objective

Verify that the first learning-based reconstruction model can accept an image tensor and return an output tensor with **the same spatial dimensions**.

---

## Motivation

Before implementing SSDU training, the reconstruction model architecture must be tested independently. This experiment checks whether the simple CNN baseline can process image-domain MRI inputs without shape errors.

---

## Model

**Model:** `SimpleCNNReconstructor`

The model uses a **residual learning** structure:

$$\hat{x} = x + g_{\theta}(x)$$

| Term | Description |
|------|-------------|
| $x$ | Input image |
| $g_{\theta}(x)$ | CNN-predicted residual correction |
| $\hat{x}$ | Refined output image |
| $\theta$ | Learnable CNN parameters |

Rather than generating a full reconstruction from scratch, the model learns a **correction** to the input — making training easier and preserving the zero-filled input as a starting point.

---

## Input

A dummy image tensor was used:

$$x \in \mathbb{R}^{1 \times 1 \times 320 \times 320}$$

| Dimension | Size |
|-----------|------|
| Batch size | 1 |
| Channels | 1 |
| Height | 320 |
| Width | 320 |

---

## Output

$$\hat{x} \in \mathbb{R}^{1 \times 1 \times 320 \times 320}$$

---

## Results

| Quantity | Value |
|----------|-------|
| Input shape | `1 × 1 × 320 × 320` |
| Output shape | `1 × 1 × 320 × 320` |
| Spatial dimensions preserved | ✅ `True` |
| Forward pass successful | ✅ `True` |

---

## Interpretation

The model preserved the spatial dimensions of the input image, confirming that `SimpleCNNReconstructor` is structurally valid and ready for the next stage.

The residual formulation $\hat{x} = x + g_{\theta}(x)$ is well-suited to this setting: rather than generating an image from scratch, the model learns corrections to the zero-filled reconstruction, which accelerates training and keeps the known input signal intact.

---

## Conclusion

The simple CNN reconstruction baseline passed the initial forward-pass test.

**Next step:** connect this model to real fastMRI image-domain inputs from $\Theta$ and define the SSDU training loss on $\Lambda$.
