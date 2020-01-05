import itertools

import numpy as np
import pytest
from pytest import raises

from mathematics.algebra.matrix import *
from .. import name_func


class Test2:
    @pytest.mark.parametrize("permutation_scheme", [row_pivoting, complete_pivoting, None], ids=name_func)
    @pytest.mark.parametrize("elimination_scheme", [doolittle_scheme, gauss_jordan_scheme], ids=name_func)
    def test_2_16(self, permutation_scheme, elimination_scheme):
        f = Matrix([[1.0, 2.0, 2.0], [4.0, 4.0, 2.0], [4.0, 6.0, 4.0]])
        fx = [3.0, 6.0, 10.0]
        x = f.inversed(fx, methods=(arg for arg in (permutation_scheme, elimination_scheme) if arg))
        assert x == [-1.0, 3.0, -1.0]


def is_upper_triangular(A):
    for row_no, row in enumerate(A):
        for col_no, col in enumerate(row):
            if (col_no < row_no) and col != 0:
                return False
    return True


def is_lower_triangular(A):
    for row_no, row in enumerate(A):
        for col_no, col in enumerate(row):
            if (row_no < col_no) and col != 0:
                return False
    return True


class TestGaussian:
    @pytest.mark.parametrize("permutation_scheme", [row_pivoting, complete_pivoting, None], ids=name_func)
    @pytest.mark.parametrize("elimination_scheme", [doolittle_scheme, gauss_jordan_scheme], ids=name_func)
    @pytest.mark.parametrize("rescale_scheme", [reduced_row_echelon, None], ids=name_func)
    def test_gaussian_elimination(self, permutation_scheme, elimination_scheme, rescale_scheme):
        f = [
            [1.0, 3.0, 1.0],
            [1.0, 1.0, -1.0],
            [3.0, 11.0, 5.0],
        ]
        U, R, C = Matrix(f).gaussian_elimination(
            permutation_scheme=permutation_scheme, elimination_scheme=elimination_scheme, rescale_scheme=rescale_scheme,
        )
        assert is_upper_triangular(U)

    @pytest.mark.parametrize("permutation_scheme", [row_pivoting, complete_pivoting, None], ids=name_func)
    @pytest.mark.parametrize("elimination_scheme", [doolittle_scheme, gauss_jordan_scheme], ids=name_func)
    @pytest.mark.parametrize("rescale_scheme", [reduced_row_echelon, None], ids=name_func)
    def test_2_18(self, permutation_scheme, elimination_scheme, rescale_scheme):
        f = [
            [1.0, 2.0, 2.0],
            [4.0, 4.0, 2.0],
            [4.0, 6.0, 4.0],
        ]
        U, R, C = Matrix(f).gaussian_elimination(
            permutation_scheme=permutation_scheme, elimination_scheme=elimination_scheme, rescale_scheme=rescale_scheme,
        )
        assert is_upper_triangular(U)

    @pytest.mark.parametrize("permutation_scheme", [row_pivoting, complete_pivoting], ids=name_func)
    @pytest.mark.parametrize("elimination_scheme", [doolittle_scheme, gauss_jordan_scheme], ids=name_func)
    @pytest.mark.parametrize("rescale_scheme", [reduced_row_echelon, None], ids=name_func)
    def test_wide_matrix(self, permutation_scheme, elimination_scheme, rescale_scheme):
        # https://en.wikibooks.org/wiki/Linear_Algebra/Row_Reduction_and_Echelon_Forms
        f = [
            [0, 3, -6, 6, 4, -5],
            [3, -7, 8, -5, 8, 9],
            [3, -9, 12, -9, 6, 15],
        ]
        U, R, C = Matrix(f).gaussian_elimination(
            permutation_scheme=permutation_scheme, elimination_scheme=elimination_scheme, rescale_scheme=rescale_scheme,
        )
        assert is_upper_triangular(U)

    @pytest.mark.parametrize("permutation_scheme", [row_pivoting, complete_pivoting, None], ids=name_func)
    @pytest.mark.parametrize("elimination_scheme", [doolittle_scheme, gauss_jordan_scheme], ids=name_func)
    @pytest.mark.parametrize("rescale_scheme", [reduced_row_echelon, None], ids=name_func)
    def test_tall_matrix(self, permutation_scheme, elimination_scheme, rescale_scheme):
        f = [
            [2, 3, 13, 16],
            [16, 8, 0, -1],
            [11, 16, 15, 9],
            [8, 7, 16, 16],
            [15, 14, 10, 6],
        ]
        U, R, C = Matrix(f).gaussian_elimination(
            permutation_scheme=row_pivoting, elimination_scheme=gauss_jordan_scheme, rescale_scheme=reduced_row_echelon,
        )
        assert is_upper_triangular(U)


class TestMatrix:
    @pytest.mark.timeout(1)
    def test_cofactor(self):
        # https://en.wikipedia.org/wiki/Minor_(linear_algebra)#First_minors
        A = [[1, 4, 7], [3, 0, 5], [-1, 9, 11]]
        submatrix23 = [[1, 4], [-1, 9]]
        minor23 = 13
        cofactor23 = -13
        actualSubmatrix = Matrix.submatrix(A, 1, 2)
        actualMinor = Matrix.minor(A, 1, 2)
        actualCofactor = Matrix.cofactor(A, 1, 2)
        np.testing.assert_allclose(actualSubmatrix, submatrix23)
        np.testing.assert_allclose(actualMinor, minor23)
        np.testing.assert_allclose(actualCofactor, cofactor23)

    @pytest.mark.timeout(1)
    def test_matrix_inverse2x2(self):
        A = [[4, 3], [3, 2]]
        desired = [[-2, 3], [3, -4]]
        actual = Matrix.inverse(A)
        np.testing.assert_allclose(actual, desired)

    @pytest.mark.timeout(1)
    def test_matrix_inverse3x3(self):
        A = [[1, 2, 3], [0, 4, 5], [1, 0, 6]]
        desired = [
            [12.0 / 11, -6.0 / 11, -1.0 / 11],
            [5.0 / 22, 3.0 / 22, -5.0 / 22],
            [-2.0 / 11, 1.0 / 11, 2.0 / 11],
        ]
        actual = Matrix.inverse(A)
        np.testing.assert_allclose(actual, desired)
