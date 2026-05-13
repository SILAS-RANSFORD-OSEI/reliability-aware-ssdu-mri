"""
Uncertainty utilities for reliability-aware MRI reconstruction.

This module contains basic functions for computing mean reconstructions
and voxel-wise uncertainty maps from multiple stochastic reconstructions.
"""

import numpy as np


def mean_reconstruction(reconstructions):
    """
    Compute the mean reconstruction from multiple stochastic reconstructions.

    Parameters
    ----------
    reconstructions : np.ndarray
        Array of reconstructed images.

        Expected shape:
        T x height x width

        where T is the number of stochastic samples.

    Returns
    -------
    mean_image : np.ndarray
        Mean reconstructed image.
    """
    reconstructions = np.asarray(reconstructions)

    if reconstructions.ndim < 3:
        raise ValueError("Expected reconstructions with shape T x height x width.")

    return np.mean(reconstructions, axis=0)


def voxelwise_variance(reconstructions):
    """
    Compute voxel-wise uncertainty as sample variance.

    Parameters
    ----------
    reconstructions : np.ndarray
        Array of reconstructed images.

        Expected shape:
        T x height x width

    Returns
    -------
    variance_map : np.ndarray
        Voxel-wise variance map.
    """
    reconstructions = np.asarray(reconstructions)

    if reconstructions.ndim < 3:
        raise ValueError("Expected reconstructions with shape T x height x width.")

    return np.var(reconstructions, axis=0, ddof=1)


def normalize_map(x, eps=1e-12):
    """
    Normalize a map to the range [0, 1].

    Parameters
    ----------
    x : np.ndarray
        Input map.

    eps : float
        Small constant to avoid division by zero.

    Returns
    -------
    normalized : np.ndarray
        Normalized map.
    """
    x = np.asarray(x)
    x = np.abs(x)

    min_val = np.min(x)
    max_val = np.max(x)

    return (x - min_val) / (max_val - min_val + eps)


def uncertainty_residual_alignment(uncertainty_map, residual_energy_map):
    """
    Compute a simple correlation between uncertainty and residual energy.

    This is an early diagnostic metric for checking whether uncertainty is spatially aligned
    with the image-domain held-out residual signal.

    Parameters
    ----------
    uncertainty_map : np.ndarray
        Predicted voxel-wise uncertainty map.

    residual_energy_map : np.ndarray
        Image-domain held-out residual energy map.

    Returns
    -------
    correlation : float
        Pearson correlation between flattened maps.
    """
    u = normalize_map(uncertainty_map).ravel()
    e = normalize_map(residual_energy_map).ravel()

    if np.std(u) == 0 or np.std(e) == 0:
        return 0.0

    return np.corrcoef(u, e)[0, 1]
