import math
import unittest
import pytest
from parameterized import parameterized
import numpy as np
from .ode_step import *


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
            *[(order, method) for order in (2, 3, 4) for method in (Lobatto.iiia,)],
            *[(order, method) for order in (2, 3, 4) for method in (Lobatto.iiib,)],
            *[(order, method) for order in (2, 3, 4, 5) for method in (Lobatto.iiic,)],
            *[(order, method) for order in (2, 3) for method in (Lobatto.iiicstar,)],
        ],
        testcase_func_name=custom_name_func,
    )
    def test_hardcoded_fulfills_requirements(self, order, method):
        soft_0 = lambda lhs, cmp, rhs: (not cmp(lhs, rhs)) * np.linalg.norm(lhs - rhs)
        butcher_matrix, weights, abscissae = Lobatto.hardcoded_butcher_tableu(
            order, method
        )
        constraints = Lobatto.create_constraint_system(method, soft=soft_0)
        actual = constraints(Lobatto.pack(butcher_matrix, weights, abscissae))
        expected = np.zeros_like(actual)
        np.testing.assert_allclose(actual, expected, atol=1e-15)


class TestLobattoCorrespondenceBetweenMethods(unittest.TestCase):
    @parameterized.expand(
        [
            *[
                (order, variant, Lobatto.iiic, Lobatto.iiicstar)
                for order in (2, 3)
                for variant in (Lobatto.hardcoded_butcher_tableu,)
            ],
            *[
                (order, variant, Lobatto.iiic, Lobatto.iiicstar)
                for order in (2, 3, 4)
                for variant in (Lobatto.estimate_butcher_tableu,)
            ],
            *[
                (order, variant, Lobatto.iiia, Lobatto.iiib)
                for order in (2, 3, 4)
                for variant in (
                    Lobatto.estimate_butcher_tableu,
                    Lobatto.hardcoded_butcher_tableu,
                )
            ],
        ],
        testcase_func_name=custom_name_func,
    )
    @pytest.mark.timeout(5)
    def test_correspondence_between_methods(
        self, order, variant, first_method, second_method
    ):
        butcher_matrix_1, weights_1, _ = variant(order, first_method)
        butcher_matrix_2, weights_2, _ = variant(order, second_method)
        nof_dimensions = len(weights_1)
        condition = dict()
        condition["first"] = np.ndarray((nof_dimensions, nof_dimensions))
        condition["second"] = np.ndarray((nof_dimensions, nof_dimensions))
        condition["neighbor"] = np.ndarray((nof_dimensions, nof_dimensions))
        for dimension_i in range(nof_dimensions):
            for dimension_j in range(nof_dimensions):
                # Don't know which interpretation is correct...
                condition["first"][dimension_i][dimension_j] = (
                    weights_1[dimension_i] * butcher_matrix_2[dimension_i][dimension_j]
                    + weights_1[dimension_j]
                    * butcher_matrix_1[dimension_j][dimension_i]
                    - weights_1[dimension_i] * weights_1[dimension_j]
                )
                condition["second"][dimension_i][dimension_j] = (
                    weights_2[dimension_i] * butcher_matrix_2[dimension_i][dimension_j]
                    + weights_2[dimension_j]
                    * butcher_matrix_1[dimension_j][dimension_i]
                    - weights_2[dimension_i] * weights_2[dimension_j]
                )
                condition["neighbor"][dimension_i][dimension_j] = (
                    weights_2[dimension_i] * butcher_matrix_2[dimension_i][dimension_j]
                    + weights_1[dimension_j]
                    * butcher_matrix_1[dimension_j][dimension_i]
                    - weights_2[dimension_i] * weights_1[dimension_j]
                )
        np.testing.assert_almost_equal(
            condition["first"], np.zeros((nof_dimensions, nof_dimensions)), decimal=2
        )
        np.testing.assert_almost_equal(
            condition["second"], np.zeros((nof_dimensions, nof_dimensions)), decimal=2
        )
        np.testing.assert_almost_equal(
            condition["neighbor"], np.zeros((nof_dimensions, nof_dimensions)), decimal=2
        )


