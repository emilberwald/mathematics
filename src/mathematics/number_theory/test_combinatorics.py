import unittest
import pytest
import itertools
from parameterized import parameterized
from sympy import symbols
import numpy as np
from mathematics.number_theory.combinatorics import *


class TestPermutation(unittest.TestCase):
    @pytest.mark.timeout(1)
    def test_equivalence_of_parity_methods(self):
        permutation = np.random.permutation(range(0, 10))
        parities = [parity(permutation, method) for method in list(ParityMethod)]
        self.assertEqual(len(set(parities)), 1)

    @parameterized.expand(
        [
            (method, permutation, desired)
            for method in list(ParityMethod)
            for permutation, desired in zip([range(0, 10), [3, 4, 5, 2, 1]], [1, -1])
        ]
    )
    @pytest.mark.timeout(1)
    def test_parity_methods(self, method, permutation, desired):
        self.assertEqual(parity(permutation, method), desired)

    @parameterized.expand(
        [
            ([1, 2, 3, 4], [0, 0, 0, 0]),
            ([2, 1, 3, 4], [1, 0, 0, 0]),
            ([1, 3, 2, 4], [0, 1, 0, 0]),
            ([3, 1, 2, 4], [1, 1, 0, 0]),
            ([2, 3, 1, 4], [2, 0, 0, 0]),
            ([3, 2, 1, 4], [2, 1, 0, 0]),
            ([1, 2, 4, 3], [0, 0, 1, 0]),
            ([2, 1, 4, 3], [1, 0, 1, 0]),
            ([1, 4, 2, 3], [0, 1, 1, 0]),
            ([4, 1, 2, 3], [1, 1, 1, 0]),
            ([2, 4, 1, 3], [2, 0, 1, 0]),
            ([4, 2, 1, 3], [2, 1, 1, 0]),
            ([1, 3, 4, 2], [0, 2, 0, 0]),
            ([3, 1, 4, 2], [1, 2, 0, 0]),
            ([1, 4, 3, 2], [0, 2, 1, 0]),
            ([4, 1, 3, 2], [1, 2, 1, 0]),
            ([3, 4, 1, 2], [2, 2, 0, 0]),
            ([4, 3, 1, 2], [2, 2, 1, 0]),
            ([2, 3, 4, 1], [3, 0, 0, 0]),
            ([3, 2, 4, 1], [3, 1, 0, 0]),
            ([2, 4, 3, 1], [3, 0, 1, 0]),
            ([4, 2, 3, 1], [3, 1, 1, 0]),
            ([3, 4, 2, 1], [3, 2, 0, 0]),
            ([4, 3, 2, 1], [3, 2, 1, 0]),
        ]
    )  # https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)
    @pytest.mark.timeout(1)
    def test_inversion_vector(self, permutation, desired):
        self.assertEqual(
            inversion_vector(permutation),
            desired,
            msg="{0}".format((permutation, desired)),
        )

    @parameterized.expand(
        [
            ([1, 2, 3, 4], [0, 0, 0, 0]),
            ([2, 1, 3, 4], [0, 1, 0, 0]),
            ([1, 3, 2, 4], [0, 0, 1, 0]),
            ([3, 1, 2, 4], [0, 1, 1, 0]),
            ([2, 3, 1, 4], [0, 0, 2, 0]),
            ([3, 2, 1, 4], [0, 1, 2, 0]),
            ([1, 2, 4, 3], [0, 0, 0, 1]),
            ([2, 1, 4, 3], [0, 1, 0, 1]),
            ([1, 4, 2, 3], [0, 0, 1, 1]),
            ([4, 1, 2, 3], [0, 1, 1, 1]),
            ([2, 4, 1, 3], [0, 0, 2, 1]),
            ([4, 2, 1, 3], [0, 1, 2, 1]),
            ([1, 3, 4, 2], [0, 0, 0, 2]),
            ([3, 1, 4, 2], [0, 1, 0, 2]),
            ([1, 4, 3, 2], [0, 0, 1, 2]),
            ([4, 1, 3, 2], [0, 1, 1, 2]),
            ([3, 4, 1, 2], [0, 0, 2, 2]),
            ([4, 3, 1, 2], [0, 1, 2, 2]),
            ([2, 3, 4, 1], [0, 0, 0, 3]),
            ([3, 2, 4, 1], [0, 1, 0, 3]),
            ([2, 4, 3, 1], [0, 0, 1, 3]),
            ([4, 2, 3, 1], [0, 1, 1, 3]),
            ([3, 4, 2, 1], [0, 0, 2, 3]),
            ([4, 3, 2, 1], [0, 1, 2, 3]),
        ]
    )  # https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)
    @pytest.mark.timeout(1)
    def test_left_inversion_count(self, permutation, desired):
        self.assertEqual(
            left_inversion_count(permutation),
            desired,
            msg="{0}".format((permutation, desired)),
        )

    @parameterized.expand(
        [
            ([1, 2, 3, 4], [0, 0, 0, 0]),
            ([2, 1, 3, 4], [1, 0, 0, 0]),
            ([1, 3, 2, 4], [0, 1, 0, 0]),
            ([3, 1, 2, 4], [2, 0, 0, 0]),
            ([2, 3, 1, 4], [1, 1, 0, 0]),
            ([3, 2, 1, 4], [2, 1, 0, 0]),
            ([1, 2, 4, 3], [0, 0, 1, 0]),
            ([2, 1, 4, 3], [1, 0, 1, 0]),
            ([1, 4, 2, 3], [0, 2, 0, 0]),
            ([4, 1, 2, 3], [3, 0, 0, 0]),
            ([2, 4, 1, 3], [1, 2, 0, 0]),
            ([4, 2, 1, 3], [3, 1, 0, 0]),
            ([1, 3, 4, 2], [0, 1, 1, 0]),
            ([3, 1, 4, 2], [2, 0, 1, 0]),
            ([1, 4, 3, 2], [0, 2, 1, 0]),
            ([4, 1, 3, 2], [3, 0, 1, 0]),
            ([3, 4, 1, 2], [2, 2, 0, 0]),
            ([4, 3, 1, 2], [3, 2, 0, 0]),
            ([2, 3, 4, 1], [1, 1, 1, 0]),
            ([3, 2, 4, 1], [2, 1, 1, 0]),
            ([2, 4, 3, 1], [1, 2, 1, 0]),
            ([4, 2, 3, 1], [3, 1, 1, 0]),
            ([3, 4, 2, 1], [2, 2, 1, 0]),
            ([4, 3, 2, 1], [3, 2, 1, 0]),
        ]
    )  # https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)
    @pytest.mark.timeout(1)
    def test_right_inversion_count(self, permutation, desired):
        self.assertEqual(
            right_inversion_count(permutation),
            desired,
            msg="{0}".format((permutation, desired)),
        )

    @parameterized.expand(
        itertools.product(
            [
                permutation_to_adjacent_transpositions,
                permutation_to_cycles,
                permutation_to_transpositions,
            ],
            [[7, 13, 4, 5]],
        )
    )
    @pytest.mark.timeout(1)
    def test_nontcontiguous_sequence_raises_exception(self, method, not_permutation):
        self.assertRaises(IndexError, lambda: method(not_permutation))

    @parameterized.expand(
        [
            ([2, 5, 4, 3, 1], {(1, 2, 5), (3, 4)}),
            ([4, 2, 7, 6, 5, 8, 1, 3], {(1, 4, 6, 8, 3, 7), (2,), (5,)}),
            ([4, 5, 7, 6, 8, 2, 1, 3], {(1, 4, 6, 2, 5, 8, 3, 7)}),
        ]
    )
    @pytest.mark.timeout(1)
    def test_permutation_to_cycle(self, permutation, desired):
        # assumes canonical order with min first is used
        actual = permutation_to_cycles(permutation)
        self.assertEqual(actual, desired)

    @parameterized.expand(
        [
            ([1, 2, 3, 4], set()),
            ([2, 1, 3, 4], {(1, 2)}),
            ([3, 2, 1, 4], {(1, 3)}),
            ([4, 2, 3, 1], {(1, 4)}),
            ([1, 3, 2, 4], {(2, 3)}),
            ([1, 4, 3, 2], {(2, 4)}),
            ([1, 2, 4, 3], {(3, 4)}),
            ([2, 1, 4, 3], {(1, 2), (3, 4)}),
        ]
    )
    @pytest.mark.timeout(1)
    def test_permutation_to_transpositions(self, permutation, desired):
        # assumes canonical order with min first is used
        actual = permutation_to_transpositions(permutation)
        self.assertEqual(actual, desired)


if __name__ == "__main__":
    unittest.main()
