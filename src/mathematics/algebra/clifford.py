import itertools
from mathematics.algebra.tensor import tensor
from mathematics.number_theory.combinatorics import permutation_to_adjacent_transpositions


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
		result = type(self)()
		for tensor_base_vector in self:
			result_base_vectors = list()
			coefficient = self[tensor_base_vector]
			Vcurrent, Vlookahead = itertools.tee(tensor_base_vector, 2)
			next(Vlookahead, None)
			for v_i in Vcurrent:
				v_j = next(Vlookahead, None)
				if v_j and v_i == v_j:
					coefficient = coefficient * type(
					    self).symmetric_bilinear_form(v_i, v_j)
					next(Vcurrent, None)
					next(Vlookahead, None)
				else:
					result_base_vectors.append(v_i)
			result = result + type(self)({
			    tensor._puretensorproduct(*[result_base_vectors]):
			    coefficient
			})
		return result

	def swap(self, adjacent_transposition):
		r"""
		Swaps the tensor order of the basis in place
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
			    tensor._puretensorproduct((e_j, ), (e_i, )):
			    -1,
			    tensor._puretensorproduct():
			    2 * type(self).symmetric_bilinear_form(e_i, e_j)
			})

		result = type(self)()
		for base_tensor in self:
			#ensure that the root indices are swappable
			if max(adjacent_transposition) <= len(base_tensor):
				prefix = type(self)({
				    tensor._puretensorproduct(*base_tensor[0:min(adjacent_transposition)]):
				    self[base_tensor]
				})
				root = clifford_swap(*base_tensor[min(
				    adjacent_transposition):max(adjacent_transposition) + 1])
				postfix = type(self)({
				    tensor._puretensorproduct(*base_tensor[max(adjacent_transposition) + 1:]):
				    1
				})
				result = result + prefix @ root @ postfix
			else:
				result = result + type(self)({base_tensor: self[base_tensor]})
		return result

	def braiding_map(self, index_permutation):
		r"""Overrides the functionality to incorporate 
		:math::
			v\otimes w = -w\otimes v + (2\cdot \langle v,w\rangle) \cdot 1
		which is valid if the characteristic of the unital associative algebra is not 2.
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

	def simplify(self):
		for e_A in self:
			indices_by_value = {
			    e: [i for i, ei in enumerate(e_A) if ei == e]
			    for e in set(e_A)
			}
			for e_I, I in indices_by_value.items():
				if len(I) > 1:
					permutation = I + [
					    i for i in range(0, len(e_A)) if i not in I
					]
					result = self.braiding_map(
					    permutation).quotient().without_zeros()
					return result.simplify()
			for permutable in [
			    E for E in self if E != e_A and set(E) == set(e_A)
			]:
				other = clifford({permutable: self[permutable]})
				permutation = [e_A.index(o) for o in permutable]
				result = (self - other + other.braiding_map(permutation)
				          ).quotient().without_zeros()
				return result.simplify()
		return self