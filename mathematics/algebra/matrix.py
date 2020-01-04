import functools as _functools
import itertools as _itertools
import operator as _operator

from ..number_theory.combinatorics import parity


class Matrix:
    @staticmethod
    def determinant(A):
        return _functools.reduce(
            _operator.add,
            [
                (parity(permutation) if len(permutation) > 1 else 1)
                * _functools.reduce(_operator.mul, [ai[permutation_i] for ai, permutation_i in zip(A, permutation)],)
                for permutation in _itertools.permutations(range(0, len(A)))
            ],
        )

    @staticmethod
    def submatrix(A, exclude_i, exclude_j):
        return [[aj for j, aj in enumerate(ai) if j != exclude_j] for i, ai in enumerate(A) if i != exclude_i]

    @staticmethod
    def minor(A, i, j):
        return Matrix.determinant(Matrix.submatrix(A, i, j))

    @staticmethod
    def cofactor(A, i, j):
        return (-1) ** (i + j) * Matrix.minor(A, i, j)

    @staticmethod
    def inverse(A):
        return [
            [Matrix.determinant(A) ** (-1) * Matrix.cofactor(A, j, i) for j, aj in enumerate(ai)]
            for i, ai in enumerate(A)
        ]
