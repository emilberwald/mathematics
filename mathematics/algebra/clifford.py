r"""
Clifford algebra
"""

import itertools
from collections import namedtuple

from mathematics.number_theory.combinatorics import (
    permutation_to_adjacent_transpositions,
)
from .tensor import Tensor


class Clifford(Tensor):
    r"""
	Subclass of tensor that implements clifford algebra behavior when given a symmetric bilinear form.
	
	.. math::
		\textrm{Tensor algebra quotient:}\,u\otimes u - Q(u)1 \in [0]\\
		(u+v)\otimes(u+v) = u\otimes u + u\otimes v + v\otimes u + v\otimes v\\
		\Leftrightarrow Q(u+v)1 = Q(u)1 + u\otimes v + v\otimes u + Q(v)1\\
		\operatorname{char}(K) \neq 2 \Rightarrow u\otimes v + v\otimes u = (Q(u+v) - Q(u) - Q(v))1 = 2\langle u,v\rangle_Q 1\\
		\Leftrightarrow u\otimes v = -v\otimes u + 2\langle u,v\rangle_Q 1\\
	"""

    symmetric_bilinear_form = (
        lambda x, y: 0
    )  # could this be improved with metaclasses ??

    def __eq__(self, other):
        """Overrides the default implementation, want to check that the quadratic form is equal as well"""
        if type(other) is type(self):
            # TODO: check that this does not mix Clifford classes without different symmetric bilinear forms,
            # as created with class factories.
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))

    def quotient(self):
        r"""
		Quotient

		.. math::
			u\otimes u - Q(u)1 \in [0]

		NOTE: mutates self and returns self (to allow chains)

		:return: self
		:rtype: :py:class:`type(self)`
		"""

        result = type(self)()
        for key_self in self.keys():
            key_result = list()
            value_self = self[key_self]
            current_key, lookahead_key = itertools.tee(key_self, 2)
            next(lookahead_key, None)
            for slot_i in current_key:
                slot_j = next(lookahead_key, None)
                if slot_j and slot_i == slot_j:
                    value_self = value_self * type(self).symmetric_bilinear_form(
                        slot_i, slot_j
                    )
                    next(current_key, None)
                    next(lookahead_key, None)
                else:
                    key_result.append(slot_i)
            result = result + type(self)(
                {type(self).__merge_keys(*[key_result]): value_self}
            )
        self.clear()
        self.update(result)
        return self

    def swap(self, adjacent_transposition):
        r"""
		Swaps the order of the tensor multiplications
		NOTE: mutates self and returns self (to allow chains)

		:param self: [description]
		:param adjacent_transposition: pair with two adjacent slots to be swapped; (u,v) in expression :math:`\cdots\otimes u \otimes v\otimes\cdots`
		"""

        def clifford_swap(slot_i, slot_j):
            r"""Uses the ideal in the clifford algebra,

			.. math::
				u\otimes u - Q(u)1 \in [0]
				\operatorname{char}(K) \neq 2 \Rightarrow u\otimes v = -v\otimes u + 2\langle u,v\rangle_Q 1

			TODO: can this be generalized to any ideals, e.g. Weyl algebra:

			.. math::
				u\otimes v - v\otimes u -\omega(u,v) \in [0]
				\Leftrightarrow u\otimes v = v\otimes u + \omega(u,v)

			Perhaps something like :math:`\operatorname{Ideal}(u\otimes v) - u\otimes v`?
			"""

            return type(self)(
                {
                    type(self).__merge_keys((slot_j,), (slot_i,)): -1,
                    type(self).__merge_keys(): 2
                    * type(self).symmetric_bilinear_form(slot_i, slot_j),
                }
            )

        result = type(self)()
        for key_self in self.keys():
            # ensure that the swap can be made with the available slots
            if max(adjacent_transposition) <= len(key_self):
                prefix = type(self)(
                    {
                        type(self).__merge_keys(
                            *key_self[0 : min(adjacent_transposition)]
                        ): self[key_self]
                    }
                )
                root = clifford_swap(
                    *key_self[
                        min(adjacent_transposition) : max(adjacent_transposition) + 1
                    ]
                )
                postfix = type(self)(
                    {
                        type(self).__merge_keys(
                            *key_self[max(adjacent_transposition) + 1 :]
                        ): 1
                    }
                )
                result = result + prefix @ root @ postfix
            else:
                result = result + type(self)({key_self: self[key_self]})
        self.clear()
        self.update(result)
        return self

    def braiding_map(self, slot_permutation):
        r"""
		NOTE: mutates self and returns self (to allow chains)
		Overrides the functionality to incorporate

		.. math::
			v\otimes w = -w\otimes v + (2\cdot \langle v,w\rangle) \cdot 1

		which is valid if the characteristic of the unital associative algebra is not 2.

		:param slot_permutation: [description]
		:type slot_permutation: [type]
		:return: [description]
		:rtype: [type]
		"""
        adjacent_transpositions = permutation_to_adjacent_transpositions(
            slot_permutation
        )
        for adjacent_transposition in adjacent_transpositions:
            self.swap(adjacent_transposition)
        return self

    # region simplification

    def find_first_key_with_duplicate_slots_and_their_indices(self):
        for key_self in self.keys():
            duplicate_slot_in_key_to_indices = {
                slot: [i for i, slot_i in enumerate(key_self) if slot_i == slot]
                for slot in set(key_self)
            }
            for _, indices in duplicate_slot_in_key_to_indices.items():
                if len(indices) > 1:
                    return namedtuple("key_with_indices", ["key", "indices"])(
                        key=key_self, indices=indices
                    )
        return None

    def equal_slots_reduced_yet(self):
        """
		[summary]
		NOTE: returns False if it mutated self, otherwise True
		"""
        already_reduced = True
        while True:
            key_with_duplicate_slots_and_their_indices = (
                self.find_first_key_with_duplicate_slots_and_their_indices()
            )
            if key_with_duplicate_slots_and_their_indices:
                permutation = key_with_duplicate_slots_and_their_indices.indices + [
                    slot_index
                    for slot_index in range(
                        0, len(key_with_duplicate_slots_and_their_indices.key)
                    )
                    if slot_index
                    not in key_with_duplicate_slots_and_their_indices.indices
                ]
                self.braiding_map(permutation).quotient().without_zeros()
                already_reduced = False
            else:
                break
        return already_reduced

    def normalized_key_yet(self, key_normal_form):
        """[summary]
		NOTE: returns False if it mutated self, otherwise True
		
		:param key_normal_form: [description]
		:type key_normal_form: [type]
		:return: [description]
		:rtype: [type]
		"""

        def first_key_not_in_normal_form(keys, key_normal_form):
            for key in keys:
                if key != key_normal_form and set(key) == set(key_normal_form):
                    return key
            return None

        already_normalized = True
        while True:
            key_not_in_normal_form = first_key_not_in_normal_form(
                self.keys(), key_normal_form
            )
            if key_not_in_normal_form:
                slot_permutation = [
                    key_normal_form.index(slot) for slot in key_not_in_normal_form
                ]
                other_summand_to_permute = type(self)(
                    {key_not_in_normal_form: self[key_not_in_normal_form]}
                )
                result = (
                    (
                        self
                        - other_summand_to_permute
                        + other_summand_to_permute.braiding_map(slot_permutation)
                    )
                    .quotient()
                    .without_zeros()
                )
                self.clear()
                self.update(result)
                already_normalized = False
            else:
                return already_normalized

    def simplified_yet(self):
        """[summary]
		NOTE: returns False if it mutated self, otherwise True

		:return: [description]
		:rtype: [type]
		"""

        maybe = self.equal_slots_reduced_yet()
        if maybe:
            for key_self in self.keys():
                maybe = maybe and self.normalized_key_yet(key_self)
                if maybe:
                    continue
                else:
                    break
        return maybe

    def simplify(self):
        """[summary]
		NOTE: mutates self if necessary and then returns self (to allow chains)
		
		:return: [description]
		:rtype: [type]
		"""
        while not self.simplified_yet():
            pass
        return self


# endregion
