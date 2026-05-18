# Manuscript Outline

## Proposed Title

**Four-Way Self-Supervised K-Space Partitioning for Residual-Calibrated Reliability Learning in Accelerated Brain MRI**

---

## Paper Type

Methods / feasibility study.

---

## Central Claim

This paper proposes a four-way self-supervised k-space partitioning framework for residual-calibrated reliability learning in accelerated brain MRI.

The framework partitions acquired k-space into four disjoint subsets:

$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

where:

* $\Theta$ is used for reconstruction input,
* $\Lambda_{\mathrm{train}}$ is used for self-supervised reconstruction training,
* $\Lambda_{\mathrm{cal}}$ is used for reliability calibration,
* $\Lambda_{\mathrm{eval}}$ is reserved for independent held-out reliability evaluation.

A ReliabilityCNN trained against calibration residual energy modestly improves held-out residual-energy prediction over input intensity in leave-one-volume-out validation and clearly outperforms dropout uncertainty, edge maps, and reconstruction-intensity baselines.

This paper does **not** claim clinical uncertainty calibration or image-domain error prediction. The claim is limited to **residual-calibrated reliability prediction using held-out acquired k-space consistency**.

---

# 1. Abstract

## Structure

1. **Background:** Accelerated MRI reduces scan time but creates a difficult inverse problem because images are reconstructed from undersampled k-space.
2. **Problem:** Deep reconstruction models may produce spatially unreliable outputs, and fully sampled reference images are often unavailable for supervised reliability estimation.
3. **Gap:** Existing self-supervised reconstruction methods such as SSDU enable training without fully sampled targets, but they do not explicitly separate reconstruction training, reliability calibration, and independent reliability evaluation.
4. **Method:** We propose a four-way k-space partitioning framework and a residual-calibrated ReliabilityCNN.
5. **Experiments:** The method is evaluated on five matched fastMRI brain AXT2/R=4 volumes using leave-one-volume-out validation.
6. **Results:** The ReliabilityCNN outperformed input intensity in four out of five held-out volumes and clearly outperformed dropout uncertainty and edge-based baselines.
7. **Conclusion:** Four-way k-space partitioning provides a feasible self-supervised framework for residual-calibrated reliability learning without fully sampled ground truth.

---

# 2. Introduction

## 2.1 Clinical and Engineering Motivation

Accelerated MRI aims to reduce scan time by acquiring fewer k-space samples. This improves patient comfort, reduces motion artifacts, and increases scanner throughput.

However, reducing k-space sampling creates an ill-posed inverse problem. The image must be reconstructed from incomplete Fourier measurements, which can introduce aliasing artifacts, noise amplification, and spatially varying reconstruction errors.

Deep learning reconstruction methods can produce visually plausible images from undersampled k-space. However, visual plausibility alone is not sufficient. A reconstruction method should also indicate where the reconstructed image may be unreliable.

## 2.2 Reliability Problem in Accelerated MRI

In clinical imaging, reconstruction errors can be problematic when they occur near diagnostically important structures.

A model may remove visible aliasing while still producing local errors, suppressing subtle structures, or amplifying residual artifacts. Therefore, accelerated MRI reconstruction requires not only image recovery but also reliability estimation.

A reliability map should answer:

> Where is the reconstruction likely to be inconsistent with the acquired measurement data?

## 2.3 Challenge of Fully Supervised Reliability Estimation

Fully supervised reliability estimation usually requires fully sampled reference images or known image-domain error maps.

In many accelerated MRI settings, fully sampled references are unavailable, expensive, or impractical to acquire. This limits the ability to train voxel-wise reliability predictors using direct ground-truth image errors.

This motivates self-supervised approaches that estimate reliability using only acquired undersampled k-space.

## 2.4 Existing Self-Supervised Reconstruction Methods

Self-supervised methods such as SSDU use acquired k-space splitting to train reconstruction models without fully sampled reference images.

Standard SSDU partitions acquired k-space into:

$$\Omega = \Theta \cup \Lambda$$

