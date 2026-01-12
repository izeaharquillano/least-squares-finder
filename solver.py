import numpy as np


def get_ls_xhat(A, b):
    AT = A.T
    ATA = AT @ A
    ATb = AT @ b
    x_hat = np.linalg.solve(ATA, ATb)
    return x_hat


def get_ls_error(A, b, x_hat):
    residual = b - (A @ x_hat)
    return np.linalg.norm(residual)
