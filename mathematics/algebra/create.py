import functools as _functools
import itertools as _itertools
import operator as _operator

import sympy

from .clifford import Clifford
from .pointwise import Pointwise


def class_factory(name, *baseclasses, **kwargs):
    if name in globals():
        return globals()[name]
    else:
        result = type(name, baseclasses, kwargs)
        globals()[name] = result
        return globals()[name]


def create_clifford(name, symmetric_bilinear_form):
    return class_factory(name, Clifford, symmetric_bilinear_form=symmetric_bilinear_form)


def multilinear_mapping_as_tensor(cls, slot_to_dual, *bases):
    r"""
	Expands multilinear function as tensor.
	NOTE: not sure if the math is valid for vector valued multilinear mappings.

	:param slot_to_dual:	Converts a (basis-)vector to its corresponding dual
	:param *bases:			tuple where each element is an ordered basis.
							Each ordered basis appears in same order as in the function call.
	:return:				Returns a lambda with domain over (scalar or vector-valued-)multilinear functions.

	.. math::
		f \mapsto \mathsf{F}
		\\=
		f(\mathbf{e}_{i_1}^{(1)},\ldots,\mathbf{e}_{i_k}^{(k)}) \otimes {\mathbf{e}_{i_1}^{(1)}}^{*}\otimes\cdots\otimes{\mathbf{e}_{i_k}^{(k)}}^{*}
		\\=
		\begin{cases}
			f(\mathbf{e}_{i_1}^{(1)},\ldots,\mathbf{e}_{i_k}^{(k)}) \otimes \mathbf{e}_{(1)}^{i_1}\otimes\cdots\otimes\mathbf{e}_{(k)}^{i_k} &\text{(codomain is field)}
		\\  f(\mathbf{e}_{i_1}^{(1)},\ldots,\mathbf{e}_{i_k}^{(k)})^{i_{\operatorname{cod}f}} \otimes \mathbf{e}^{(\operatorname{cod}f)}_{i_{\operatorname{cod}f}} \otimes \mathbf{e}_{(1)}^{i_1}\otimes\cdots\otimes\mathbf{e}_{(k)}^{i_k} & \text{(codomain is vector space)}
		\end{cases}

	:rtype: [type]
	"""
    return lambda multilinear_mapping: _functools.reduce(
        _operator.add,
        [
            cls(
                {
                    tuple(
                        slot_to_dual(bases[base_index][base_index_to_basis_index[base_index]])
                        for base_index in range(0, len(bases))
                    ): multilinear_mapping(
                        *[
                            bases[base_index][base_index_to_basis_index[base_index]]
                            for base_index in range(0, len(bases))
                        ]
                    )
                }
            )
            for base_index_to_basis_index in _itertools.product(*[range(0, len(basis)) for basis in bases])
        ],
    )


def kronecker_delta_tensor(cls, basis, slot_to_dual):
    r"""Returns kronecker delta
	(GUESS) :math:`\boldsymbol{\delta} = \sum_{i,j} e_j^{*}(e_i) e_i^{**} \otimes e_j^{*}`
	:param cls:
	:param basis:
	:param slot_to_dual:
	:return: kronecker delta as a mixed tensor
	"""
    return multilinear_mapping_as_tensor(cls, slot_to_dual, basis, tuple(slot_to_dual(slot) for slot in basis))


def make_symbol(symbol, basis, dual_basis, tensor_base):
    def latex_base(slot):
        return "".join(
            [
                "^{",
                str(dual_basis.index(slot) if slot in dual_basis else " "),
                "}",
                "_{",
                str(basis.index(slot) if slot in basis else " "),
                "}",
            ]
        )

    def latex_tensor_base(tensor_base):
        return "".join([latex_base(slot) for slot in tensor_base])

    return sympy.Symbol((symbol + "{indices}").format(indices=latex_tensor_base(basis)))


def mixed_tensor(cls, symbol, basis, order, slot_to_dual):
    """
		:param cls:
		:param symbol:	Example: "A"
		:param basis:	Contravariant basis
						Examples:
						.. code-block:: python
							sympy.symbols("e_{0:3}")
							standard_base_vectorspace(dimension)
		:param order:			(contravariant order, covariant order)
		:param slot_to_dual:	maps vector basis base to dual vector basis base
		:return: [description]

		A change of scale from meters to smaller unit...
			*contravariant* vector (component bigger, base shorter)
				ex: velocity			(distance/time)
			*covariant* vector base (component smaller, base longer)
				ex: spatial gradient	(1/distance)
	"""

    contravariant_order, covariant_order = order
    return multilinear_mapping_as_tensor(
        cls,
        slot_to_dual,
        *((basis,) * contravariant_order),
        *((tuple(slot_to_dual(base) for base in basis),) * covariant_order)
    )
