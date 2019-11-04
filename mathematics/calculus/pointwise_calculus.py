import numbers

from ..algebra.pointwise import Pointwise
from ..finite_difference.differential import directional_derivative
from ..algebra.matrix import Matrix


class PointwiseCalculus(Pointwise):
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
        koszul = [
            PointwiseCalculus.KoszulFormula(g, X, Y, ei) for i, ei in enumerate(E)
        ]
        return [koszul[i] * ei for i, ei in enumerate(gramianInverse)]

    def connection(self, rhs, g, E):
        return self.derivation()(abs(rhs)) * (rhs / abs(rhs)) + abs(
            rhs
        ) * PointwiseCalculus.KoszulExpansion(g, self, rhs / abs(rhs), E)

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

    def derivation(self):
        return type(self)(directional_derivative(self))

    def derivative(self):
        def __derivative_in_direction(direction):
            if isinstance(direction, numbers.Number):
                return type(direction)(0)
            elif isinstance(direction, Pointwise):
                return direction.derivation()(self)
            else:
                raise NotImplementedError()

        return type(self)(__derivative_in_direction)