where $\Theta$ is used as reconstruction input and $\Lambda$ is used as a self-supervised loss subset.

This is effective for reconstruction training. However, when the goal is reliability estimation, the same hidden k-space evidence should not be reused for multiple roles.

## 2.5 Gap in Current Methods

Existing self-supervised MRI reconstruction pipelines do not explicitly separate:

* reconstruction input,
* reconstruction training loss,
* reliability calibration,
* final independent reliability evaluation.

This creates a circularity risk when the same held-out data are used for reconstruction supervision, reliability tuning, and evaluation.

## 2.6 Proposed Solution

We propose a four-way self-supervised k-space partitioning framework:

$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

This framework separates reconstruction learning from reliability calibration and final reliability evaluation.

The proposed ReliabilityCNN predicts a residual-calibrated reliability map from reconstruction-derived structural features:

$$R_{\phi} = h_{\phi} ( x_{\Theta}, \hat{x}, |\nabla \hat{x}| )$$

where:

* $x_{\Theta}$ is the image reconstructed from the input subset,
* $\hat{x}$ is the SSDU reconstruction,
* $|\nabla \hat{x}|$ is the reconstruction gradient magnitude,
* $R_{\phi}$ is the predicted reliability map.

## 2.7 Contributions

The contributions of this work are:

1. A four-way self-supervised k-space partitioning framework for residual-calibrated reliability learning.
2. A calibration target based on backprojected held-out k-space residual energy.
3. A structural ReliabilityCNN that predicts residual-energy reliability maps from reconstruction-derived features.
4. Leave-one-volume-out validation across five matched fastMRI brain AXT2/R=4 volumes.
5. Baseline comparison against input intensity, mean reconstruction intensity, edge magnitude, and dropout uncertainty.
6. A cautious feasibility analysis showing modest improvement over input intensity and clear improvement over dropout and edge-based baselines.

---

# 3. Related Work

## 3.1 Accelerated MRI Reconstruction

MRI measures data in k-space, the Fourier domain of the image. Accelerated MRI undersamples k-space to reduce scan time.

For a multicoil acquisition, the forward model can be written as:

$$y_{\Omega,c} = M_{\Omega} F(S_c x) + \varepsilon_c$$

where:

* $x \in \mathbb{C}^{H \times W}$ is the unknown complex-valued image,
* $c$ indexes the receiver coil,
* $S_c$ is the coil sensitivity map for coil $c$,
* $F$ is the Fourier transform,
* $M_{\Omega}$ is the undersampling mask over acquired k-space locations,
* $y_{\Omega,c}$ is the acquired k-space for coil $c$,
* $\varepsilon_c$ is measurement noise.

Classical methods include parallel imaging and compressed sensing. Recent methods include CNN-based reconstructions, unrolled networks, and physics-guided deep learning models.

## 3.2 Self-Supervised MRI Reconstruction

Self-supervised MRI reconstruction methods train reconstruction models without fully sampled image targets.

SSDU is a key example. It divides acquired k-space into input and loss subsets, allowing the network to learn from acquired data alone.

However, SSDU is primarily reconstruction-oriented. It does not explicitly define separate subsets for reliability calibration and independent reliability evaluation.

## 3.3 Reliability and Uncertainty in MRI Reconstruction

Reliability and uncertainty estimation are important because deep reconstruction models can produce visually convincing but locally unreliable images.

Existing uncertainty strategies include:

* Monte Carlo dropout,
* Bayesian approximations,
* ensembles,
* data-consistency residuals,
* calibration-based uncertainty methods.

This paper focuses on **residual-calibrated reliability**, not statistical uncertainty calibration.

The predicted map should be interpreted as a map of agreement with held-out acquired k-space residual structure, not as a probabilistic confidence interval or clinical diagnostic certainty map.

## 3.4 Literature Gap

Few methods explicitly separate reconstruction training, reliability calibration, and independent reliability evaluation using only acquired k-space.

This motivates the proposed four-way partitioning framework.

---

# 4. Methods

## 4.1 MRI Forward Model

