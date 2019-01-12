import math
import unittest
import logging
from .ode_step import *
import logging
import numpy as np


class TestLobattoHardcodedCorrespondenceBetweenMethods(unittest.TestCase):
    def test_IIICstar_correspondence_IIIC_hardcoded(self):
        for order in range(2, 4):
            a_first, b_first, c_first = Lobatto.hardcoded_butcher_tableu(
                order, Lobatto.IIIC
            )
            a_second, b_second, c_second = Lobatto.hardcoded_butcher_tableu(
                order, Lobatto.IIICstar
            )
            s = len(c_first)
            condition = dict()
            condition["first"] = np.ndarray((s, s))
            condition["second"] = np.ndarray((s, s))
            condition["neighbor"] = np.ndarray((s, s))
            for i in range(s):
                for j in range(s):
                    # Don't know which interpretation is correct...
                    condition["first"][i][j] = (
                        b_first[i] * a_second[i][j]
                        + b_first[j] * a_first[j][i]
                        - b_first[i] * b_first[j]
                    )
                    condition["second"][i][j] = (
                        b_second[i] * a_second[i][j]
                        + b_second[j] * a_first[j][i]
                        - b_second[i] * b_second[j]
                    )
                    condition["neighbor"][i][j] = (
                        b_second[i] * a_second[i][j]
                        + b_first[j] * a_first[j][i]
                        - b_second[i] * b_first[j]
                    )
            np.testing.assert_almost_equal(
                condition["first"], np.zeros((s, s)), decimal=2
            )
            np.testing.assert_almost_equal(
                condition["second"], np.zeros((s, s)), decimal=2
            )
            np.testing.assert_almost_equal(
                condition["neighbor"], np.zeros((s, s)), decimal=2
            )

    def test_IIIB_correspondence_IIIA_hardcoded(self):
        for order in range(2, 4):
            a_first, b_first, c_first = Lobatto.hardcoded_butcher_tableu(
                order, Lobatto.IIIA
            )
            a_second, b_second, c_second = Lobatto.hardcoded_butcher_tableu(
                order, Lobatto.IIIB
            )
            s = len(c_first)
            condition = dict()
            condition["first"] = np.ndarray((s, s))
            condition["second"] = np.ndarray((s, s))
            condition["neighbor"] = np.ndarray((s, s))
            for i in range(s):
                for j in range(s):
                    # Don't know which interpretation is correct...
                    condition["first"][i][j] = (
                        b_first[i] * a_second[i][j]
                        + b_first[j] * a_first[j][i]
                        - b_first[i] * b_first[j]
                    )
                    condition["second"][i][j] = (
                        b_second[i] * a_second[i][j]
                        + b_second[j] * a_first[j][i]
                        - b_second[i] * b_second[j]
                    )
                    condition["neighbor"][i][j] = (
                        b_second[i] * a_second[i][j]
                        + b_first[j] * a_first[j][i]
                        - b_second[i] * b_first[j]
                    )
            np.testing.assert_almost_equal(
                condition["first"], np.zeros((s, s)), decimal=2
            )
            np.testing.assert_almost_equal(
                condition["second"], np.zeros((s, s)), decimal=2
            )
            np.testing.assert_almost_equal(
                condition["neighbor"], np.zeros((s, s)), decimal=2
            )


class TestLobattoEstimateCorrespondenceBetweenMethods(unittest.TestCase):
    def test_IIICstar_correspondence_IIIC(self):
        for order in range(3, 5):
            a_first, b_first, c_first = Lobatto.estimate_butcher_tableu(
                order, Lobatto.IIIC
            )
            a_second, b_second, c_second = Lobatto.estimate_butcher_tableu(
                order, Lobatto.IIICstar
            )
            s = len(c_first)
            condition = dict()
            condition["first"] = np.ndarray((s, s))
            condition["second"] = np.ndarray((s, s))
            condition["neighbor"] = np.ndarray((s, s))
            for i in range(s):
                for j in range(s):
                    # Don't know which interpretation is correct...
                    condition["first"][i][j] = (
                        b_first[i] * a_second[i][j]
                        + b_first[j] * a_first[j][i]
                        - b_first[i] * b_first[j]
                    )
                    condition["second"][i][j] = (
                        b_second[i] * a_second[i][j]
                        + b_second[j] * a_first[j][i]
                        - b_second[i] * b_second[j]
                    )
                    condition["neighbor"][i][j] = (
                        b_second[i] * a_second[i][j]
                        + b_first[j] * a_first[j][i]
                        - b_second[i] * b_first[j]
                    )
            np.testing.assert_almost_equal(
                condition["first"], np.zeros((s, s)), decimal=2
            )
            np.testing.assert_almost_equal(
                condition["second"], np.zeros((s, s)), decimal=2
            )
            np.testing.assert_almost_equal(
                condition["neighbor"], np.zeros((s, s)), decimal=2
            )

    def test_IIIB_correspondence_IIIA(self):
        for order in range(3, 5):
            a_first, b_first, c_first = Lobatto.estimate_butcher_tableu(
                order, Lobatto.IIIA
            )
            a_second, b_second, c_second = Lobatto.estimate_butcher_tableu(
                order, Lobatto.IIIB
            )
            s = len(c_first)
            condition = dict()
            condition["first"] = np.ndarray((s, s))
            condition["second"] = np.ndarray((s, s))
            condition["neighbor"] = np.ndarray((s, s))
            for i in range(s):
                for j in range(s):
                    # Don't know which interpretation is correct...
                    condition["first"][i][j] = (
                        b_first[i] * a_second[i][j]
                        + b_first[j] * a_first[j][i]
                        - b_first[i] * b_first[j]
                    )
                    condition["second"][i][j] = (
                        b_second[i] * a_second[i][j]
                        + b_second[j] * a_first[j][i]
                        - b_second[i] * b_second[j]
                    )
                    condition["neighbor"][i][j] = (
                        b_second[i] * a_second[i][j]
                        + b_first[j] * a_first[j][i]
                        - b_second[i] * b_first[j]
                    )
            np.testing.assert_almost_equal(
                condition["first"], np.zeros((s, s)), decimal=2
            )
            np.testing.assert_almost_equal(
                condition["second"], np.zeros((s, s)), decimal=2
            )
            np.testing.assert_almost_equal(
                condition["neighbor"], np.zeros((s, s)), decimal=2
            )


