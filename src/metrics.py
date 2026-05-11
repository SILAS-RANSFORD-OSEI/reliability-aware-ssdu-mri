"""
Evaluation metrics for MRI reconstruction.

These metrics compare reconstructed images against reference images.
They will be used first for zero-filled reconstruction and later for learned models.
"""

import numpy as np


def nmse(pred, target, eps=1e-12):
    """
    Normalized mean squared error.

    NMSE = ||pred - target||_2^2 / ||target||_2^2
    """
    pred = np.asarray(pred)
    target = np.asarray(target)

    numerator = np.sum(np.abs(pred - target) ** 2)
    denominator = np.sum(np.abs(target) ** 2) + eps

    return numerator / denominator


def psnr(pred, target, max_value=None, eps=1e-12):
    """
    Peak signal-to-noise ratio.

    PSNR = 20 log10(MAX / RMSE)
    """
    pred = np.asarray(pred)
    target = np.asarray(target)

    mse = np.mean(np.abs(pred - target) ** 2)

    if max_value is None:
        max_value = np.max(np.abs(target))

    return 20 * np.log10((max_value + eps) / (np.sqrt(mse) + eps))


def normalize_image(image, eps=1e-12):
    """
    Normalize image magnitude to the range [0, 1].
    """
    image = np.asarray(image)
    image = np.abs(image)

    min_val = np.min(image)
    max_val = np.max(image)

    return (image - min_val) / (max_val - min_val + eps)
