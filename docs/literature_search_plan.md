# Literature Search Plan

## Working Paper Topic

Reliability-aware self-supervised k-space MRI reconstruction with calibrated uncertainty for accelerated brain MRI.

---

## Core Paper Claim

This work investigates whether held-out k-space consistency can be used not only for self-supervised MRI reconstruction, but also as a reliability signal for calibrating voxel-wise uncertainty maps.

---

## Research Questions

### RQ1: Method

What self-supervised or unsupervised methods have been proposed for accelerated MRI reconstruction without fully sampled ground-truth training labels?

### RQ2: Outcome

How have MRI reconstruction methods evaluated image quality, uncertainty, reliability, and reconstruction failure?

### RQ3: Problem

What gaps remain in self-supervised MRI reconstruction regarding uncertainty calibration, hallucination risk, and spatial reliability?

---

## Literature Buckets

### Bucket 1: Seminal MRI Reconstruction Papers

Purpose: establish that physics-guided and unrolled reconstruction methods already exist.

Target papers: 8 to 10.

Key terms:

- compressed sensing MRI
- parallel imaging
- variational network MRI reconstruction
- MoDL MRI reconstruction
- unrolled MRI reconstruction

---

### Bucket 2: Self-Supervised MRI Reconstruction

Purpose: establish SSDU and related self-supervised reconstruction methods.

Target papers: 12 to 15.

Key terms:

- SSDU MRI reconstruction
- self-supervised MRI reconstruction
- self-supervision via data undersampling
- zero-shot SSDU
- multi-mask SSDU
- robust SSDU

---

### Bucket 3: Uncertainty Quantification in MRI Reconstruction

Purpose: establish what uncertainty MRI reconstruction already does.

Target papers: 10 to 12.

Key terms:

- uncertainty quantification MRI reconstruction
- probabilistic MRI reconstruction
- Bayesian MRI reconstruction
- calibrated uncertainty MRI reconstruction
- epistemic uncertainty MRI reconstruction
- aleatoric uncertainty MRI reconstruction

---

### Bucket 4: Reliability, Hallucination, and Failure Detection

Purpose: support the clinical reliability problem.

Target papers: 8 to 10.

Key terms:

- hallucination MRI reconstruction
- reliability deep learning MRI reconstruction
- reconstruction error detection MRI
- uncertainty error correlation MRI
- trustworthy MRI reconstruction

---

### Bucket 5: Benchmarks and Dataset Papers

Purpose: justify fastMRI and evaluation metrics.

Target papers: 5 to 8.

Key terms:

- fastMRI dataset
- fastMRI brain reconstruction
- accelerated MRI benchmark
- MRI reconstruction metrics NMSE PSNR SSIM

---

### Bucket 6: Recent Current Papers

Purpose: show currency from 2022 to 2026.

Target papers: 15 to 20.

Key terms:

- self-supervised MRI reconstruction 2024
- self-supervised MRI reconstruction 2025
- uncertainty MRI reconstruction 2024
- accelerated MRI reconstruction foundation model
- diffusion MRI reconstruction uncertainty

---

## Search Databases

Primary databases:

- PubMed
- IEEE Xplore
- Google Scholar
- Semantic Scholar

Secondary databases:

- arXiv
- Europe PMC
- journal publisher pages

---

## Inclusion Criteria

Include papers that:

- focus on accelerated MRI reconstruction
- use k-space or physics-guided reconstruction
- discuss self-supervised, unsupervised, or scan-specific learning
- discuss uncertainty, reliability, hallucination, or calibration
- use fastMRI or comparable MRI reconstruction benchmarks
- are relevant to brain MRI or general MRI reconstruction

---

## Exclusion Criteria

Exclude papers that:

- focus only on MRI segmentation or classification
- do not address reconstruction
- do not involve MRI
- are purely clinical imaging studies without reconstruction method relevance
- are not methodologically relevant to the paper

---

## Required Literature Matrix Columns

Each paper should be recorded with:

| Column | Meaning |
|---|---|
| ID | Paper number |
| Citation | Author and year |
| Title | Full paper title |
| Category | Literature bucket |
| Method | Main method used |
| Problem addressed | What problem the paper solves |
| Outcome | Main result or finding |
| Limitation | What it does not solve |
| Relevance to our work | How it supports or challenges our project |
| Use in paper | Introduction, related work, method, gap, discussion |
| Priority | High, medium, or low |

---

## Initial Seed Papers

| Role | Paper |
|---|---|
| Seminal physics-guided reconstruction | Hammernik et al., Variational Network |
| Seminal unrolled reconstruction | Aggarwal et al., MoDL |
| Dataset benchmark | fastMRI dataset paper |
| Core self-supervised method | Yaman et al., SSDU |
| SSDU extension | Multi-mask SSDU |
| Recent SSDU extension | Robust SSDU |
| Uncertainty reconstruction | Edupuganti et al., Uncertainty Quantification in Deep MRI Reconstruction |
| Recent uncertainty | Predictive uncertainty in DL-based MR reconstruction |
| Reliability concern | Hallucination / instability / trustworthy reconstruction papers |

---

## Current Working Novelty Claim

The novelty is not self-supervised MRI reconstruction alone.

The novelty is:

Using held-out k-space residuals not only for self-supervised reconstruction loss, but also as a self-supervised reliability signal for calibrating voxel-wise uncertainty in accelerated brain MRI reconstruction.

---

## Immediate Next Task

Build a 60-paper literature matrix.
