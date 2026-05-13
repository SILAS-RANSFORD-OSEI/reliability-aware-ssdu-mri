"""
Simple CNN reconstruction baseline.

This is the first learning-based reconstruction model for SSDU experiments.
It is intentionally small so we can test the training pipeline before moving to U-Net or unrolled models.
"""

import torch
import torch.nn as nn


class SimpleCNNReconstructor(nn.Module):
    """
    Simple image-domain CNN for MRI reconstruction refinement.

    Input:
        Tensor with shape: batch x channels x height x width

    Output:
        Tensor with shape: batch x channels x height x width
    """

    def __init__(self, in_channels=1, out_channels=1, features=32):
        super().__init__()

        self.net = nn.Sequential(
            nn.Conv2d(in_channels, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(features, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(features, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(features, out_channels, kernel_size=3, padding=1),
        )

    def forward(self, x):
        """
        Forward pass.

        Parameters
        ----------
        x : torch.Tensor
            Input image tensor.

        Returns
        -------
        out : torch.Tensor
            Reconstructed image tensor.
        """
        residual = self.net(x)

        return x + residual
