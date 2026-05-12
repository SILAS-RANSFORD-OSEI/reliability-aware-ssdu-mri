"""
SSDU k-space splitting utilities.

SSDU uses acquired k-space samples in two roles:

1. Theta: used inside the reconstruction model for data consistency.
2. Lambda: held out for the self-supervised loss.

This module creates Theta/Lambda masks from an existing acquired sampling mask.
"""

import numpy as np


def split_acquired_mask(mask, rho=0.4, seed=None):
    """
    Split an acquired k-space mask into Theta and Lambda subsets.

    Parameters
    ----------
    mask : np.ndarray
        Binary acquired k-space mask. Nonzero entries indicate acquired samples.

    rho : float
        Fraction of acquired samples assigned to Lambda, the held-out loss set.

    seed : int or None
        Random seed for reproducibility.

    Returns
    -------
    theta_mask : np.ndarray
        Mask for samples used inside the reconstruction model.

    lambda_mask : np.ndarray
        Mask for held-out samples used for self-supervised loss.
    """
    if not 0.0 < rho < 1.0:
        raise ValueError("rho must be between 0 and 1.")

    rng = np.random.default_rng(seed)

    mask = np.asarray(mask).astype(np.float32)
    acquired_indices = np.where(mask > 0)[0]

    num_acquired = len(acquired_indices)
    num_lambda = int(round(rho * num_acquired))

    lambda_indices = rng.choice(
        acquired_indices,
        size=num_lambda,
        replace=False,
    )

    lambda_mask = np.zeros_like(mask, dtype=np.float32)
    lambda_mask[lambda_indices] = 1.0

    theta_mask = mask.copy()
    theta_mask[lambda_indices] = 0.0

    return theta_mask, lambda_mask


def check_disjoint_masks(theta_mask, lambda_mask):
    """
    Check whether Theta and Lambda masks are disjoint.

    Returns
    -------
    is_disjoint : bool
        True if there is no overlap between Theta and Lambda.
    """
    overlap = np.sum(theta_mask * lambda_mask)
    return overlap == 0


def mask_fraction(mask):
    """
    Compute the fraction of sampled k-space locations.
    """
    mask = np.asarray(mask)
    return np.mean(mask > 0)
