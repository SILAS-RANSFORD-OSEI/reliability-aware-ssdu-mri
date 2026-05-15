"""
Calibration utilities for residual-calibrated reliability mapping.

These utilities support the four-way SSDU reliability framework:

Omega = Theta ∪ Lambda_train ∪ Lambda_cal ∪ Lambda_eval

The calibration subset Lambda_cal is used to fit a reliability map,
which is then evaluated on Lambda_eval.
"""

import numpy as np


def flatten_norm(x, eps=1e-12):
    """
    Normalize a 2D map to [0, 1] and flatten it.

    Parameters
    ----------
    x : np.ndarray
        Input 2D map.

    eps : float
        Small constant to avoid division by zero.

    Returns
    -------
    x_flat : np.ndarray
        Flattened normalized map.
    """
    x = np.asarray(x)
    x = np.abs(x)

    min_val = x.min()
    max_val = x.max()

    x_norm = (x - min_val) / (max_val - min_val + eps)

    return x_norm.ravel()


def gradient_magnitude(image):
    """
    Compute simple 2D gradient magnitude.

    Parameters
    ----------
    image : np.ndarray
        Input 2D image.

    Returns
    -------
    grad_mag : np.ndarray
        Gradient magnitude map.
    """
    gy, gx = np.gradient(image)

    grad_mag = np.sqrt(gx**2 + gy**2)

    return grad_mag


def fit_ridge_reliability_map(
    target_map,
    predictor_maps,
    output_shape,
    ridge_lambda=1e-3,
):
    """
    Fit a ridge-regression reliability map.

    The fitted model is:

        R = beta_0 + beta_1 P_1 + beta_2 P_2 + ... + beta_n P_n

    where:
        R is the predicted residual/reliability map,
        P_i are predictor maps such as uncertainty, intensity, or edge magnitude.

    Parameters
    ----------
    target_map : np.ndarray
        Calibration residual energy map.

    predictor_maps : list of np.ndarray
        List of predictor maps.

        Example:
            [dropout_uncertainty, input_intensity, edge_map]

    output_shape : tuple
        Desired 2D output shape.

    ridge_lambda : float
        Ridge regularization strength.

    Returns
    -------
    reliability_map : np.ndarray
        Predicted residual-calibrated reliability map.

    beta : np.ndarray
        Fitted coefficients, including intercept.
    """
    y = flatten_norm(target_map)

    X_list = [flatten_norm(p) for p in predictor_maps]
    X = np.stack(X_list, axis=1)

    # Add intercept column
    X = np.concatenate(
        [np.ones((X.shape[0], 1)), X],
        axis=1,
    )

    # Ridge regression:
    # beta = (X^T X + lambda I)^(-1) X^T y
    identity = np.eye(X.shape[1])
    identity[0, 0] = 0.0  # do not penalize intercept

    beta = np.linalg.solve(
        X.T @ X + ridge_lambda * identity,
        X.T @ y,
    )

    prediction = X @ beta
    reliability_map = prediction.reshape(output_shape)

    return reliability_map, beta


def fit_structural_reliability_map(
    residual_cal,
    input_image,
    mean_image,
    ridge_lambda=1e-3,
):
    """
    Fit structural reliability map using input intensity and edge magnitude.

    Model:

        R_struct = beta_0 + beta_1 I + beta_2 G

    where:
        I is input intensity,
        G is gradient magnitude of the mean reconstruction.
    """
    input_intensity = np.abs(input_image)
    edge_map = gradient_magnitude(mean_image)

    return fit_ridge_reliability_map(
        target_map=residual_cal,
        predictor_maps=[input_intensity, edge_map],
        output_shape=residual_cal.shape,
        ridge_lambda=ridge_lambda,
    )


def fit_hybrid_reliability_map(
    residual_cal,
    uncertainty_map,
    input_image,
    mean_image,
    ridge_lambda=1e-3,
):
    """
    Fit hybrid reliability map using dropout uncertainty, input intensity,
    and edge magnitude.

    Model:

        R_hybrid = beta_0 + beta_1 U + beta_2 I + beta_3 G

    where:
        U is uncertainty,
        I is input intensity,
        G is gradient magnitude of the mean reconstruction.
    """
    input_intensity = np.abs(input_image)
    edge_map = gradient_magnitude(mean_image)

    return fit_ridge_reliability_map(
        target_map=residual_cal,
        predictor_maps=[uncertainty_map, input_intensity, edge_map],
        output_shape=residual_cal.shape,
        ridge_lambda=ridge_lambda,
    )
