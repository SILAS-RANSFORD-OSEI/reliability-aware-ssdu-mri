"""
Loss utilities for self-supervised MRI reconstruction.

This module contains SSDU-style k-space residual and loss functions.
"""

import numpy as np

from transforms import fft2c


def expand_mask(mask, target_shape):
    """
    Expand a 1D k-space mask so it can broadcast to a target k-space shape.

    Parameters
    ----------
    mask : np.ndarray
        1D mask with shape:
        width

    target_shape : tuple
        Target k-space shape, for example:
        coils x height x width

    Returns
    -------
    expanded_mask : np.ndarray
        Mask reshaped for broadcasting.
    """
    mask = np.asarray(mask).astype(np.float32)

    if mask.ndim != 1:
        raise ValueError("Expected a 1D mask.")

    mask_shape = [1] * len(target_shape)
    mask_shape[-1] = mask.shape[0]

    return mask.reshape(mask_shape)


def heldout_kspace_residual(reconstructed_coil_images, measured_kspace, lambda_mask):
    """
    Compute the held-out k-space residual on Lambda.

    Parameters
    ----------
    reconstructed_coil_images : np.ndarray
        Complex-valued reconstructed coil images.

        Expected shape:
        coils x height x width

    measured_kspace : np.ndarray
        Measured multicoil k-space.

        Expected shape:
        coils x height x width

    lambda_mask : np.ndarray
        1D held-out Lambda mask.

    Returns
    -------
    residual : np.ndarray
        Complex-valued held-out k-space residual.
    """
    predicted_kspace = fft2c(reconstructed_coil_images)

    expanded_lambda = expand_mask(lambda_mask, measured_kspace.shape)

    residual = expanded_lambda * (predicted_kspace - measured_kspace)

    return residual


def ssdu_l2_loss(reconstructed_coil_images, measured_kspace, lambda_mask, eps=1e-12):
    """
    Compute SSDU held-out k-space L2 loss.

    Parameters
    ----------
    reconstructed_coil_images : np.ndarray
        Complex-valued reconstructed coil images.

    measured_kspace : np.ndarray
        Measured multicoil k-space.

    lambda_mask : np.ndarray
        Held-out Lambda mask.

    eps : float
        Small value to avoid division by zero.

    Returns
    -------
    loss : float
        Normalized held-out k-space residual energy.
    """
    residual = heldout_kspace_residual(
        reconstructed_coil_images=reconstructed_coil_images,
        measured_kspace=measured_kspace,
        lambda_mask=lambda_mask,
    )

    expanded_lambda = expand_mask(lambda_mask, measured_kspace.shape)
    measured_heldout = expanded_lambda * measured_kspace

    numerator = np.sum(np.abs(residual) ** 2)
    denominator = np.sum(np.abs(measured_heldout) ** 2) + eps

    return numerator / denominator


def backproject_kspace_residual(residual):
    """
    Backproject a k-space residual into the image domain.

    Parameters
    ----------
    residual : np.ndarray
        Complex-valued k-space residual.

        Expected shape:
        coils x height x width

    Returns
    -------
    residual_image_coils : np.ndarray
        Complex-valued image-domain residual for each coil.
    """
    from transforms import ifft2c

    residual_image_coils = ifft2c(residual)

    return residual_image_coils


def residual_energy_map(residual_image_coils, coil_axis=0):
    """
    Compute image-domain residual energy map from multicoil residual images.

    Parameters
    ----------
    residual_image_coils : np.ndarray
        Complex-valued image-domain residuals.

        Expected shape:
        coils x height x width

    coil_axis : int
        Axis corresponding to the coil dimension.

    Returns
    -------
    energy_map : np.ndarray
        Image-domain residual energy map.
    """
    energy_map = np.sum(np.abs(residual_image_coils) ** 2, axis=coil_axis)

    return energy_map


def heldout_residual_energy_map(reconstructed_coil_images, measured_kspace, lambda_mask):
    """
    Compute image-domain energy map from held-out k-space residual.

    This combines:
    1. Held-out k-space residual computation
    2. Backprojection to image domain
    3. Multicoil residual energy calculation

    Parameters
    ----------
    reconstructed_coil_images : np.ndarray
        Complex-valued reconstructed coil images.

    measured_kspace : np.ndarray
        Measured multicoil k-space.

    lambda_mask : np.ndarray
        Held-out Lambda mask.

    Returns
    -------
    energy_map : np.ndarray
        Image-domain held-out residual energy map.
    """
    residual = heldout_kspace_residual(
        reconstructed_coil_images=reconstructed_coil_images,
        measured_kspace=measured_kspace,
        lambda_mask=lambda_mask,
    )

    residual_image_coils = backproject_kspace_residual(residual)

    energy_map = residual_energy_map(
        residual_image_coils=residual_image_coils,
        coil_axis=0,
    )

    return energy_map
