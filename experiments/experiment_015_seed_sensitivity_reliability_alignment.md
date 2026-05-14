# Experiment 015: Seed Sensitivity of Uncertainty-Residual Alignment

## Objective

Evaluate whether uncertainty-residual alignment is stable under different random seeds.

---

## Motivation

The previous experiment showed strong uncertainty-residual alignment for one trained dropout SSDU model.

However, a single result is not enough for a publishable method. We need to test whether the alignment is stable under different sources of randomness.

This experiment separates two sources of randomness:

1. SSDU split randomness
2. Model initialization and dropout randomness

---

## Setup

- Dataset: fastMRI Brain
- Acquisition: AXT2
- Acceleration: R = 4
- Slice index: 8
- Coil index: 0
- Model: DropoutCNNReconstructor
- Training steps: 50
- Number of stochastic reconstructions: 8
- SSDU held-out fraction: 0.4

---

## Test 1: Fixed SSDU Split, Varying Model Seed

The SSDU split was fixed using:

$$
\text{split seed} = 42
$$

The model seed was varied from 0 to 4.

### Results

| Model Seed | Initial SSDU Loss | Final SSDU Loss | SSDU Reduction (%) | Alignment |
|---:|---:|---:|---:|---:|
| 0 | 10,912,285 | 9,636,117 | 11.69 | 0.661 |
| 1 | 11,113,994 | 10,719,709 | 3.55 | 0.601 |
| 2 | 11,180,112 | 9,586,817 | 14.25 | 0.156 |
| 3 | 10,317,614 | 7,328,033 | 28.98 | 0.659 |
| 4 | 9,736,413 | 4,039,148.25 | 58.52 | 0.696 |

### Summary

| Quantity | Value |
|---|---:|
| Mean SSDU reduction | 23.40% |
| Std SSDU reduction | 21.67% |
| Mean alignment | 0.554 |
| Std alignment | 0.225 |
| Minimum alignment | 0.156 |
| Maximum alignment | 0.696 |

---

## Test 2: Fixed Model Seed, Varying SSDU Split Seed

The model seed was fixed using:

$$
\text{model seed} = 0
$$

The SSDU split seed was varied from 0 to 4.

### Results

| Split Seed | Initial SSDU Loss | Final SSDU Loss | SSDU Reduction (%) | Alignment |
|---:|---:|---:|---:|---:|
| 0 | 10,138,312 | 9,039,799 | 10.84 | 0.735 |
| 1 | 22,203,380 | 19,738,796 | 11.10 | 0.782 |
| 2 | 34,829,616 | 21,775,648 | 37.48 | 0.668 |
| 3 | 6,563,271.5 | 5,961,636 | 9.17 | 0.528 |
| 4 | 8,400,630 | 7,493,101.5 | 10.80 | 0.654 |

### Summary

| Quantity | Value |
|---|---:|
| Mean SSDU reduction | 15.88% |
| Std SSDU reduction | 12.10% |
| Mean alignment | 0.674 |
| Std alignment | 0.096 |
| Minimum alignment | 0.528 |
| Maximum alignment | 0.782 |

---

## Interpretation

The uncertainty-residual alignment remained positive when the SSDU split varied while the model seed was fixed.

The alignment was more variable when the model seed varied while the SSDU split was fixed.

This suggests that the reliability mechanism is more sensitive to:

- model initialization,
- dropout randomness,
- and training dynamics,

than to the specific Theta/Lambda split.

---

## Importance for the Proposed Method

This experiment is important because it tests whether the uncertainty-residual alignment is repeatable rather than a single lucky result.

The result is promising because most alignments remain positive.

However, the model-seed experiment shows that training stability must be improved before strong journal-level claims can be made.

---

## Current Limitation

This experiment still uses:

- one slice,
- one coil,
- one file,
- a simple dropout CNN,
- and no fully sampled reference image.

Therefore, the result supports method development but is not yet final validation.

---

## Conclusion

The reliability mechanism appears more stable with respect to SSDU mask splitting than model initialization.

The next technical priority is to improve training stability and then test across multiple slices.
