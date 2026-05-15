# Experiment 020 — All-Slice Four-Way Reliability Evaluation

## Objective

Evaluate whether the four-way SSDU uncertainty–residual alignment remains **positive across all slices** of one fastMRI brain volume, addressing reviewer concern about favorable slice selection in prior experiments.

---

## Motivation

Previous experiments tested selected slices only. A reviewer may question whether the positive uncertainty–residual relationship depended on favorable slice selection.

This experiment applies the four-way reliability workflow exhaustively to **all 16 slices** of one fastMRI brain volume, providing a stronger within-volume reliability claim.

---

## Dataset

| Property | Value |
|---|---|
| Dataset | fastMRI Brain |
| Acquisition type | AXT2 |
| Data type | Multicoil source file |
| Working setup | Single-coil-equivalent baseline |
| Acceleration | R = 4 |
| Selected coil | Coil 0 |
| Tested slices | 0 – 15 (all 16 slices) |

---

## Four-Way SSDU Partition

The acquired k-space mask $\Omega$ is split into four disjoint subsets:

$$
\Omega = \Theta \;\cup\; \Lambda_{\mathrm{train}} \;\cup\; \Lambda_{\mathrm{cal}} \;\cup\; \Lambda_{\mathrm{eval}}
$$

| Subset | Role |
|---|---|
| $\Theta$ | Forms the zero-filled reconstruction input |
| $\Lambda_{\mathrm{train}}$ | Provides the SSDU training loss |
| $\Lambda_{\mathrm{cal}}$ | Used for calibration-style reliability analysis |
| $\Lambda_{\mathrm{eval}}$ | Reserved held-out subset for final reliability evaluation |

The critical design property: $\Lambda_{\mathrm{eval}}$ is **never seen during training**. Any correlation between uncertainty and $\Lambda_{\mathrm{eval}}$ residual energy must arise from genuine generalization, not overfitting.

---

## Method

For each of the 16 slices:

1. Select coil 0 from the multicoil k-space.
2. Split the acquired mask into four disjoint subsets $\{\Theta, \Lambda_{\mathrm{train}}, \Lambda_{\mathrm{cal}}, \Lambda_{\mathrm{eval}}\}$.
3. Form the $\Theta$-only zero-filled input image.
4. Train a dropout CNN using only $\Lambda_{\mathrm{train}}$ as the SSDU supervision signal.
5. Generate stochastic dropout reconstructions at inference.
6. Compute the voxel-wise **mean reconstruction**.
7. Compute voxel-wise **dropout uncertainty** $U$.
8. Compute residual energy on $\Lambda_{\mathrm{cal}}$ (calibration check).
9. Compute residual energy on $\Lambda_{\mathrm{eval}}$ (held-out evaluation).
10. Measure Pearson correlation between uncertainty and each residual energy map.

### Primary Evaluation Metric

$$
\rho\!\left(U,\; E_{\Lambda_{\mathrm{eval}}}\right)
$$

where:
- $U$ — voxel-wise dropout-derived uncertainty map
- $E_{\Lambda_{\mathrm{eval}}}$ — backprojected residual energy from the held-out evaluation subset $\Lambda_{\mathrm{eval}}$

A positive $\rho$ indicates that regions where the model is uncertain spatially correspond to regions with high unseen residual energy — a necessary condition for a useful reliability signal.

---

## Results

### Per-Slice Metrics

| Slice | Initial SSDU Loss | Final SSDU Loss | Train Reduction (%) | $\rho(U, E_{\Lambda_{\mathrm{cal}}})$ | $\rho(U, E_{\Lambda_{\mathrm{eval}}})$ |
|---:|---:|---:|---:|---:|---:|
| 0 | 195,396,224 | 88,244,464 | 54.84 | 0.335 | 0.381 |
| 1 | 252,891,232 | 124,315,192 | 50.84 | 0.355 | 0.413 |
| 2 | 134,028,280 | 67,938,600 | 49.31 | 0.375 | 0.439 |
| 3 | 86,146,960 | 44,620,792 | 48.20 | 0.343 | 0.453 |
| 4 | 77,422,920 | 40,357,816 | 47.87 | 0.393 | 0.405 |
| 5 | 70,205,912 | 37,586,504 | 46.46 | 0.348 | 0.458 |
| 6 | 36,439,496 | 21,719,716 | 40.40 | 0.392 | 0.447 |
| 7 | 41,045,204 | 24,071,168 | 41.35 | 0.371 | 0.467 |
| 8 | 34,236,328 | 20,935,760 | 38.85 | 0.424 | 0.512 |
| 9 | 39,558,752 | 24,140,456 | 38.98 | 0.429 | 0.502 |
| 10 | 38,363,132 | 23,740,318 | 38.12 | 0.430 | 0.491 |
| 11 | 50,481,560 | 31,555,356 | 37.49 | 0.459 | 0.482 |
| 12 | 55,932,456 | 35,439,108 | 36.64 | 0.433 | 0.518 |
| 13 | 73,542,904 | 48,026,880 | 34.70 | 0.451 | 0.503 |
| 14 | 232,301,776 | 144,909,680 | 37.62 | 0.386 | 0.535 |
| 15 | 375,929,824 | 221,489,904 | 41.08 | 0.336 | 0.518 |

