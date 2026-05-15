# Experiment 017: Four-Way SSDU Mask Split

## Table of Contents

- [Objective](#objective)
- [Motivation](#motivation)
- [Definitions](#definitions)
- [Method](#method)
- [Results](#results)
- [Verification](#verification)
- [Interpretation](#interpretation)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Current Limitation](#current-limitation)
- [Conclusion](#conclusion)

---

## Objective

Implement and verify a reviewer-defensible SSDU k-space partitioning strategy that separates reconstruction input, training loss, uncertainty calibration, and final reliability evaluation into four independent subsets.

---

## Motivation

The earlier SSDU setup used a two-way split:

$$\Omega = \Theta \cup \Lambda$$

where:

- $\Theta$ was used for reconstruction input and data consistency.
- $\Lambda$ was used for held-out loss and reliability analysis.

This setup is useful for feasibility testing, but it can be criticised because the same held-out samples serve multiple roles simultaneously. To address this, the acquired k-space mask is now split into four disjoint subsets:

$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

with all pairwise intersections equal to zero.

---

## Definitions

| Subset | Role |
|--------|------|
| $\Theta$ | Reconstruction input / data consistency |
| $\Lambda_{\mathrm{train}}$ | SSDU reconstruction training loss |
| $\Lambda_{\mathrm{cal}}$ | Uncertainty calibration signal |
| $\Lambda_{\mathrm{eval}}$ | Final held-out reliability evaluation |

---

## Method

The original acquired mask $\Omega$ was partitioned using the following fractions of acquired samples:

| Subset | Fraction of Acquired Samples |
|--------|-----------------------------:|
| $\Lambda_{\mathrm{train}}$ | 0.20 |
| $\Lambda_{\mathrm{cal}}$ | 0.10 |
| $\Lambda_{\mathrm{eval}}$ | 0.10 |
| $\Theta$ | Remainder |

The remaining acquired samples after assigning the three held-out subsets were assigned to $\Theta$.

The original fastMRI file had acceleration factor $R = 4$, so approximately 25% of full k-space columns were acquired.

---

## Results

| Mask | Fraction of Full K-Space |
|------|-------------------------:|
| Original acquired mask $\Omega$ | 0.2500 |
| $\Theta$ | 0.14899 |
| $\Lambda_{\mathrm{train}}$ | 0.05051 |
| $\Lambda_{\mathrm{cal}}$ | 0.02525 |
| $\Lambda_{\mathrm{eval}}$ | 0.02525 |

The four subsets satisfied:

$$\Theta + \Lambda_{\mathrm{train}} + \Lambda_{\mathrm{cal}} + \Lambda_{\mathrm{eval}} = \Omega$$

with all pairwise overlaps equal to zero.

---

## Verification

| Check | Result |
|-------|--------|
| Combined masks equal original acquired mask $\Omega$ | ✅ `True` |
| $\Theta \cap \Lambda_{\mathrm{train}}$ | 0 |
| $\Theta \cap \Lambda_{\mathrm{cal}}$ | 0 |
| $\Theta \cap \Lambda_{\mathrm{eval}}$ | 0 |
| $\Lambda_{\mathrm{train}} \cap \Lambda_{\mathrm{cal}}$ | 0 |
| $\Lambda_{\mathrm{train}} \cap \Lambda_{\mathrm{eval}}$ | 0 |
| $\Lambda_{\mathrm{cal}} \cap \Lambda_{\mathrm{eval}}$ | 0 |

---

## Interpretation

The four-way SSDU split was implemented correctly and all pairwise disjointness conditions are satisfied.

This improves the methodological defensibility of the project because training, calibration, and evaluation now operate on independent held-out measurements. The previous two-way split was sufficient for early feasibility experiments, but the four-way split is better suited for a journal-level method.

---

## Importance for the Proposed Method

This experiment directly addresses a key reviewer concern:

> **The same held-out samples should not be used for training, uncertainty calibration, and final reliability evaluation.**

The four-way split allows the future method to use each subset independently:

$$\Lambda_{\mathrm{train}}$$

for self-supervised reconstruction learning,

$$\Lambda_{\mathrm{cal}}$$

for residual-based uncertainty calibration,

$$\Lambda_{\mathrm{eval}}$$

for final held-out reliability evaluation.

This separation reduces circularity and strengthens the reliability argument.

---

## Current Limitation

This experiment only verifies the mask partitioning logic. The training and reliability workflow has not yet been adapted to use the four-way split.

The next step is to update the pipeline so that:

- the model trains on $\Lambda_{\mathrm{train}}$,
- uncertainty is calibrated using $\Lambda_{\mathrm{cal}}$,
- final reported alignment is computed on $\Lambda_{\mathrm{eval}}$.

---

## Conclusion

The four-way SSDU mask split works correctly and provides a more reviewer-defensible foundation for reliability-aware self-supervised MRI reconstruction.

**Next step:** adapt the training and reliability workflow to use $\Lambda_{\mathrm{train}}$, $\Lambda_{\mathrm{cal}}$, and $\Lambda_{\mathrm{eval}}$ as independent subsets.
