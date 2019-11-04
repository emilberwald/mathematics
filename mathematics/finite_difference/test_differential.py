import functools

import pytest

from mathematics.tools.decorators import timeout
from mathematics.tools.testing import name_func
from .differential import *


def product(*args):
    return functools.reduce(lambda x0, x1: x0 * x1, args)


class TestFlow:
    @timeout(seconds=1.0)
    def test_flow(self):
        np.testing.assert_allclose([0.1], flow(np.array(1), 0.1)(lambda t: t)(0))
        np.testing.assert_allclose([-0.1], flow(np.array(-1), 0.1)(lambda t: t)(0))


class TestFiniteForwardDifference:
    @timeout(seconds=1.0)
    def test_finite_forward_difference(self):
        C, x = np.random.rand(2)
        actual = finite_forward_difference(1, 0.1)(lambda x: C * x)(x)
        expected = C
        np.testing.assert_allclose(actual, expected)
        actual = finite_forward_difference(1, 0.1)(lambda x: -C * x)(x)
        expected = -C
        np.testing.assert_allclose(actual, expected)


class TestDifferentialWithScalarFunction:
    @pytest.mark.parametrize(
        "function,known_derivative",
        [
            (np.sin, np.cos),
            (np.cos, lambda x: -np.sin(x)),
            (lambda x: x ** 2.0, lambda x: 2.0 * x),
            (lambda x: x ** 0.5, lambda x: 0.5 * x ** (-0.5)),
        ],
        ids=name_func,
    )
    @timeout(seconds=1.0)
    def test_scalar_derivative(self, function, known_derivative):
        x = np.random.rand(1)
        actual_derivative = directional_derivative(1)(function)(x)
        expected_derivative = known_derivative(x)
        np.testing.assert_allclose(
            actual_derivative, expected_derivative, atol=1e-5, rtol=1e-5
        )


class TestDifferentialWithVectorFunction:
    @pytest.mark.parametrize(
        "bilinear_map", [lambda t: np.dot(t[0], t[1])], ids=name_func
    )
    @timeout(seconds=1.0)
    def test_frechet_derivative_of_bilinear_map(self, bilinear_map):
        # https://math.stackexchange.com/questions/562820/what-is-the-second-frechet-derivative-of-a-bilinear-map
        # First derivative
        # import inspect
        # inspect.getargspec()
        def vect(*args):
            return np.asarray(args)

        u = np.random.rand(2)
        v = np.random.rand(2)
        x = np.random.rand(2)
        y = np.random.rand(2)
        actual = directional_derivative(vect(u, v))(bilinear_map)(vect(x, y))
        desired = bilinear_map(vect(x, v)) + bilinear_map(vect(u, y))
        np.testing.assert_allclose(actual, desired, atol=1e-5)


class TestSecondDifferentialWithVectorFunction:
    @pytest.mark.parametrize("order", [(1,), (2,)], ids=name_func)
    @timeout(seconds=1.0)
    def test_frechet_derivative(self, order):
        # http://www.math.udel.edu/~angell/Opt/differ.pdf
        def vect(*args):
            return np.asarray(args, order="C")

        def f(application_point):
            x, y = application_point
            return (x ** 3) * (y ** 2)

        def gradf(application_point):
            x, y = application_point
            return vect(3 * (x ** 2) * (y ** 2), 2 * (x ** 3) * y)

        def hessf(application_point):
            x, y = application_point
            return vect(
                vect(6 * x * (y ** 2), 6 * (x ** 2) * y),
                vect(6 * (x ** 2) * y, 2 * x ** 3),
            )

        def first_frechet(application_point, direction):
            return np.dot(gradf(application_point), direction)

        def second_frechet(application_point, first_direction, second_direction):
            return np.matmul(
                second_direction, np.matmul(hessf(application_point), first_direction)
            )

        application_point = np.random.rand(2)
        directions = [vect(*np.random.rand(2)), vect(*np.random.rand(2))]
        if order == 1:
            for direction in directions:
                actual = directional_derivative(direction)(f)(application_point)
                desired = first_frechet(application_point, direction)
                np.testing.assert_allclose(actual, desired, atol=1e-4, rtol=1e-4)
        elif order == 2:
            actual = directional_derivative(directions[1], directions[0])(f)(
                application_point
            )
            desired = second_frechet(application_point, directions[0], directions[1])
            np.testing.assert_allclose(actual, desired, atol=1e-4, rtol=1e-4)
