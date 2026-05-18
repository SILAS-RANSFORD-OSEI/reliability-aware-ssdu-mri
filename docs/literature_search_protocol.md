# Literature Search Protocol

**Project Title:**
*Four-Way Self-Supervised K-Space Partitioning for Residual-Calibrated Reliability Learning in Accelerated Brain MRI*

---

## 1. Purpose of the Literature Search

The purpose of this literature search is to build the scholarly foundation for a Scopus-indexed methods/feasibility paper.

The search will identify literature supporting:

* The problem of reliability in accelerated MRI reconstruction.
* The need for self-supervised MRI reconstruction when fully sampled reference images are unavailable.
* The role of k-space partitioning in SSDU-style methods.
* The gap in independent reliability calibration and evaluation.
* The proposed four-way residual-calibrated reliability framework.

This follows the mentorship structure you were given: problem literature, problem-statement support, gap synthesis, solution literature, and seed-method papers.

---

## 2. Research Questions

* **RQ1: Problem**
Why is reliability estimation needed in accelerated MRI reconstruction, especially when fully sampled reference data are unavailable?
* **RQ2: Method**
How have self-supervised and SSDU-style MRI reconstruction methods used acquired k-space partitioning?
* **RQ3: Outcome**
Can held-out acquired k-space residual energy support residual-calibrated reliability learning and independent reliability evaluation?

---

## 3. Databases

The literature search will use:

* PubMed
* IEEE Xplore
* Semantic Scholar
* Google Scholar
* arXiv
* Scopus-indexed journal websites where accessible

---

## 4. Search Strings

### 4.1 Accelerated MRI Reconstruction

> ("accelerated MRI" OR "undersampled MRI" OR "MRI reconstruction" OR "MR image reconstruction" OR "k-space reconstruction")
> AND
> ("deep learning" OR "neural network" OR "unrolled network" OR "compressed sensing" OR "physics-guided")

### 4.2 Self-Supervised MRI Reconstruction

> ("self-supervised" OR "unsupervised" OR "SSDU" OR "zero-shot")
> AND
> ("MRI reconstruction" OR "accelerated MRI" OR "k-space")

### 4.3 Reliability / Uncertainty in MRI Reconstruction

> ("uncertainty" OR "reliability" OR "calibration" OR "confidence" OR "robustness")
> AND
> ("MRI reconstruction" OR "accelerated MRI" OR "deep learning")

### 4.4 K-Space Residual / Data Consistency

> ("data consistency" OR "k-space residual" OR "measurement consistency" OR "held-out k-space")
> AND
> ("MRI reconstruction" OR "self-supervised MRI")

### 4.5 Clinical Risk / Hallucination / Failure Modes

> ("hallucination" OR "artifact" OR "failure mode" OR "generalization" OR "out-of-distribution")
> AND
> ("deep learning MRI reconstruction" OR "accelerated MRI reconstruction")

---

## 5. Inclusion Criteria

Include papers that:

* Focus on MRI reconstruction.
* Address accelerated or undersampled MRI.
* Use self-supervised, unsupervised, weakly supervised, or physics-guided reconstruction.
* Discuss uncertainty, reliability, robustness, hallucination, calibration, or failure modes.
* Use k-space data, data consistency, or residual-based evaluation.
* Are peer-reviewed papers or technically important preprints.
* Are relevant to medical imaging, inverse problems, or reconstruction reliability.

---

## 6. Exclusion Criteria

Exclude papers that:

* Focus only on classification or segmentation without reconstruction relevance.
* Do not involve MRI or k-space.
* Are unrelated to reliability, uncertainty, robustness, or reconstruction quality.
* Are low-quality non-peer-reviewed sources without technical value.
* Focus only on clinical diagnosis without reconstruction methodology.
* Are not relevant to accelerated MRI, inverse problems, or reliability evaluation.

---

## 7. Literature Categories

### Category A: Problem Literature — 10 Papers

**Purpose:** To support the problem that accelerated MRI reconstruction can produce unreliable outputs and requires reliability estimation.

| Subgroup | Target |
| --- | --- |
| Seminal works | 2 |
| Review papers | 2 |
| Current papers within last 5 years | 5 |
| Organization / dataset / benchmark source | 1 |
| **Total** | **10** |

