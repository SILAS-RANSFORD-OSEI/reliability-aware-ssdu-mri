# Experiment 001 Results: Synthetic Zero-Filled Reconstruction

## Test Type

Synthetic MRI-style reconstruction test.

## Purpose

The purpose of this test was to verify the basic MRI reconstruction pipeline before using real MRI data.

The tested pipeline was:

image -> FFT -> k-space -> undersampling mask -> undersampled k-space -> inverse FFT -> zero-filled reconstruction

## Setup

- Image size: 128 x 128
- Synthetic object: rectangular phantom
- Acceleration factor: R = 4
- Sampling rate: 0.25
- Center fraction: 0.08
- Random seed: 42

## Results

| Quantity | Value |
|---|---:|
| FFT/IFFT max reconstruction error | 3.1764347e-07 |
| Sampling rate | 0.25 |
| Zero-filled NMSE | 0.06380156 |
| Zero-filled PSNR | 22.334974 dB |

## Interpretation

The FFT followed by inverse FFT recovered the original image with very small numerical error. This confirms that the centered Fourier transform utilities are working correctly.

The Cartesian undersampling mask achieved the expected sampling rate of 0.25, corresponding to acceleration factor R = 4.

The zero-filled reconstruction produced visible aliasing artifacts, as expected from undersampled Cartesian k-space. The NMSE and PSNR values provide the first quantitative baseline.

## Conclusion

The basic MRI physics pipeline is functioning correctly on synthetic data.

The next step is to test the same pipeline on real fastMRI brain k-space data.
