import unittest
import pytest
from .multi_index import *


class TestMultiIndex(unittest.TestCase):
    @pytest.mark.timeout(1)
    def test_factorial(self):
        alfa = MultiIndex((1, 2, 3))
        self.assertAlmostEqual(alfa.factorial(), 12)
