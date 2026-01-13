import numpy as np


def get_ls_xhat(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    return np.linalg.pinv(A.T @ A) @ A.T @ b

def get_ls_error(A, b, x):
    
    prediction = np.dot(A, x)
    ls_error = np.sum((b - prediction)**2)

    return ls_error