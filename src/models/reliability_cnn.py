"""
Structural-aware reliability CNN.

This network predicts a residual-calibrated reliability map from structural
and uncertainty-related feature maps.

Inputs may include:
1. Theta-only input image
2. Reconstructed image
3. Edge / gradient magnitude map
4. Optional uncertainty map

Output:
    reliability_map
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ReliabilityCNN(nn.Module):
    """
    CNN for predicting a voxel-wise reliability / residual-energy map.

    Input shape:
        batch x channels x height x width

    Output shape:
        batch x 1 x height x width

    The output is positive because residual energy is nonnegative.
    """

    def __init__(self, in_channels=3, features=32):
        super().__init__()

        self.net = nn.Sequential(
            nn.Conv2d(in_channels, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(features, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(features, features, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(features, 1, kernel_size=3, padding=1),
        )

    def forward(self, x):
        """
        Predict a positive reliability map.

        Parameters
        ----------
        x : torch.Tensor
            Feature tensor with shape:
            batch x channels x height x width

        Returns
        -------
        reliability_map : torch.Tensor
            Positive reliability map with shape:
            batch x 1 x height x width
        """
        raw = self.net(x)

        reliability_map = F.softplus(raw) + 1e-6

        return reliability_map
