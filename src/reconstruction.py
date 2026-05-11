"""
Basic MRI reconstruction functions.

This module contains simple reconstruction utilities used before deep learning models are introduced.
"""

import numpy as np

from transforms import ifft2c, complex_abs, rss_combine


def zero_filled_reconstruction(kspace, mask=None, coil_axis=0):
    """
    Perform zero-filled MRI reconstruction.

    Parameters
    ----------
    kspace : np.ndarray
        Complex-valued k-space data.

        Expected single-coil shape:
        height x width

        Expected multicoil shape:
        coils x height x width

    mask : np.ndarray or None
        Undersampling mask. If provided, it is applied to k-space before reconstruction.

    coil_axis : int
        Axis corresponding to coil dimension for multicoil data.

    Returns
    -------
    image : np.ndarray
        Reconstructed magnitude image.
    """
    if mask is not None:
        kspace = kspace * mask

    coil_images = ifft2c(kspace)

    if coil_images.ndim >= 3:
        image = rss_combine(coil_images, axis=coil_axis)
    else:
        image = complex_abs(coil_images)

    return image


def normalize_to_unit_range(image, eps=1e-12):
    """
    Normalize image to [0, 1].

    Parameters
    ----------
    image : np.ndarray
        Input image.

    eps : float
        Small constant to avoid division by zero.

    Returns
    -------
    normalized : np.ndarray
        Normalized image.
    """
    image = np.asarray(image)
    image = np.abs(image)

    min_val = image.min()
    max_val = image.max()

    return (image - min_val) / (max_val - min_val + eps)
