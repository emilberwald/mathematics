from autologging import traced
import copy
from mathematics.number_theory.combinatorics import integer_partitions
import itertools
import functools
import operator
import sympy
from pylatexenc.latex2text import LatexNodes2Text


@traced
class tensor(dict):
	@classmethod
	def __prepare__(mcs, *args, **kwargs):
		return {}

	def __new__(mcs, *args, **kwargs):
		return super().__new__(mcs, *args, **kwargs)

	def __rmul__(self, scalar):
		r"""scalar product
		(DEFINITION) Compatability of tensor scalar multiplication with vector scalar multiplication
		:math::
			\lambda\cdot(a\otimes b) = (\lambda \cdot a)\otimes b = a\otimes(\lambda \cdot b)
		(GUESS) Compatability of tensor scalar multiplication with field multiplication
		:math::
			\lambda\cdot(c\cdot_F a\otimes b) = (\lambda \cdot_F c)a\otimes b
		(GUESS) Distributivity of scalar multiplication with respect to vector addition
		:math::
			\lambda\cdot(a\otimes b + c\otimes d) = \lambda\cdot(a\otimes b) + \lambda\cdot(c\otimes d) 
		(GUESS) The scalar can be distributed into the coefficient of each pure tensor term.
		
		:param self: vector
		:param scalar: scalar
		:type scalar: [type]
		:return: 
		:rtype: [type]
		"""

		return tensor({
		    tensor_product_vector: scalar * self[tensor_product_vector]
		    for tensor_product_vector in self
		})

	def __add__(self, B):
		r"""tensor addition
		
		(DEFINITION) (not used) If all but one coordinate are the same, addition can be combined.
		:math::
			(v_1 + v_2)\otimes w_1 = v_1\otimes w_1 + v_2\otimes w_1
			v_1\otimes (w_1+w_2) = v_1\otimes w_1 + v_1\otimes w_2
		(GUESS): Distributivity of scalar multiplication with respect to field addition
		:math::
			(c_1 + c_2)(e_i\otimes e_j) = c_1 (e_i \otimes e_j) + c_2 (e_i\otimes \ej)

		We want to distribute the addition as much as possible.
		The internal state of the tensor is in terms of pure tensors of the vector bases.

		:param self: tensor
		:type self: [tensor]
		:param B: the tensor(-like) object to add
		:return: self+B
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
		return tensor({
		    tensor_base_vector: -self[tensor_base_vector]
		    for tensor_base_vector in self
		})

	def __sub__(self, B):
		return self.__add__(-B)

	def without_zeros(self, zero_coefficient=0):
		return tensor({
		    base_vector: coefficient
		    for base_vector, coefficient in self.items()
		    if coefficient != zero_coefficient
		})

	@staticmethod
	def __pure_tensorXpure_tensor(tensor_base_vector_a, tensor_base_vector_b):
		tensor_base_vector_result = list()
		for ei in tensor_base_vector_a:
			tensor_base_vector_result.append(ei)
		for ek in tensor_base_vector_b:
			tensor_base_vector_result.append(ek)
		return tuple(tensor_base_vector_result)

	def __matmul__(self, B):
		r"""Tensor procuct of tensors.
		(GUESS) This whole function is guesswork. I think the proper term is unbiased monodial category?
		
		:param B: [description]
		:return: :math:`self\otimes B`
		:rtype: [type]
		"""
		result = tensor()
		for tensor_base_vector_self, coefficient_self in self.items():
			for tensor_base_vector_b, coefficient_b in B.items():
				tensor_base_vector_result = tensor.__pure_tensorXpure_tensor(
				    tensor_base_vector_self, tensor_base_vector_b)
				if tensor_base_vector_result not in result:
					result[
					    tensor_base_vector_result] = coefficient_self * coefficient_b
				else:
					# perhaps this could happen if one of the tensor base vectors are zeroth order?
					# GUESS: summation best way to handle this?
					result = result + tensor({
					    tensor_base_vector_result:
					    coefficient_self * coefficient_b
					})
		return result

	class dual:
		def __init__(self, vector_base, result_type, i):
			self.vector_base = vector_base
			self.result_type = result_type
			self.i = i

		def __call__(self, vector_base_vector):
			return self.result_type(
			    self.vector_base.index(vector_base_vector) == self.i)

		def __eq__(self, other):
			"""Overrides the default implementation, want to check if semantics are equal"""
			if type(other) is type(self):
				return self.__dict__ == other.__dict__
			return NotImplemented

		def __hash__(self):
			"""Overrides the default implementation"""
			return hash(tuple(sorted(self.__dict__.items())))

		def __str__(self):
			return r"{e_i}^{{*}}".format(e_i=self.vector_base[self.i])

	@staticmethod
	def standard_dual_vector_base(vector_base, result_type=int):
		return tuple(
		    tensor.dual(vector_base, result_type, i)
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
		#assumes that the tensor is not "mixed-order"
		#NOTE: rank is smallest number of pure tensor terms required. order is the number of vector spaces taken in the tensor products.
		result = self @ tensor_arg
		order = max(
		    [len(tensor_base_vector) for tensor_base_vector in self.keys()])
		for r in range(0, order):
			result = result.trace(0, order - r)
		return result

	@staticmethod
	def kronecker_delta(dimension):
		r"""Returns kronecker delta
		(GUESS) :math:`\boldsymbol{\delta} = \sum_{i,j} [i=j] e_i\otimes e^j`
		:param dimension: dimension of vector space
		:return: kronecker delta as a mixed tensor
		"""

		def iversion_bracket(proposition):
			return 1 if proposition else 0

		vector_base = tensor.standard_vector_base(dimension)
		dual_base = tensor.standard_dual_vector_base(vector_base)
		return tensor({
		    tensor.__pure_tensorXpure_tensor(
		        (vector_base[i], ), (dual_base[j], )): iversion_bracket(i == j)
		    for i, j in itertools.product(range(0, dimension), repeat=2)
		})

	@staticmethod
	def symbolic(vector_base, rank, symbol='A'):
		"""[summary]
		
		:param vector_base: e.g. tensor.standard_vector_base(dimension) or sympy.symbols("e_{0:3}")
		:type vector_base: [type]
		:param rank: [description]
		:type rank: [type]
		:param symbol: [description], defaults to 'A'
		:param symbol: str, optional
		:return: [description]
		:rtype: [type]
		"""

		def latex_vector_base_vector(v, vector_base, dual_base):
			return ''.join([
			    "^{",
			    str(vector_base.index(v) if v in vector_base else " "), "}",
			    "_{",
			    str(dual_base.index(v) if v in dual_base else " "), "}"
			])

		def latex_tensor_base_vector(V, vector_base, dual_base):
			return ''.join([
			    latex_vector_base_vector(v, vector_base, dual_base) for v in V
			])

		contravariant_rank, covariant_rank = rank
		dual_base = tensor.standard_dual_vector_base(vector_base)
		result = tensor()
		for tensor_base_vector in itertools.product(
		    *[vector_base] * contravariant_rank,
		    *[dual_base] * covariant_rank):
			result = result + tensor({
			    tuple(tensor_base_vector):
			    sympy.Symbol((symbol + "{indices}").format(
			        indices=latex_tensor_base_vector(tensor_base_vector,
			                                         vector_base, dual_base)))
			})
		return result

	@staticmethod
	def same_coefficient(dimension, rank, coefficient=0):
		contravariant_rank, covariant_rank = rank
		vector_base = tensor.standard_vector_base(dimension)
		dual_base = tensor.standard_dual_vector_base(vector_base)
		result = tensor()
		for tensor_base_vector in itertools.product(
		    *[vector_base] * contravariant_rank,
		    *[dual_base] * covariant_rank):
			result = result + tensor({tuple(tensor_base_vector): coefficient})
		return result

	def latex(self):
		return r' + '.join([
		    r' \cdot '.join([
		        r"({0})".format(coefficient),
		        r' \otimes '.join(["{0}".format(v) for v in base])
		    ]) for base, coefficient in self.items()
		])

	def __str__(self):
		return LatexNodes2Text().latex_to_text(self.latex())

	#A=tensor({((1,0),):1,((0,1),):2});B=tensor({((1,0),):3});
	def trace(
	    self,
	    first_slot,
	    second_slot,
	    pairing=lambda cov, con: cov(con) if callable(cov) else con(cov)
	):  # the "else"-part is probably related to the double dual isomorphism (V*)* ~ V
		"""Trace/contraction of tensor
		
		NOTE: Does not work for braided monodial categories
		:return: [description]
		:rtype: [type]
		"""

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
