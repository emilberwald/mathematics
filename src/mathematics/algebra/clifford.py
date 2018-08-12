r"""
Clifford algebra
"""

import itertools
from collections import namedtuple

from mathematics.number_theory.combinatorics import permutation_to_adjacent_transpositions
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

	symmetric_bilinear_form = lambda x, y: 0  #could this be improved with metaclasses ??

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
		for indices_self in self:
			indices_result = list()
			coefficient = self[indices_self]
			current_v, lookahead_v = itertools.tee(indices_self, 2)
			next(lookahead_v, None)
			for v_i in current_v:
				v_j = next(lookahead_v, None)
				if v_j and v_i == v_j:
					coefficient = coefficient * type(
						self).symmetric_bilinear_form(v_i, v_j)
					next(current_v, None)
					next(lookahead_v, None)
				else:
					indices_result.append(v_i)
			result = result + type(self)({
				Tensor._merge_indices(*[indices_result]):
				coefficient
			})
		self.clear()
		self.update(result)
		return self

	def swap(self, adjacent_transposition):
		r"""
		Swaps the order of the tensor multiplications
		:param self: [description]
		:type self: [tensor]
		:param first_slot: slot of u in expression :math:`\cdots\otimes u \otimes v\otimes\cdots`

		NOTE: mutates self and returns self (to allow chains)
		"""

		def clifford_swap(e_i, e_j):
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

			return type(self)({
				Tensor._merge_indices((e_j, ), (e_i, )):
				-1,
				Tensor._merge_indices():
				2 * type(self).symmetric_bilinear_form(e_i, e_j)
			})

		result = type(self)()
		for indices_self in self:
			#ensure that the swap can be made with the available slots
			if max(adjacent_transposition) <= len(indices_self):
				prefix = type(self)({
					Tensor._merge_indices(*indices_self[0:min(adjacent_transposition)]):
					self[indices_self]
				})
				root = clifford_swap(*indices_self[min(
					adjacent_transposition):max(adjacent_transposition) + 1])
				postfix = type(self)({
					Tensor._merge_indices(*indices_self[max(adjacent_transposition) + 1:]):
					1
				})
				result = result + prefix @ root @ postfix
			else:
				result = result + type(self)({
					indices_self: self[indices_self]
				})
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
			slot_permutation)
		for adjacent_transposition in adjacent_transpositions:
			self.swap(adjacent_transposition)
		return self

#region simplification

	def find_first_indices_and_slots_with_multiple_occurences_of_a_index(self):
		for indices in self:
			slots_with_same_index_by_index = {
				e: [i for i, ei in enumerate(indices) if ei == e]
				for e in set(indices)
			}
			for index, slots_with_same_index in slots_with_same_index_by_index.items(
			):
				if len(slots_with_same_index) > 1:
					return namedtuple("indices_and_slots",
						["indices", "slots"])(
						indices=indices,
						slots=slots_with_same_index)
		return None

	def equal_indices_reduced_yet(self):
		"""
		[summary]
		NOTE: returns False if it mutated self, otherwise True
		
		:param indices_of_summand: [description]
		:type indices_of_summand: [type]
		"""
		already_reduced = True
		while True:
			indices_and_slots = self.find_first_indices_and_slots_with_multiple_occurences_of_a_index(
			)
			if indices_and_slots:
				permutation = indices_and_slots.slots + [
					slot for slot in range(0, len(indices_and_slots.indices))
					if slot not in indices_and_slots.slots
				]
				self.braiding_map(permutation).quotient().without_zeros()
				already_reduced = False
			else:
				break
		return already_reduced

	def normalized_indices_yet(self, indices_normal_form):
		"""[summary]
		NOTE: returns False if it mutated self, otherwise True
		
		:param indices_normal_form: [description]
		:type indices_normal_form: [type]
		:return: [description]
		:rtype: [type]
		"""

		def first_indices_not_in_normal_form(search_space,
			indices_normal_form):
			for indices_of_other_summand in search_space:
				if indices_of_other_summand != indices_normal_form and set(
					indices_of_other_summand) == set(indices_normal_form):
					return indices_of_other_summand
			return None

		already_normalized = True
		while True:
			indices_not_in_normal_form = first_indices_not_in_normal_form(
				self, indices_normal_form)
			if indices_not_in_normal_form:
				slot_permutation = [
					indices_normal_form.index(slot)
					for slot in indices_not_in_normal_form
				]
				other_summand_to_permute = type(self)({
					indices_not_in_normal_form:
					self[indices_not_in_normal_form]
				})
				result = (
					self - other_summand_to_permute +
					other_summand_to_permute.braiding_map(slot_permutation)
				).quotient().without_zeros()
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

		maybe = self.equal_indices_reduced_yet()
		if maybe:
			for indices in self:
				maybe = maybe and self.normalized_indices_yet(indices)
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

#endregion