These papers should support claims such as:

* Accelerated MRI is important for reducing scan time.
* Undersampling causes reconstruction artifacts and inverse-problem instability.
* Deep reconstruction models may produce spatially varying errors.
* Reliability and robustness remain important challenges.

### Category B: Problem Statement Literature — 5 Papers

**Purpose:** To support the exact problem statement of this manuscript.

**Working problem statement:** Deep learning MRI reconstruction can recover images from undersampled k-space, but its outputs may contain spatially varying residual errors or unreliable regions. In self-supervised settings, fully sampled image-domain references are unavailable, making it difficult to train and independently validate spatial reliability maps.

| Category | Target Papers |
| --- | --- |
| Problem statement support | 5 |

These papers should support:

* Lack of fully sampled reference data.
* Limitations of supervised reconstruction evaluation.
* Need for self-supervised reconstruction.
* Need for reliability or uncertainty estimation.

### Category C: Gap Literature — 10 Papers

**Purpose:** To show that existing SSDU/self-supervised approaches do not explicitly separate reconstruction training, reliability calibration, and independent reliability evaluation.

For each gap paper, extract:

* What the paper does.
* What problem it addresses.
* What method it uses.
* What it does not address.
* How the gap supports our four-way framework.

| Category | Target Papers |
| --- | --- |
| Gap synthesis papers | 10 |

**Working gap:** Existing SSDU-style methods split acquired k-space for reconstruction learning, but they do not clearly define separate k-space subsets for reliability calibration and independent reliability evaluation.

### Category D: Solution Literature — 10 Papers

**Purpose:** To support the use of residual consistency, uncertainty estimation, calibration, and held-out measurements for reliability learning.

| Category | Target Papers |
| --- | --- |
| Solution-support papers | 10 |

These papers should support:

* Uncertainty estimation in MRI reconstruction.
* Reliability maps.
* Data consistency as a reliability signal.
* Residual-based evaluation.
* Calibration without fully sampled references.
* Robustness and failure-mode detection.

### Category E: Method / Seed Paper Literature — 5 Papers

**Purpose:** To identify the direct methodological foundation for the proposed method.

**Seed method:** SSDU / self-supervision via data undersampling.

| Category | Target Papers |
| --- | --- |
| Seed and method papers | 5 |

The seed-method logic is:

**SSDU:**


$$\Omega = \Theta \cup \Lambda$$

**Zero-shot or validation SSDU:**


$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{val}}$$

**Proposed method:**


$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

Our method extends k-space partitioning from reconstruction learning toward residual-calibrated reliability learning and independent held-out reliability evaluation.

---

## 8. Target Literature Count

**Minimum target:**

| Literature Group | Target Papers |
| --- | --- |
| Problem literature | 10 |
| Problem statement literature | 5 |
| Gap literature | 10 |
| Solution literature | 10 |
| Method / seed papers | 5 |
| Review / background papers | 10 |
| Current supporting papers | 10 |
| **Total** | **60** |

*Some papers may support more than one category, but the literature matrix should still record the primary role of each paper.*

---

## 9. Literature Matrix Columns

The literature matrix will use the following columns:

| Column | Description |
| --- | --- |
| **ID** | Paper number |
| **Citation** | Author, year, title |
| **Year** | Publication year |
| **Paper type** | Seminal, review, current, method, dataset |
| **Category** | Problem, problem statement, gap, solution, method |
| **Modality** | Brain MRI, knee MRI, general MRI, multicoil MRI |
| **Method** | SSDU, unrolled network, uncertainty, residual, Bayesian, dropout |
| **Dataset** | fastMRI, private MRI dataset, simulation, clinical dataset |
| **Key contribution** | What the paper contributes |
| **Limitation** | What the paper does not solve |
| **Relevance to our work** | How it supports our manuscript |
| **Manuscript section** | Introduction, Related Work, Methods, Discussion |

---

## 10. Working Problem Statement

