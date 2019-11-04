import math

import numpy as np
import pytest

from mathematics.tools.decorators import timeout
from mathematics.tools.testing import name_func

from .pointwise_calculus import PointwiseCalculus


class TestPointwiseCalculus:
    # @timeout(seconds=1.0)
    def test_derivation(self):
        def vect(*args):
            return np.asarray(args)

        # https://en.wikipedia.org/wiki/Lie_derivative#Examples
        _phi = lambda x, y: x ** 2 - math.sin(y)
        phi = PointwiseCalculus(lambda p: _phi(*p))
        _X = lambda x, y: vect(-(y ** 2), math.sin(x))
        X = PointwiseCalculus(lambda p: _X(*p))
        Lxphi = X.derivation()(phi)
        _desired_f = lambda x, y: -math.sin(x) * math.cos(y) - 2 * x * y ** 2
        desired_f = PointwiseCalculus(lambda p: _desired_f(*p))
        for x in np.random.rand(2):
            for y in np.random.rand(2):
                actual = Lxphi((x, y))
                desired = desired_f((x, y))
                np.testing.assert_allclose(actual, desired, atol=1e-5, rtol=1e-5)
