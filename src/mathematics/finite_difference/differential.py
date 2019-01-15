import numpy as np


def flow():
    # flow()(direction)(t)(f)(application_point)
    return lambda direction: lambda dt: lambda f: lambda application_point: f(
        application_point + dt * direction
    )


def finite_forward_difference():
    # finite_forward_difference()(direction)(f)(application_point)(dt)
    return lambda direction: (
        lambda f: lambda application_point: lambda dt: (
            flow()(direction)(dt)(f)(application_point)
            - flow()(direction)(0)(f)(application_point)
        )
        / dt
    )


def dt_heuristic():
    # dt_heuristic()(direction)(f)(application_point)(derivative_order,approximation_order)
    # inspired from https://math.stackexchange.com/a/2488893/68036
    return lambda direction: lambda f: lambda application_point: lambda derivative_order, approximation_order: (
        max(
            [
                np.spacing(fi)
                for fi in np.ravel(
                    flow()(direction)(0)(f)(application_point)
                )  # np.ravel for the corner case that fi is a float
            ]
        )
    ) ** (
        1.0 / (derivative_order + approximation_order)
    )


def directional_derivative(*directions):
    """
        The directional derivative of F in the direction v at the application point u is usually written DF(u)(v)
        Here it is instead D(v)(F)(u)
    """

    # https://en.wikipedia.org/wiki/Differentiation_in_Fr%C3%A9chet_spaces#Mathematical_details
    # gradient_of_function(direction)(f)(application_point)
    if len(directions) == 1:
        return lambda f: lambda application_point: finite_forward_difference()(
            directions[-1]
        )(f)(application_point)(
            dt_heuristic()(directions[-1])(f)(application_point)(1, 1)
        )
    elif len(directions) > 1:
        return lambda f: lambda application_point: directional_derivative(
            directions[-1]
        )(directional_derivative(*directions[:-1])(f))(application_point)


def covariant_derivative(connection_for_coordinate_system):
    """[summary]
    
    :param directions: [description]
    :param connection_for_coordinate_system: covariant_derivative(connection)(direction)(v)(p) = directional_derivative()(direction)(v)(p) + connection_for_coordinate_system(direction,v)(p)
                       NOTE: the connection_for_coordinate_system transforms when the coordinate system is changed. It depends on first and second derivatives.
                             Imposing compatability with metric makes it unique.
    :rtype: [type]
    """
    return lambda direction: lambda vector_valued_vector_function: lambda application_point: directional_derivative()(
        direction
    )(
        vector_valued_vector_function
    )(
        application_point
    ) + connection_for_coordinate_system(
        direction, vector_valued_vector_function
    )(
        application_point
    )
