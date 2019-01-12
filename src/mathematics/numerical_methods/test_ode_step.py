import math
import unittest
from parameterized import parameterized
import logging
from .ode_step import *
import logging
import numpy as np


def custom_name_func(testcase_func, param_num, param):
    return "_".join(
        [
            parameterized.to_safe_name(x)
            for x in [f"{testcase_func.__name__}", f"{param_num}", f"{param}"]
        ]
    )


class TestLobattoHardcodedFulfillsConstraints(unittest.TestCase):
    @parameterized.expand(
        [
            *[(order, method) for order in (2, 3, 4) for method in (Lobatto.IIIA,)],
            *[(order, method) for order in (2, 3, 4) for method in (Lobatto.IIIB,)],
            *[(order, method) for order in (2, 3, 4, 5) for method in (Lobatto.IIIC,)],
            *[(order, method) for order in (2, 3) for method in (Lobatto.IIICstar,)],
        ],
        testcase_func_name=custom_name_func,
    )
    def test_hardcoded_fulfills_requirements(self, order, method):
        soft_0 = lambda lhs, cmp, rhs: (not (cmp(lhs, rhs))) * np.linalg.norm(lhs - rhs)
        a, b, c = Lobatto.hardcoded_butcher_tableu(order, method)
        constraints = Lobatto.create_constraint_system(method, soft=soft_0)
        actual = constraints(Lobatto.pack(a, b, c))
        expected = np.zeros_like(actual)
        np.testing.assert_allclose(actual, expected, atol=1e-15)


class TestLobattoCorrespondenceBetweenMethods(unittest.TestCase):
    @parameterized.expand(
        [
            *[
                (order, variant, Lobatto.IIIC, Lobatto.IIICstar)
                for order in (2, 3)
                for variant in (Lobatto.hardcoded_butcher_tableu,)
            ],
            *[
                (order, variant, Lobatto.IIIC, Lobatto.IIICstar)
                for order in (2, 3, 4)
                for variant in (Lobatto.estimate_butcher_tableu,)
            ],
            *[
                (order, variant, Lobatto.IIIA, Lobatto.IIIB)
                for order in (2, 3, 4)
                for variant in (
                    Lobatto.estimate_butcher_tableu,
                    Lobatto.hardcoded_butcher_tableu,
                )
            ],
        ],
        testcase_func_name=custom_name_func,
    )
    def test_correspondence_between_methods(
        self, order, variant, first_method, second_method
    ):
        a_first, b_first, c_first = variant(order, first_method)
        a_second, b_second, c_second = variant(order, second_method)
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
        np.testing.assert_almost_equal(condition["first"], np.zeros((s, s)), decimal=2)
        np.testing.assert_almost_equal(condition["second"], np.zeros((s, s)), decimal=2)
        np.testing.assert_almost_equal(
            condition["neighbor"], np.zeros((s, s)), decimal=2
        )


class TestLobattoEstimateApproximatesHardcoded(unittest.TestCase):
    @parameterized.expand(
        [
            *[(order, method) for order in (2, 3, 4) for method in (Lobatto.IIIA,)],
            *[(order, method) for order in (2, 3, 4) for method in (Lobatto.IIIB,)],
            *[(order, method) for order in (2, 3, 4, 5) for method in (Lobatto.IIIC,)],
            *[(order, method) for order in (2, 3) for method in (Lobatto.IIICstar,)],
        ],
        testcase_func_name=custom_name_func,
    )
    def test_estimate_approximates_hardcoded(self, order, method):
        [
            np.testing.assert_allclose(actual, desired, atol=1e-2, rtol=1e-2)
            for actual, desired in zip(
                Lobatto.estimate_butcher_tableu(order, method),
                Lobatto.hardcoded_butcher_tableu(order, method),
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