The full multicoil MRI acquisition model is:

$$y_{\Omega,c} = M_{\Omega}F(S_cx)+\varepsilon_c$$

where:

* $x \in \mathbb{C}^{H \times W}$ is the target image,
* $S_c$ is the sensitivity profile of coil $c$,
* $F$ is the Fourier transform,
* $M_{\Omega}$ is the sampling mask,
* $y_{\Omega,c}$ is the undersampled k-space measurement,
* $\varepsilon_c$ is measurement noise.

In this feasibility study, we use one selected coil as a single-coil-equivalent setting:

$$y_{\Omega} = M_{\Omega}Fx+\varepsilon$$

This simplification isolates the proposed reliability-learning framework before extending to full multicoil sensitivity-encoded reconstruction.

## 4.2 Four-Way K-Space Partitioning

The acquired sampling set $\Omega$ is partitioned into four pairwise disjoint subsets:

$$\Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}$$

with:

$$\Theta \cap \Lambda_{\mathrm{train}} = \Theta \cap \Lambda_{\mathrm{cal}} = \Theta \cap \Lambda_{\mathrm{eval}} = \Lambda_{\mathrm{train}} \cap \Lambda_{\mathrm{cal}} = \Lambda_{\mathrm{train}} \cap \Lambda_{\mathrm{eval}} = \Lambda_{\mathrm{cal}} \cap \Lambda_{\mathrm{eval}} = \emptyset$$

The roles are:

* $\Theta$: reconstruction input and data consistency subset,
* $\Lambda_{\mathrm{train}}$: SSDU reconstruction training subset,
* $\Lambda_{\mathrm{cal}}$: reliability calibration subset,
* $\Lambda_{\mathrm{eval}}$: final independent reliability evaluation subset.

This design avoids using the same k-space samples for both reliability training and final reliability evaluation.

Reference: Figure 1.

## 4.3 SSDU Reconstruction Training

The reconstruction network receives the input subset $y_{\Theta}$ and estimates:

$$\hat{x}_{\theta} = f_{\theta}(y_{\Theta})$$

The predicted k-space is:

$$\hat{y} = F\hat{x}_{\theta}$$

The SSDU reconstruction loss is:

$$\mathcal{L}_{\mathrm{SSDU}} = \left\| M_{\Lambda_{\mathrm{train}}} (\hat{y}-y) \right\|_2^2$$

where $M_{\Lambda_{\mathrm{train}}}$ selects k-space locations assigned to the SSDU training subset.

## 4.4 Calibration Residual Energy

After reconstruction, the calibration residual is:

$$r_{\Lambda_{\mathrm{cal}}} = M_{\Lambda_{\mathrm{cal}}} (\hat{y}-y)$$

The calibration residual is backprojected into image space:

$$E_{\Lambda_{\mathrm{cal}}} = \left| F^{-1} r_{\Lambda_{\mathrm{cal}}} \right|^2$$

This map is used as the residual-calibration target for reliability learning.

## 4.5 Evaluation Residual Energy

The independent evaluation residual is:

$$r_{\Lambda_{\mathrm{eval}}} = M_{\Lambda_{\mathrm{eval}}} (\hat{y}-y)$$

The corresponding evaluation residual energy is:

$$E_{\Lambda_{\mathrm{eval}}} = \left| F^{-1} r_{\Lambda_{\mathrm{eval}}} \right|^2$$

This map is never used for reconstruction training or reliability calibration. It is reserved for final evaluation.

## 4.6 ReliabilityCNN

The ReliabilityCNN receives a three-channel feature stack:

$$z = [ x_{\Theta}, \hat{x}, |\nabla \hat{x}| ]$$

where:

* $x_{\Theta}$ is the input reconstruction from $\Theta$,
* $\hat{x}$ is the SSDU reconstruction,
* $|\nabla \hat{x}|$ is the reconstruction gradient magnitude.

The tensor shape is:

$$z \in \mathbb{R}^{1 \times 3 \times 768 \times 396}$$

where:

