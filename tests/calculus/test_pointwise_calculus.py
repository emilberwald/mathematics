import math

import numpy as np
import pytest

from mathematics.tools.decorators import timeout
from .. import name_func

from mathematics.calculus.pointwise_calculus import *


class TestPointwiseCalculus:
    @timeout(handler=lambda: pytest.skip("timeout"), seconds=1.0)
    def test_connection(self):
        def vect(*args):
            return np.asarray(args)

        def g(p):
            def g(x, y, z):
                return vect(1, 1, 1) / z ** 2

            return g(*p)

        g = PointwiseCalculus(g)

        def A(p):
            def A(x, y, z):
                return vect(z, 0, 0)

            return A(*p)

        A = PointwiseCalculus(A)

        def B(p):
            def B(x, y, z):
                return vect(0, z, 0)

            return B(*p)

        B = PointwiseCalculus(B)

        def C(p):
            def C(x, y, z):
                return vect(0, 0, z)

            return C(*p)

        C = PointwiseCalculus(C)
        A.connection(B, g, (vect(1, 0, 0), vect(0, 1, 0), vect(0, 0, 1)))

    @timeout(handler=lambda: pytest.skip("timeout"), seconds=1.0)
    def test_derivation(self):
        def vect(*args):
            return np.asarray(args)

        # https://en.wikipedia.org/wiki/Lie_derivative#Examples
        def phi(p):
            def phi(x, y):
                return x ** 2 - math.sin(y)

            return phi(*p)

        phi = PointwiseCalculus(phi)

        def X(p):
            def X(x, y):
                return vect(-(y ** 2), math.sin(x))

            return X(*p)

        X = PointwiseCalculus(X)

        def desiredLxphi(p):
            def desiredLxphi(x, y):
                return -math.sin(x) * math.cos(y) - 2 * x * y ** 2

            return desiredLxphi(*p)

        desiredLxphi = PointwiseCalculus(desiredLxphi)

        Lxphi = X.derivation()(phi)

        for x in np.random.rand(2):
            for y in np.random.rand(2):
                actual = Lxphi((x, y))
                desired = desiredLxphi((x, y))
                np.testing.assert_allclose(actual, desired, atol=1e-5, rtol=1e-5)
