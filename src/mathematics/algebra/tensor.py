from autologging import traced
import copy
from mathematics.number_theory.combinatorics import integer_partitions
import itertools
import functools
import operator


@traced
class tensor(dict):
	@classmethod
	def __prepare__(mcs, *args, **kwargs):
		return {}

	def __new__(mcs, *args, **kwargs):
		return super().__new__(mcs, *args, **kwargs)

	def __add__(self, B):
		A = copy.deepcopy(self)
		for tensor_base_vector in B:
			if tensor_base_vector in self:
				A[tensor_base_vector] = self[tensor_base_vector] + B[tensor_base_vector]
			else:
				A[tensor_base_vector] = B[tensor_base_vector]
		return A

	def __neg__(self):
		return tensor({
		    tensor_base_vector: -self[tensor_base_vector]
		    for tensor_base_vector in self
		})

	def __sub__(self, B):
		A = copy.deepcopy(self)
		for tensor_base_vector in B:
			if tensor_base_vector in self:
				A[tensor_base_vector] = self[tensor_base_vector] - B[tensor_base_vector]
			else:
				A[tensor_base_vector] = -B[tensor_base_vector]
		return A

	def delete_zeros(self, zero_coefficient=0):
		for base_vector, coefficient in self.items():
			if coefficient == zero_coefficient:
				del self[base_vector]
		return self

	@staticmethod
	def __X(tensor_base_vector_a, tensor_base_vector_b):
		tensor_base_vector_result = list()
		for ei in tensor_base_vector_a:
			tensor_base_vector_result.append(ei)
		for ek in tensor_base_vector_b:
			tensor_base_vector_result.append(ek)
		return tuple(tensor_base_vector_result)

	def __matmul__(self, B):
		result = tensor()
		for tensor_base_vector_self, coefficient_self in self.items():
			for tensor_base_vector_b, coefficient_b in B.items():
				tensor_base_vector_result = tensor.__X(tensor_base_vector_self,
				                                       tensor_base_vector_b)
				if tensor_base_vector_result in result:
					raise NotImplementedError(
					    "Same resulting base {0} several times !?".format(
					        tensor_base_vector_result))
				else:
					result[
					    tensor_base_vector_result] = coefficient_self * coefficient_b
		return result

	@staticmethod
	def standard_dual_vector_base(vector_base, zero=0, one=1):
		return tuple(
		    lambda vector_base_vector, vector_base=vector_base, i=i: one if vector_base.index(vector_base_vector) == i else zero
		    for i in range(0, len(vector_base)))

	@staticmethod
	def standard_vector_base(dimension):
		return tuple(integer_partitions(dimension, 1))

	@staticmethod
	def multilinear_mapping_tensor_expansion(*vector_bases):
		"""expands multilinear function as tensor. 
		
		NOTE: the coeficcients might be vector valued! Not sure if this works! the codomain of the multilinear mapping might not be R! The duck hopefully quacks and walks like R.
		:return: [description]
		:rtype: [type]
		"""
		dual_vectorspace_bases = [
		    tensor.standard_dual_vector_base(vector_base)
		    for vector_base in vector_bases
		]
		return lambda f, vector_bases=vector_bases, dual_bases=dual_vectorspace_bases: functools.reduce(operator.add,[tensor({
		     tuple(dual_bases[vector_space_index][tensor_index[vector_space_index]] for vector_space_index in range(
		               0, len(dual_bases))):
		     f(*[
		         vector_bases[vector_space_index]
		         [tensor_index[vector_space_index]]
		         for vector_space_index in range(0, len(vector_bases))
		     ])
		 }) for tensor_index in itertools.product(
		    *[range(0, len(vector_base)) for vector_base in vector_bases])],tensor())

	def __call__(self, tensor_arg):
		#assumes that the tensor is not "mixed-rank"
		result = self @ tensor_arg
		rank = max(
		    [len(tensor_base_vector) for tensor_base_vector in self.keys()])
		for r in range(0, rank):
			result = result.trace(0, rank - r)
		return result

	@staticmethod
	def standard_kronecker_delta(dimension):
		def kronecker_delta(cobase_vector, base_vector):
			return cobase_vector(base_vector)

		contravariant_rank, covariant_rank = 1, 1
		vector_base = tensor.standard_vector_base(dimension)
		dual_base = tensor.standard_dual_vector_base(vector_base)
		result = tensor()
		for tensor_base_vector in itertools.product(
		    *[vector_base] * contravariant_rank,
		    *[dual_base] * covariant_rank):
			result = result + tensor({
			    tuple(tensor_base_vector):
			    kronecker_delta(*tensor_base_vector)
			})
		return result

	@staticmethod
	def same_coefficient(dimension, rank, coefficient):
		contravariant_rank, covariant_rank = rank
		vector_base = tensor.standard_vector_base(dimension)
		dual_base = tensor.standard_dual_vector_base(vector_base)
		result = tensor()
		for tensor_base_vector in itertools.product(
		    *[vector_base] * contravariant_rank,
		    *[dual_base] * covariant_rank):
			result = result + tensor({tuple(tensor_base_vector): coefficient})
		return result

	#A=tensor({((1,0),):1,((0,1),):2});B=tensor({((1,0),):3});
	def trace(
	    self,
	    first_slot,
	    second_slot,
	    pairing=lambda cov, con: cov(con) if callable(cov) else con(cov)):
		result = tensor()
		for tensor_base_vector_self in self:
			first_element = tensor_base_vector_self[first_slot]
			second_element = tensor_base_vector_self[second_slot]
			pairing_factor = pairing(first_element, second_element)
			coefficient = self[tensor_base_vector_self]
			contracted_tensor_base_vector = tuple(
			    tensor_base_vector_self[slot]
			    for slot in range(0, len(tensor_base_vector_self))
			    if slot not in (first_slot, second_slot))
			contracted_summand = tensor({
			    contracted_tensor_base_vector:
			    coefficient * pairing_factor
			})
			result = result + contracted_summand
		return result

	def __rmul__(self, a):
		r"""scalar product
		
		:param self: vector
		:param a: scalar
		:type a: [type]
		:return: :math:`a\cdot \mathbf{x} = a \cdot (x^ke_k) =  (ax^k) e_k`
		:rtype: [type]
		"""

		return tensor({
		    tensor_product_vector: a * self[tensor_product_vector]
		    for tensor_product_vector in self
		})
