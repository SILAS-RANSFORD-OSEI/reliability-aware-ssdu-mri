"""
Training utilities for SSDU MRI reconstruction.

This module contains reusable functions for preparing single-coil SSDU inputs
and computing differentiable SSDU loss in PyTorch.
"""

import numpy as np
import torch


def prepare_single_coil_ssdu_input(kspace_single, theta_mask, normalize=True, eps=1e-12):
    """
    Prepare a single-coil Theta-only zero-filled image input for SSDU training.

    Parameters
    ----------
    kspace_single : np.ndarray
        Complex-valued single-coil k-space with shape:
        height x width

    theta_mask : np.ndarray
        1D Theta mask with shape:
        width

    normalize : bool
        Whether to normalize the magnitude image to [0, 1].

    eps : float
        Small constant to avoid division by zero.

    Returns
    -------
    x_input : torch.Tensor
        Input tensor with shape:
        1 x 1 x height x width

    kspace_theta : np.ndarray
        Theta-only k-space with shape:
        height x width
    """
    theta_mask_2d = theta_mask[None, :]
    kspace_theta = theta_mask_2d * kspace_single

    image_complex = np.fft.fftshift(
        np.fft.ifft2(
            np.fft.ifftshift(kspace_theta, axes=(-2, -1)),
            axes=(-2, -1),
            norm="ortho",
        ),
        axes=(-2, -1),
    )

    image_mag = np.abs(image_complex)

    if normalize:
        min_val = image_mag.min()
        max_val = image_mag.max()
        image_mag = (image_mag - min_val) / (max_val - min_val + eps)

    x_input = torch.from_numpy(image_mag).float()
    x_input = x_input.unsqueeze(0).unsqueeze(0)

    return x_input, kspace_theta


def torch_fft2c(image):
    """
    Centered 2D FFT for PyTorch tensors.

    Parameters
    ----------
    image : torch.Tensor
        Real-valued image tensor with shape:
        height x width

    Returns
    -------
    kspace : torch.Tensor
        Complex-valued centered k-space tensor.
    """
    image_complex = torch.complex(image, torch.zeros_like(image))

    kspace = torch.fft.fftshift(
        torch.fft.fft2(
            torch.fft.ifftshift(image_complex, dim=(-2, -1)),
            norm="ortho",
        ),
        dim=(-2, -1),
    )

    return kspace


def single_coil_ssdu_loss(x_pred_tensor, kspace_single, lambda_mask, eps=1e-12):
    """
    Compute differentiable single-coil SSDU loss.

    Parameters
    ----------
    x_pred_tensor : torch.Tensor
        Predicted image tensor with shape:
        1 x 1 x height x width

    kspace_single : np.ndarray
        Complex-valued measured single-coil k-space with shape:
        height x width

    lambda_mask : np.ndarray
        1D Lambda mask with shape:
        width

    eps : float
        Small constant to avoid division by zero.

    Returns
    -------
    loss : torch.Tensor
        Normalized SSDU Lambda loss.
    """
    x_pred = x_pred_tensor[0, 0]

    k_pred = torch_fft2c(x_pred)

    lambda_mask_2d = lambda_mask[None, :]

    true_lambda = lambda_mask_2d * kspace_single

    true_lambda_torch = torch.from_numpy(true_lambda).to(k_pred.device)
    lambda_mask_torch = torch.from_numpy(lambda_mask_2d).float().to(k_pred.device)

    residual = lambda_mask_torch * (k_pred - true_lambda_torch)

    numerator = torch.sum(torch.abs(residual) ** 2)
    denominator = torch.sum(torch.abs(true_lambda_torch) ** 2) + eps

    loss = numerator / denominator

    return loss


def image_consistency_loss(x_pred_tensor, x_input_tensor):
    """
    Compute L1 image consistency loss.

    Parameters
    ----------
    x_pred_tensor : torch.Tensor
        Predicted reconstruction.

    x_input_tensor : torch.Tensor
        Input Theta-only image.

    Returns
    -------
    loss : torch.Tensor
        Mean absolute difference.
    """
    return torch.mean(torch.abs(x_pred_tensor - x_input_tensor))


def total_ssdu_training_loss(
    x_pred_tensor,
    x_input_tensor,
    kspace_single,
    lambda_mask,
    lambda_img=1e7,
):
    """
    Compute total SSDU training loss.

    Total loss:

        L_total = L_SSDU + lambda_img * L_img

    Parameters
    ----------
    x_pred_tensor : torch.Tensor
        Model output.

    x_input_tensor : torch.Tensor
        Theta-only input image.

    kspace_single : np.ndarray
        Measured single-coil k-space.

    lambda_mask : np.ndarray
        Held-out Lambda mask.

    lambda_img : float
        Weight for image consistency regularization.

    Returns
    -------
    total_loss : torch.Tensor
        Total training loss.

    ssdu_loss : torch.Tensor
        Held-out k-space SSDU loss.

    img_loss : torch.Tensor
        Image consistency loss.
    """
    ssdu_loss = single_coil_ssdu_loss(
        x_pred_tensor=x_pred_tensor,
        kspace_single=kspace_single,
        lambda_mask=lambda_mask,
    )

    img_loss = image_consistency_loss(
        x_pred_tensor=x_pred_tensor,
        x_input_tensor=x_input_tensor,
    )

    total_loss = ssdu_loss + lambda_img * img_loss

    return total_loss, ssdu_loss, img_loss