Accelerated MRI reconstruction aims to recover high-quality images from undersampled k-space. Deep learning methods can improve reconstruction quality, but they may produce spatially varying residual errors or unreliable regions. In many self-supervised settings, fully sampled reference images are unavailable, limiting direct supervised training or validation of reliability maps. Existing SSDU-style methods enable self-supervised reconstruction, but they do not explicitly separate reconstruction training, reliability calibration, and independent reliability evaluation.

---

## 11. Working Gap Statement

Existing self-supervised MRI reconstruction methods use acquired k-space splitting to train reconstruction models without fully sampled reference images. However, most approaches are primarily reconstruction-oriented and do not explicitly assign separate acquired k-space subsets to reconstruction training, reliability calibration, and independent reliability evaluation.

This creates a potential circularity problem when the same held-out k-space evidence is reused for multiple roles. This motivates a four-way k-space partitioning framework for residual-calibrated reliability learning using held-out acquired k-space consistency.

---

## 12. Working Solution Statement

The proposed solution is a four-way self-supervised k-space partitioning framework:

$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

where:

* $\Theta$ provides reconstruction input.
* $\Lambda_{\mathrm{train}}$ supports SSDU reconstruction training.
* $\Lambda_{\mathrm{cal}}$ provides residual-energy targets for reliability learning.
* $\Lambda_{\mathrm{eval}}$ provides independent held-out residual-energy evaluation.

This design enables residual-calibrated reliability learning without fully sampled ground-truth images.

---

## 13. Working Method Statement

The proposed ReliabilityCNN predicts a residual-risk reliability map:

$$R_{\phi} = h_{\phi} ( |x_{\Theta}|, |\hat{x}|, |\nabla|\hat{x}|| )$$

where:

* $|x_{\Theta}|$ is the magnitude image reconstructed from the input subset.
* $|\hat{x}|$ is the magnitude SSDU reconstruction.
* $|\nabla|\hat{x}||$ is the magnitude-gradient map.
* $R_{\phi}$ is the predicted residual-risk reliability map.

The model is trained against calibration residual energy:

$$E_{\Lambda_{\mathrm{cal}}} = \left| F^{-1} M_{\Lambda_{\mathrm{cal}}} (\hat{y}-y) \right|^2$$

and evaluated against independent held-out evaluation residual energy:

$$E_{\Lambda_{\mathrm{eval}}} = \left| F^{-1} M_{\Lambda_{\mathrm{eval}}} (\hat{y}-y) \right|^2$$

---

## 14. Literature Screening Workflow

1. Search databases using the defined strings.
2. Export titles, abstracts, and citations into Zotero.
3. Remove duplicates.
4. Screen titles and abstracts.
5. Classify each paper into one or more categories:
* Problem
* Problem statement
* Gap
* Solution
* Method
* Review
* Dataset / benchmark


6. Read full papers for high-priority references.
7. Fill the literature matrix.
8. Select the final 60 papers.
9. Use the matrix to write the Introduction and Related Work.

---

## 15. Priority Papers to Identify First

The first priority papers are:

* SSDU seed paper.
* Zero-shot SSDU / validation SSDU paper.
* fastMRI dataset / benchmark paper.
* Deep learning MRI reconstruction review.
* Self-supervised MRI reconstruction review or current paper.
* MRI reconstruction uncertainty paper.
* MRI reconstruction robustness or hallucination paper.
* Data-consistency or residual-based MRI reconstruction paper.
* Physics-guided or unrolled MRI reconstruction paper.
* Recent paper on pixel-wise uncertainty or reliability without fully sampled references.

---

## 16. Expected Use of Literature in Manuscript

| Manuscript Section | Literature Needed |
| --- | --- |
| **Introduction** | Problem, clinical motivation, accelerated MRI, reliability need |
| **Related Work** | SSDU, self-supervised reconstruction, uncertainty, residual consistency |
| **Methods** | Seed method, k-space partitioning, residual-energy formulation |
| **Results** | Baseline interpretation, uncertainty comparison |
| **Discussion** | Gap, limitations, future work |
| **Conclusion** | Positioning and contribution |

---

## 17. Next Output

The next file after this protocol will be:
`docs/literature_matrix.md`
or:
`results/literature_matrix.csv`

The literature matrix will contain the selected papers and synthesized relevance to the manuscript.
