# Experiment 002: Real fastMRI Brain Zero-Filled Reconstruction

## Table of Contents

- [Objective](#objective)
- [Dataset](#dataset)
- [File Structure](#file-structure)
- [Reconstruction Method](#reconstruction-method)
- [Output](#output)
- [Observations](#observations)
- [Important Note](#important-note)
- [Interpretation](#interpretation)
- [Conclusion](#conclusion)

---

## Objective

Test the zero-filled reconstruction pipeline on **real fastMRI brain multicoil k-space data**.

---

## Dataset

| Property | Value |
|----------|-------|
| Dataset | fastMRI Brain |
| Data type | Multicoil |
| Split | Test |
| File | `file_brain_AXT1_206_2120004.h5` |
| Acquisition | AXT1 |
| Acceleration | $R = 4$ |

---

## File Structure

The selected HDF5 file contained the following keys:

| Key | Description |
|-----|-------------|
| `kspace` | Complex-valued multicoil k-space data |
| `mask` | Sampling mask |
| `ismrmrd_header` | MRI acquisition metadata |

**K-space tensor shape:**

$$16 \times 20 \times 640 \times 320$$

| Dimension | Size |
|-----------|------|
| Slices | 16 |
| Coils | 20 |
| Height | 640 |
| Width | 320 |

**Mask shape:** $320$ — matching the last k-space dimension, confirming that undersampling was applied along the **phase-encoding direction**.

---

## Reconstruction Method

One central slice was selected at index $8$, with shape $20 \times 640 \times 320$ (20 coils, height 640, width 320).

**Per-coil reconstruction** via centered inverse Fourier transform:

$$x_c = \mathcal{F}^{-1}(y_c)$$

| Term | Description |
|------|-------------|
| $y_c$ | K-space data from coil $c$ |
| $x_c$ | Reconstructed image from coil $c$ |
| $\mathcal{F}^{-1}$ | Inverse Fourier transform |

**Coil combination** via root-sum-of-squares (RSS):

$$x_{\mathrm{RSS}} = \sqrt{\sum_{c=1}^{C} |x_c|^2}$$

| Term | Description |
|------|-------------|
| $C = 20$ | Number of receiver coils |
| $x_c$ | Reconstructed image from coil $c$ |
| $x_{\mathrm{RSS}}$ | Final coil-combined magnitude image |

---

## Output

The reconstructed zero-filled image shape was $640 \times 320$.

**Raw intensity range:**

| Quantity | Value |
|----------|------:|
| Minimum intensity | `3.6329302e-06` |
| Maximum intensity | `0.00072155934` |

The image was normalised to $[0, 1]$ for visualisation. A central crop was also generated to show the brain region more clearly.

---

## Observations

- The reconstruction produced a visible axial brain MRI slice
- The full image contained a large background region — cropping improved visual inspection
- The image showed expected zero-filled behavior, consistent with test data already accelerated at $R = 4$

---

## Important Note

> This test file does **not** contain a fully sampled reference reconstruction.
> Quantitative metrics (NMSE, PSNR, SSIM) were therefore **not computed** for this experiment.

This experiment only verifies that the pipeline can load real fastMRI brain k-space data and produce a valid zero-filled multicoil image.

---

## Interpretation

The pipeline successfully completed the following steps:

| Step | Action |
|------|--------|
| 1 | Loading real fastMRI brain HDF5 data |
| 2 | Inspecting k-space dimensions |
| 3 | Selecting one central slice |
| 4 | Centered inverse Fourier reconstruction per coil |
| 5 | Root-sum-of-squares coil combination |
| 6 | Normalisation and visualisation |

This confirms that the basic MRI reconstruction code works correctly on real multicoil brain MRI data.

---

## Conclusion

The basic reconstruction pipeline is verified on real fastMRI brain multicoil k-space data.

**Planned extensions toward the self-supervised reliability-aware method:**

| Stage | Extension |
|-------|-----------|
| 1 | SSDU-style k-space splitting |
| 2 | Held-out k-space consistency loss |
| 3 | Stochastic reconstruction |
| 4 | Voxel-wise uncertainty estimation |
| 5 | Uncertainty calibration using held-out k-space residuals |