class TestLobattoEstimateApproximatesHardcoded(unittest.TestCase):
    def test_IIIA(self):
        version = Lobatto.IIIA
        for order in [2, 3, 4]:
            [
                np.testing.assert_allclose(actual, desired, atol=1e-2, rtol=1e-2)
                for actual, desired in zip(
                    Lobatto.estimate_butcher_tableu(order, version),
                    Lobatto.hardcoded_butcher_tableu(order, version),
                )
            ]

    def test_IIIB(self):
        version = Lobatto.IIIB
        for order in [2, 3, 4]:
            [
                np.testing.assert_allclose(actual, desired, atol=1e-2, rtol=1e-2)
                for actual, desired in zip(
                    Lobatto.estimate_butcher_tableu(order, version),
                    Lobatto.hardcoded_butcher_tableu(order, version),
                )
            ]

    def test_IIIC(self):
        version = Lobatto.IIIC
        for order in [2, 3, 4, 5]:
            [
                np.testing.assert_allclose(actual, desired, atol=1e-2, rtol=1e-2)
                for actual, desired in zip(
                    Lobatto.estimate_butcher_tableu(order, version),
                    Lobatto.hardcoded_butcher_tableu(order, version),
                )
            ]

    def test_IIICstar(self):
        version = Lobatto.IIICstar
        for order in [2, 3]:
            [
                np.testing.assert_allclose(actual, desired, atol=1e-2, rtol=1e-2)
                for actual, desired in zip(
                    Lobatto.estimate_butcher_tableu(order, version),
                    Lobatto.hardcoded_butcher_tableu(order, version),
                )
            ]


class TestRungeKutta(unittest.TestCase):
    def test_implicit_runge_kutta(self):
        a, b, c = Lobatto.estimate_butcher_tableu(4, Lobatto.IIIC)

        Ks = np.hstack((np.random.uniform(-5, 0, 5), np.random.uniform(0, 5, 5)))
        for K in Ks:

            def F(t, y):
                return K * y

            t = [0]
            y = [1]
            expected_y = [1]
            delta_t = 0.001
            max_t = 2.0
            for i in range(0, int(max_t / delta_t)):
                y.append(RungeKutta(F, t[-1], y[-1], a, b, c)(delta_t))
                t.append(t[-1] + delta_t)
                expected_y.append(np.exp(K * t[-1]))
                error_estimate = expected_y[-1] - y[-1]
                np.testing.assert_allclose(
                    y[-1],
                    expected_y[-1],
                    err_msg=f"K={K} e={error_estimate} h={delta_t} log_h(e)={math.log(abs(error_estimate if error_estimate else np.nextafter(error_estimate,error_estimate+1)),delta_t)} [t={t[-1]}, i={i}/{int(max_t/delta_t)}]",
                )

    def test_explicit_runge_kutta(self):
        # https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods#Use
        """Ralston's method"""
        a = np.array([[0, 0], [2 / 3, 0]])
        b = np.array([1 / 4, 3 / 4])
        c = np.array([0, 2 / 3])

        def F(t, y):
            return np.tan(y) + 1

        t = [1]
        y = [1]
        delta_t = 0.025
        for i in range(0, 4):
            y.append(RungeKutta(F, t[-1], y[-1], a, b, c)(delta_t))
            t.append(t[-1] + delta_t)
        expected_t = [1, 1.025, 1.05, 1.075, 1.1]
        expected_y = [1, 1.066_869_388, 1.141_332_181, 1.227_417_567, 1.335_079_087]

        np.testing.assert_almost_equal(t, expected_t)
        np.testing.assert_almost_equal(y, expected_y)


if __name__ == "__main__":
    unittest.main()

