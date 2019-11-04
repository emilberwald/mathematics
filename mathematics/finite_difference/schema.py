from math import gamma

import numpy as _np


# https://en.wikipedia.org/wiki/Finite_difference_coefficient#Arbitrary_stencil_points
def one_dimensional_schema(stencil_points, derivative_order):
    """

    Order of accuracy: O(h^(nof_stencil_points-derivative_order))

    :param stencil_points:
    :param derivative_order:
    :return: weights for stencil points
    """
    assert derivative_order < len(stencil_points)
    nof_stencil_points = len(stencil_points)
    lhs = [
        [point ** order for point in stencil_points]
        for order in range(0, nof_stencil_points)
    ]
    factorial = gamma(derivative_order + 1)
    rhs = [
        factorial if derivative_order == order else 0
        for order in range(0, len(stencil_points))
    ]

    weights = _np.linalg.solve(lhs, rhs)
    return weights


def fornberg(upper_derivative_order, x0, grid_points):
    d = [
        [
            [0 for gridpoint_no in range(0, upper_gridpoint_no + 1)]
            for upper_gridpoint_no in range(0, len(grid_points))
        ]
        for derivative_order in range(0, upper_derivative_order + 1)
    ]
    d[0][0][0] = 1
    c1 = 1
    for upper_gridpoint_no in range(1, len(grid_points)):
        c2 = 1
        for gridpoint_no in range(0, upper_gridpoint_no):
            c3 = grid_points[upper_gridpoint_no] - grid_points[gridpoint_no]
            c2 = c2 * c3
            for derivative_order in range(
                0, min(upper_gridpoint_no, upper_derivative_order) + 1
            ):
                try:
                    coeff0 = d[derivative_order][upper_gridpoint_no - 1][gridpoint_no]
                except (IndexError, KeyError) as _:
                    coeff0 = 0
                try:
                    coeff1 = d[derivative_order - 1][upper_gridpoint_no - 1][
                        gridpoint_no
                    ]
                except (IndexError, KeyError) as _:
                    coeff1 = 0
                d[derivative_order][upper_gridpoint_no][gridpoint_no] = (
                    (grid_points[upper_gridpoint_no] - x0) * coeff0
                    - derivative_order * coeff1
                ) / c3
        for derivative_order in range(
            0, min(upper_gridpoint_no, upper_derivative_order) + 1
        ):
            try:
                coeff0 = d[derivative_order - 1][upper_gridpoint_no - 1][
                    upper_gridpoint_no - 1
                ]
            except (IndexError, KeyError) as _:
                coeff0 = 0
            try:
                coeff1 = d[derivative_order][upper_gridpoint_no - 1][
                    upper_gridpoint_no - 1
                ]
            except (IndexError, KeyError) as _:
                coeff1 = 0
            d[derivative_order][upper_gridpoint_no][upper_gridpoint_no] = (
                c1
                / c2
                * (
                    derivative_order * coeff0
                    - (grid_points[upper_gridpoint_no - 1] - x0) * coeff1
                )
            )
        c1 = c2
    return d


def lambda_fornberg(upper_derivative_order, x0, grid_points):
    d = fornberg(upper_derivative_order, x0, grid_points)
    return [
        [
            lambda f: sum(
                [
                    d[derivative_order][upper_gridpoint_no][grid_point_no]
                    * f(grid_points[grid_point_no])
                    for grid_point_no in range(0, upper_gridpoint_no + 1)
                ]
            )
            for upper_gridpoint_no in range(derivative_order, len(grid_points))
        ]
        for derivative_order in range(0, upper_derivative_order + 1)
    ]
