# -*- coding: utf-8 -*-

import numpy as np


def compute_loss_mse(y, tx, w):
    """
    Compute the mean square error of the estimations compared to true values

    Parameters:
    y: The true values
    tx: The data
    w: The weights

    Returns:
    mse: The mean square error

    """
    e = y - tx @ w
    mse = (e @ e) / (2 * e.shape[0])

    return mse


def compute_gradient_mse(y, tx, w):
    """
    Compute the mean square error's gradient

    Parameters:
    y: The true values
    tx: The data
    w: The weights

    Returns:
    gradient: The computed gradient
    """
    e = y - tx @ w
    gradient = -1/tx.shape[0] * tx.T @ e

    return gradient


def gradient_descent(y, tx, initial_w, max_iters, gamma):
    """
    Compute the linear regression using gradient descent

    Parameters:
    y: The true values
    tx: The data
    initial_w: The initial weights
    max_iters: Max number of gradient descent iterations
    gamma: Gamma (learning rate)

    Returns:
    w: The final weights
    loss: The final loss
    """
    w = initial_w

    for n_iter in range(max_iters):
        gradient = compute_gradient_mse(y, tx, w)
        
        w = w - gamma * gradient

    loss = compute_loss_mse(y, tx, w)

    return w, loss


def stochastic_gradient_descent(y, tx, initial_w, max_iters, gamma):
    """
    Compute the linear regression using stochastic gradient descent

    Parameters:
    y: The true values
    tx: The data
    initial_w: The initial weights
    max_iters: Max number of gradient descent iterations
    gamma: Gamma (learning rate)

    Returns:
    w: The final weights
    loss: The final loss
    """
    # Define parameters to store w and loss
    w = initial_w

    for n_iter in range(max_iters):
        minibatch = np.random.choice(tx.shape[0], 1)

        minibatch_tx = tx[minibatch]
        minibatch_y = y[minibatch]

        gradient = compute_gradient_mse(minibatch_y, minibatch_tx, w)
        loss = compute_loss_mse(minibatch_y, minibatch_tx, w)

        w = w - gamma * gradient

    loss = compute_loss_mse(y, tx, w)

    return w, loss


def ridge_regression(y, tx, lambda_):
    """
    Compute the ridge regression using normal equations

    Parameters:
    y: The true values
    tx: The data
    lambda_: lambda

    Returns:
    w: The computed weights
    mse: The mean square error loss
    """
    regularizer = 2 * y.shape[0] * lambda_ * np.identity(tx.shape[1])

    A = tx.T @ tx + regularizer
    b = tx.T @ y
    
    w = np.linalg.solve(A, b)
    mse = compute_mse(y, tx, w)

    return w, mse


def least_squares(y, tx):
    """
    Compute the least squares regression using normal equations

    Parameters:
    y: The true values
    tx: The data

    Returns:
    w: The computed weights
    mse: The mean square error loss
    """
    A = tx.T @ tx
    b = tx.T @ y
    
    w = np.linalg.solve(A, b)
    mse = compute_mse(y, tx, w)

    return w, mse


# Logistic
def sigmoid(t):
    """
    Apply sigmoid fuction

    Parameters:
    t: The argument we want to apply sigmoid on

    Returns:
    sigmoid(t)
    """
    sigmoid_t = (np.exp(t)) / (1 + np.exp(t))

    return sigmoid_t

def compute_loss_logistic(y, tx, w):
    """
    Compute the loss by negative log likelihood

    Parameters:
    y: The true values
    tx: The data
    w: The weights

    Returns:
    loss: The loss by negative log likelihood
    """
    exp = np.exp(tx @ w)
    log = np.log(1 + exp)
    s = np.sum(log)

    loss = s - y.T @ tx @ w

    return loss

def compute_gradient_logistic(y, tx, w):
    """
    Compute the gradient of the loss by negative log likelihood

    Parameters:
    y: The true values
    tx: The data
    w: The weights
    """
    gradient = tx.T @ (sigmoid(tx @ w) -y)

    return gradient


def logistic_regression(y, tx, initial_w, max_iters, gamma):
    """
    Compute the logistic regression using gradient descent

    Parameters:
    y: The true values
    tx: The data
    initial_w: The initial weights
    max_iters: The max number of iterations
    gamma: Gamma (learning rate)

    Returns:
    w: The final weights
    loss: The final loss by negative log likelihood
    """
    # init parameters
    threshold = 1e-8

    w = initial_w
    loss = compute_loss_logistic(y, tx, w)

    # start the logistic regression
    for iter in range(max_iter):
        gradient = compute_gradient_logistic(y, tx, w)

        w = w - gamma * gradient

        new_loss = compute_loss_logistic(y, tx, w)

        if np.abs(loss - new_loss) < threshold:
            loss = new_loss
            break

        loss = new_loss

    return w, loss

