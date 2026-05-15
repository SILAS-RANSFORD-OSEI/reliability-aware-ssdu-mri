"""
Heteroscedastic CNN reconstruction model.

This model predicts both:
1. reconstructed image
2. voxel-wise uncertainty / variance map

Output:
    x_hat, sigma2_hat
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class HeteroscedasticCNNReconstructor(nn.Module):
    """
    CNN with two output heads:

    1. Reconstruction head:
        x_hat = x_input + residual

    2. Uncertainty head:
        sigma2_hat > 0

    Input shape:
        batch x channels x height x width

    Output:
        x_hat:       batch x 1 x height x width
        sigma2_hat:  batch x 1 x height x width
    """

    def __init__(self, in_channels=1, features=32):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Conv2d(in_channels, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(features, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(features, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
        )

        self.reconstruction_head = nn.Conv2d(
            features,
            1,
            kernel_size=3,
            padding=1,
        )

        self.log_variance_head = nn.Conv2d(
            features,
            1,
            kernel_size=3,
            padding=1,
        )

    def forward(self, x):
        """
        Forward pass.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor with shape:
            batch x 1 x height x width

        Returns
        -------
        x_hat : torch.Tensor
            Reconstructed image.

        sigma2_hat : torch.Tensor
            Positive voxel-wise variance map.
        """
        features = self.encoder(x)

        residual = self.reconstruction_head(features)
        x_hat = x + residual

        log_sigma2 = self.log_variance_head(features)

        # Softplus ensures positive variance and avoids zero variance.
        sigma2_hat = F.softplus(log_sigma2) + 1e-6

        return x_hat, sigma2_hat
