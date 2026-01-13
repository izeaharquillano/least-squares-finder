def get_ls_xhat(A, b):
  A = np.array(A, dtype=float)
  b = np.array(b, dtype=float)
  return np.linalg.inv(A.T @ A) @ A.T @ b
