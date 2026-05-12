# Data Status

## Current Dataset

The project currently uses:

- Dataset: fastMRI Brain
- Data type: Multicoil
- Split: Test
- Batch: brain_multicoil_test_batch_0
- Number of extracted HDF5 files: 186

## Available File Contents

The current test files contain:

| Key | Status | Role |
|---|---|---|
| kspace | Available | Raw multicoil k-space data |
| mask | Available | Sampling mask |
| ismrmrd_header | Available | MRI acquisition metadata |

## Missing Reference Data

The current test files do not contain:

- reconstruction_rss
- reconstruction_esc
- target
- fully sampled reference image

Therefore, the current test batch cannot be used for quantitative evaluation with:

- NMSE
- PSNR
- SSIM
- uncertainty-error correlation

## Current Usefulness

The current test batch is useful for:

- Loading real fastMRI brain k-space
- Inspecting HDF5 structure
- Testing multicoil inverse FFT reconstruction
- Testing root-sum-of-squares coil combination
- Visualizing zero-filled accelerated brain MRI reconstructions
- Building the initial qualitative reconstruction pipeline

## Limitation

Because there is no fully sampled reference image, this dataset batch is not enough for final paper evaluation.

Training can be self-supervised, but evaluation still requires reference data to prove whether the uncertainty map corresponds to actual reconstruction error.

## Next Data Requirement

For quantitative paper experiments, the project needs fastMRI brain data with reference reconstructions.

Possible next datasets:

- brain_multicoil_val_batch_0
- brain_multicoil_train_batch_0

The validation or training data are much larger, so the next step should be planned carefully to avoid storage and Colab disk issues.

## Current Data Conclusion

The current test data are sufficient for qualitative reconstruction pipeline development.

They are not sufficient for final quantitative evaluation.
