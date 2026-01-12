def split_aug_mat(aug_mat):
    A = aug_mat[:, :-1]
    b = aug_mat[:, -1]
    return A, b


def subscript(number):
    sub_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return str(number).translate(sub_map)
