from mathematics.algebra.tensor import tensor
import itertools
from mathematics.number_theory.combinatorics import permutation_to_adjacent_transpositions


class clifford(tensor):
	symmetric_bilinear_form = lambda x, y: 0  #could this be improved with metaclasses ??

	@classmethod
	def set_symmetric_bilinear_form(cls, symmetric_bilinear_form):
		cls.symmetric_bilinear_form = symmetric_bilinear_form

	@classmethod
	def set_induced_symmetric_bilinear_form(cls, quadratic_form):
		def induced(u, v):
			return 1 / 4 * (quadratic_form(u + v) - quadratic_form(u - v))

		cls.symmetric_bilinear_form = induced

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def __eq__(self, other):
		"""Overrides the default implementation, want to check that the quadratic form is equal as well"""
		if type(other) is type(self):
			return self.__dict__ == other.__dict__  #might need changing if I find another way to get symmetric_bilinear_form into the constructor. a factory probably doesnt work since I want @ to return cliffords
		return NotImplemented

	def __hash__(self):
		"""Overrides the default implementation"""
		return hash(tuple(sorted(self.__dict__.items())))

	def quotient(self):
		result = clifford()
		for tensor_base_vector in self:
			result_base_vectors = list()
			coefficient = self[tensor_base_vector]
			Vcurrent, Vlookahead = itertools.tee(tensor_base_vector, 2)
			next(Vlookahead, None)
			for v_i in Vcurrent:
				v_j = next(Vlookahead, None)
				if v_j and v_i == v_j:
					coefficient = coefficient * self.symmetric_bilinear_form(
					    v_i, v_j)
				else:
					result_base_vectors.append(v_i)
			result = result + clifford(
			    self.symmetric_bilinear_form,
			    {tensor._puretensorproduct(*result_base_vectors): coefficient})

	def swap(self, adjacent_transposition):
		r"""
		Swaps the tensor order of the basis in place
		:math::
			v\otimes w = -w\otimes v + (2\cdot \langle v,w\rangle) \cdot 1

		:param self: [description]
		:type self: [tensor]
		:param first_slot: slot of u in expression :math:`\cdots\otimes u \otimes v\otimes\cdots`
		"""

		def clifford_swap(e_i, e_j):
			return clifford({
			    tensor._puretensorproduct(e_j, e_i):
			    -1,
			    tensor._puretensorproduct():
			    2 * self.symmetric_bilinear_form(e_i, e_j)
			})

		result = clifford()
		for base_tensor in self:
			#ensure that the root indices are swappable
			if max(adjacent_transposition) <= len(base_tensor):
				prefix = clifford({
				    tensor._puretensorproduct(*base_tensor[0:min(adjacent_transposition)]):
				    self[base_tensor]
				})
				root = clifford_swap(*base_tensor[min(
				    adjacent_transposition):max(adjacent_transposition) + 1])
				postfix = clifford({
				    tensor._puretensorproduct(*base_tensor[max(adjacent_transposition) + 1:]):
				    1
				})
				result = result + prefix @ root @ postfix
			else:
				result = result + clifford({base_tensor: self[base_tensor]})
		return result

	def braiding_map_pure_tensor(self, e_A, index_permutation):
		r"""Overrides the functionality to incorporate 
		:math::
			v\otimes w = -w\otimes v + (2\cdot \langle v,w\rangle) \cdot 1
		which is valid if the characteristic of the unital associative algebra is not 2.
		:param e_A: [description]
		:type e_A: [type]
		:param index_permutation: [description]
		:type index_permutation: [type]
		:return: [description]
		:rtype: [type]
		"""
		adjacent_transpositions = permutation_to_adjacent_transpositions(
		    index_permutation)
		result = self
		for adjacent_transposition in adjacent_transpositions:
			result = result.swap(adjacent_transposition)
		return result
