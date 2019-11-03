import functools
import itertools
import math
import numbers
import operator
import sys

from .matrix import Matrix


class Pointwise:
    def __init__(self, function):
        self.function = function

    def __repr__(self):
        return repr(self.function) + "-pointwise"

    def __call__(self, *args, **kwargs):
        if callable(self.function):
            return self.function(*args, **kwargs)
        else:
            return self.function

    @staticmethod
    def __op(lhs, op, *args, **kwargs):
        return op(lhs(*args, **kwargs))

    @staticmethod
    def __binop(lhs, op, rhs, *args, **kwargs):
        return op(lhs(*args, **kwargs), rhs(*args, **kwargs))

    def __abs__(self):
        def __abs(*args, **kwargs):
            return type(self).__op(self, operator.abs, *args, **kwargs)

        return type(self)(__abs)

    def __neg__(self):
        def __neg(*args, **kwargs):
            return type(self).__op(self, operator.__neg__, *args, **kwargs)

        return type(self)(__neg)

    def __pos__(self):
        def __pos(*args, **kwargs):
            return type(self).__op(self, operator.__pos__, *args, **kwargs)

        return type(self)(__pos)

    def __rmul__(self, lhs):
        def __rmul(*args, **kwargs):
            return (lhs(*args, **kwargs) if callable(lhs) else lhs) * self(
                *args, **kwargs
            )

        return type(self)(__rmul)

    def __lt__(self, rhs):
        # assert isinstance(rhs, Pointwise)
        def __lt(*args, **kwargs):
            return type(self).__binop(self, operator.__lt__, rhs, *args, **kwargs)

        return type(self)(__lt)

    def __le__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __le(*args, **kwargs):
            return type(self).__binop(self, operator.__le__, rhs, *args, **kwargs)

        return type(self)(__le)

    def __eq__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __eq(*args, **kwargs):
            return type(self).__binop(self, operator.__eq__, rhs, *args, **kwargs)

        return type(self)(__eq)

    def __ne__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __ne(*args, **kwargs):
            return type(self).__binop(self, operator.__ne__, rhs, *args, **kwargs)

        return type(self)(__ne)

    def __ge__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __ge(*args, **kwargs):
            return type(self).__binop(self, operator.__ge__, rhs, *args, **kwargs)

        return type(self)(__ge)

    def __gt__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __gt(*args, **kwargs):
            return type(self).__binop(self, operator.__gt__, rhs, *args, **kwargs)

        return type(self)(__gt)

    def __add__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __add(*args, **kwargs):
            return type(self).__binop(self, operator.__add__, rhs, *args, **kwargs)

        return type(self)(__add)

    def __and__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __and(*args, **kwargs):
            return type(self).__binop(self, operator.__and__, rhs, *args, **kwargs)

        return type(self)(__and)

    def __floordiv__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __floordiv(*args, **kwargs):
            return type(self).__binop(self, operator.__floordiv__, rhs, *args, **kwargs)

        return type(self)(__floordiv)

    def __mod__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __mod(*args, **kwargs):
            return type(self).__binop(self, operator.__mod__, rhs, *args, **kwargs)

        return type(self)(__mod)

    def __mul__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __mul(*args, **kwargs):
            return type(self).__binop(self, operator.__mul__, rhs, *args, **kwargs)

        return type(self)(__mul)

    def __or__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __or(*args, **kwargs):
            return type(self).__binop(self, operator.__or__, rhs, *args, **kwargs)

        return type(self)(__or)

    def __pow__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __pow(*args, **kwargs):
            return type(self).__binop(self, operator.__pow__, rhs, *args, **kwargs)

        return type(self)(__pow)

    def __sub__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __sub(*args, **kwargs):
            return type(self).__binop(self, operator.__sub__, rhs, *args, **kwargs)

        return type(self)(__sub)

    def __truediv__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __truediv(*args, **kwargs):
            return type(self).__binop(self, operator.__truediv__, rhs, *args, **kwargs)

        return type(self)(__truediv)

    def after(self, rhs):
        """
        compose
        """
        # assert isinstance(rhs, Pointwise)

        def __after(*args, **kwargs):
            try:
                return self(*rhs(*args, **kwargs))
            except:
                return self(rhs(*args, **kwargs))

        return type(self)(__after)

    def before(self, rhs):
        """
        precompose
        """
        # assert isinstance(rhs, Pointwise)

        def __before(*args, **kwargs):
            try:
                return rhs(*self(*args, **kwargs))
            except:
                return rhs(self(*args, **kwargs))

        return type(self)(__before)

    @staticmethod
    def KoszulFormula(g, X, Y, Z):
        """
        g(\nabla_X Y, Z)
        """
        return 0.5 * (
            X.derivation(g(Y, Z))
            + Y.derivation(g(X, Z))
            - Z.derivation(g(X, Y))
            + g(X.commutator(Y), Z)
            - g(X.commutator(Z), Y)
            - g(Y.commutator(Z), X)
        )

    @staticmethod
    def KoszulExpansion(g, X, Y, E):
        # https://math.stackexchange.com/a/2878272
        # v = u_1*a_1 + u_2*a_2
        # <v, u_i> = sum_j <u_i, u_j> * a_j
        # a_j = <u_i, u_j>^{-1} * <v, u_i>
        # KoszulFormula gives g(\nabla_X Y, Z) ~ <v, u_i>
        gramian = [[g(ei, ej) for j, ej in enumerate(E)] for i, ei in enumerate(E)]
        gramianInverse = Matrix.inverse(gramian)
        koszul = [Pointwise.KoszulFormula(g, X, Y, ei) for i, ei in enumerate(E)]
        return [koszul[i] * ei for i, ei in enumerate(gramianInverse)]

    def connection(self, rhs, g, E):
        return self.derivation(abs(rhs)) * (rhs / abs(rhs)) + abs(
            rhs
        ) * Pointwise.KoszulExpansion(g, self, rhs / abs(rhs), E)

    def commutator(self, rhs):
        # assert isinstance(rhs, Pointwise)
        return self.after(rhs) - rhs.after(self)

    def torsion(self, rhs, g, E):
        # assert isinstance(rhs, Pointwise)
        return (
            self.connection(rhs, g, E)
            - rhs.connection(self, g, E)
            - self.commutator(rhs)
        )

    def riemann(self, rhs, g, E):
        # assert isinstance(rhs, Pointwise)

        def __riemann(application):
            assert isinstance(application, Pointwise)
            return (
                self.connection(rhs.connection(application, g, E), g, E)
                - rhs.connection(self.connection(application, g, E), g, E)
                - self.commutator(rhs).connection(application, g, E)
            )

        return type(self)(__riemann)

    def derivative(self, approximation_order=2):
        DERIVATIVE_ORDER = 1

        def __directional_derivative(direction):
            # rule of thumb used
            # https://math.stackexchange.com/a/2488893/68036
            # https://math.stackexchange.com/a/819015/68036
            # perhaps use finite_difference .... ?
            dt = sys.float_info.epsilon ** (
                1.0 / (DERIVATIVE_ORDER + approximation_order)
            )
            return (
                self.after(Pointwise(lambda point: point + dt * direction(point)))
                - self
            ) / abs(Pointwise(lambda point: dt))

        return type(self)(__directional_derivative)

    def derivation(self, approximation_order=2):
        def __applied_derivation(function):
            if isinstance(function, numbers.Number):
                return type(function)(0)
            elif isinstance(function, Pointwise):
                return function.derivative(approximation_order=approximation_order)(
                    self
                )
            else:
                raise NotImplementedError()

        return type(self)(__applied_derivation)
