import unittest
import functools
from parameterized import parameterized
import numpy as np

if __name__ == "__main__":
    from differential import *
else:
    from .differential import *


def custom_name_func(testcase_func, param_num, param):
    return "_".join(
        [
            parameterized.to_safe_name(x)
            for x in [f"{testcase_func.__name__}", f"{param_num}", f"{param}"]
        ]
    )


def product(*args):
    return functools.reduce(lambda x0, x1: x0 * x1, args)


class TestDifferential(unittest.TestCase):
    def test_flow(self):
        np.allclose([0.1], flow()(np.array(1))(0.1)(lambda t: t)(0))
        np.allclose([-0.1], flow()(np.array(-1))(0.1)(lambda t: t)(0))

    def test_finite_forward_difference(self):
        C, x = np.random.rand(2)
        np.allclose([2], finite_forward_difference()(1)(lambda x: C * x)(x)(0.1))
        np.allclose([-2], finite_forward_difference()(1)(lambda x: -C * x)(x)(0.1))

    @parameterized.expand(
        [
            (np.sin, np.cos),
            (np.cos, lambda x: -np.sin(x)),
            (lambda x: x ** 2.0, lambda x: 2.0 * x),
            (lambda x: x ** 0.5, lambda x: 0.5 * x ** (-0.5)),
        ],
        testcase_func_name=custom_name_func,
    )
    def test_scalar_derivative(self, function, known_derivative):
        x = np.random.rand(1)
        actual_derivative = directional_derivative(1)(function)(x)
        expected_derivative = known_derivative(x)
        np.allclose(actual_derivative, expected_derivative)

    @parameterized.expand([(product,)], testcase_func_name=custom_name_func)
    def test_frechet_derivative_of_bilinear_map(self, bilinear_map):
        # https://math.stackexchange.com/questions/562820/what-is-the-second-frechet-derivative-of-a-bilinear-map
        # First derivative
        u, v = np.random.rand(2)
        x, y = np.random.rand(2)
        np.testing.assert_allclose(
            directional_derivative(np.array([u, v]))(bilinear_map)(np.array([x, y])),
            bilinear_map(np.array([x, v])) + bilinear_map(np.array([u, y])),
            atol=1e-5,
        )

    @parameterized.expand([(product,)], testcase_func_name=custom_name_func)
    def test_second_frechet_derivative_of_bilinear_map(self, bilinear_map):
        # https://math.stackexchange.com/questions/562820/what-is-the-second-frechet-derivative-of-a-bilinear-map
        u, v = np.random.rand(2)
        x, y = np.random.rand(2)
        z, w = np.random.rand(2)
        np.testing.assert_allclose(
            directional_derivative(np.array([u, v]), np.array([z, w]))(bilinear_map)(
                np.array([x, y])
            ),
            bilinear_map(np.array([z, v])) + bilinear_map(np.array([u, w])),
            atol=1e-5,
        )


if __name__ == "__main__":
    unittest.main()

