import unittest
from .multi_index import *


class test_multi_index(unittest.TestCase):
    def test_factorial(self):
        a = multi_index((1, 2, 3))
        self.assertAlmostEqual(a.factorial(), 12)
