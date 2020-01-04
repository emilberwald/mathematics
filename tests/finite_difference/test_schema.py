import numpy as np
import pytest

from mathematics.finite_difference.schema import *


class TestStencilPoints:
    def test_one_dimensional(self):
        """
		Taken from https://en.wikipedia.org/wiki/Finite_difference_coefficient#Arbitrary_stencil_points
		:return:
		"""

        weights = one_dimensional_schema([-3, -2, -1, 0, 1], 4)
        np.testing.assert_allclose(weights, [1, -4, 6, -4, 1])

    def test_fornberg(self):
        weights = fornberg(4, 0, (-4, -3, -2, -1, 0, 1, 2, 3, 4))
        pass
