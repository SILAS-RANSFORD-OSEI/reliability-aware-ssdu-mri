"""
Dropout CNN reconstruction model.

This model is used for stochastic reconstruction. During inference, dropout can be kept active
to generate multiple reconstructions from the same input, allowing voxel-wise uncertainty estimation.
"""

import torch
import torch.nn as nn


class DropoutCNNReconstructor(nn.Module):
    """
    Dropout-enabled CNN for stochastic MRI reconstruction.

    Input:
        batch x channels x height x width

    Output:
        batch x channels x height x width
    """

    def __init__(self, in_channels=1, out_channels=1, features=32, dropout_p=0.1):
        super().__init__()

        self.net = nn.Sequential(
            nn.Conv2d(in_channels, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Dropout2d(p=dropout_p),

            nn.Conv2d(features, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Dropout2d(p=dropout_p),

            nn.Conv2d(features, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Dropout2d(p=dropout_p),

            nn.Conv2d(features, out_channels, kernel_size=3, padding=1),
        )

    def forward(self, x):
        """
        Forward pass with residual learning.

        The network predicts a correction term and adds it to the input.
        """
        residual = self.net(x)
        return x + residual
