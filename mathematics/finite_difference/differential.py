from collections import Counter as _Counter

import numpy as _np

from ..algebra.pointwise import Pointwise as _Pointwise


def _flow(direction, dt):
    def flow_for(function):
        return (
            function if isinstance(function, _Pointwise) else _Pointwise(function)
        ).after(
            lambda point: point
            + dt
            * (
                direction
                if isinstance(direction, _Pointwise)
                else _Pointwise(direction)
            )(point)
        )

    return flow_for


def _finite_forward_difference(direction, dt):
    def finite_forward_difference_for(function):
        return (
            _flow(direction, dt)(function) - _flow(direction, 0)(function)
        ) / _Pointwise(dt)

    return finite_forward_difference_for


def _finite_central_difference(direction, dt):
    def finite_central_difference_for(function):
        return (
            _flow(direction, dt)(function)
            - 2.0 * _flow(direction, 0)(function)
            + _flow(direction, -dt)(function)
        ) / _Pointwise(dt ** 2)

    return finite_central_difference_for


def __dt_heuristic(direction, function, derivative_order, approximation_order, *args):
    """
    informative stackexchange answers:
        https://math.stackexchange.com/a/2488893/68036
        https://math.stackexchange.com/a/819015/68036
    """
    max_float_spacing_in_codomain = max(
        (_np.spacing(fi)) for fi in _np.ravel(function(*args))
    )

    recommended_dt = abs(max_float_spacing_in_codomain) ** (
        1.0 / (derivative_order + approximation_order)
    )
    trial_dts = [recommended_dt * (10.0 ** exponent) for exponent in range(0, 10)]
    trial_dfs = [
        _finite_forward_difference(direction, dt)(function)(*args) for dt in trial_dts
    ]
    trial_dfs_rounded = [
        tuple(float(format(val, ".3e")) for val in _np.ravel(trial_df))
        for trial_df in trial_dfs
    ]
    counts = _Counter(trial_dfs_rounded)
    for rounded_value, _ in counts.most_common(1):
        first_common_dt = trial_dts[trial_dfs_rounded.index(rounded_value)]
        return first_common_dt


def __finite_forward_difference_heuristic(direction):
    def finite_forward_difference_heuristic_for(function):
        return lambda *args: _finite_forward_difference(
            direction, __dt_heuristic(direction, function, 1, 1, *args)
        )(function)(*args)

    return finite_forward_difference_heuristic_for


def __finite_central_difference_heuristic(direction):
    def finite_central_difference_heuristic_for(function):
        return lambda *args: _finite_central_difference(
            direction, __dt_heuristic(direction, function, 1, 2, *args)
        )(function)(*args)

    return finite_central_difference_heuristic_for


def directional_derivative(*directions):
    """
    The directional derivative of F in the direction v at the application point u is usually written DF(u)(v), here it is more like D(v)(F)(u)
    https://en.wikipedia.org/wiki/Differentiation_in_Fr%C3%A9chet_spaces#Mathematical_details

    directional_derivative(direction)(f)(application_point)

    directional_derivative(dn,...,d2,d1)(f)(application_point)
    """

    if len(directions) == 1:
        return lambda function: __finite_forward_difference_heuristic(directions[-1])(
            function
        )
    elif len(directions) > 1:
        return lambda function: __finite_forward_difference_heuristic(directions[:-1])(
            directional_derivative(*directions[:-1])
        )
