import numpy as np
from common.util.export import MockCf, List


def compressed_row_sparse_matrix(dense_matrix):
    """
    Convert a dense matrix to its Compressed Row Sparse (CSR) representation.

    :param dense_matrix: 2D list representing a dense matrix
    :return: A tuple containing (values array, column indices array, row pointer array)
    """

    ret: List[list] = [[], [], [0]]
    for i, row in enumerate(dense_matrix):
        ret[2].append(ret[2][-1])
        for j, v in enumerate(row):
            if v != 0:
                ret[0].append(v)
                ret[1].append(j)
                ret[2][-1] += 1
    return ret


def main():
    MockCf(
        compressed_row_sparse_matrix,
        dict(
            case0=dict(
                dense_matrix=[
                    [1, 0, 0, 0],
                    [0, 2, 0, 0],
                    [3, 0, 4, 0],
                    [1, 0, 0, 5],
                ],
                result=[
                    [1, 2, 3, 4, 1, 5],
                    [0, 1, 0, 2, 0, 3],
                    [0, 1, 2, 4, 6],
                ],
            ),
        ),
    ).run()
