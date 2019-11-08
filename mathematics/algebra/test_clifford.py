import itertools
import functools
import operator

import numpy as np
import pytest

from mathematics.algebra.tensor import *
from mathematics.algebra.create import *


class TestClifford:
    # @pytest.mark.timeout(1)
    def test_quaternions(self):
        # https://en.wikipedia.org/wiki/Clifford_algebra#Quaternions
        basis = tuple(sympy.symbols("e_{0:3}"))
        dual_basis = tuple(sympy.symbols("e^{0:3}"))

        def scalar_product(ei, ej):
            return (
                -(1 if ei in basis else abs(ei))
                * (1 if ej in basis else abs(ej))
                * (1 if (ei / abs(ei)) == (ej / abs(ej)) else 0)
            )

        def slot_to_dual(e):
            if e in basis:
                return dual_basis[basis.index(e)]
            if e in dual_basis:
                return basis[dual_basis.index(e)]
            raise NotImplementedError()

        Quaternion = create_clifford("Quaternion", scalar_product)
        I = Quaternion({(): 1})
        e1 = Quaternion({basis[0]: 1})
        e2 = Quaternion({basis[1]: 1})
        e3 = Quaternion({basis[2]: 1})
        assert e1 * e1 + e1 * e1 == -2 * I
        assert e2 * e2 + e2 * e2 == -2 * I
        assert e3 * e3 + e3 * e3 == -2 * I

        assert e2 * e3 == -e3 * e2
        assert e3 * e1 == -e1 * e3
        assert e1 * e2 == -e2 * e1

        assert e1 * e1 == -I
        assert e2 * e2 == -I
        assert e3 * e3 == -I

        i = e2 * e3
        j = e3 * e1
        k = e1 * e2

        assert i * i == e2 * e3 * e2 * e3
        assert i * i == -e2 * e2 * e3 * e3
        assert i * i == -I
        assert i * j == e2 * e3 * e3 * e1
        assert i * j == -e2 * e1
        assert i * j == e1 * e2
        assert i * j == k

        assert i * j * k == e2 * e3 * e3 * e1 * e1 * e2
        assert i * j * k == -I

        pass
