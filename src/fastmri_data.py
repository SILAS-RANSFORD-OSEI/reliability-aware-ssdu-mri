"""
Data loading utilities for fastMRI brain reconstruction experiments.

This module provides simple helper functions for reading fastMRI HDF5 files,
inspecting metadata, and extracting k-space slices.
"""

import h5py
import numpy as np


def load_fastmri_file(file_path):
    """
    Load k-space data, mask, and metadata from a fastMRI HDF5 file.

    Parameters
    ----------
    file_path : str
        Path to the fastMRI .h5 file.

    Returns
    -------
    data : dict
        Dictionary containing k-space, mask, attributes, and file keys.
    """
    with h5py.File(file_path, "r") as hf:
        keys = list(hf.keys())

        kspace = hf["kspace"][:] if "kspace" in hf else None
        mask = hf["mask"][:] if "mask" in hf else None

        attrs = {}
        for key, value in hf.attrs.items():
            attrs[key] = value

    data = {
        "kspace": kspace,
        "mask": mask,
        "attrs": attrs,
        "keys": keys,
        "file_path": file_path,
    }

    return data


def print_fastmri_summary(data):
    """
    Print a summary of a loaded fastMRI file.

    Parameters
    ----------
    data : dict
        Dictionary returned by load_fastmri_file.
    """
    print("File path:", data["file_path"])
    print("Keys:", data["keys"])

    print("\nAttributes:")
    for key, value in data["attrs"].items():
        print(f"{key}: {value}")

    kspace = data["kspace"]
    mask = data["mask"]

    if kspace is not None:
        print("\nK-space shape:", kspace.shape)
        print("K-space dtype:", kspace.dtype)

    if mask is not None:
        print("Mask shape:", mask.shape)
        print("Mask dtype:", mask.dtype)


def get_kspace_slice(kspace, slice_index=None):
    """
    Extract one slice from fastMRI k-space data.

    Parameters
    ----------
    kspace : np.ndarray
        fastMRI k-space array.

        Expected multicoil shape:
        slices x coils x height x width

    slice_index : int or None
        Slice index to extract. If None, the central slice is used.

    Returns
    -------
    kspace_slice : np.ndarray
        Selected k-space slice.

        Expected shape:
        coils x height x width

    slice_index : int
        Index of selected slice.
    """
    if kspace is None:
        raise ValueError("kspace is None.")

    if kspace.ndim < 3:
        raise ValueError(f"Expected at least 3D k-space, got shape {kspace.shape}")

    if slice_index is None:
        slice_index = kspace.shape[0] // 2

    kspace_slice = kspace[slice_index]

    return kspace_slice, slice_index