* $1$ is the batch size,
* $3$ is the number of input channels,
* $768$ is image height,
* $396$ is image width.

The network predicts:

$$R_{\phi} = h_{\phi}(z)$$

with:

$$R_{\phi} \in \mathbb{R}^{1 \times 1 \times 768 \times 396}$$

The reliability training loss is:

$$\mathcal{L}_{\mathrm{rel}} = \left\| \mathrm{norm}(R_{\phi}) - \mathrm{norm}(E_{\Lambda_{\mathrm{cal}}}) \right\|_2^2$$

where $\mathrm{norm}(\cdot)$ denotes min-max normalization.

Reference: Figure 2.

## 4.7 Baseline Reliability Maps

The proposed ReliabilityCNN is compared with:

* input intensity,
* mean reconstruction intensity,
* edge magnitude,
* dropout uncertainty.

Monte Carlo dropout is used only as a baseline and not as the central method.

## 4.8 Alignment Metric

Reliability quality is evaluated by map alignment:

$$\rho(R, E_{\Lambda_{\mathrm{eval}}})$$

where:

* $R$ is a candidate reliability map,
* $E_{\Lambda_{\mathrm{eval}}}$ is the held-out evaluation residual energy,
* $\rho$ is a correlation-based alignment metric.

---

# 5. Experiments

## 5.1 Dataset

The experiments use fastMRI brain multicoil data.

The feasibility subset is restricted to:

* acquisition: AXT2,
* acceleration: R = 4,
* k-space shape: $16 \times 16 \times 768 \times 396$,
* mask shape: $396$,
* five matched volumes,
* one selected coil.

The selected-coil setup is used to isolate the residual-calibrated reliability-learning framework.

## 5.2 Experiment Progression

| Experiment | Purpose | Main Finding |
| --- | --- | --- |
| 017 | Four-way split verification | Confirmed disjoint partitioning |
| 018 | Four-way reliability evaluation | Independent reliability signal survived |
| 024 | Per-slice ReliabilityCNN | Beat dropout and edge, but not input intensity |
| 025 | Cross-slice ReliabilityCNN | Beat input intensity within one volume |
| 026 | Dropout channel test | Dropout channel degraded performance |
| 027 | One-volume cross-volume test | Partial transfer only |
| 028 | Multi-volume training | Reached input-intensity parity |
| 029 | Leave-one-volume-out validation | Beat input intensity in 4/5 held-out volumes |

## 5.3 Leave-One-Volume-Out Validation

Experiment 029 uses five-fold leave-one-volume-out validation:

$$4 \text{ volumes train} \rightarrow 1 \text{ volume test}$$

Each fold uses:

* 64 training slices,
* 16 held-out test slices.

Because only five volumes are used, results are interpreted as observed feasibility trends rather than claims of statistical significance.

---

# 6. Results

## 6.1 Main Leave-One-Volume-Out Result

Across five held-out volumes:

| Method | Mean Alignment |
| --- | --- |
| ReliabilityCNN | 0.5713 |
| Input intensity | 0.5580 |
| Dropout uncertainty | 0.4900 |
| Mean reconstruction intensity | 0.4980 |
| Edge map | 0.4005 |

Mean margins:

$$R_{\mathrm{net}} - I_{\mathrm{input}} = +0.0132$$

$$R_{\mathrm{net}} - U_{\mathrm{dropout}} = +0.0813$$

$$R_{\mathrm{net}} - E_{\mathrm{edge}} = +0.1708$$

Reference: Figures 3 and 4.

## 6.2 Full Leave-One-Volume-Out Fold Table

| Fold | Held-Out Volume | ReliabilityCNN | Input Intensity | Margin |
| --- | --- | --- | --- | --- |
| 1 | file_brain_AXT2_200_6002495.h5 | 0.5657 | 0.5529 | +0.0128 |
| 2 | file_brain_AXT2_200_6002623.h5 | 0.5733 | 0.5546 | +0.0187 |
| 3 | file_brain_AXT2_200_6002398.h5 | 0.5449 | 0.5364 | +0.0085 |
| 4 | file_brain_AXT2_200_2000341.h5 | 0.5916 | 0.5641 | +0.0275 |
| 5 | file_brain_AXT2_200_2000271.h5 | 0.5808 | 0.5821 | -0.0013 |

