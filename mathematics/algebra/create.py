import functools
import itertools
import operator

import sympy

from .clifford import Clifford


def class_factory(name, baseclasses, **kwargs):
    if name in globals():
        return globals()[name]
    else:
        result = type(name, baseclasses, kwargs)
        globals()[name] = result
        return globals()[name]


def create_clifford(name, symmetric_bilinear_form):
    return class_factory(
        name, (Clifford,), symmetric_bilinear_form=symmetric_bilinear_form
    )


def multilinear_mapping_as_tensor(cls, vector_base_to_dual_base, *vector_bases):
    r"""
	Expands multilinear function as tensor. 
	NOTE: not sure if the math is valid for vector valued multilinear mappings.

	:param: *vector_bases: Vector space base of each argument of the function.
	:return: Returns a lambda function which takes the mulilinear function. 

	.. math::
		f \mapsto \mathsf{F}=
		f(\mathbf{e}_{i_1}^{(1)},\ldots,\mathbf{e}_{i_k}^{(k)}) \cdot {\mathbf{e}_{i_1}^{(1)}}^{*}\otimes\cdots\otimes{\mathbf{e}_{i_k}^{(k)}}^{*} 
		= f(\mathbf{e}_{i_1}^{(1)},\ldots,\mathbf{e}_{i_k}^{(k)}) \cdot \mathbf{e}_{(1)}^{i_1}\otimes\cdots\otimes\mathbf{e}_{(k)}^{i_k} 

	:rtype: [type]
	"""
    dual_vector_bases = tuple(
        vector_base_to_dual_base(vector_base) for vector_base in vector_bases
    )
    return lambda f, vector_bases=vector_bases, dual_bases=dual_vector_bases: functools.reduce(
        operator.add,
        [
            cls(
                {
                    tuple(
                        dual_bases[vector_space_index][tensor_index[vector_space_index]]
                        for vector_space_index in range(0, len(dual_bases))
                    ): f(
                        *[
                            vector_bases[vector_space_index][
                                tensor_index[vector_space_index]
                            ]
                            for vector_space_index in range(0, len(vector_bases))
                        ]
                    )
                }
            )
            for tensor_index in itertools.product(
                *[range(0, len(vector_base)) for vector_base in vector_bases]
            )
        ],
        cls(),
    )


def mixed_tensor(cls, vector_base, order, vector_base_to_dual_base):
    contravariant_order, covariant_order = order
    dual_base = vector_base_to_dual_base(vector_base)
    return multilinear_mapping_as_tensor(
        cls,
        vector_base_to_dual_base,
        *[dual_base] * contravariant_order,
        *[vector_base] * covariant_order
    )


def kronecker_delta_tensor(cls, vector_base, vector_base_to_dual_base):
    r"""Returns kronecker delta
	(GUESS) :math:`\boldsymbol{\delta} = \sum_{i,j} e_j^{*}(e_i) e_i^{**} \otimes e_j^{*}`
    :param cls:
    :param vector_base:
    :param vector_base_to_dual_base:
	:return: kronecker delta as a mixed tensor
	"""
    return mixed_tensor(cls, vector_base, vector_base_to_dual_base, (1, 1))(
        lambda cov, con: cov(con)
    )


def symbolic_tensor(cls, symbol, vector_base, order, vector_base_to_dual_base):
    """[summary]
	
    :param cls:
	:param symbol: Example: "A"
	:param symbol: [str]
	:param vector_base: e.g. tensor.standard_base_vectorspace(dimension) or sympy.symbols("e_{0:3}")
	:param order: [description]
    :param vector_base_to_dual_base:
	:return: [description]
	"""

    def latex_vector_base_vector(vector_base, dual_base, v):
        return "".join(
            [
                "^{",
                str(dual_base.index(v) if v in dual_base else " "),
                "}",
                "_{",
                str(vector_base.index(v) if v in vector_base else " "),
                "}",
            ]
        )

    def latex_tensor_base_vector(vector_base, dual_base, tensor_base_vector):
        return "".join(
            [
                latex_vector_base_vector(vector_base, dual_base, v)
                for v in tensor_base_vector
            ]
        )

    def make_symbol(symbol, vector_base, dual_base, tensor_base_vector):
        return sympy.Symbol(
            (symbol + "{indices}").format(
                indices=latex_tensor_base_vector(
                    vector_base, dual_base, tensor_base_vector
                )
            )
        )

    return mixed_tensor(cls, vector_base, order, vector_base_to_dual_base)(
        lambda *tensor_base_vector, symbol=symbol, vector_base=vector_base, dual_base=vector_base_to_dual_base(
            vector_base
        ): make_symbol(
            symbol, vector_base, dual_base, tensor_base_vector
        )
    )


def same_coefficient_tensor(
    cls, coefficient, vector_base, rank, vector_base_to_dual_base
):
    return mixed_tensor(cls, vector_base, rank, vector_base_to_dual_base)(
        lambda *indices: coefficient
    )
