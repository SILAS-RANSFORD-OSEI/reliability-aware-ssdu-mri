"""
MRI Fourier transform utilities.

This module contains basic centered FFT and inverse FFT operations used in MRI reconstruction.

The first implementation target is zero-filled reconstruction.
"""

import numpy as np


def fft2c(image):
    """
    Centered 2D Fourier transform.

    Parameters
    ----------
    image : np.ndarray
        Complex-valued image-domain data.

    Returns
    -------
    kspace : np.ndarray
        Complex-valued centered k-space data.
    """
    image = np.asarray(image)

    kspace = np.fft.fftshift(
        np.fft.fft2(
            np.fft.ifftshift(image, axes=(-2, -1)),
            axes=(-2, -1),
            norm="ortho",
        ),
        axes=(-2, -1),
    )

    return kspace


def ifft2c(kspace):
    """
    Centered 2D inverse Fourier transform.

    Parameters
    ----------
    kspace : np.ndarray
        Complex-valued centered k-space data.

    Returns
    -------
    image : np.ndarray
        Complex-valued image-domain data.
    """
    kspace = np.asarray(kspace)

    image = np.fft.fftshift(
        np.fft.ifft2(
            np.fft.ifftshift(kspace, axes=(-2, -1)),
            axes=(-2, -1),
            norm="ortho",
        ),
        axes=(-2, -1),
    )

    return image


def complex_abs(x):
    """
    Compute magnitude of complex-valued data.

    Parameters
    ----------
    x : np.ndarray
        Complex-valued input.

    Returns
    -------
    magnitude : np.ndarray
        Magnitude image.
    """
    return np.abs(x)


def rss_combine(coil_images, axis=0):
    """
    Root-sum-of-squares coil combination.

    Parameters
    ----------
    coil_images : np.ndarray
        Complex-valued coil images.

    axis : int
        Coil dimension.

    Returns
    -------
    rss_image : np.ndarray
        Coil-combined magnitude image.
    """
    return np.sqrt(np.sum(np.abs(coil_images) ** 2, axis=axis))