class TestLobattoEstimateApproximatesHardcoded(unittest.TestCase):
    @parameterized.expand(
        [
            *[(order, method) for order in (2, 3, 4) for method in (Lobatto.iiia,)],
            *[(order, method) for order in (2, 3, 4) for method in (Lobatto.iiib,)],
            *[(order, method) for order in (2, 3, 4, 5) for method in (Lobatto.iiic,)],
            *[(order, method) for order in (2, 3) for method in (Lobatto.iiicstar,)],
        ],
        testcase_func_name=custom_name_func,
    )
    @pytest.mark.timeout(5)
    def test_estimate_approximates_hardcoded(self, order, method):
        for actual, desired in zip(
            Lobatto.estimate_butcher_tableu(order, method),
            Lobatto.hardcoded_butcher_tableu(order, method),
        ):
            np.testing.assert_allclose(actual, desired, atol=1e-2, rtol=1e-2)


class TestRungeKutta(unittest.TestCase):
    def test_implicit_runge_kutta(self):
        butcher_matrix, weights, abscissae = Lobatto.estimate_butcher_tableu(
            4, Lobatto.iiic
        )

        constants = np.hstack((np.random.uniform(-5, 0, 5), np.random.uniform(0, 5, 5)))
        for constant in constants:

            def get_function(coefficient):
                def function(_, dependent_variable):
                    return coefficient * dependent_variable

                return function

            def get_solution(coefficient):
                def solution(independent_variable):
                    return np.exp(coefficient * independent_variable)

                return solution

            independent_variable_evolution = [0]
            estimated_dependent_variable_evolution = [1]
            expected_dependent_variable_evolution = [1]
            delta_t = 0.001
            max_t = 2.0
            function = get_function(constant)
            dependent_variable_evolution = get_solution(constant)
            for i in range(0, int(max_t / delta_t)):
                estimated_dependent_variable_evolution.append(
                    RungeKutta(
                        function,
                        independent_variable_evolution[-1],
                        estimated_dependent_variable_evolution[-1],
                        butcher_matrix,
                        weights,
                        abscissae,
                    )(delta_t)
                )
                independent_variable_evolution.append(
                    independent_variable_evolution[-1] + delta_t
                )
                expected_dependent_variable_evolution.append(
                    dependent_variable_evolution(independent_variable_evolution[-1])
                )
                error_estimate = (
                    expected_dependent_variable_evolution[-1]
                    - estimated_dependent_variable_evolution[-1]
                )
                np.testing.assert_allclose(
                    estimated_dependent_variable_evolution[-1],
                    expected_dependent_variable_evolution[-1],
                    err_msg=f"constant={constant} e={error_estimate} h={delta_t} log_h(e)=\
                    {math.log(abs(error_estimate if error_estimate else np.nextafter(error_estimate,error_estimate+1)),delta_t)}\
                     [time={independent_variable_evolution[-1]}, i={i}/{int(max_t/delta_t)}]",
                )

    def test_explicit_runge_kutta(self):
        # https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods#Use
        """Ralston's method"""
        butcher_matrix = np.array([[0, 0], [2 / 3, 0]])
        weights = np.array([1 / 4, 3 / 4])
        abscissae = np.array([0, 2 / 3])

        def function(_, dependent_variable):
            return np.tan(dependent_variable) + 1

        times = [1]
        solution = [1]
        delta_t = 0.025
        for _ in range(0, 4):
            solution.append(
                RungeKutta(
                    function,
                    times[-1],
                    solution[-1],
                    butcher_matrix,
                    weights,
                    abscissae,
                )(delta_t)
            )
            times.append(times[-1] + delta_t)
        expected_times = [1, 1.025, 1.05, 1.075, 1.1]
        expected_solution = [
            1,
            1.066_869_388,
            1.141_332_181,
            1.227_417_567,
            1.335_079_087,
        ]

        np.testing.assert_almost_equal(times, expected_times)
        np.testing.assert_almost_equal(solution, expected_solution)


if __name__ == "__main__":
    unittest.main()
