"""
calculus.py
"""

import functools as _functools
import itertools as _itertools

import numpy as _np


def projected_metric(metric_tensor):
    r"""
	:param metric_tensor: :math:`\gamma(e_i,e_j)=g(e_i,e_j)-\frac{g(e_0,e_i)g(e_0,e_j)}{g(e_0,e_0}`
		:param metric_tensor: :math:`g(e_i,e_j)e^i\otimes e^j`
	"""
    return _np.array(
        [
            metric_tensor[(i, j)] - metric_tensor[(0, i)] * metric_tensor[(0, j)] / metric_tensor[(0, 0)]
            for (i, j) in _itertools.product(range(1, 4), repeat=2)
        ]
    ).reshape((3, 3), order="C")


def permutation_symbol(*indices):
    return _functools.reduce(
        lambda x, y: x * y,
        [_np.sign(indices[j] - indices[i]) for i in range(0, len(indices)) for j in range(i + 1, len(indices))],
    )


def musical_isomorphism_flat(metric_tensor, tensor, nof_indices_lowered=None):
    r"""Lower index (of component of contravariant tensor)
		:param metric_tensor: :math:`g(e_i,e_j)e^i\otimes e^j`
		:param tensor: :math:`T(e^{i})e_i`
		:param nof_indices_lowered:
		:return: ::math:`Xb(e_j)e^j`
	"""
    nof_dimensions = max(metric_tensor.shape)
    nof_indices = len(tensor.shape)  # Number of tensored spaces / tensor degree
    nof_indices_lowered = nof_indices if nof_indices_lowered is None else nof_indices_lowered
    return _np.array(
        [
            sum(
                [
                    _functools.reduce(lambda x, y: x * y, [metric_tensor[(i, j)] for (i, j) in zip(I_i, I_j)],)
                    * tensor[(I_i + I_rest)]
                    for I_i in _itertools.product(range(0, nof_dimensions), repeat=nof_indices_lowered)
                ]
            )
            for I_j in _itertools.product(range(0, nof_dimensions), repeat=nof_indices_lowered)
            for I_rest in _itertools.product(range(0, nof_dimensions), repeat=nof_indices - nof_indices_lowered)
        ]
    ).reshape((nof_dimensions,) * nof_indices, order="C")


def musical_isomorphism_sharp(metric_tensor, tensor, nof_indices_raised=None):
    r"""Raise index (of component of covariant tensor)
		:param metric_tensor: :math:`g(e_i,e_j)e^i\otimes e^j`
		:param tensor: :math:`T(e_i)e^i`
		:param nof_indices_raised:
		:return: :math:`T♯(e^j)e_j`
	"""
    nof_dimensions = max(metric_tensor.shape)
    nof_indices = len(tensor.shape)  # Number of tensored spaces / tensor degree
    nof_indices_raised = nof_indices if nof_indices_raised is None else nof_indices_raised
    ginv = _np.linalg.inv(metric_tensor)
    return _np.array(
        [
            sum(
                [
                    _functools.reduce(lambda x, y: x * y, [ginv[(i, j)] for (i, j) in zip(I_i, I_j)])
                    * tensor[(I_i + I_rest)]
                    for I_i in _itertools.product(range(0, nof_dimensions), repeat=nof_indices_raised)
                ]
            )
            for I_j in _itertools.product(range(0, nof_dimensions), repeat=nof_indices_raised)
            for I_rest in _itertools.product(range(0, nof_dimensions), repeat=nof_indices - nof_indices_raised)
        ]
    ).reshape((nof_dimensions,) * nof_indices, order="C")


def create_covariant_permutation_tensor(metric_tensor, nof_indices):
    nof_dimensions = max(metric_tensor.shape)
    coeff = _np.sqrt(_np.abs(_np.linalg.det(metric_tensor)))
    return _np.array(
        [
            coeff * permutation_symbol(*indices)
            for indices in _itertools.product(range(0, nof_dimensions), repeat=nof_indices)
        ]
    ).reshape((nof_dimensions,) * nof_indices, order="C")


