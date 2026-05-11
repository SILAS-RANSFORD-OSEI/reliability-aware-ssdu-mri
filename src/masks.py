"""
Undersampling mask utilities for MRI reconstruction.

This module creates simple Cartesian undersampling masks and applies them to k-space data.
"""

import numpy as np


def cartesian_mask(shape, acceleration=4, center_fraction=0.08, seed=None):
    """
    Create a 1D Cartesian undersampling mask along the phase-encoding direction.

    Parameters
    ----------
    shape : tuple
        Shape of the k-space data. The last two dimensions are assumed to be height and width.

    acceleration : int
        Acceleration factor. Example: acceleration=4 keeps roughly 1/4 of phase-encoding lines.

    center_fraction : float
        Fraction of low-frequency central k-space lines to always keep.

    seed : int or None
        Random seed for reproducibility.

    Returns
    -------
    mask : np.ndarray
        Undersampling mask broadcastable to the input k-space shape.
    """
    rng = np.random.default_rng(seed)

    num_cols = shape[-1]
    num_low_freqs = int(round(num_cols * center_fraction))

    mask_1d = np.zeros(num_cols, dtype=np.float32)

    center = num_cols // 2
    pad = num_low_freqs // 2
    low_freq_start = center - pad
    low_freq_end = center + pad

    mask_1d[low_freq_start:low_freq_end] = 1.0

    target_samples = num_cols // acceleration
    remaining_samples = max(target_samples - num_low_freqs, 0)

    available_indices = np.where(mask_1d == 0)[0]

    if remaining_samples > 0:
        selected = rng.choice(
            available_indices,
            size=remaining_samples,
            replace=False,
        )
        mask_1d[selected] = 1.0

    mask_shape = [1] * len(shape)
    mask_shape[-1] = num_cols

    mask = mask_1d.reshape(mask_shape)

    return mask


def apply_mask(kspace, mask):
    """
    Apply an undersampling mask to k-space data.

    Parameters
    ----------
    kspace : np.ndarray
        Complex-valued k-space data.

    mask : np.ndarray
        Undersampling mask broadcastable to kspace.

    Returns
    -------
    undersampled_kspace : np.ndarray
        Masked k-space data.
    """
    return kspace * mask
