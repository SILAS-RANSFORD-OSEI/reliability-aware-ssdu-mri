# Verified Seed Papers

## Working Topic

Reliability-aware self-supervised k-space MRI reconstruction with calibrated uncertainty for accelerated brain MRI.

---

## Seed Paper Matrix

| ID | Citation | Role | What It Establishes | Limitation Relevant to Our Work | How We Use It |
|---|---|---|---|---|---|
| S1 | Lustig et al., 2007 | Seminal accelerated MRI | Compressed sensing MRI showed that sparse reconstruction can recover images from undersampled k-space | Classical iterative method; not deep learning or uncertainty-aware | Background for accelerated MRI as an inverse problem |
| S2 | Pruessmann et al., 1999 | Seminal parallel MRI | SENSE established coil-sensitivity-based multicoil reconstruction | Requires coil sensitivity modeling; not self-supervised uncertainty calibration | Supports multicoil forward-model discussion |
| S3 | Griswold et al., 2002 | Seminal parallel MRI | GRAPPA established k-space-based parallel MRI reconstruction | Classical interpolation method; no learned reliability map | Background for multicoil MRI reconstruction |
| S4 | Hammernik et al., 2018 | Physics-guided deep reconstruction | Variational Networks established learned physics-guided MRI reconstruction | Mainly reconstruction-focused; not SSDU uncertainty calibration | Shows physics-guided reconstruction already exists |
| S5 | Aggarwal et al., 2019 | Model-based deep learning | MoDL established model-based deep learning for MRI inverse problems | Typically reference/supervised setting; not reliability-calibrated SSDU | Supports unrolled/model-based reconstruction background |
| S6 | Sriram et al., 2020 | fastMRI reconstruction baseline | End-to-end VarNet became a strong fastMRI reconstruction baseline | Supervised benchmark model; not self-supervised uncertainty calibration | Baseline/comparison background |
| S7 | Zbontar et al., 2018 | Benchmark dataset | fastMRI introduced large-scale raw k-space data for ML reconstruction | Dataset/benchmark paper, not a reliability method | Justifies fastMRI dataset use |
| S8 | Knoll et al., 2020 | Dataset resource | fastMRI provides publicly available raw k-space and DICOM data for accelerated MRI research | Mostly dataset description | Supports dataset credibility |
| S9 | Yaman et al., 2020 | Core SSDU seed paper | SSDU trains physics-guided MRI reconstruction without fully sampled reference data by splitting acquired measurements | Focuses on reconstruction quality, not calibrated voxel-wise uncertainty | Main method seed paper |
| S10 | Yaman et al., 2022 | SSDU extension | Multi-mask SSDU improves data use in self-supervised physics-guided reconstruction | Still not primarily uncertainty-calibrated reliability mapping | Supports active SSDU extension literature |
| S11 | Yaman et al., 2021 | Zero-shot SSDU | ZS-SSDU enables scan-specific self-supervised reconstruction | Focuses on scan-specific reconstruction and generalization, not uncertainty calibration | Supports self-supervised extension background |
| S12 | Edupuganti et al., 2021 | Uncertainty MRI reconstruction | Demonstrates uncertainty quantification in deep MRI reconstruction | Not specifically calibrated using SSDU held-out residuals | Supports uncertainty motivation |
| S13 | Antun et al., 2020 | Reliability / instability | Shows deep learning image reconstruction can be unstable and clinically risky | Problem-focused; not an SSDU uncertainty method | Supports problem statement and reliability motivation |
| S14 | Zeng et al., 2021 | Review | Reviews DL MRI reconstruction without fully sampled data | Review paper; not a new method | Helps frame self-supervised reconstruction literature |
| S15 | Heckel et al., 2024 | Review / current literature | Reviews recent deep learning MRI reconstruction, robustness, and acceleration | Review paper; not our specific method | Supports currency and broad positioning |

---

## Initial Gap Derived from Seed Papers

The seed literature shows that:

1. Accelerated MRI reconstruction is a well-established inverse problem.
2. Physics-guided deep reconstruction is already established.
3. SSDU-style self-supervised reconstruction already exists.
4. Uncertainty quantification in MRI reconstruction already exists.
5. Reliability and instability concerns in deep reconstruction are real.

Therefore, the gap is not any single one of these topics.

The gap is the intersection:

> self-supervised k-space reconstruction plus calibrated voxel-wise uncertainty using held-out k-space residuals as a reliability signal.

---

## Working Novelty Claim

This project extends SSDU-style reconstruction by using held-out k-space residuals not only as a self-supervised reconstruction loss, but also as a self-supervised signal for calibrating spatial uncertainty and identifying unreliable reconstructed regions.

---

## Next Literature Task

Expand this seed set into a full 60-paper matrix organized into:

- problem-supporting literature,
- method-supporting literature,
- gap-supporting literature,
- solution-supporting literature,
- evaluation-supporting literature,
- and recent current work from 2022 onward.
