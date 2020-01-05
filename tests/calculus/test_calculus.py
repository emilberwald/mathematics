import numpy as np
import pytest
from sympy import Derivative, symbols

from mathematics.tools.decorators import timeout

from mathematics.calculus.calculus import *


class TestCurl:
    @pytest.mark.skip(reason="[TODO]")
    @timeout(seconds=1.0)
    def test_curl(self):
        tensor = np.array(symbols("A B C"))

        def derivative(tensor):
            return np.array([Derivative(tensor, ei) for ei in symbols("x y z")])

        metric_tensor = np.diag([1, 1, 1])
        curl_tensor = curl(derivative, metric_tensor, tensor)
        expected_curl_tensor = tensor  # TODO: Find out what the expected value is
        for a, b in zip(np.ravel(curl_tensor), np.ravel(expected_curl_tensor)):
            assert a == b
