# Discussion Draft

## 1. Principal Findings

This study proposed a four-way self-supervised k-space partitioning framework for residual-calibrated reliability learning in accelerated brain MRI.

The central methodological idea was to partition acquired k-space into four disjoint subsets:

$$ \Omega = \Theta \cup \Lambda_{\mathrm{train}} \cup \Lambda_{\mathrm{cal}} \cup \Lambda_{\mathrm{eval}}. $$

This allowed reconstruction input, reconstruction training, reliability calibration, and independent reliability evaluation to be separated.

The main empirical finding was that the proposed ReliabilityCNN achieved slightly higher held-out residual-energy alignment than input intensity in leave-one-volume-out validation:

$$ R_{\mathrm{net}} = 0.5713, $$

compared with:

$$ I_{\mathrm{input}} = 0.5580. $$

The mean margin over input intensity was modest:

$$ R_{\mathrm{net}} - I_{\mathrm{input}} = +0.0133. $$

However, the ReliabilityCNN exceeded input intensity in four of five held-out volumes and clearly outperformed dropout uncertainty, edge magnitude, and mean reconstruction intensity.

These results support the feasibility of residual-calibrated reliability learning using held-out acquired k-space consistency.

---

## 2. Why Four-Way Partitioning Matters

Standard self-supervised MRI reconstruction methods such as SSDU split acquired k-space into input and loss subsets. This is effective for reconstruction learning, but reliability estimation requires an additional separation between calibration and final evaluation.

The four-way partition addresses this issue by assigning different acquired k-space samples to different roles:

* $\Theta$: reconstruction input,
* $\Lambda_{\mathrm{train}}$: reconstruction training loss,
* $\Lambda_{\mathrm{cal}}$: reliability calibration,
* $\Lambda_{\mathrm{eval}}$: independent reliability evaluation.

This separation reduces circularity. In particular, the reliability map is trained using residual energy from $\Lambda_{\mathrm{cal}}$ but evaluated using residual energy from $\Lambda_{\mathrm{eval}}$.

Therefore, the model is not evaluated on the same residual evidence used to train the reliability predictor.

This is the main methodological contribution of the work.

---

## 3. Interpretation of the ReliabilityCNN

The ReliabilityCNN was intentionally lightweight. Its value does not come from architectural complexity, but from the residual-calibrated learning setup.

The model receives magnitude-domain structural features:

$$ z = [ |x_{\Theta}|, |\hat{x}|, |\nabla |\hat{x}|| ]. $$

These features encode:

1. the information available from the input subset,
2. the reconstructed image structure,
3. local anatomical gradients.

The output,

$$ R_{\phi}, $$

is best interpreted as a residual-risk reliability map. Larger values indicate regions predicted to have higher held-out residual energy.

The model does not estimate clinical diagnostic uncertainty, lesion probability, or true image-domain reconstruction error.

---

## 4. Why Input Intensity Is a Strong Baseline

Input intensity was the strongest competing baseline.

This is physically expected. Residual-energy magnitude is partly coupled to anatomical signal magnitude. Regions with higher signal can naturally contribute larger k-space residual-energy structure because Fourier-domain discrepancies backproject according to image energy and spatial structure.

Therefore, a simple input-intensity map can already align with held-out residual-energy patterns.

The fact that the ReliabilityCNN only modestly improved over input intensity shows that the task is difficult and that raw anatomical signal structure is a strong predictor of residual-risk patterns.

However, the ReliabilityCNN improved over input intensity in four of five held-out volumes. This suggests that combining input intensity, reconstruction intensity, and edge information provides additional predictive value beyond any single structural baseline.

---

## 5. Why Dropout Uncertainty Was Weaker

Monte Carlo dropout uncertainty performed worse than the ReliabilityCNN and input intensity.

This suggests that stochastic variance from the dropout reconstruction model did not strongly correspond to held-out k-space residual-energy structure in this feasibility setting.

There are several possible reasons.

