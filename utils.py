import numpy as np


def subscript(number):
    sub_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return str(number).translate(sub_map)


def split_aug_mat(aug_matrix):
    aug_matrix = np.array(aug_matrix, dtype=float)

    A = aug_matrix[:, :-1]
    b = aug_matrix[:, -1].reshape(-1, 1)

    return A, b
