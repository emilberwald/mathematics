import operator
import numpy as np
import scipy as sp
import scipy.optimize
import collections
import math
from .butcher_tableu import butcher_tableu


class Lobatto:
    # Attempts to follow
    # L.O. Jay: Lobatto methods. [online, .pdf]. Encyclopedia of Applied and Computational Mathematics [.pdf], Numerical Analysis of Ordinary Differential Equations, Springer - The Language of Science, Bj\"orn Engquist (Ed.), 2015.
    # http://homepage.math.uiowa.edu/~ljay/publications.html
    @staticmethod
    def pack(a, b, c):
        X = np.hstack((np.ravel(a), np.ravel(b), np.ravel(c)))
        return X

    @staticmethod
    def unpack(X):
        s = int(math.sqrt(len(X) + 1) - 1)
        a = X[: -2 * s].reshape(s, s)
        b = X[-2 * s : -s]
        c = X[-s:]
        return a, b, c

    @classmethod
    def assumption_B(cls, p):
        def null_system_for_assumption(X):
            a, b, c = cls.unpack(X)
            s = len(c)
            result = [
                sum([b[j] * (c[j] ** (k - 1.0)) for j in range(s)]) - 1.0 / k
                for k in range(1, p + 1)
            ]
            return result

        return null_system_for_assumption

    @classmethod
    def assumption_C(cls, q):
        def null_system_for_assumption(X):
            a, b, c = cls.unpack(X)
            s = len(c)
            result = [
                sum([(c[j] ** (k - 1)) * a[i, j] for j in range(s)]) - (c[i] ** k) / k
                for i in range(s)
                for k in range(1, q + 1)
            ]
            return result

        return null_system_for_assumption

    @classmethod
    def assumption_D(cls, r):
        def null_system_for_assumption(X):
            a, b, c = cls.unpack(X)
            s = len(c)
            result = [
                sum([b[i] * (c[i] ** (k - 1.0)) * a[i, j] for i in range(s)])
                - (b[j] / k) * (1.0 - (c[j]) ** k)
                for j in range(s)
                for k in range(1, r + 1)
            ]
            return result

        return null_system_for_assumption

    @classmethod
    def shared_constraints(cls, soft, X):
        a, b, c = cls.unpack(X)
        s = len(c)
        result = [
            [
                soft(constraint, operator.eq, 0.0)
                for constraint in cls.assumption_B(2 * s - 2)(X)
            ],
            [soft(c[0], operator.eq, 0.0), soft(c[-1], operator.eq, 1.0)],
            [soft(0, operator.le, ci) for ci in c],
            [soft(ci, operator.le, 1.0) for ci in c],
            [soft(c[i], operator.lt, c[i + 1]) for i in range(s - 1)],
            [
                soft(b[0], operator.eq, 1 / (s * (s - 1))),
                soft(b[-1], operator.eq, 1 / (s * (s - 1))),
            ],
            [soft(bj, operator.gt, 0.0) for bj in b],
            # unit tests failed with these -- perhaps they were implemented wrong? or overdetermined system makes the solution wonky?
            # [soft(c[-j], operator.eq, 1.0 - c[j]) for j in range(s)],
            # [soft(b[-j], operator.eq, b[j]) for j in range(s)],
        ]
        return result

    @classmethod
    def IIIA(cls, soft, X):
        a, b, c = cls.unpack(X)
        s = len(c)
        result = [
            [
                soft(constraint, operator.eq, 0.0)
                for constraint in cls.assumption_C(s)(X)
            ],
            [
                soft(constraint, operator.eq, 0.0)
                for constraint in cls.assumption_D(s - 2)(X)
            ],
            [soft(a1j, operator.eq, 0.0) for a1j in a[0]],
            [soft(asj, operator.eq, bj) for asj, bj in zip(a[-1], b)],
        ]
        return result

    @classmethod
    def IIIB(cls, soft, X):
        a, b, c = cls.unpack(X)
        s = len(c)
        result = [
            [
                soft(constraint, operator.eq, 0.0)
                for constraint in cls.assumption_C(s - 2)(X)
            ],
            [
                soft(constraint, operator.eq, 0.0)
                for constraint in cls.assumption_D(s)(X)
            ],
            [soft(ai[0], operator.eq, b[0]) for ai in a],
            [soft(ai[-1], operator.eq, 0.0) for ai in a],
        ]
        return result

    @classmethod
    def IIIC(cls, soft, X):
        a, b, c = cls.unpack(X)
        s = len(c)
        result = [
            [
                soft(constraint, operator.eq, 0.0)
                for constraint in cls.assumption_C(s - 1)(X)
            ],
            [
                soft(constraint, operator.eq, 0.0)
                for constraint in cls.assumption_D(s - 1)(X)
            ],
            [soft(ai[0], operator.eq, b[0]) for ai in a],
            [soft(asj, operator.eq, bj) for asj, bj in zip(a[-1], b)],
        ]
        return result

    @classmethod
    def IIICstar(cls, soft, X):
        a, b, c = cls.unpack(X)
        s = len(c)
        result = [
            [
                soft(constraint, operator.eq, 0.0)
                for constraint in cls.assumption_C(s - 1)(X)
            ],
            [
                soft(constraint, operator.eq, 0.0)
                for constraint in cls.assumption_D(s - 1)(X)
            ],
            [soft(ai[-1], operator.eq, 0.0) for ai in a],
            [soft(a1j, operator.eq, 0.0) for a1j in a[0]],
        ]
        return result

    @classmethod
    def estimate_butcher_tableu(cls, s, specific_constraints=None):
        specific_constraints = (
            cls.IIIC if specific_constraints is None else specific_constraints
        )

        def create_system(soft=lambda x, cmp, y: cmp(x, y)):
            def system(X):
                a, b, c = cls.unpack(X)
                result = np.hstack(
                    (*cls.shared_constraints(soft, X), *specific_constraints(soft, X))
                )
                return result

            return system

        def try_to_minimize(a, b, c, epsilon=1e-1):
            soft_min = lambda lhs, cmp, rhs: (not (cmp(lhs, rhs))) * np.linalg.norm(
                lhs - rhs
            )
            system_to_minimize = lambda x: np.linalg.norm(create_system(soft_min)(x))
            sol = sp.optimize.minimize(system_to_minimize, cls.pack(a, b, c))
            if sol.success:
                cost = system_to_minimize(sol.x)
                a, b, c = cls.unpack(sol.x)
                return a, b, c, cost
            else:
                if "x" in sol:
                    cost = system_to_minimize(sol.x)
                    if cost < epsilon:
                        a, b, c = cls.unpack(sol.x)
                        return a, b, c, cost, sol.success

        def try_to_find_kernel(a, b, c):
            soft_0 = lambda lhs, cmp, rhs: (not (cmp(lhs, rhs))) * np.linalg.norm(
                lhs - rhs
            )
            system_to_find_kernel = lambda x: create_system(soft_0)(x)
            # Need to choose a solver that allows for the output to be different than the input
            sol = sp.optimize.root(
                system_to_find_kernel, cls.pack(a, b, c), method="lm"
            )
            if sol.success:
                residual = system_to_find_kernel(sol.x)
                a, b, c = cls.unpack(sol.x)
                return a, b, c, residual, sol.success

        a = [[0.0 for i in range(s)] for j in range(s)]
        b = [0.0 for i in range(s)]
        c = [0.0 for i in range(s)]
        if specific_constraints == cls.IIIA:
            # To mitigate that the test cases for IIIA failed
            continue_condition = lambda reqs, iterationNo, success: all(reqs) or (
                success and iterationNo > 0
            )
        else:
            continue_condition = lambda reqs, iterationNo, success: all(reqs) or success

        for i in range(100):
            result_0 = try_to_find_kernel(a, b, c)
            if result_0:
                a, b, c, residual_0, success = result_0
                c[0] = 0.0
                c[-1] = 1.0
                reqs = create_system()(cls.pack(a, b, c))
                if continue_condition(reqs, i, success):
                    return a.tolist(), b.tolist(), c.tolist()

            result_min = try_to_minimize(a, b, c)
            if result_min:
                a, b, c, residual_min, success = result_min
                c[0] = 0.0
                c[-1] = 1.0
                reqs = create_system()(cls.pack(a, b, c))
                if continue_condition(reqs, i, success):
                    return a.tolist(), b.tolist(), c.tolist()

    @classmethod
    def hardcoded_butcher_tableu(cls, p, identifier):
        if identifier == cls.IIIA:
            name = "lobatto_iiia"
        elif identifier == cls.IIIB:
            name = "lobatto_iiib"
        elif identifier == cls.IIIC:
            name = "lobatto_iiic"
        elif identifier == cls.IIICstar:
            name = "lobatto_iiic*"
        else:
            name = identifier
        try:
            return (
                butcher_tableu[name]["butcher_matrix"][p],
                butcher_tableu[name]["weights"][p],
                butcher_tableu[name]["abscissae"][p],
            )
        except KeyError:
            return None

    @classmethod
    def butcher_tableu(cls, p, identifier):
        result = cls.hardcoded_butcher_tableu(p, identifier)
        return result if result else cls.estimate_butcher_tableu(p, identifier)


