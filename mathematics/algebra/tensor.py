"""
Tensor algebra
"""

__all__ = ["Tensor"]
import copy

from pylatexenc.latex2text import LatexNodes2Text

from .dual import Dual


class Tensor(dict):
    @staticmethod
    def __merge_indices(*base_tensors):
        r"""Tensor product for pure tensors without coefficients.
		
		:param base_tensors: each argument is a tensor base vector :math:`\mathsf{e_A} = \mathbf{e}_0\otimes\ldots\otimes \mathbf{e}_{order(\mathsf{e_A})-1}`
		:type e_A: [tuple]
		:return: :math:`\bigotimes_{\mathsf{e_A}\in \textup{base tensors}}\mathsf{e_A} = \bigotimes_{\mathsf{e_A}\in \textup{base tensors}}(\bigotimes_{\mathbf{e}_k\in \mathsf{e_A}} \mathbf{e}_k)`
		:rtype: [tuple]
		"""
        base_tensor_result = list()
        for base_tensor in base_tensors:
            for base_vector in base_tensor:
                base_tensor_result.append(base_vector)
        return tuple(base_tensor_result)

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

        return type(self)(
            {
                tensor_product_vector: scalar * self[tensor_product_vector]
                for tensor_product_vector in self
            }
        )

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
        for tensor_base_vector in B:
            if tensor_base_vector in self:
                A[tensor_base_vector] = self[tensor_base_vector] + B[tensor_base_vector]
            else:
                A[tensor_base_vector] = B[tensor_base_vector]
        return A

    def __neg__(self):
        return type(self)(
            {
                tensor_base_vector: -self[tensor_base_vector]
                for tensor_base_vector in self
            }
        )

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
        result = type(self)()
        for indices_self, coefficient_self in self.items():
            for indices_b, coefficient_b in B.items():
                indices_result = type(self).__merge_indices(indices_self, indices_b)
                if indices_result not in result:
                    result[indices_result] = coefficient_self * coefficient_b
                else:
                    # perhaps this could happen if one of the tensor base vectors are of mixed order?
                    # GUESS: summation best way to handle this?
                    result = result + type(self)(
                        {indices_result: coefficient_self * coefficient_b}
                    )
        return result

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
                tuple(indices[slot] for slot in slot_permutation): self[indices]
                for indices in self
            }
        )
        self.clear()
        self.update(result)
        return self

    def trace(self, first_slot, second_slot, pairing=None):
        r"""Trace/contraction of tensor, over vector space indices as indicated in first_slot and second_slot, 
		
		NOTE: Might not work for braided monodial categories since it does not contract until fixpoint (it calls braiding_map though)
		NOTE: the default pairing tries both cov(con) and con(cov)
		:param self: 
		:type self: tensor
		:param first_slot: index of first vector space in pairing 
		:param second_slot: index of second vector space in pairing 
		:param pairing: :math:`\langle \mathbf{v_1},\mathbf{v_2} \rangle`
		:return: Contracted tensor.
		TODO: Write math.
		:rtype: [tensor]
		"""
        pairing = Dual.default_pairing if pairing is None else pairing

        result = type(self)()
        for indices_self in self:
            braided_tensor = type(self)(
                {indices_self: self[indices_self]}
            ).braiding_map(
                [first_slot]
                + [second_slot]
                + [
                    slot
                    for slot in range(0, len(indices_self))
                    if slot not in (first_slot, second_slot)
                ]
            )
            for braided_indices in braided_tensor:
                coefficient = braided_tensor[braided_indices]
                pairing_factor = pairing(*braided_indices[0:2])
                contracted_summand = type(self)(
                    {braided_indices[2:]: coefficient * pairing_factor}
                )
                result = result + contracted_summand
        return result

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
        order_self = max(
            [len(tensor_base_vector) for tensor_base_vector in self.keys()]
        )
        order_arg = max([len(tensor_base_vector) for tensor_base_vector in arg.keys()])
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
            {
                base_vector: coefficient
                for base_vector, coefficient in self.items()
                if coefficient != zero_coefficient
            }
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
                        r"({0})".format(coefficient),
                        r" \otimes ".join(["{0}".format(v) for v in base])
                        if base
                        else r"1",  # scalar 𝟙
                    ]
                )
                for base, coefficient in self.items()
            ]
        )

    def __str__(self):
        return LatexNodes2Text().latex_to_text(self.latex())


# endregion