def create_contravariant_permutation_tensor(metric_tensor, nof_indices):
    return musical_isomorphism_sharp(
        metric_tensor, create_covariant_permutation_tensor(metric_tensor, nof_indices), nof_indices,
    )


def hodge_star(metric_tensor, tensor):
    """https://en.wikipedia.org/wiki/Hodge_star_operator#Expression_in_index_notation
	http://phys.columbia.edu/~cyr/notes/Electrodynamics/CPope-DiffForms-p56-67.pdf
	"""
    nof_indices = len(tensor.shape)
    nof_dimensions = max(metric_tensor.shape)
    permutation_tensor_cov = create_covariant_permutation_tensor(metric_tensor, nof_dimensions)
    permutation_tensor_con_cov = musical_isomorphism_sharp(metric_tensor, permutation_tensor_cov, nof_indices)
    coefficient = 1.0 / _np.math.factorial(nof_dimensions - nof_indices)
    return _np.array(
        [
            sum(
                [
                    coefficient * tensor[I_k] * permutation_tensor_con_cov[I_k + I_rest]
                    for I_k in _itertools.product(range(0, nof_dimensions), repeat=nof_indices)
                ]
            )
            for I_rest in _itertools.product(range(0, nof_dimensions), repeat=nof_dimensions - nof_indices)
        ]
    ).reshape((nof_dimensions,) * (nof_dimensions - nof_indices), order="C")


def grad(exterior_derivative, metric_tensor, function):
    r"""https://physics.stackexchange.com/a/377844/28273
		:param exterior_derivative: D(x) => (d/dx_0 x, d/dx_1 x, d/dx_2 x)
		:param metric_tensor: :math:`g(e_i,e_j) e^i \otimes e^j` also see :func:`projected_metric`
		:param function: :math:`f`
	"""
    return musical_isomorphism_sharp(metric_tensor, exterior_derivative(function), 1)


def curl(exterior_derivative, metric_tensor, tensor):
    r"""https://physics.stackexchange.com/a/377844/28273
		https://math.stackexchange.com/questions/337971/can-the-curl-operator-be-generalized-to-non-3d
		:param exterior_derivative: D(x) => (d/dx_0 x, d/dx_1 x, d/dx_2 x)
		:param metric_tensor: :math:`g(e_i,e_j) e^i \otimes e^j` also see :func:`projected_metric`
		:param tensor: :math:`x^i e_i`
	"""
    nof_indices = len(tensor.shape)
    nof_dimensions = max(metric_tensor.shape)
    tensor_b = musical_isomorphism_flat(metric_tensor, tensor, nof_indices)
    d_tensor_b = _np.array(
        [
            exterior_derivative(tensor_b[I])[j]
            for I in _itertools.product(range(0, nof_dimensions), repeat=nof_indices)
            for j in range(0, nof_dimensions)
        ]
    ).reshape((nof_dimensions,) * (nof_indices + 1))
    star_d_tensor_b = hodge_star(metric_tensor, d_tensor_b)
    return musical_isomorphism_sharp(metric_tensor, star_d_tensor_b, nof_dimensions - (nof_indices + 1))


def div(exterior_derivative, metric_tensor, tensor):
    r"""https://physics.stackexchange.com/a/377844/28273
		:param exterior_derivative: D(x) => (d/dx_0 x, d/dx_1 x, d/dx_2 x)
		:param metric_tensor: :math:`g(e_i,e_j) e^i \otimes e^j` also see :func:`projected_metric`
		:param tensor: :math:`x^i e_i`
	"""
    nof_indices = len(tensor.shape)
    nof_dimensions = max(metric_tensor.shape)
    tensor_flat = musical_isomorphism_flat(metric_tensor, tensor, nof_indices)
    star_tensor_flat = hodge_star(metric_tensor, tensor_flat)
    d_star_tensor_b = _np.array(
        [
            exterior_derivative(star_tensor_flat[I])[j]
            for I in _itertools.product(range(0, nof_dimensions), repeat=nof_dimensions - nof_indices)
            for j in range(0, nof_dimensions)
        ]
    ).reshape((nof_dimensions,) * (nof_dimensions - nof_indices + 1))
    return hodge_star(metric_tensor, d_star_tensor_b)
