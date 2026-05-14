"""
Reliability and uncertainty-alignment utilities.

This module supports reliability-aware SSDU reconstruction by generating
dropout-based stochastic reconstructions and comparing uncertainty maps
with held-out residual energy.
"""

import numpy as np

from transforms import fft2c, ifft2c


def stochastic_reconstructions(model, x_input_tensor, num_samples=8):
    """
    Generate multiple stochastic reconstructions using dropout.

    Parameters
    ----------
    model : torch.nn.Module
        Dropout-enabled reconstruction model.

    x_input_tensor : torch.Tensor
        Input image tensor with shape:
        1 x 1 x height x width

    num_samples : int
        Number of stochastic forward passes.

    Returns
    -------
    outputs : np.ndarray
        Stochastic reconstructions with shape:
        num_samples x height x width
    """
    model.train()  # keep dropout active

    outputs = []

    import torch

    with torch.no_grad():
        for _ in range(num_samples):
            out = model(x_input_tensor)
            out_np = out.detach().cpu().numpy()[0, 0]
            outputs.append(out_np)

    return np.stack(outputs, axis=0)


def compute_mean_and_uncertainty(stochastic_outputs):
    """
    Compute mean reconstruction and voxel-wise uncertainty.

    Parameters
    ----------
    stochastic_outputs : np.ndarray
        Array with shape:
        T x height x width

    Returns
    -------
    mean_image : np.ndarray
        Mean reconstruction.

    uncertainty_map : np.ndarray
        Voxel-wise variance map.
    """
    mean_image = np.mean(stochastic_outputs, axis=0)
    uncertainty_map = np.var(stochastic_outputs, axis=0, ddof=1)

    return mean_image, uncertainty_map


def backproject_lambda_residual(mean_image, measured_kspace, lambda_mask):
    """
    Compute backprojected Lambda residual energy from a mean reconstruction.

    Parameters
    ----------
    mean_image : np.ndarray
        Mean reconstructed image with shape:
        height x width

    measured_kspace : np.ndarray
        Measured single-coil k-space with shape:
        height x width

    lambda_mask : np.ndarray
        1D Lambda mask with shape:
        width

    Returns
    -------
    residual_energy : np.ndarray
        Image-domain residual energy map.
    """
    predicted_kspace = fft2c(mean_image)

    lambda_mask_2d = lambda_mask[None, :]

    residual_lambda = lambda_mask_2d * (predicted_kspace - measured_kspace)

    residual_image = ifft2c(residual_lambda)

    residual_energy = np.abs(residual_image) ** 2

    return residual_energy


def normalize_map(x, eps=1e-12):
    """
    Normalize a map to [0, 1].
    """
    x = np.asarray(x)
    x = np.abs(x)

    min_val = x.min()
    max_val = x.max()

    return (x - min_val) / (max_val - min_val + eps)


def map_alignment(map_a, map_b):
    """
    Compute Pearson correlation between two spatial maps.

    Parameters
    ----------
    map_a : np.ndarray
        First image/map.

    map_b : np.ndarray
        Second image/map.

    Returns
    -------
    correlation : float
        Pearson correlation between normalized flattened maps.
    """
    a = normalize_map(map_a).ravel()
    b = normalize_map(map_b).ravel()

    if np.std(a) == 0 or np.std(b) == 0:
        return 0.0

    return np.corrcoef(a, b)[0, 1]
