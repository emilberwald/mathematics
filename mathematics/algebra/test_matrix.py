import itertools

import numpy as _np
import pytest
from pytest import raises

from mathematics.algebra.matrix import *


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
        _np.testing.assert_allclose(actualSubmatrix, submatrix23)
        _np.testing.assert_allclose(actualMinor, minor23)
        _np.testing.assert_allclose(actualCofactor, cofactor23)

    @pytest.mark.timeout(1)
    def test_matrix_inverse2x2(self):
        A = [[4, 3], [3, 2]]
        desired = [[-2, 3], [3, -4]]
        actual = Matrix.inverse(A)
        _np.testing.assert_allclose(actual, desired)

    @pytest.mark.timeout(1)
    def test_matrix_inverse3x3(self):
        A = [[1, 2, 3], [0, 4, 5], [1, 0, 6]]
        desired = [
            [12.0 / 11, -6.0 / 11, -1.0 / 11],
            [5.0 / 22, 3.0 / 22, -5.0 / 22],
            [-2.0 / 11, 1.0 / 11, 2.0 / 11],
        ]
        actual = Matrix.inverse(A)
        _np.testing.assert_allclose(actual, desired)