The ReliabilityCNN outperformed input intensity in four out of five held-out volumes.

Because of the small number of volumes, this is reported as a modest observed improvement rather than a statistically significant improvement.

## 6.3 Representative Visual Example

For Fold 4, Volume V4, Slice 15:

| Map | Alignment With Held-Out Eval Residual |
| --- | --- |
| ReliabilityCNN | 0.5749 |
| Input intensity | 0.4595 |
| Mean reconstruction | 0.4553 |
| Dropout uncertainty | 0.3617 |
| Edge map | 0.2614 |

Reference: Figure 5.

---

# 7. Discussion

## 7.1 Main Finding

The proposed four-way SSDU framework enables residual-calibrated reliability learning without fully sampled ground truth.

In leave-one-volume-out validation, the ReliabilityCNN showed modest improvement over input intensity and clear improvement over dropout uncertainty and edge-based baselines.

## 7.2 Why Four-Way Partitioning Matters

The four-way partition separates:

* reconstruction input,
* reconstruction training,
* reliability calibration,
* independent reliability evaluation.

This makes the reliability evaluation less circular than standard two-way SSDU-style partitioning.

## 7.3 Interpretation of the ReliabilityCNN

The ReliabilityCNN learns a structural residual-reliability map from input intensity, reconstruction intensity, and edge information.

The improvement over input intensity is modest, which indicates that anatomical intensity structure is already a strong predictor of held-out residual energy.

However, the learned ReliabilityCNN improves over intensity in most held-out volumes and clearly outperforms dropout uncertainty and edge maps.

## 7.4 Interpretation of Residual Energy

The held-out residual energy is a physics-derived consistency signal from acquired k-space.

It should not be interpreted as:

* lesion probability,
* diagnostic uncertainty,
* fully sampled image-domain error,
* calibrated probabilistic confidence.

It is a self-supervised residual-consistency target.

## 7.5 Statistical Caution

The current study uses five matched volumes. Therefore, results should be interpreted as preliminary feasibility evidence.

The paper should use language such as:

* observed improvement,
* modest improvement,
* feasibility evidence,
* held-out residual-energy prediction.

The paper should avoid language such as:

* statistically significant superiority,
* clinically validated uncertainty,
* robust scanner-general reliability.

---

# 8. Limitations

Current limitations include:

* five volumes only,
* one selected coil,
* single-coil-equivalent implementation,
* one acquisition type,
* one acceleration factor,
* no fully sampled image-domain reference error,
* no multicoil sensitivity-encoded reconstruction,
* no external scanner or protocol validation,
* no radiologist reader study.

These limitations mean the work should be framed as a feasibility/methods study rather than a clinical validation paper.

---

# 9. Conclusion

This work proposes a four-way self-supervised k-space partitioning framework for residual-calibrated reliability learning in accelerated brain MRI.

The framework separates reconstruction input, reconstruction training, reliability calibration, and independent reliability evaluation.

In leave-one-volume-out validation across five matched AXT2/R=4 fastMRI brain volumes, the proposed ReliabilityCNN modestly improved held-out residual-energy prediction over input intensity and clearly outperformed dropout uncertainty and edge-based baselines.

The method is best interpreted as a self-supervised feasibility framework for residual-calibrated reliability learning without fully sampled reference images.

---

# 10. Target Journal Positioning

This work is suitable as:

* a Scopus-indexed methods paper,
* a biomedical signal or image processing paper,
* a medical imaging engineering feasibility paper.

It is not yet suitable as:

* a full clinical validation paper,
* an IEEE TMI-level benchmark paper,
* a clinically calibrated uncertainty paper.

Potential journal directions include:

* Magnetic Resonance Imaging,
* Biomedical Signal Processing and Control,
* Computerized Medical Imaging and Graphics,
* Computers in Biology and Medicine.
