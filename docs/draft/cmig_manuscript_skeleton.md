# CMIG Manuscript Skeleton

## Title

Four-Way Self-Supervised K-Space Partitioning for Residual-Calibrated Reliability Learning in Accelerated Brain MRI

---

## Highlights

- Four-way k-space partitioning separates reconstruction and reliability roles.
- Residual-calibrated reliability is learned without fully sampled references.
- Held-out k-space residual energy enables independent reliability evaluation.
- ReliabilityCNN modestly improves over input intensity in LOVO validation.
- The framework supports feasibility-level trustworthy MRI reconstruction.

---

## Abstract

To be written last using BOMRC:

- Background
- Objective
- Method
- Results
- Contribution

---

## Keywords

Accelerated MRI; self-supervised learning; k-space reconstruction; SSDU; reliability estimation; uncertainty; residual consistency

---

# 1. Introduction

Use PGS:

1. Problem: accelerated MRI and reliability risk.
2. Gap: SSDU does not independently calibrate and evaluate reliability.
3. Solution: four-way k-space partitioning and residual-calibrated ReliabilityCNN.

---

# 2. Related Work

## 2.1 Accelerated and Deep MRI Reconstruction

## 2.2 Self-Supervised MRI Reconstruction and SSDU

## 2.3 Uncertainty and Reliability in MRI Reconstruction

## 2.4 Gap: From Reconstruction Partitioning to Reliability Partitioning

---

# 3. Methods

Use the finalized Methods draft.

Main subsections:

## 3.1 Study Design

## 3.2 MRI Forward Model

## 3.3 Four-Way K-Space Partitioning

## 3.4 SSDU Reconstruction Training

## 3.5 Residual-Energy Reliability Targets

## 3.6 ReliabilityCNN Architecture

## 3.7 Baselines and Evaluation Metric

## 3.8 Experimental Protocol

## 3.9 Implementation Details

---

# 4. Experiments

## 4.1 Dataset

## 4.2 Leave-One-Volume-Out Validation

## 4.3 Baselines

## 4.4 Evaluation Metrics

---

# 5. Results

Use the finalized Results draft.

Main subsections:

## 5.1 Model Design Progression

## 5.2 Main Leave-One-Volume-Out Result

## 5.3 Per-Fold Results

## 5.4 Baseline Comparison

## 5.5 Representative Reliability Maps

---

# 6. Discussion

Use the finalized Discussion draft.

Main subsections:

## 6.1 Principal Findings

## 6.2 Why Four-Way Partitioning Matters

## 6.3 Interpretation of ReliabilityCNN

## 6.4 Why Input Intensity Is a Strong Baseline

## 6.5 Clinical Interpretation and Caution

## 6.6 Limitations

## 6.7 Future Work

---

# 7. Conclusion

To be drafted after Introduction and Related Work.

---

# Data Availability

The study used fastMRI data. Processed experimental results and figures are available in the project repository.

---

# Code Availability

Code, figures, and result tables are available in the GitHub repository:

https://github.com/SILAS-RANSFORD-OSEI/reliability-aware-ssdu-mri

---

# Declaration of Generative AI and AI-Assisted Technologies

To be written according to the target journal requirement.

---

# Conflict of Interest

The author declares no competing interests.

---

# References

To be generated from Zotero after final citation selection.
