# Verified Bibliographic Details

## Purpose

This document records verified bibliographic details for the core seed papers supporting the manuscript.

These papers define the foundation of the project and will be cited carefully in the Introduction, Related Work, Method, and Dataset sections.

---

## Verified Anchor Papers

| ID | Citation | Full Title | Venue / Source | Year | DOI / Identifier | Role in Manuscript |
|---|---|---|---|---:|---|---|
| V1 | Lustig, Donoho, and Pauly | Sparse MRI: The Application of Compressed Sensing for Rapid MR Imaging | Magnetic Resonance in Medicine | 2007 | 10.1002/mrm.21391 | Establishes compressed sensing MRI as a foundation for accelerated MRI reconstruction |
| V2 | Pruessmann et al. | SENSE: Sensitivity Encoding for Fast MRI | Magnetic Resonance in Medicine | 1999 | 10.1002/(SICI)1522-2594(199911)42:5<952::AID-MRM16>3.0.CO;2-S | Establishes coil-sensitivity-based parallel MRI |
| V3 | Griswold et al. | Generalized Autocalibrating Partially Parallel Acquisitions (GRAPPA) | Magnetic Resonance in Medicine | 2002 | 10.1002/mrm.10171 | Establishes k-space-based parallel MRI reconstruction |
| V4 | Hammernik et al. | Learning a Variational Network for Reconstruction of Accelerated MRI Data | Magnetic Resonance in Medicine | 2018 | 10.1002/mrm.26977 | Establishes physics-guided learned variational reconstruction |
| V5 | Aggarwal, Mani, and Jacob | MoDL: Model-Based Deep Learning Architecture for Inverse Problems | IEEE Transactions on Medical Imaging | 2019 | 10.1109/TMI.2018.2865356 | Establishes model-based deep learning reconstruction with learned regularization and data consistency |
| V6 | Zbontar et al. | fastMRI: An Open Dataset and Benchmarks for Accelerated MRI | arXiv / fastMRI benchmark | 2018 | arXiv:1811.08839 | Justifies use of fastMRI raw k-space benchmark data |
| V7 | Yaman et al. | Self-Supervised Learning of Physics-Guided Reconstruction Neural Networks without Fully-Sampled Reference Data | Magnetic Resonance in Medicine | 2020 | 10.1002/mrm.28378 | Main SSDU seed paper; establishes self-supervised k-space splitting |
| V8 | Sriram et al. | End-to-End Variational Networks for Accelerated MRI Reconstruction | MICCAI | 2020 | 10.1007/978-3-030-59713-9_7 | Establishes strong VarNet-style fastMRI reconstruction baseline |

---

## Why These Papers Matter

These verified anchors define what is already established:

- accelerated MRI as an inverse problem,
- parallel and multicoil MRI reconstruction,
- physics-guided deep reconstruction,
- fastMRI as a benchmark,
- and SSDU-style self-supervised reconstruction.

Therefore, the proposed paper should not claim novelty in those areas.

The contribution should remain focused on:

> using held-out k-space residuals not only for self-supervised reconstruction loss, but also as a reliability signal for calibrating voxel-wise uncertainty.

---

## Next Verification Batch

The next papers to verify should focus on:

- uncertainty quantification in MRI reconstruction,
- hallucination and instability in deep reconstruction,
- robust or multi-mask SSDU variants,
- recent self-supervised MRI reconstruction papers from 2022 onward.