### Summary Statistics

| Metric | Mean | Std | Min | Max |
|---|---:|---:|---:|---:|
| Train SSDU reduction (%) | 42.67 | 6.01 | — | — |
| Calibration alignment $\rho(U, E_{\Lambda_{\mathrm{cal}}})$ | 0.391 | 0.042 | 0.335 | 0.459 |
| Evaluation alignment $\rho(U, E_{\Lambda_{\mathrm{eval}}})$ | 0.470 | 0.045 | 0.381 | 0.535 |

**Key observation:** Evaluation alignment is consistently higher than calibration alignment across all slices, and both remain strictly positive with no exception across the full 16-slice stack.

---

## Interpretation

The mean evaluation alignment was:

$$
\rho\!\left(U,\; E_{\Lambda_{\mathrm{eval}}}\right) = 0.470 \pm 0.045
$$

This indicates that dropout-derived uncertainty remains positively associated with residual energy from $\Lambda_{\mathrm{eval}}$ across every slice — even though $\Lambda_{\mathrm{eval}}$ was never used during training. The consistent positive spread (min 0.381, max 0.535) rules out the possibility that the result is an artifact of favorable slice selection.

The slight but consistent upward shift from calibration alignment to evaluation alignment is noteworthy. One plausible interpretation is that $\Lambda_{\mathrm{eval}}$ captures k-space structure that is marginally more spatially complementary to the uncertainty map than $\Lambda_{\mathrm{cal}}$ — though this warrants further investigation before drawing strong conclusions.

---

## Reviewer-Level Significance

This experiment was designed to address a specific reviewability concern:

> *Does the positive uncertainty–residual alignment depend on favorable slice selection?*

The all-slice experiment answers this with:

> Under a four-way SSDU split, dropout-derived uncertainty remains positively aligned with unseen held-out residual energy **across all 16 slices** of one fastMRI brain volume.

This is a stronger claim than the prior three-slice result because it exhausts all anatomical positions within the tested volume and shows no slice for which the relationship fails.

---

## Limitations

This experiment is not final validation. Remaining gaps include:

- Only **one fastMRI file** tested — cross-file generalization is unverified
- Only **one coil** (coil 0) — sensitivity encoding and multicoil geometry are not modelled
- A **simple dropout CNN** — no comparison against learned uncertainty methods (e.g. normalizing flows, conformal prediction)
- **No fully sampled reference image** — true image-domain error cannot be computed
- **No multicoil sensitivity model** — coil combination artifacts may affect results
- **No naive reliability baselines** — random maps, intensity maps, and edge maps have not yet been tested as controls

---

## Importance for the Proposed Method

This experiment strengthens the **reliability-aware SSDU** direction by demonstrating that:

1. The positive uncertainty–residual relationship is not a cherry-picked result.
2. The four-way split generalizes across all anatomical slice positions within one volume.
3. The relationship holds at both the calibration and evaluation partition levels, consistent with a genuine reliability signal rather than distributional coincidence.

The result supports continuing toward baseline-controlled and multi-file reliability evaluation.

---

## Next Steps

- [ ] Compare dropout uncertainty against naive reliability baselines (random maps, intensity maps, edge maps)
- [ ] Extend evaluation to multiple fastMRI files to test cross-volume generalization
- [ ] Incorporate multicoil sensitivity modelling
- [ ] Establish fully sampled reference comparisons where available
- [ ] Quantify the calibration–evaluation alignment gap more rigorously

---

## Conclusion

Across all 16 slices of one fastMRI brain volume, the four-way SSDU workflow produced **consistently positive evaluation alignment** between dropout uncertainty and unseen held-out residual energy. No slice failed to show a positive correlation. The mean evaluation alignment of $0.470 \pm 0.045$ supports the reliability-aware SSDU hypothesis and motivates the next phase of baseline-controlled and multi-file evaluation.
