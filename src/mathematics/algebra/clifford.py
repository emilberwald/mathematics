__all__ = ["induced_symmetric_bilinar_form", "clifford_constructor"]
import itertools
from mathematics.algebra.tensor import tensor
from mathematics.number_theory.combinatorics import permutation_to_adjacent_transpositions
from collections import namedtuple


def class_factory(name, baseclasses, **kwargs):
	if name in globals():
		return globals()[name]
	else:
		result = type(name, baseclasses, kwargs)
		globals()[name] = result
		return globals()[name]


def induced_symmetric_bilinar_form(quadratic_form):
	def symmetric_bilinear_form(u, v):
		return 1 / 4 * (quadratic_form(u + v) - quadratic_form(u - v))

	return symmetric_bilinear_form


def clifford_constructor(name, symmetric_bilinear_form):
	return class_factory(
	    name, (clifford, ), symmetric_bilinear_form=symmetric_bilinear_form)


class clifford(tensor):
	symmetric_bilinear_form = lambda x, y: 0  #could this be improved with metaclasses ??

	def __eq__(self, other):
		"""Overrides the default implementation, want to check that the quadratic form is equal as well"""
		if type(other) is type(self):
			return self.__dict__ == other.__dict__  #might need changing if I find another way to get symmetric_bilinear_form into the constructor. a factory probably doesnt work since I want @ to return cliffords
		return NotImplemented

	def __hash__(self):
		"""Overrides the default implementation"""
		return hash(tuple(sorted(self.__dict__.items())))

	def quotient(self):
		"""
		Quotient
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
			    tensor._merge_indices(*[indices_result]):
			    coefficient
			})
		self.clear()
		self.update(result)
		return self

	def swap(self, adjacent_transposition):
		r"""
		Swaps the tensor order of the basis in place

		NOTE: mutates self and returns self (to allow chains)
		:math::
			v\otimes w = -w\otimes v + (2\cdot \langle v,w\rangle) \cdot 1
		based on :math:`(u+v)\otimes(u+v) = u\otimes u + u\otimes v + v\otimes u + v\otimes v` being an ideal that is quotiented,
		so it has the representative [0] since 0 + Ideal = [0] or something. 
		NOTE: perhaps this class can be generalized to any ideals? That way the weyl algebra can be included (:math:`u\otimes v - v\otimes u -\omega(u,v) = [0] <=> u\otimes v = [0] + v\otimes u + \omega(u,v)` since it is the ideal in weyl algebra).
		:param self: [description]
		:type self: [tensor]
		:param first_slot: slot of u in expression :math:`\cdots\otimes u \otimes v\otimes\cdots`
		"""

		def clifford_swap(e_i, e_j):
			return type(self)({
			    tensor._merge_indices((e_j, ), (e_i, )):
			    -1,
			    tensor._merge_indices():
			    2 * type(self).symmetric_bilinear_form(e_i, e_j)
			})

		result = type(self)()
		for indices_self in self:
			#ensure that the swap can be made with the available slots
			if max(adjacent_transposition) <= len(indices_self):
				prefix = type(self)({
				    tensor._merge_indices(*indices_self[0:min(adjacent_transposition)]):
				    self[indices_self]
				})
				root = clifford_swap(*indices_self[min(
				    adjacent_transposition):max(adjacent_transposition) + 1])
				postfix = type(self)({
				    tensor._merge_indices(*indices_self[max(adjacent_transposition) + 1:]):
				    1
				})
				result = result + prefix @ root @ postfix
			else:
				result = result + type(self)({indices_self: self[indices_self]})
		self.clear()
		self.update(result)
		return self

	def braiding_map(self, slot_permutation):
		r"""
		Overrides the functionality to incorporate 
		
		NOTE: mutates self and returns self (to allow chains)

		:math::
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

		def first_indices_not_in_normal_form(search_space, indices_normal_form):
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
				other_summand_to_permute = clifford({
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
