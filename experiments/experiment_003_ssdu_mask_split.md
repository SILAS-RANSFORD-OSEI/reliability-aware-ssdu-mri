# Experiment 003: SSDU K-Space Mask Splitting

## Table of Contents

- [Objective](#objective)
- [Dataset](#dataset)
- [Method](#method)
- [Results](#results)
- [Interpretation](#interpretation)
- [Importance for the Proposed Method](#importance-for-the-proposed-method)
- [Conclusion](#conclusion)

---

## Objective

Test SSDU-style splitting of an acquired fastMRI brain k-space mask into two disjoint subsets:

| Subset | Role |
|--------|------|
| $\Theta$ | Used for reconstruction / data consistency |
| $\Lambda$ | Held out for self-supervised loss |

---

## Dataset

| Property | Value |
|----------|-------|
| Dataset | fastMRI Brain |
| Data type | Multicoil |
| Split | Test |
| Acquisition | AXT2 |
| Acceleration | $R = 4$ |

---

## Method

The acquired k-space mask is denoted $\Omega$. SSDU splits it into two disjoint subsets:

$$\Omega = \Theta \cup \Lambda, \qquad \Theta \cap \Lambda = \varnothing$$

| Term | Description |
|------|-------------|
| $\Theta$ | Samples used inside the reconstruction model |
| $\Lambda$ | Samples held out for the self-supervised loss |
| $\rho = 0.4$ | Held-out fraction — approximately 40% of acquired samples assigned to $\Lambda$ |

---

## Results

| Quantity | Value |
|----------|------:|
| Original acquired mask fraction | 0.2500 |
| $\Theta$ mask fraction | 0.1490 |
| $\Lambda$ mask fraction | 0.1010 |
| $\Theta$ and $\Lambda$ disjoint | ✅ `True` |
| $\Theta \cup \Lambda$ equals acquired mask | ✅ `True` |

---

## Interpretation

The original acquired mask retained 25% of k-space columns, consistent with acceleration factor $R = 4$.

After SSDU splitting, the acquired samples were separated into two non-overlapping subsets, confirming:

$$\Omega = \Theta \cup \Lambda \qquad \text{and} \qquad \Theta \cap \Lambda = \varnothing$$

This validates the core SSDU sampling logic required for self-supervised MRI reconstruction.

---

## Importance for the Proposed Method

The proposed reliability-aware method depends critically on the held-out subset $\Lambda$. In this project, $\Lambda$ serves **two purposes** — extending beyond standard SSDU:

| Step | Use of $\Lambda$ |
|------|-----------------|
| Standard SSDU | Self-supervised reconstruction loss |
| **This project** | Self-supervised reconstruction loss **+** uncertainty calibration via held-out k-space residuals |

This experiment therefore verifies the **first technical step** toward the proposed reliability-aware SSDU framework.

---

## Conclusion

The SSDU mask split works correctly on real fastMRI brain sampling masks.

**Next step:** compute the held-out k-space residual on $\Lambda$ and use it as a reliability signal.
