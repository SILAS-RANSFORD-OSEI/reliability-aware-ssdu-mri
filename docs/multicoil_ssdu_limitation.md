# Multicoil SSDU Limitation Note

## Table of Contents

- [Problem Observed](#problem-observed)
- [Why This Happened](#why-this-happened)
- [Consequence](#consequence)
- [Correct Direction](#correct-direction)
- [Immediate Research Decision](#immediate-research-decision)
- [Importance for the Paper](#importance-for-the-paper)
- [Conclusion](#conclusion)

---

## Problem Observed

A temporary test replicated a single-channel CNN output image across all receiver coils and compared it against measured multicoil k-space using the SSDU $\Lambda$ loss.

The tensor shapes matched:

| Tensor | Shape |
|--------|-------|
| CNN output after coil replication | `16 × 768 × 396` |
| Measured multicoil k-space | `16 × 768 × 396` |

However, the SSDU loss was **extremely large**:

$$\mathcal{L}_{\mathrm{SSDU}} = 38{,}491{,}630$$

---

## Why This Happened

The shortcut was **physically invalid**.

In multicoil MRI, each receiver coil observes the object through a different spatial sensitivity profile:

$$x_c = S_c\, x$$

| Term | Description |
|------|-------------|
| $x$ | Underlying object image |
| $S_c$ | Sensitivity map of coil $c$ |
| $x_c$ | Coil-specific image |
| $c$ | Receiver coil index |

The temporary test assumed:

$$x_1 = x_2 = \cdots = x_C$$

by copying the same CNN output across all coils — ignoring coil sensitivity variation entirely. This produces **incorrect predicted multicoil k-space**, regardless of whether the tensor shapes are compatible.

---

## Consequence

> **Correct shape does not imply correct physics.**

Although the pipeline was dimensionally consistent, the forward model was wrong. The following approach must **not** be used as the final SSDU method:

> RSS image reconstruction followed by naive replication across coils.

---

## Correct Direction

A scientifically valid multicoil SSDU method requires one of the following approaches:

| Option | Description |
|--------|-------------|
| 1 | Coil sensitivity estimation with a proper multicoil forward model |
| 2 | A model that operates directly on multicoil images or k-space |
| 3 | A single-coil-equivalent baseline before extending to full multicoil reconstruction |

---

## Immediate Research Decision

> **Start with a single-coil-equivalent SSDU baseline to verify learning behaviour, then extend to multicoil physics using coil sensitivity maps.**

This is the safest route: confirm that the model learns meaningful reconstructions under SSDU supervision before introducing the added complexity of coil sensitivity estimation.

---

## Importance for the Paper

This note prevents a physically invalid shortcut from entering the method section.

The final paper must respect the full multicoil MRI acquisition model:

$$y_{\Omega,c} = M_{\Omega}\, \mathcal{F}(S_c\, x) + n_c$$

| Term | Description |
|------|-------------|
| $y_{\Omega,c}$ | Undersampled k-space from coil $c$ |
| $M_{\Omega}$ | Undersampling mask |
| $\mathcal{F}$ | Fourier transform |
| $S_c$ | Coil sensitivity map |
| $x$ | Object image |
| $n_c$ | Measurement noise in coil $c$ |

Any SSDU loss that does not account for $S_c$ is comparing predicted k-space from the wrong forward model against real measurements — producing a meaningless loss value.

---

## Conclusion

The temporary CNN-to-$\Lambda$ SSDU loss test was useful as a **pipeline shape check**, but it exposed the need for a proper coil-aware forward model.

**Next implementation steps:**

| Priority | Action |
|----------|--------|
| Immediate | Implement a single-coil-equivalent SSDU baseline |
| Follow-up | Estimate coil sensitivity maps ($S_c$) for full multicoil extension |
| Avoid | Naive coil replication of a single-channel reconstruction |
