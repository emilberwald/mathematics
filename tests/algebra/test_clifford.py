import functools
import itertools
import operator

import numpy as np
import pytest

from mathematics.algebra.create import *
from mathematics.tools.decorators import timeout


class TestClifford:
    @staticmethod
    def normalize(clifford):
        return {key: value.expand() for key, value in clifford.items()}

    @timeout(handler=lambda: pytest.skip("timeout"), seconds=10)
    def test_exterior_algebra_cross_and_triple_product(self):
        # https://en.wikipedia.org/wiki/Exterior_algebra#Cross_and_triple_products
        basis = tuple(sympy.symbols("e_{0:3}"))

        def scalar_product(ei, ej):
            return 0

        Multivector = create_clifford("Exterior Algebra", scalar_product)

        e1 = Multivector({basis[0]: 1})
        e2 = Multivector({basis[1]: 1})
        e3 = Multivector({basis[2]: 1})

        u1, u2, u3 = sympy.symbols("u_{0:3}")
        u = e1 * u1 + e2 * u2 + e3 * u3
        v1, v2, v3 = sympy.symbols("v_{0:3}")
        v = e1 * v1 + e2 * v2 + e3 * v3
        w1, w2, w3 = sympy.symbols("w_{0:3}")
        w = e1 * w1 + e2 * w2 + e3 * w3

        lhs = TestClifford.normalize(u * v)
        rhs = TestClifford.normalize(
            e1 * e2 * (u1 * v2 - u2 * v1) + e3 * e1 * (u3 * v1 - u1 * v3) + e2 * e3 * (u2 * v3 - u3 * v2)
        )
        assert len(lhs) == len(rhs) == 3
        assert lhs == rhs

        lhs = TestClifford.normalize(u * v * w)
        rhs = TestClifford.normalize(
            e1 * e2 * e3 * (u1 * v2 * w3 + u2 * v3 * w1 + u3 * v1 * w2 - u1 * v3 * w2 - u2 * v1 * w3 - u3 * v2 * w1)
        )
        assert len(lhs) == len(rhs) == 1
        assert lhs == rhs

    # @timeout(handler=lambda: pytest.skip("timeout"), seconds=1)
    def test_exterior_algebra_areas_in_the_plane(self):
        # https://en.wikipedia.org/wiki/Exterior_algebra#Areas_in_the_plane
        basis = tuple(sympy.symbols("e_{0:3}"))

        def scalar_product(ei, ej):
            return 0

        Multivector = create_clifford("Exterior Algebra", scalar_product)
        Zero = Multivector({})
        e1 = Multivector({basis[0]: 1})
        e2 = Multivector({basis[1]: 1})

        a = sympy.Symbol("a")
        b = sympy.Symbol("b")
        c = sympy.Symbol("c")
        d = sympy.Symbol("d")

        v = e1 * a + e2 * b
        w = e1 * c + e2 * d

        assert e1 * e1 == e2 * e2 == Zero
        assert e2 * e1 == -e1 * e2
        assert (
            v * w
            == e1 * e1 * a * c + e1 * e2 * a * d + e2 * e1 * b * c + e2 * e2 * b * d
            == e1 * e2 * a * d + e2 * e1 * b * c
            == e1 * e2 * (a * d - b * c)
        )

    @timeout(handler=lambda: pytest.skip("timeout"), seconds=5)
    def test_quaternions(self):
        # https://en.wikipedia.org/wiki/Clifford_algebra#Quaternions
        basis = tuple(sympy.symbols("e_{0:3}"))

        def scalar_product(ei, ej):
            return (
                -(1 if ei in basis else abs(ei))
                * (1 if ej in basis else abs(ej))
                * (1 if (ei / abs(ei)) == (ej / abs(ej)) else 0)
            )

        Quaternion = create_clifford("Quaternion Algebra", scalar_product)
        I = Quaternion({(): 1})
        e1 = Quaternion({basis[0]: 1})
        e2 = Quaternion({basis[1]: 1})
        e3 = Quaternion({basis[2]: 1})
        assert e1 * e1 + e1 * e1 == e2 * e2 + e2 * e2 == e3 * e3 + e3 * e3 == -2 * I

        assert e2 * e3 == -e3 * e2
        assert e3 * e1 == -e1 * e3
        assert e1 * e2 == -e2 * e1

        assert e1 * e1 == e2 * e2 == e3 * e3 == -I

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
