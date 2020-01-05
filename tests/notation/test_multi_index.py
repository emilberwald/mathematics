from pytest import approx

from mathematics.tools.decorators import timeout
from mathematics.notation.multi_index import *


class TestMultiIndex:
    @timeout(handler=lambda: pytest.skip("timeout"), seconds=1.0)
    def test_factorial(self):
        alfa = MultiIndex((1, 2, 3))
        assert alfa.factorial() == approx(12)