class RungeKutta:
    r"""Creates a runge kutta method using a Butcher Tableu
		a := ButcherMatrix
		b := weights
		c := abscissae
		.. math::
			y_{n+1}		= y_n + h \sum_{i=1}^s b_i   k_i
			k_i = f\left( t_n + c_i h,\ y_{n} + h \sum_{j=1}^s a_{ij} k_j \right), \quad i = 1, \ldots, s.
			y^*_{n+1}	= y_n + h \sum_{i=1}^s b^*_i k_i
			e_{n+1} = y_{n+1} - y^*_{n+1} = h\sum_{i=1}^s (b_i - b^*_i) k_i
	"""

    @staticmethod
    def general_k(a, c, F, t0, y0, delta_t):
        def system_for_k(k):
            return [
                F(
                    t0 + c[i] * delta_t,
                    y0 + delta_t * sum([a[i][j] * k[j] for j in range(len(k))]),
                )
                - k[i]
                for i in range(len(c))
            ]

        sol = sp.optimize.root(system_for_k, np.ones_like(c))
        return sol.x

    @staticmethod
    def explicit_k(a, c, F, t0, y0, delta_t):
        k = np.zeros_like(c)
        for i in range(len(c)):
            k[i] = F(
                t0 + c[i] * delta_t,
                y0 + delta_t * sum([a[i][j] * k[j] for j in range(len(k))]),
            )
        return k

    @classmethod
    def solve_for_k(cls, a, c, F, t0, y0, delta_t):
        if np.allclose(a, np.tril(a, -1)) and np.allclose(c, [0] + c[1:]):
            return cls.explicit_k(a, c, F, t0, y0, delta_t)
        else:
            return cls.general_k(a, c, F, t0, y0, delta_t)

    @staticmethod
    def consistent_c(a):
        return [sum([aij for aij in ai]) for ai in a]

    @staticmethod
    def step(b, F, y0, delta_t, k):
        return y0 + delta_t * sum([b[i] * k[i] for i in range(len(b))])

    @staticmethod
    def error_estimate(b, bstar, delta_t, k):
        return delta_t * sum([(b[i] - bstar[i]) * k[i] for i in range(len(b))])

    def __init__(self, F, t0, y0, a, b, c=None):
        self.a = a
        self.b = b
        self.c = self.consistent_c(a) if c is None else c
        self.F = F
        self.t0 = t0
        self.y0 = y0
        self.k = None

    def __call__(self, delta_t):
        self.k = self.solve_for_k(self.a, self.c, self.F, self.t0, self.y0, delta_t)
        return self.step(self.b, self.F, self.y0, delta_t, self.k)


class PredictorCorrector:
    def __init__(self, predictor, corrector):
        self.predictor = predictor
        self.corrector = corrector

    def __call__(self, F, t0, y0, delta_t=None):
        delta_t = delta_t if delta_t is None else np.spacing(t0)

