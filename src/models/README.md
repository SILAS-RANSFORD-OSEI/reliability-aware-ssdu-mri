# Models

This folder will contain neural network models for MRI reconstruction.

## Planned Models

### 1. Simple CNN Baseline

A small image-domain convolutional reconstruction model.

Purpose:

- Test the training loop.
- Verify SSDU loss behavior.
- Establish the first learning-based baseline.

### 2. U-Net Baseline

A stronger image-domain reconstruction model.

Purpose:

- Improve reconstruction quality over the simple CNN.
- Provide a reasonable baseline before unrolled models.

### 3. Unrolled Physics-Guided Model

A reconstruction network with repeated data-consistency and learned-regularization blocks.

Purpose:

- Move closer to physics-guided MRI reconstruction.
- Support the final reliability-aware SSDU framework.

### 4. Stochastic Reconstruction Model

A dropout-enabled or ensemble-based model.

Purpose:

- Generate multiple stochastic reconstructions.
- Compute voxel-wise uncertainty maps.
- Support uncertainty calibration using held-out residual energy.

## Current Status

Planned.

The immediate next model is a simple CNN baseline before implementing a full U-Net or unrolled network.
