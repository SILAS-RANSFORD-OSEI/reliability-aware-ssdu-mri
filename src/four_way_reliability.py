"""
Four-way SSDU reliability experiment utilities.

This module implements a reviewer-defensible reliability workflow:

Omega = Theta ∪ Lambda_train ∪ Lambda_cal ∪ Lambda_eval

Roles:
- Theta: reconstruction input
- Lambda_train: SSDU training loss
- Lambda_cal: calibration-style residual analysis
- Lambda_eval: final held-out reliability evaluation
"""

import numpy as np
import torch

from ssdu import split_acquired_mask_four_way
from models.dropout_cnn import DropoutCNNReconstructor
from training import prepare_single_coil_ssdu_input, total_ssdu_training_loss
from reliability import (
    stochastic_reconstructions,
    compute_mean_and_uncertainty,
    backproject_lambda_residual,
    map_alignment,
)


def run_four_way_reliability_experiment(
    kspace,
    mask,
    slice_index,
    coil_index=0,
    train_fraction=0.2,
    cal_fraction=0.1,
    eval_fraction=0.1,
    split_seed=42,
    model_seed=0,
    num_steps=50,
    num_samples=8,
    features=16,
    dropout_p=0.1,
    lr=1e-4,
    lambda_img=1e7,
):
    """
    Run a four-way SSDU reliability experiment on one single-coil slice.

    The model is trained only on Lambda_train.
    Reliability alignment is measured separately on Lambda_cal and Lambda_eval.

    Parameters
    ----------
    kspace : np.ndarray
        Multicoil k-space array with shape:
        slices x coils x height x width

    mask : np.ndarray
        1D acquired k-space mask.

    slice_index : int
        Slice index to use.

    coil_index : int
        Coil index to use for the single-coil-equivalent experiment.

    train_fraction : float
        Fraction of acquired samples assigned to Lambda_train.

    cal_fraction : float
        Fraction of acquired samples assigned to Lambda_cal.

    eval_fraction : float
        Fraction of acquired samples assigned to Lambda_eval.

    split_seed : int
        Random seed controlling the four-way mask split.

    model_seed : int
        Random seed controlling model initialization and dropout randomness.

    num_steps : int
        Number of training steps.

    num_samples : int
        Number of stochastic dropout reconstructions.

    features : int
        Number of CNN feature channels.

    dropout_p : float
        Dropout probability.

    lr : float
        Learning rate.

    lambda_img : float
        Image-consistency regularization weight.

    Returns
    -------
    result : dict
        Dictionary containing losses, alignments, reconstructions, uncertainty map,
        and residual energy maps.
    """
    np.random.seed(model_seed)
    torch.manual_seed(model_seed)

    # Select one slice and one coil
    kspace_slice = kspace[slice_index]
    kspace_single = kspace_slice[coil_index]

    # Four-way SSDU split
    theta_mask, lambda_train_mask, lambda_cal_mask, lambda_eval_mask = (
        split_acquired_mask_four_way(
            mask=mask,
            train_fraction=train_fraction,
            cal_fraction=cal_fraction,
            eval_fraction=eval_fraction,
            seed=split_seed,
        )
    )

    # Prepare Theta-only input
    x_input, kspace_theta = prepare_single_coil_ssdu_input(
        kspace_single=kspace_single,
        theta_mask=theta_mask,
        normalize=True,
    )

    # Dropout reconstruction model
    model = DropoutCNNReconstructor(
        in_channels=1,
        out_channels=1,
        features=features,
        dropout_p=dropout_p,
    )

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    loss_history = []
    ssdu_history = []
    img_history = []

    model.train()

    for _ in range(num_steps):
        optimizer.zero_grad()

        x_pred = model(x_input)

        # Train only on Lambda_train
        total_loss, ssdu_loss, img_loss = total_ssdu_training_loss(
            x_pred_tensor=x_pred,
            x_input_tensor=x_input,
            kspace_single=kspace_single,
            lambda_mask=lambda_train_mask,
            lambda_img=lambda_img,
        )

        total_loss.backward()
        optimizer.step()

        loss_history.append(total_loss.item())
        ssdu_history.append(ssdu_loss.item())
        img_history.append(img_loss.item())

    # Stochastic dropout inference
    stochastic_outputs = stochastic_reconstructions(
        model=model,
        x_input_tensor=x_input,
        num_samples=num_samples,
    )

    mean_image, uncertainty_map = compute_mean_and_uncertainty(
        stochastic_outputs
    )

    # Calibration residual energy
    residual_energy_cal = backproject_lambda_residual(
        mean_image=mean_image,
        measured_kspace=kspace_single,
        lambda_mask=lambda_cal_mask,
    )

    # Evaluation residual energy
    residual_energy_eval = backproject_lambda_residual(
        mean_image=mean_image,
        measured_kspace=kspace_single,
        lambda_mask=lambda_eval_mask,
    )

    alignment_cal = map_alignment(
        uncertainty_map,
        residual_energy_cal,
    )

    alignment_eval = map_alignment(
        uncertainty_map,
        residual_energy_eval,
    )

    result = {
        "slice_index": slice_index,
        "coil_index": coil_index,
        "split_seed": split_seed,
        "model_seed": model_seed,
        "initial_train_ssdu_loss": ssdu_history[0],
        "final_train_ssdu_loss": ssdu_history[-1],
        "train_ssdu_reduction_percent": (
            100 * (ssdu_history[0] - ssdu_history[-1]) / ssdu_history[0]
        ),
        "initial_image_loss": img_history[0],
        "final_image_loss": img_history[-1],
        "alignment_cal": alignment_cal,
        "alignment_eval": alignment_eval,
        "loss_history": loss_history,
        "ssdu_history": ssdu_history,
        "img_history": img_history,
        "mean_image": mean_image,
        "uncertainty_map": uncertainty_map,
        "residual_energy_cal": residual_energy_cal,
        "residual_energy_eval": residual_energy_eval,
        "x_input": x_input.detach().cpu().numpy()[0, 0],
        "theta_mask": theta_mask,
        "lambda_train_mask": lambda_train_mask,
        "lambda_cal_mask": lambda_cal_mask,
        "lambda_eval_mask": lambda_eval_mask,
    }

    return result
