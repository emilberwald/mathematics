import functools

from parameterized import parameterized

from mathematics.tools.decorators import timeout
from mathematics.tools.testing import custom_name_func
from .differential import *


def product(*args):
    return functools.reduce(lambda x0, x1: x0 * x1, args)


class TestFlow:
    @timeout(seconds=1.0)
    def test_flow(self):
        np.testing.assert_allclose([0.1], flow()(np.array(1))(0.1)(lambda t: t)(0))
        np.testing.assert_allclose([-0.1], flow()(np.array(-1))(0.1)(lambda t: t)(0))


class TestFiniteForwardDifference:
    @timeout(seconds=1.0)
    def test_finite_forward_difference(self):
        C, x = np.random.rand(2)
        actual = finite_forward_difference()(1)(lambda x: C * x)(x)(0.1)
        expected = C
        np.testing.assert_allclose(actual, expected)
        actual = finite_forward_difference()(1)(lambda x: -C * x)(x)(0.1)
        expected = -C
        np.testing.assert_allclose(actual, expected)


class TestDifferentialWithScalarFunction:
    @parameterized.expand(
        [
            (np.sin, np.cos),
            (np.cos, lambda x: -np.sin(x)),
            (lambda x: x ** 2.0, lambda x: 2.0 * x),
            (lambda x: x ** 0.5, lambda x: 0.5 * x ** (-0.5)),
        ],
        name_func=custom_name_func,
    )
    @timeout(seconds=1.0)
    def test_scalar_derivative(self, function, known_derivative):
        x = np.random.rand(1)
        actual_derivative = directional_derivative(1)(function)(x)
        expected_derivative = known_derivative(x)
        np.testing.assert_allclose(actual_derivative, expected_derivative)


class TestDifferentialWithVectorFunction:
    @parameterized.expand([(lambda t: np.dot(t[0], t[1]),)], name_func=custom_name_func)
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
        np.testing.assert_allclose(
            directional_derivative(vect(u, v))(bilinear_map)(vect(x, y)),
            bilinear_map(vect(x, v)) + bilinear_map(vect(u, y)),
            atol=1e-5,
        )


class TestSecondDifferentialWithVectorFunction:
    @parameterized.expand([(order,) for order in (1, 2)], name_func=custom_name_func)
    # @timeout(seconds=1.0)
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
        first_direction = vect(*np.random.rand(2))
        second_direction = vect(*np.random.rand(2))
        if order == 1:
            np.testing.assert_allclose(
                directional_derivative(first_direction)(f)(application_point),
                first_frechet(application_point, first_direction),
                atol=1e-5,
            )
            np.testing.assert_allclose(
                directional_derivative(second_direction)(f)(application_point),
                first_frechet(application_point, second_direction),
                atol=1e-5,
            )
        elif order == 2:
            np.testing.assert_allclose(
                directional_derivative(second_direction, first_direction)(f)(
                    application_point
                ),
                second_frechet(application_point, first_direction, second_direction),
                atol=1e-5,
            )
