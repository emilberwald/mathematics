import operator
import logging
import collections
import math
import numpy as np
import scipy as sp
import scipy.optimize
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
            return [
                sum([b[j] * (c[j] ** (k - 1.0)) for j in range(s)]) - 1.0 / k
                for k in range(1, p + 1)
            ]

        return null_system_for_assumption

    @classmethod
    def assumption_C(cls, q):
        def null_system_for_assumption(X):
            a, b, c = cls.unpack(X)
            s = len(c)
            return [
                sum([(c[j] ** (k - 1)) * a[i, j] for j in range(s)]) - (c[i] ** k) / k
                for i in range(s)
                for k in range(1, q + 1)
            ]

        return null_system_for_assumption

    @classmethod
    def assumption_D(cls, r):
        def null_system_for_assumption(X):
            a, b, c = cls.unpack(X)
            s = len(c)
            return [
                sum([b[i] * (c[i] ** (k - 1.0)) * a[i, j] for i in range(s)])
                - (b[j] / k) * (1.0 - (c[j]) ** k)
                for j in range(s)
                for k in range(1, r + 1)
            ]

        return null_system_for_assumption

    @classmethod
    def shared_constraints(cls, soft, X):
        a, b, c = cls.unpack(X)
        s = len(c)
        return [
            [
                soft(constraint, operator.eq, 0.0)
                for constraint in cls.assumption_B(2 * s - 2)(X)
            ],
            [soft(c[0], operator.eq, 0.0), soft(c[-1], operator.eq, 1.0)],
            [soft(0, operator.le, ci) for ci in c],
            [soft(ci, operator.le, 1.0) for ci in c],
            [soft(c[i], operator.lt, c[i + 1]) for i in range(s - 1)],
            # This version did not give good results !? Something wrong with it? Keep the alternative one for the endpoints meanwhile.
            # [
            #     soft(
            #         bj,
            #         operator.eq,
            #         1.0
            #         / (
            #             s
            #             * (s - 1)
            #             * (
            #                 np.polynomial.legendre.legval(
            #                     (2 * cj - 1), [1 if i == s - 1 else 0 for i in range(s)]
            #                 )
            #                 ** 2
            #             )
            #         ),
            #     )
            #     for bj, cj in zip(b, c)
            # ],
            [
                soft(b[0], operator.eq, 1 / (s * (s - 1))),
                soft(b[-1], operator.eq, 1 / (s * (s - 1))),
            ],
            [soft(bj, operator.gt, 0.0) for bj in b],
            # unit tests failed with these -- perhaps they were implemented wrong? or overdetermined system makes the solution wonky?
            # [soft(c[-(1 + j)], operator.eq, 1.0 - c[j]) for j in range(s)],
            # [soft(b[-(1 + j)], operator.eq, b[j]) for j in range(s)],
        ]

    @classmethod
    def IIIA(cls, soft, X):
        a, b, c = cls.unpack(X)
        s = len(c)
        return [
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

    @classmethod
    def IIIB(cls, soft, X):
        a, b, c = cls.unpack(X)
        s = len(c)
        return [
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

    @classmethod
    def IIIC(cls, soft, X):
        a, b, c = cls.unpack(X)
        s = len(c)
        return [
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

    @classmethod
    def IIICstar(cls, soft, X):
        a, b, c = cls.unpack(X)
        s = len(c)
        return [
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

    @classmethod
    def create_constraint_system(
        cls, specific_constraints, soft=lambda x, cmp, y: cmp(x, y)
    ):
        def system(X):
            return np.hstack(
                (*cls.shared_constraints(soft, X), *specific_constraints(soft, X))
            )

        return system

    @classmethod
    def estimate_butcher_tableu(cls, s, specific_constraints=None, initial_guess=None):
        specific_constraints = (
            cls.IIIC if specific_constraints is None else specific_constraints
        )
        if initial_guess is None:
            a = [[0.0 for i in range(s)] for j in range(s)]
            b = [0.0 for i in range(s)]
            c = [0.0 for i in range(s)]
            c[0] = 0.0
            c[-1] = 1.0
        else:
            a, b, c = initial_guess

        soft_min = lambda lhs, cmp, rhs: (not (cmp(lhs, rhs))) * np.linalg.norm(
            lhs - rhs
        )
        constraints_min = cls.create_constraint_system(specific_constraints, soft_min)
        system_to_minimize = lambda x: np.linalg.norm(constraints_min(x))

        soft_0 = lambda lhs, cmp, rhs: (not (cmp(lhs, rhs))) * np.linalg.norm(lhs - rhs)
        constraints_0 = cls.create_constraint_system(specific_constraints, soft_0)
        system_to_find_kernel = lambda x: constraints_0(x)

        constraints_req = cls.create_constraint_system(specific_constraints)
        system_requirements = lambda x: constraints_req(x)

        def try_to_minimize(a, b, c, epsilon=1e-1):
            sol = sp.optimize.minimize(system_to_minimize, cls.pack(a, b, c))
            if sol.success:
                cost = system_to_minimize(sol.x)
                a, b, c = cls.unpack(sol.x)
                return a, b, c, cost, sol.success
            else:
                if "x" in sol:
                    cost = system_to_minimize(sol.x)
                    if cost < epsilon:
                        a, b, c = cls.unpack(sol.x)
                        return a, b, c, cost, sol.success

        def try_to_find_kernel(a, b, c):
            # Need to choose a solver that allows for the output to be different than the input
            sol = sp.optimize.root(
                system_to_find_kernel, cls.pack(a, b, c), method="lm"
            )
            if sol.success:
                residual = system_to_find_kernel(sol.x)
                a, b, c = cls.unpack(sol.x)
                return a, b, c, residual, sol.success

        def check_converged(saved, latest):
            a, b, c = latest
            reqs = system_requirements(cls.pack(a, b, c))
            if all(
                [np.allclose(savedi, latesti) for savedi, latesti in zip(saved, latest)]
            ):
                c[0] = 0.0
                c[-1] = 1.0
                return (a.tolist(), b.tolist(), c.tolist()), True, sum(reqs)
            else:
                c[0] = 0.0
                c[-1] = 1.0
                return (a, b, c), False, sum(reqs)

        saved_0 = (a, b, c)
        saved_min = (a, b, c)
        while True:
            for attemptNo in range(2):
                result_0 = try_to_find_kernel(a, b, c)
                if result_0:
                    a, b, c, residual_0, success = result_0
                    saved_0, converged_0, quality_0 = check_converged(
                        saved_0, (a, b, c)
                    )
                    if converged_0:
                        return saved_0

            for attemptNo in range(2):
                result_min = try_to_minimize(a, b, c)
                if result_min:
                    a, b, c, residual_min, success = result_min
                    saved_min, converged_min, quality_min = check_converged(
                        saved_min, (a, b, c)
                    )
                    if converged_min:
                        return saved_min
            try:
                if converged_0 and converged_min:
                    return saved_0 if quality_0 < quality_min else saved_min
            except UnboundLocalError as e:
                logging.error(e)
                return None

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
