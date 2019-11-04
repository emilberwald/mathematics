"""
Functionality for stepping forward in dynamical systems.
"""

import math as _math
import operator as _operator

import numpy as _np
import scipy as _sp
from scipy import optimize as _optimize

from .butcher_tableu import BUTCHER_TABLEU


class Lobatto:
    """
    Attempts to follow
    L.O. Jay: Lobatto methods. [online, .pdf]. Encyclopedia of Applied and
    Computational Mathematics [.pdf], Numerical Analysis of Ordinary
    Differential Equations, Springer - The Language of Science, Bj\"orn
    Engquist (Ed.), 2015.
    http://homepage.math.uiowa.edu/~ljay/publications.html
    """

    @staticmethod
    def pack(butcher_matrix, weights, abscissae):
        model_parameters = _np.hstack(
            (_np.ravel(butcher_matrix), _np.ravel(weights), _np.ravel(abscissae))
        )
        return model_parameters

    @staticmethod
    def unpack(model_parameters):
        dimension = int(_math.sqrt(len(model_parameters) + 1) - 1)
        butcher_matrix = model_parameters[: -2 * dimension].reshape(
            dimension, dimension
        )
        weights = model_parameters[-2 * dimension : -dimension]
        abscissae = model_parameters[-dimension:]
        return butcher_matrix, weights, abscissae

    @classmethod
    def assumption_b(cls, nof_orders):
        def null_system_for_assumption(model_parameters):
            _, weights, abscissae = cls.unpack(model_parameters)
            dimension = len(abscissae)
            return [
                sum(
                    [
                        weights[dimension_no]
                        * (abscissae[dimension_no] ** (order_no - 1.0))
                        for dimension_no in range(dimension)
                    ]
                )
                - 1.0 / order_no
                for order_no in range(1, nof_orders + 1)
            ]

        return null_system_for_assumption

    @classmethod
    def assumption_c(cls, nof_orders):
        def null_system_for_assumption(model_parameters):
            butcher_matrix, _, abscissae = cls.unpack(model_parameters)
            nof_dimensions = len(abscissae)
            return [
                sum(
                    [
                        (abscissae[dimension_j] ** (order_no - 1))
                        * butcher_matrix[dimension_i, dimension_j]
                        for dimension_j in range(nof_dimensions)
                    ]
                )
                - (abscissae[dimension_i] ** order_no) / order_no
                for dimension_i in range(nof_dimensions)
                for order_no in range(1, nof_orders + 1)
            ]

        return null_system_for_assumption

    @classmethod
    def assumption_d(cls, nof_orders):
        def null_system_for_assumption(model_parameters):
            butcher_matrix, weights, abscissae = cls.unpack(model_parameters)
            nof_dimensions = len(abscissae)
            return [
                sum(
                    [
                        weights[dimension_i]
                        * (abscissae[dimension_i] ** (order_no - 1.0))
                        * butcher_matrix[dimension_i, dimension_j]
                        for dimension_i in range(nof_dimensions)
                    ]
                )
                - (weights[dimension_j] / order_no)
                * (1.0 - (abscissae[dimension_j]) ** order_no)
                for dimension_j in range(nof_dimensions)
                for order_no in range(1, nof_orders + 1)
            ]

        return null_system_for_assumption

    @classmethod
    def shared_constraints(cls, soft, model_parameters):
        _, weights, abscissae = cls.unpack(model_parameters)
        nof_dimensions = len(abscissae)
        return [
            [
                soft(constraint, _operator.eq, 0.0)
                for constraint in cls.assumption_b(2 * nof_dimensions - 2)(
                    model_parameters
                )
            ],
            [
                soft(abscissae[0], _operator.eq, 0.0),
                soft(abscissae[-1], _operator.eq, 1.0),
            ],
            [soft(0, _operator.le, ci) for ci in abscissae],
            [soft(ci, _operator.le, 1.0) for ci in abscissae],
            [
                soft(abscissae[i], _operator.lt, abscissae[i + 1])
                for i in range(nof_dimensions - 1)
            ],
            # This version did not give good results !? Something wrong with it?
            # Keep the alternative one for the endpoints meanwhile.
            # [
            #     soft(
            #         bj,
            #         operator.eq,
            #         1.0
            #         / (
            #             nof_dimensions
            #             * (nof_dimensions - 1)
            #             * (
            #                 np.polynomial.legendre.legval(
            #                     (2 * cj - 1),
            #                     [
            #                         1 if dimension_i == nof_dimensions - 1 else 0
            #                         for dimension_i in range(nof_dimensions)
            #                     ],
            #                 )
            #                 ** 2
            #             )
            #         ),
            #     )
            #     for bj, cj in zip(weights, abscissae)
            # ],
            [
                soft(
                    weights[0],
                    _operator.eq,
                    1 / (nof_dimensions * (nof_dimensions - 1)),
                ),
                soft(
                    weights[-1],
                    _operator.eq,
                    1 / (nof_dimensions * (nof_dimensions - 1)),
                ),
            ],
            # [soft(bj, operator.gt, 0.0) for bj in weights],#?
            # unit tests failed with these -- perhaps they were implemented wrong?
            # or overdetermined system makes the solution wonky?
            [
                soft(
                    abscissae[-(1 + dimension)],
                    _operator.eq,
                    1.0 - abscissae[dimension],
                )
                for dimension in range(nof_dimensions)
            ],
            [
                soft(weights[-(1 + dimension)], _operator.eq, weights[dimension])
                for dimension in range(nof_dimensions)
            ],
        ]

    @classmethod
    def iiia(cls, soft, model_parameters):
        butcher_matrix, weights, abscissae = cls.unpack(model_parameters)
        nof_dimensions = len(abscissae)
        return [
            [
                soft(constraint, _operator.eq, 0.0)
                for constraint in cls.assumption_c(nof_dimensions)(model_parameters)
            ],
            [
                soft(constraint, _operator.eq, 0.0)
                for constraint in cls.assumption_d(nof_dimensions - 2)(model_parameters)
            ],
            [soft(a1j, _operator.eq, 0.0) for a1j in butcher_matrix[0]],
            [
                soft(asj, _operator.eq, bj)
                for asj, bj in zip(butcher_matrix[-1], weights)
            ],
        ]

    @classmethod
    def iiib(cls, soft, model_parameters):
        butcher_matrix, weights, abscissae = cls.unpack(model_parameters)
        nof_dimensions = len(abscissae)
        return [
            [
                soft(constraint, _operator.eq, 0.0)
                for constraint in cls.assumption_c(nof_dimensions - 2)(model_parameters)
            ],
            [
                soft(constraint, _operator.eq, 0.0)
                for constraint in cls.assumption_d(nof_dimensions)(model_parameters)
            ],
            [soft(ai[0], _operator.eq, weights[0]) for ai in butcher_matrix],
            [soft(ai[-1], _operator.eq, 0.0) for ai in butcher_matrix],
        ]

    @classmethod
    def iiic(cls, soft, model_parameters):
        butcher_matrix, weights, abscissae = cls.unpack(model_parameters)
        nof_dimensions = len(abscissae)
        return [
            [
                soft(constraint, _operator.eq, 0.0)
                for constraint in cls.assumption_c(nof_dimensions - 1)(model_parameters)
            ],
            [
                soft(constraint, _operator.eq, 0.0)
                for constraint in cls.assumption_d(nof_dimensions - 1)(model_parameters)
            ],
            [soft(ai[0], _operator.eq, weights[0]) for ai in butcher_matrix],
            [
                soft(asj, _operator.eq, bj)
                for asj, bj in zip(butcher_matrix[-1], weights)
            ],
        ]

    @classmethod
    def iiicstar(cls, soft, model_parameters):
        butcher_matrix, _, abscissae = cls.unpack(model_parameters)
        nof_dimensions = len(abscissae)
        return [
            [
                soft(constraint, _operator.eq, 0.0)
                for constraint in cls.assumption_c(nof_dimensions - 1)(model_parameters)
            ],
            [
                soft(constraint, _operator.eq, 0.0)
                for constraint in cls.assumption_d(nof_dimensions - 1)(model_parameters)
            ],
            [soft(ai[-1], _operator.eq, 0.0) for ai in butcher_matrix],
            [soft(a1j, _operator.eq, 0.0) for a1j in butcher_matrix[0]],
        ]

    @classmethod
    def create_constraint_system(
        cls, specific_constraints, soft=lambda x, cmp, y: cmp(x, y)
    ):
        def system(model_parameters):
            return _np.hstack(
                (
                    *cls.shared_constraints(soft, model_parameters),
                    *specific_constraints(soft, model_parameters),
                )
            )

        return system

    @classmethod
    def __try_to_minimize(
        cls, system_to_minimize, butcher_matrix, weights, abscissae, epsilon=1e-1
    ):
        sol = _sp.optimize.minimize(
            system_to_minimize, cls.pack(butcher_matrix, weights, abscissae)
        )
        if sol.success:
            cost = system_to_minimize(sol.x)
            butcher_matrix, weights, abscissae = cls.unpack(sol.x)
            return butcher_matrix, weights, abscissae, cost, sol.success
        else:
            if "x" in sol:
                cost = system_to_minimize(sol.x)
                if cost < epsilon:
                    butcher_matrix, weights, abscissae = cls.unpack(sol.x)
                    return butcher_matrix, weights, abscissae, cost, sol.success

    @classmethod
    def __try_to_find_kernel(
        cls, system_to_find_kernel, butcher_matrix, weights, abscissae
    ):
        # Need to choose a solver that allows for the output to be different than the input
        sol = _sp.optimize.root(
            system_to_find_kernel,
            cls.pack(butcher_matrix, weights, abscissae),
            method="lm",
        )
        if sol.success:
            residual = system_to_find_kernel(sol.x)
            butcher_matrix, weights, abscissae = cls.unpack(sol.x)
            return butcher_matrix, weights, abscissae, residual, sol.success

    @classmethod
    def __check_converged(cls, system_requirements, saved, latest):
        butcher_matrix, weights, abscissae = latest
        reqs = system_requirements(cls.pack(butcher_matrix, weights, abscissae))
        if all(
            [_np.allclose(savedi, latesti) for savedi, latesti in zip(saved, latest)]
        ):
            abscissae[0] = 0.0
            abscissae[-1] = 1.0
            return (
                (butcher_matrix.tolist(), weights.tolist(), abscissae.tolist()),
                True,
                sum(reqs),
            )
        else:
            abscissae[0] = 0.0
            abscissae[-1] = 1.0
            return (butcher_matrix, weights, abscissae), False, sum(reqs)

    @classmethod
    def estimate_butcher_tableu(
        cls, nof_dimensions, specific_constraints=None, initial_guess=None
    ):
        specific_constraints = (
            cls.iiic if specific_constraints is None else specific_constraints
        )
        if initial_guess is None:
            butcher_matrix = [
                [0.0 for _i in range(nof_dimensions)] for _j in range(nof_dimensions)
            ]
            weights = [0.0 for _i in range(nof_dimensions)]
            abscissae = [0.0 for _i in range(nof_dimensions)]
            abscissae[0] = 0.0
            abscissae[-1] = 1.0
        else:
            butcher_matrix, weights, abscissae = initial_guess

        def soft_min(lhs, cmp, rhs):
            return (not cmp(lhs, rhs)) * _np.linalg.norm(lhs - rhs)

        constraints_min = cls.create_constraint_system(specific_constraints, soft_min)

        def system_to_minimize(x):
            return _np.linalg.norm(constraints_min(x))

        def soft_0(lhs, cmp, rhs):
            return (not cmp(lhs, rhs)) * _np.linalg.norm(lhs - rhs)

        system_to_find_kernel = cls.create_constraint_system(
            specific_constraints, soft_0
        )

        system_requirements = cls.create_constraint_system(specific_constraints)

        saved_0 = (butcher_matrix, weights, abscissae)
        saved_min = (butcher_matrix, weights, abscissae)
        while True:
            converged_0 = None
            converged_min = None
            quality_0 = None
            quality_min = None
            for _ in range(2):
                result_0 = cls.__try_to_find_kernel(
                    system_to_find_kernel, butcher_matrix, weights, abscissae
                )
                if result_0:
                    butcher_matrix, weights, abscissae, _, _ = result_0
                    saved_0, converged_0, quality_0 = cls.__check_converged(
                        system_requirements,
                        saved_0,
                        (butcher_matrix, weights, abscissae),
                    )
                    if converged_0:
                        return saved_0

            for _ in range(2):
                result_min = cls.__try_to_minimize(
                    system_to_minimize, butcher_matrix, weights, abscissae
                )
                if result_min:
                    butcher_matrix, weights, abscissae, _, _ = result_min
                    saved_min, converged_min, quality_min = cls.__check_converged(
                        system_requirements,
                        saved_min,
                        (butcher_matrix, weights, abscissae),
                    )
                    if converged_min:
                        return saved_min
            if converged_0 and converged_min and quality_0 and quality_min:
                return saved_0 if quality_0 < quality_min else saved_min
            else:
                return None

    @classmethod
    def hardcoded_butcher_tableu(cls, order, identifier):
        if _operator.eq(identifier, cls.iiia):
            name = "lobatto_iiia"
        elif _operator.eq(identifier, cls.iiib):
            name = "lobatto_iiib"
        elif _operator.eq(identifier, cls.iiic):
            name = "lobatto_iiic"
        elif _operator.eq(identifier, cls.iiicstar):
            name = "lobatto_iiic*"
        else:
            name = identifier
        try:
            return (
                BUTCHER_TABLEU[name]["butcher_matrix"][order],
                BUTCHER_TABLEU[name]["weights"][order],
                BUTCHER_TABLEU[name]["abscissae"][order],
            )
        except KeyError:
            return None

    @classmethod
    def butcher_tableu(cls, order, identifier):
        result = cls.hardcoded_butcher_tableu(order, identifier)
        return result if result else cls.estimate_butcher_tableu(order, identifier)


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
    def general_intermediate_stages(
        butcher_matrix, abscissae, function, t_0, y_0, delta_t
    ):
        def system_for_intermediate_stages(intermediate_stages):
            nof_dimensions = len(abscissae)
            return [
                function(
                    t_0 + abscissae[dimension_i] * delta_t,
                    y_0
                    + delta_t
                    * sum(
                        [
                            butcher_matrix[dimension_i][dimension_j]
                            * intermediate_stages[dimension_j]
                            for dimension_j in range(nof_dimensions)
                        ]
                    ),
                )
                - intermediate_stages[dimension_i]
                for dimension_i in range(nof_dimensions)
            ]

        sol = _sp.optimize.root(
            system_for_intermediate_stages, _np.ones_like(abscissae)
        )
        return sol.x

    @staticmethod
    def explicit_intermediate_stages(
        butcher_matrix, abscissae, function, t_0, y_0, delta_t
    ):
        intermediate_stages = _np.zeros_like(abscissae)
        nof_dimensions = len(abscissae)
        for dimension_i in range(nof_dimensions):
            intermediate_stages[dimension_i] = function(
                t_0 + abscissae[dimension_i] * delta_t,
                y_0
                + delta_t
                * sum(
                    [
                        butcher_matrix[dimension_i][dimension_j]
                        * intermediate_stages[dimension_j]
                        for dimension_j in range(nof_dimensions)
                    ]
                ),
            )
        return intermediate_stages

    @classmethod
    def solve_for_intermediate_stages(
        cls, butcher_matrix, abscissae, function, t_0, y_0, delta_t
    ):
        if _np.allclose(butcher_matrix, _np.tril(butcher_matrix, -1)) and _np.allclose(
            abscissae, [0] + abscissae[1:]
        ):
            return cls.explicit_intermediate_stages(
                butcher_matrix, abscissae, function, t_0, y_0, delta_t
            )
        else:
            return cls.general_intermediate_stages(
                butcher_matrix, abscissae, function, t_0, y_0, delta_t
            )

    @staticmethod
    def consistent_abscissae(butcher_matrix):
        return [sum([aij for aij in ai]) for ai in butcher_matrix]

    @staticmethod
    def step(weights, _, y_0, delta_t, intermediate_stage):
        return y_0 + delta_t * sum(
            [weights[i] * intermediate_stage[i] for i in range(len(weights))]
        )

    @staticmethod
    def error_estimate(weights, weights_star, delta_t, intermediate_stages):
        nof_dimensions = len(weights)
        return delta_t * sum(
            [
                (weights[dimension_i] - weights_star[dimension_i])
                * intermediate_stages[dimension_i]
                for dimension_i in range(nof_dimensions)
            ]
        )

    def __init__(self, function, t_0, y_0, butcher_matrix, weights, abscissae=None):
        self.butcher_matrix = butcher_matrix
        self.weights = weights
        self.abscissae = (
            self.consistent_abscissae(butcher_matrix)
            if abscissae is None
            else abscissae
        )
        self.function = function
        self.t_0 = t_0
        self.y_0 = y_0
        self.intermediate_stages = None

    def __call__(self, delta_t):
        self.intermediate_stages = self.solve_for_intermediate_stages(
            self.butcher_matrix,
            self.abscissae,
            self.function,
            self.t_0,
            self.y_0,
            delta_t,
        )
        return self.step(
            self.weights, self.function, self.y_0, delta_t, self.intermediate_stages
        )


# class PredictorCorrector:
#     def __init__(self, predictor, corrector):
#         self.predictor = predictor
#         self.corrector = corrector
#
#     def __call__(self, function, t_0, y_0, delta_t=None):
#         delta_t = delta_t if delta_t is None else np.spacing(t_0)
