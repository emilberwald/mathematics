from collections import Counter
from ..algebra.pointwise import Pointwise

import numpy as np


def flow(direction, dt):
    def flow_for(function):
        return (
            function if isinstance(function, Pointwise) else Pointwise(function)
        ).after(
            lambda application_point: application_point
            + dt
            * (direction if isinstance(direction, Pointwise) else Pointwise(direction))(
                application_point
            )
        )

    return flow_for


def finite_forward_difference(direction, dt):
    def finite_forward_difference_for(function):
        return (
            flow(direction, dt)(function) - flow(direction, 0)(function)
        ) / Pointwise(dt)

    return finite_forward_difference_for


def dt_heuristic(
    direction, function, application_point, derivative_order, approximation_order
):
    """
    informative stackexchange answers:
        https://math.stackexchange.com/a/2488893/68036
        https://math.stackexchange.com/a/819015/68036
    """
    max_float_spacing_in_codomain = max(
        (np.spacing(fi)) for fi in np.ravel(function(application_point))
    )

    recommended_dt = max_float_spacing_in_codomain ** (
        1.0 / (derivative_order + approximation_order)
    )
    trial_dts = [recommended_dt * (10.0 ** exponent) for exponent in range(0, 10)]
    trial_dfs = [
        finite_forward_difference(direction, dt)(function)(application_point)
        for dt in trial_dts
    ]
    trial_dfs_rounded = [
        tuple(float(format(val, ".3e")) for val in np.ravel(trial_df))
        for trial_df in trial_dfs
    ]
    counts = Counter(trial_dfs_rounded)
    for rounded_value, _ in counts.most_common(1):
        first_common_dt = trial_dts[trial_dfs_rounded.index(rounded_value)]
        return first_common_dt


def finite_forward_difference_heuristic(direction):
    def finite_forward_difference_heuristic_for(function):
        return lambda application_point: finite_forward_difference(
            direction, dt_heuristic(direction, function, application_point, 1, 1)
        )(function)(application_point)

    return finite_forward_difference_heuristic_for


def directional_derivative(*directions):
    """
    The directional derivative of F in the direction v at the application point u is usually written DF(u)(v), here it is more like D(v)(F)(u)
    https://en.wikipedia.org/wiki/Differentiation_in_Fr%C3%A9chet_spaces#Mathematical_details

    directional_derivative(direction)(f)(application_point)

    directional_derivative(dn,...,d2,d1)(f)(application_point)
    """

    if len(directions) == 1:
        return lambda function: finite_forward_difference_heuristic(directions[-1])(
            function
        )
    elif len(directions) > 1:
        return lambda function: finite_forward_difference_heuristic(directions[:-1])(
            directional_derivative(*directions[:-1])
        )
