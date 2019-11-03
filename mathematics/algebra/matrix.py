import functools
import itertools
import operator

from ..number_theory.combinatorics import parity


class Matrix:
    @staticmethod
    def determinant(A):
        return functools.reduce(
            operator.add,
            [
                (parity(permutation) if len(permutation) > 1 else 1)
                * functools.reduce(
                    operator.mul,
                    [ai[permutation_i] for ai, permutation_i in zip(A, permutation)],
                )
                for permutation in itertools.permutations(range(0, len(A)))
            ],
        )

    @staticmethod
    def submatrix(A, exclude_i, exclude_j):
        return [
            [aj for j, aj in enumerate(ai) if j != exclude_j]
            for i, ai in enumerate(A)
            if i != exclude_i
        ]

    @staticmethod
    def minor(A, i, j):
        return Matrix.determinant(Matrix.submatrix(A, i, j))

    @staticmethod
    def cofactor(A, i, j):
        return (-1) ** (i + j) * Matrix.minor(A, i, j)

    @staticmethod
    def inverse(A):
        return [
            [
                Matrix.determinant(A) ** (-1) * Matrix.cofactor(A, j, i)
                for j, aj in enumerate(ai)
            ]
            for i, ai in enumerate(A)
        ]
