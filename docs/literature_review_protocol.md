# Literature Review Protocol

## Working Topic

Reliability-aware self-supervised k-space MRI reconstruction with calibrated uncertainty for accelerated brain MRI.

---

## Purpose

This document defines the literature-review strategy for a Scopus/IEEE-targeted manuscript.

The goal is not to collect papers randomly. The goal is to build a defensible argument for the paper's novelty, method, gap, and evaluation strategy.

---

## Core Position

This study does not claim to introduce:

- physics-guided MRI reconstruction,
- self-supervised MRI reconstruction,
- uncertainty estimation in MRI reconstruction,
- or fastMRI benchmarking.

These are already established.

The proposed contribution is:

> using held-out k-space residuals not only for self-supervised reconstruction loss, but also as a reliability signal for calibrating voxel-wise uncertainty in accelerated brain MRI reconstruction.

---

## Research Questions

### RQ1: Method

What self-supervised or unsupervised MRI reconstruction methods exist for training without fully sampled ground-truth references?

### RQ2: Reliability

How have uncertainty, hallucination risk, instability, and failure detection been studied in deep MRI reconstruction?

### RQ3: Gap

What remains unresolved at the intersection of SSDU-style reconstruction and calibrated spatial uncertainty estimation?

---

## Literature Categories

| Category | Purpose |
|---|---|
| Seminal accelerated MRI | Establish MRI as an inverse problem under undersampled k-space |
| Parallel and multicoil MRI | Support coil-sensitivity and multicoil forward-model discussion |
| Physics-guided deep reconstruction | Establish VarNet, MoDL, and unrolled reconstruction background |
| Self-supervised MRI reconstruction | Establish SSDU and related methods |
| Uncertainty MRI reconstruction | Establish existing uncertainty methods |
| Reliability and instability | Support the clinical safety problem |
| Dataset and benchmark papers | Justify fastMRI and metrics |
| Recent papers from 2022 onward | Demonstrate currency |

---

## Inclusion Criteria

Include papers that:

- focus on MRI reconstruction,
- use k-space, Fourier-domain, or physics-guided reconstruction,
- address accelerated MRI,
- use self-supervised, unsupervised, or scan-specific learning,
- discuss uncertainty, calibration, reliability, hallucination, or instability,
- use fastMRI or comparable public MRI reconstruction benchmarks,
- are peer-reviewed or highly influential preprints with strong relevance.

---

## Exclusion Criteria

Exclude papers that:

- focus only on classification or segmentation,
- do not address reconstruction,
- are unrelated to MRI,
- are only clinical imaging studies without reconstruction methodology,
- are weakly related review citations used only for padding.

---

## Evidence Rules

A paper should not be included unless it has a clear role:

| Role | Meaning |
|---|---|
| Problem | Supports why accelerated MRI reconstruction needs reliability |
| Method | Supports SSDU, unrolled networks, uncertainty, or calibration |
| Gap | Shows what existing work does not solve |
| Dataset | Justifies fastMRI or evaluation protocol |
| Comparison | Provides a method to compare against |
| Discussion | Supports limitations, clinical risk, or future work |

---

## Matrix Columns

The final literature matrix must contain:

| Column | Description |
|---|---|
| ID | Paper number |
| Citation | Author and year |
| Title | Full title |
| Venue | Journal/conference/preprint |
| Year | Publication year |
| Category | Literature category |
| Method | Main method |
| Problem addressed | What the paper solves |
| Main finding | Key result |
| Limitation | What remains unsolved |
| Relevance to our work | Why this paper matters |
| Manuscript section | Introduction, Related Work, Method, Experiments, Discussion |
| Priority | High, Medium, Low |
| Verification status | Verified or To verify |

---

## Required Paper Distribution

Minimum target: 60 papers.

| Group | Target Count |
|---|---:|
| Seminal accelerated MRI and parallel imaging | 6 |
| Physics-guided/unrolled deep reconstruction | 8 |
| Self-supervised MRI reconstruction | 12 |
| Uncertainty MRI reconstruction | 10 |
| Reliability, hallucination, and instability | 8 |
| fastMRI/datasets/benchmarks/evaluation | 6 |
| Recent papers from 2022 onward | 10 |

---

## Search Databases

Use:

- PubMed
- IEEE Xplore
- Google Scholar
- Semantic Scholar
- arXiv
- Publisher pages

Priority should be given to peer-reviewed journal and conference papers.

---

## Search Strings

### Self-supervised MRI reconstruction

("MRI reconstruction" OR "accelerated MRI" OR "k-space reconstruction")
AND
("self-supervised" OR "unsupervised" OR "SSDU" OR "zero-shot")
AND
("deep learning" OR "physics-guided" OR "unrolled")

### Uncertainty MRI reconstruction

("MRI reconstruction" OR "accelerated MRI")
AND
("uncertainty" OR "Bayesian" OR "probabilistic" OR "calibration")
AND
("deep learning" OR "neural network")

### Reliability and hallucination

("MRI reconstruction" OR "image reconstruction")
AND
("hallucination" OR "instability" OR "reliability" OR "trustworthy")
AND
("deep learning" OR "AI")

### fastMRI benchmark

("fastMRI" OR "MRI reconstruction benchmark")
AND
("k-space" OR "brain MRI" OR "accelerated MRI")

---

## Working Thesis Statement

This study proposes a reliability-aware self-supervised MRI reconstruction framework that extends SSDU-style held-out k-space consistency from a reconstruction-only loss into a calibration signal for voxel-wise uncertainty estimation, enabling accelerated brain MRI reconstructions to be accompanied by spatial reliability information.

---

## Immediate Next Task

Create a verified seed-paper matrix before expanding to the full 60-paper matrix.
