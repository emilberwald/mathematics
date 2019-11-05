"""
Tensor algebra
"""

__all__ = ["Tensor"]
import copy

from pylatexenc.latex2text import LatexNodes2Text

from .dual import Dual


class Tensor(dict):
    @staticmethod
    def __merge_keys(*keys):
        r"""Tensor product for pure tensors without coefficients.
		
		:param keys: each argument is a tensor base vector :math:`\mathsf{e_A} = \mathbf{e}_0\otimes\ldots\otimes \mathbf{e}_{order(\mathsf{e_A})-1}`
		:type e_A: [tuple]
		:return: :math:`\bigotimes_{\mathsf{e_A}\in \textup{base tensors}}\mathsf{e_A} = \bigotimes_{\mathsf{e_A}\in \textup{base tensors}}(\bigotimes_{\mathbf{e}_k\in \mathsf{e_A}} \mathbf{e}_k)`
		:rtype: [tuple]
		"""
        return tuple(slot for key in keys for slot in key)

    # region algebraic operations

    def __rmul__(self, scalar):
        r"""scalar product
		(DEFINITION) Compatability of tensor scalar multiplication with vector scalar multiplication

		.. math::
			c\cdot \mathsf{t} = c\cdot(\mathbf{t_1}\otimes \mathbf{t_2}) = (c \cdot \mathbf{t_1})\otimes \mathbf{t_2} = \mathbf{t_1}\otimes(c \cdot \mathbf{t_2})

		(GUESS) Compatability of tensor scalar multiplication with field multiplication

		.. math::
			c_1\cdot(c_2\cdot (\mathsf{t_1}\otimes \mathsf{t_2})) = (c_1 \cdot_F c_2)\mathsf{t_1}\otimes \mathsf{t_2}

		(GUESS) Distributivity of scalar multiplication with respect to tensor addition

		.. math::
			c_1\cdot(\mathsf{t_1}\otimes \mathsf{t_2} + \mathsf{t_3}\otimes \mathsf{t_4}) = c_1\cdot(\mathsf{t_1}\otimes \mathsf{t_2}) + c_1\cdot(\mathsf{t_3}\otimes \mathsf{t_4}) 

		(GUESS) The scalar can be distributed into the coefficient of each pure tensor term.
		
		:param self: tensor
		:type self: [tensor]
		:param scalar: scalar
		:return: scaled tensor 
		:rtype: [tensor]
		"""

        return type(self)({key: scalar * self[key] for key in self.keys()})

    def __add__(self, B):
        r"""tensor addition
		(DEFINITION) (not used) If all but one coordinate are the same, addition can be combined.

		.. math::
			(v_1 + v_2)\otimes w_1 = v_1\otimes w_1 + v_2\otimes w_1
			v_1\otimes (w_1+w_2) = v_1\otimes w_1 + v_1\otimes w_2
		(GUESS): Distributivity of scalar multiplication with respect to field addition

		.. math::
			(c_1 + c_2)(e_i\otimes e_j) = c_1 (e_i \otimes e_j) + c_2 (e_i\otimes e_j)
		We want to distribute the addition as much as possible.
		The internal state of the tensor is in terms of pure tensors of the vector bases.

		:param self: tensor
		:type self: [tensor]
		:param B: summand
		:type B: [tensor]
		:return:
		.. math::
			\mathsf{self}+\mathsf{B} 
			= (c_1(\mathsf{{e_1}_i}) \mathsf{{e_1}_i})+(c_2(\mathsf{{e_2}_i}) \mathsf{{e_2}_i})
			= \left[\sum_{\mathsf{{e_1}_k} \notin \{\mathsf{{e_2}_i}\}} c_1(\mathsf{{e_1}_k}) \mathsf{{e_1}_k}\right]
			+ \left[\sum_{\mathsf{{e_2}_k} \notin \{\mathsf{{e_1}_i}\}} c_2(\mathsf{{e_2}_k}) \mathsf{{e_2}_k}\right]
			+ \left[\sum_{\mathsf{{e_1}_k} \in \{\mathsf{{e_2}_i}\}} (c_1(\mathsf{{e_1}_k}) + c_2(\mathsf{{e_1}_k})) \mathsf{{e_1}_k}\right]
		:rtype: [tensor]
		"""

        A = copy.deepcopy(self)
        for B_key in B.keys():
            if B_key in self.keys():
                A[B_key] = self[B_key] + B[B_key]
            else:
                A[B_key] = B[B_key]
        return A

    def __neg__(self):
        return type(self)({key: -self[key] for key in self.keys()})

    def __sub__(self, B):
        return self.__add__(-B)

    def __matmul__(self, B):
        r"""Tensor procuct of tensors.
		(GUESS) This whole function is guesswork. I think the proper term is unbiased monodial category?
		
		:param self: tensor
		:type self: [tensor]
		:param B: tensor
		:type B: [tensor]
		:return: :math:`\mathsf{self} \otimes \mathsf{B} = (\sum_i c_1^i \mathsf{e_1}_i)\otimes(\sum_i c_2^i \mathsf{e_2}_i) = \sum_i \sum_j (c_1^i\cdot c_2^j)\cdot(\mathsf{e_1}_i \otimes \mathsf{e_2}_j)`
		:rtype: [tensor]
		"""
        tensor_product = type(self)()
        for self_key, self_value in self.items():
            for B_key, B_value in B.items():
                merged_key = type(self).__merge_keys(self_key, B_key)
                if merged_key not in tensor_product.keys():
                    tensor_product[merged_key] = self_value * B_value
                else:
                    # perhaps this could happen if one of the tensor base vectors are of mixed order?
                    # GUESS: summation best way to handle this?
                    tensor_product = tensor_product + type(self)(
                        {merged_key: self_value * B_value}
                    )
        return tensor_product

    def braiding_map(self, slot_permutation):
        """[summary]
		NOTE: mutates self and returns self (to allow chains)
		
		:param slot_permutation: [description]
		:type slot_permutation: [type]
		:return: [description]
		:rtype: [type]
		"""

        result = type(self)(
            {
                tuple(key[slot_index] for slot_index in slot_permutation): self[key]
                for key in self.keys()
            }
        )
        self.clear()
        self.update(result)
        return self

    def trace(self, first_slot_index, second_slot_index, pairing=None):
        r"""Trace/contraction of tensor, over vector space indices as indicated in first_slot_index and second_slot_index, 
		
		NOTE: Might not work for braided monodial categories since it does not contract until fixpoint (it calls braiding_map though)
		NOTE: the default pairing tries both cov(con) and con(cov)
		:param self: 
		:type self: tensor
		:param first_slot_index: index of first vector space in pairing 
		:param second_slot_index: index of second vector space in pairing 
		:param pairing: :math:`\langle \mathbf{v_1},\mathbf{v_2} \rangle`
		:return: Contracted tensor.
		TODO: Write math.
		:rtype: [tensor]
		"""
        pairing = Dual.default_pairing if pairing is None else pairing

        contraction = type(self)()
        for key_self in self.keys():
            braided_tensor = type(self)({key_self: self[key_self]}).braiding_map(
                [first_slot_index]
                + [second_slot_index]
                + [
                    slot_index
                    for slot_index in range(0, len(key_self))
                    if slot_index not in (first_slot_index, second_slot_index)
                ]
            )
            for braided_key in braided_tensor.keys():
                braided_value = braided_tensor[braided_key]
                pairing_factor = pairing(*braided_key[0:2])
                contracted_summand = type(self)(
                    {braided_key[2:]: braided_value * pairing_factor}
                )
                contraction = contraction + contracted_summand
        return contraction

    # endregion

    def __call__(self, arg):
        r"""Tensor product followed by contraction/trace, adjacent pairs in tensor product
		NOTE: Does not try to match the orders. It assumes the tensor is not mixed-order in such a way so the operation does not work.
		NOTE: rank is smallest number of pure tensor terms required. degree/ order is the number of vector spaces taken in the tensor products.
	
		:param self: 
		:type self: [tensor]
		:param arg: 
		:type arg: [tensor]
		:return: :math:`\mathsf{self}\otimes \mathsf{arg}`, followed by iterated contraction, 
			matching slots by adjacent pairs (last of self, first of arg), until either self or arg is fully contracted
		:rtype: [tensor]
		"""

        result = self @ arg
        order_self = max([len(key_self) for key_self in self.keys()])
        order_arg = max([len(key_arg) for key_arg in arg.keys()])
        for r in range(0, min(order_self, order_arg)):
            result = result.trace(order_self - r - 1, order_self - r)
        return result

    # region simplification

    def without_zeros(self, zero_coefficient=0):
        """[summary]
		NOTE: mutates self and returns self (to allow chains)
		
		:param zero_coefficient: [description], defaults to 0
		:param zero_coefficient: int, optional
		:return: [description]
		:rtype: [type]
		"""

        result = type(self)(
            {key: value for key, value in self.items() if value != zero_coefficient}
        )
        self.clear()
        self.update(result)
        return result

    # endregion

    # region presentation

    def latex(self):
        return r" + ".join(
            [
                r" \cdot ".join(
                    [
                        r"({0})".format(value),
                        r" \otimes ".join(["{0}".format(v) for v in key])
                        if key
                        else r"1",  # scalar 𝟙
                    ]
                )
                for key, value in self.items()
            ]
        )

    def __str__(self):
        return LatexNodes2Text().latex_to_text(self.latex())


# endregion
