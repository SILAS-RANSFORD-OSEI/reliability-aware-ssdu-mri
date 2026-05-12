"""
Visualization utilities for MRI reconstruction experiments.

This module keeps plotting code reusable and clean across notebooks.
"""

import numpy as np
import matplotlib.pyplot as plt


def show_kspace_and_reconstruction(kspace_slice, reconstructed_image, title="Zero-Filled RSS Reconstruction"):
    """
    Display one coil's k-space magnitude and the reconstructed image.

    Parameters
    ----------
    kspace_slice : np.ndarray
        Multicoil k-space slice with shape:
        coils x height x width

    reconstructed_image : np.ndarray
        Reconstructed magnitude image.

    title : str
        Title for the reconstructed image plot.
    """
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(np.log1p(np.abs(kspace_slice[0])), cmap="gray")
    plt.title("Log K-Space Magnitude: Coil 0")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(reconstructed_image, cmap="gray")
    plt.title(title)
    plt.axis("off")

    plt.tight_layout()
    plt.show()


def center_crop(image, crop_size):
    """
    Center crop a 2D image.

    Parameters
    ----------
    image : np.ndarray
        Input 2D image.

    crop_size : tuple
        Desired crop size as:
        crop_height, crop_width

    Returns
    -------
    cropped : np.ndarray
        Center-cropped image.
    """
    h, w = image.shape[-2:]
    crop_h, crop_w = crop_size

    if crop_h > h or crop_w > w:
        raise ValueError("Crop size must be smaller than image size.")

    start_h = (h - crop_h) // 2
    start_w = (w - crop_w) // 2

    return image[start_h:start_h + crop_h, start_w:start_w + crop_w]


def show_full_and_crop(image, crop_size=(320, 320)):
    """
    Display full image and center-cropped image.

    Parameters
    ----------
    image : np.ndarray
        Input 2D image.

    crop_size : tuple
        Desired crop size.
    """
    cropped = center_crop(image, crop_size)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap="gray")
    plt.title("Full Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(cropped, cmap="gray")
    plt.title("Center Crop")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    return cropped
