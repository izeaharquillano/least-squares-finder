import numpy as np


def get_ls_xhat(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    return np.linalg.pinv(A.T @ A) @ A.T @ b

def get_ls_error(A, b, x_hat):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    x_hat = np.array(x_hat, dtype=float)
    
    prediction = A @ x_hat

    ls_error = np.linalg.norm(b - prediction)
    
    return ls_error 
   