First, dropout variance reflects model stochasticity, not necessarily measurement inconsistency.

Second, the reconstruction model was lightweight and trained under limited data conditions, so dropout variance may not capture meaningful posterior uncertainty.

Third, uncertainty derived from image-domain stochastic variation may not align directly with residual energy derived from held-out Fourier measurements.

Thus, the results suggest that residual-calibrated reliability learning may provide a more direct self-supervised signal than dropout variance alone.

---

## 6. Interpretation of Residual-Energy Maps

The calibration and evaluation targets were derived from held-out k-space residuals:

$$ E_{\Lambda} = \left| F^{-1} M_{\Lambda} (\hat{y}-y) \right|^2. $$

These maps are not ground-truth image error maps.

Because Fourier residuals are globally backprojected into image space, residual-energy maps should be interpreted as image-domain residual-consistency proxies. They indicate where held-out acquired k-space measurements imply reconstruction inconsistency.

This distinction is important. A high residual-risk value does not necessarily mean a lesion, a clinically meaningful artifact, or a diagnostic failure. It means that the reconstruction is less consistent with held-out measured k-space evidence in that spatial pattern.

---

## 7. Clinical Relevance and Caution

The proposed method is clinically motivated because accelerated MRI reconstruction can produce spatially varying errors, and radiologists need to understand where reconstructed images may be less reliable.

However, the present study does not establish clinical reliability.

The current reliability maps are residual-consistency maps, not clinically validated uncertainty maps.

Therefore, the correct clinical interpretation is cautious:

> The method provides a self-supervised residual-risk signal that may help identify regions where reconstruction consistency with held-out k-space is weaker.

It does not yet support claims about diagnostic confidence, lesion detection reliability, or clinical decision support.

---

## 8. Limitations

This study has several important limitations.

First, only five matched fastMRI brain AXT2/R=4 volumes were used. This is sufficient for feasibility testing but not for definitive validation.

Second, the experiments used one selected coil in a single-coil-equivalent setup. Full multicoil sensitivity-encoded reconstruction was not implemented.

Third, only one acquisition type and one acceleration factor were evaluated. Therefore, protocol generalization was not tested.

Fourth, no fully sampled image-domain reference was used. As a result, the method cannot claim prediction of true image-domain reconstruction error.

Fifth, evaluation relied on Pearson correlation with held-out residual-energy maps. This measures spatial alignment, not probabilistic calibration or clinical validity.

Sixth, no radiologist reader study was performed.

These limitations mean the work should be interpreted as a methods/feasibility study rather than a clinical validation study.

---

## 9. Future Work

Future work should extend the framework in several directions.

First, the method should be evaluated with full multicoil reconstruction using coil sensitivity maps:

$$ y_{\Omega,c} = M_{\Omega}F(S_cx)+\varepsilon_c. $$

Second, validation should include more volumes, multiple acquisition types, and multiple acceleration factors.

Third, the relationship between residual-energy reliability maps and fully sampled image-domain error should be studied when reference data are available.

Fourth, alternative reliability models could be explored, including U-Net-based predictors, unrolled reliability modules, and uncertainty-aware residual predictors.

Fifth, clinical reader studies are needed to determine whether residual-risk maps are useful for interpreting accelerated MRI reconstructions.

---

## 10. Overall Interpretation

The results support the feasibility of four-way self-supervised residual reliability learning.

The improvement over input intensity was modest, so the method should not be framed as a dominant reliability predictor.

However, the framework is methodologically useful because it separates reconstruction training, reliability calibration, and independent reliability evaluation using only acquired k-space samples.

The strongest claim supported by the present study is:

> Four-way self-supervised k-space partitioning enables residual-calibrated reliability learning in accelerated brain MRI, with leave-one-volume-out feasibility results showing modest improvement over input intensity and clearer improvement over dropout, edge, and reconstruction-intensity baselines.

This framing is appropriate for a Scopus-indexed methods/feasibility manuscript.
