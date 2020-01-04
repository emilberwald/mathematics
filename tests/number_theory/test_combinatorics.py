import itertools
from math import gamma

import numpy as np
import pytest
from pytest import raises

from mathematics.number_theory.combinatorics import *
from .. import name_func


class TestRiffleShuffles:
    def test_riffle_shuffles(self):
        """
		https://en.wikipedia.org/wiki/Shuffle_algebra#Shuffle_product
		"""

        def expected_nof_shuffles(m, n):
            return int(gamma(len(m) + len(n) + 1) / (gamma(len(m) + 1) * gamma(len(n) + 1)))

        m = "ab"
        n = "xy"
        m_w_n = riffle_shuffles(m, n)
        assert "abxy" in m_w_n
        assert "axby" in m_w_n
        assert "xaby" in m_w_n
        assert "axyb" in m_w_n
        assert "xayb" in m_w_n
        assert "xyab" in m_w_n
        assert len(m_w_n) == expected_nof_shuffles(m, n)
        m = "012"
        n = "34"
        m_w_n = riffle_shuffles(m, n)
        assert len(m_w_n) == expected_nof_shuffles(m, n)


class TestPermutation:
    @pytest.mark.timeout(1)
    def test_equivalence_of_parity_methods(self):
        permutation = np.random.permutation(range(0, 10))
        parities = [parity(permutation, method) for method in list(ParityMethod)]
        assert len(set(parities)) == 1

    @pytest.mark.parametrize(
        "method,permutation,desired",
        [
            (method, permutation, desired)
            for method in list(ParityMethod)
            for permutation, desired in zip([range(0, 10), [3, 4, 5, 2, 1]], [1, -1])
        ],
        ids=name_func,
    )
    @pytest.mark.timeout(1)
    def test_parity_methods(self, method, permutation, desired):
        assert parity(permutation, method) == desired

    @pytest.mark.parametrize(
        "permutation,desired",
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
        ],
        ids=name_func,
    )  # https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)
    @pytest.mark.timeout(1)
    def test_inversion_vector(self, permutation, desired):
        assert inversion_vector(permutation) == desired

    @pytest.mark.parametrize(
        "permutation,desired",
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
        ],
        ids=name_func,
    )  # https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)
    @pytest.mark.timeout(1)
    def test_left_inversion_count(self, permutation, desired):
        assert left_inversion_count(permutation) == desired

    @pytest.mark.parametrize(
        "permutation,desired",
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
        ],
        ids=name_func,
    )  # https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)
    @pytest.mark.timeout(1)
    def test_right_inversion_count(self, permutation, desired):
        assert right_inversion_count(permutation) == desired

    @pytest.mark.parametrize(
        "method,not_permutation",
        itertools.product(
            [permutation_to_adjacent_transpositions, permutation_to_cycles, permutation_to_transpositions,],
            [[7, 13, 4, 5]],
        ),
        ids=name_func,
    )
    @pytest.mark.timeout(1)
    def test_nontcontiguous_sequence_raises_exception(self, method, not_permutation):
        with raises(IndexError):
            method(not_permutation)

    @pytest.mark.parametrize(
        "permutation, desired",
        [
            ([2, 5, 4, 3, 1], {(1, 2, 5), (3, 4)}),
            ([4, 2, 7, 6, 5, 8, 1, 3], {(1, 4, 6, 8, 3, 7), (2,), (5,)}),
            ([4, 5, 7, 6, 8, 2, 1, 3], {(1, 4, 6, 2, 5, 8, 3, 7)}),
        ],
        ids=name_func,
    )
    @pytest.mark.timeout(1)
    def test_permutation_to_cycle(self, permutation, desired):
        # assumes canonical order with min first is used
        actual = permutation_to_cycles(permutation)
        assert actual == desired

    @pytest.mark.parametrize(
        "permutation,desired",
        [
            ([1, 2, 3, 4], set()),
            ([2, 1, 3, 4], {(1, 2)}),
            ([3, 2, 1, 4], {(1, 3)}),
            ([4, 2, 3, 1], {(1, 4)}),
            ([1, 3, 2, 4], {(2, 3)}),
            ([1, 4, 3, 2], {(2, 4)}),
            ([1, 2, 4, 3], {(3, 4)}),
            ([2, 1, 4, 3], {(1, 2), (3, 4)}),
        ],
        ids=name_func,
    )
    @pytest.mark.timeout(1)
    def test_permutation_to_transpositions(self, permutation, desired):
        # assumes canonical order with min first is used
        actual = permutation_to_transpositions(permutation)
        assert actual == desired
