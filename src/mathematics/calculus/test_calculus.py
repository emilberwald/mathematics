import unittest
import pytest
from sympy import symbols, Derivative
import numpy as np
from .calculus import *


class TestCurl(unittest.TestCase):
    @pytest.mark.timeout(1)
    def test_curl(self):
        tensor = np.array(symbols("A B C"))
        derivative = lambda tensor: np.array(
            [Derivative(tensor, ei) for ei in symbols("x y z")]
        )
        metric_tensor = np.diag([1, 1, 1])
        curl_tensor = curl(derivative, metric_tensor, tensor)
        self.assertEqual(
            curl_tensor, tensor, msg="{0}".format(curl_tensor)
        )  # TODO: fix


if __name__ == "__main__":
    unittest.main()
