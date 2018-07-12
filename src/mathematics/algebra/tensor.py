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
	@staticmethod
	def _puretensorproduct(*base_tensors):
		r"""Tensor product for pure tensors without coefficients.
		
		:param base_tensors: each argument is a tensor base vector :math::
			\mathsf{e_A} = \mathbf{e}_0\otimes\ldots\otimes \mathbf{e}_{order(\mathsf{e_A})-1}
		:type e_A: [tuple]
		:return: :math::
			\bigotimes_{\mathsf{e_A}\in \textup{base tensors}}\mathsf{e_A} = \bigotimes_{\mathsf{e_A}\in \textup{base tensors}}(\bigotimes_{\mathbf{e}_k\in \mathsf{e_A}} \mathbf{e}_k)
		:rtype: [tuple]
		"""
		base_tensor_result = list()
		for base_tensor in base_tensors:
			for base_vector in base_tensor:
				base_tensor_result.append(base_vector)
		return tuple(base_tensor_result)

	def __rmul__(self, scalar):
		r"""scalar product
		(DEFINITION) Compatability of tensor scalar multiplication with vector scalar multiplication
		:math::
			c\cdot \mathsf{t} = c\cdot(\mathbf{t_1}\otimes \mathbf{t_2}) = (c \cdot \mathbf{t_1})\otimes \mathbf{t_2} = \mathbf{t_1}\otimes(c \cdot \mathbf{t_2})
		(GUESS) Compatability of tensor scalar multiplication with field multiplication
		:math::
			c_1\cdot(c_2\cdot (\mathsf{t_1}\otimes \mathsf{t_2})) = (c_1 \cdot_F c_2)\mathsf{t_1}\otimes \mathsf{t_2}
		(GUESS) Distributivity of scalar multiplication with respect to tensor addition
		:math::
			c_1\cdot(\mathsf{t_1}\otimes \mathsf{t_2} + \mathsf{t_3}\otimes \mathsf{t_4}) = c_1\cdot(\mathsf{t_1}\otimes \mathsf{t_2}) + c_1\cdot(\mathsf{t_3}\otimes \mathsf{t_4}) 
		(GUESS) The scalar can be distributed into the coefficient of each pure tensor term.
		
		:param self: tensor
		:type self: [tensor]
		:param scalar: scalar
		:return: scaled tensor 
		:rtype: [tensor]
		"""

		return type(self)({
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
			(c_1 + c_2)(e_i\otimes e_j) = c_1 (e_i \otimes e_j) + c_2 (e_i\otimes e_j)

		We want to distribute the addition as much as possible.
		The internal state of the tensor is in terms of pure tensors of the vector bases.

		:param self: tensor
		:type self: [tensor]
		:param B: the tensor to add
		:type B: [tensor]
		:return: 
		
		:math::
			\mathsf{self}+\mathsf{B} 
			= (c_1(\mathsf{e_1_i}) \mathsf{e_1_i})+(c_2(\mathsf{e_2_i}) \mathsf{e_2_i})
			= \left[\sum_{\mathsf{e_1_k} \notin \{\mathsf{e_2_i}\}} c_1(\mathsf{e_1_k}) \mathsf{e_1_k}\right]
			+ \left[\sum_{\mathsf{e_2_k} \notin \{\mathsf{e_1_i}\}} c_2(\mathsf{e_2_k}) \mathsf{e_2_k}\right]
			+ \left[\sum_{\mathsf{e_1_k} \in \{\mathsf{e_2_i}\}} (c_1(\mathsf{e_1_k}) + c_2(\mathsf{e_1_k})) \mathsf{e_1_k}\right]
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
		return type(self)({
		    tensor_base_vector: -self[tensor_base_vector]
		    for tensor_base_vector in self
		})

	def __sub__(self, B):
		return self.__add__(-B)

	def __matmul__(self, B):
		r"""Tensor procuct of tensors.
		(GUESS) This whole function is guesswork. I think the proper term is unbiased monodial category?
		
		:param self: tensor
		:type self: [tensor]
		:param B: tensor
		:type B: [tensor]
		:return: :math::
			\mathsf{self} \otimes \mathsf{B} = (\sum_i c_1^i \mathsf{e_1}_i)\otimes(\sum_i c_2^i \mathsf{e_2}_i) = \sum_i \sum_j (c_1^i\cdot c_2^j)\cdot(\mathsf{e_1}_i \otimes \mathsf{e_2}_j)
		:rtype: [tensor]
		"""
		result = type(self)()
		for tensor_base_vector_self, coefficient_self in self.items():
			for tensor_base_vector_b, coefficient_b in B.items():
				tensor_base_vector_result = tensor._puretensorproduct(
				    tensor_base_vector_self, tensor_base_vector_b)
				if tensor_base_vector_result not in result:
					result[
					    tensor_base_vector_result] = coefficient_self * coefficient_b
				else:
					# perhaps this could happen if one of the tensor base vectors are of mixed order?
					# GUESS: summation best way to handle this?
					result = result + type(self)({
					    tensor_base_vector_result:
					    coefficient_self * coefficient_b
					})
		return result

	def __call__(self, arg):
		r"""Tensor product followed by contraction/trace, adjacent pairs in tensor product
		NOTE: Does not try to match the orders. It assumes the tensor is not mixed-order in such a way so the operation does not work.
		NOTE: rank is smallest number of pure tensor terms required. order is the number of vector spaces taken in the tensor products.
	
		:param self: 
		:type self: [tensor]
		:param arg: 
		:type arg: [tensor]
		:return: :math::`\mathsf{self}\otimes \mathsf{arg}`, followed by iterated contraction, 
			matching slots by adjacent pairs (last of self, first of arg), until either self or arg is fully contracted
		:rtype: [tensor]
		"""

		result = self @ arg
		order_self = max(
		    [len(tensor_base_vector) for tensor_base_vector in self.keys()])
		order_arg = max(
		    [len(tensor_base_vector) for tensor_base_vector in arg.keys()])
		for r in range(0, min(order_self, order_arg)):
			result = result.trace(order_self - r - 1, order_self - r)
		return result

	@staticmethod
	def default_pairing(cov, con):
		if (callable(cov)):
			try:
				#assuming the first argument is the dual of the second argument...
				return cov(con)
			except:
				pass
		if (callable(con)):
			try:
				#assuming the second argument is the dual of the first argument...
				return con(cov)
			except:
				pass
		raise TypeError(
		    "The default pairing did not work, need to provide a user defined pairing."
		)

	def braiding_map(self, e_A, index_permutation_generator):
		return type(self)({
		    tuple(e_A[i] for i in index_permutation_generator): 1
		})

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
		pairing = tensor.default_pairing if pairing is None else pairing

		result = type(self)()
		for tensor_base_vector_self in self:
			braided_tensor = self.braiding_map(
			    tensor_base_vector_self, [first_slot] + [second_slot] + [
			        slot for slot in range(0, len(tensor_base_vector_self))
			        if slot not in (first_slot, second_slot)
			    ])
			for tensor_base_vector_braided_tensor in braided_tensor:
				pairing_factor = pairing(
				    *tensor_base_vector_braided_tensor[0:2])
				coefficient = self[tensor_base_vector_self] * braided_tensor[tensor_base_vector_braided_tensor]
				contracted_summand = type(self)({
				    tensor_base_vector_braided_tensor[2:]:
				    coefficient * pairing_factor
				})
				result = result + contracted_summand
		return result

	class dual:
		def __init__(self, vectorspace_base, result_type, i):
			self.vectorspace_base = vectorspace_base
			self.result_type = result_type
			self.i = i

		def __call__(self, vectorspace_base_vector):
			return self.result_type(
			    self.vectorspace_base.index(vectorspace_base_vector) == self.i)

		def __eq__(self, other):
			"""Overrides the default implementation, want to check if semantics are equal"""
			if type(other) is type(self):
				return self.__dict__ == other.__dict__
			return NotImplemented

		def __hash__(self):
			"""Overrides the default implementation"""
			return hash(tuple(sorted(self.__dict__.items())))

		def __str__(self):
			return r"{e_i}^{{*}}".format(e_i=self.vectorspace_base[self.i])

	@staticmethod
	def standard_base_dual_vectorspace(vectorspace_base, result_type=int):
		return tuple(
		    tensor.dual(vectorspace_base, result_type, i)
		    for i in range(0, len(vectorspace_base)))

	@staticmethod
	def standard_base_vectorspace(dimension):
		return tuple(integer_partitions(dimension, 1))

	@classmethod
	def multilinear_mapping_tensor_expansion(cls, *vectorspace_bases):
		r"""expands multilinear function as tensor. 

		NOTE: not sure if the math is valid for vector valued multilinear mappings.
		:param: *vectorspace_bases: Vector space base of each argument of the function.
		:return: Returns a lambda function which takes the mulilinear function. 
			:math::
				f \mapsto \mathsf{F}=
				f(\mathbf{e}_{i_1}^{(1)},\ldots,\mathbf{e}_{i_k}^{(k)}) \cdot \mathbf{e}_{i_1}^{(1)}^{*}\otimes\cdots\otimes\mathbf{e}_{i_k}^{(k)}^{*} 
				= f(\mathbf{e}_{i_1}^{(1)},\ldots,\mathbf{e}_{i_k}^{(k)}) \cdot \mathbf{e}_{(1)}^{i_1}\otimes\cdots\otimes\mathbf{e}_{(k)}^{i_k} 
		:rtype: [type]
		"""
		dual_vectorspace_bases = [
		    cls.standard_base_dual_vectorspace(vectorspace_base)
		    for vectorspace_base in vectorspace_bases
		]
		return lambda f, vectorspace_bases=vectorspace_bases, dual_bases=dual_vectorspace_bases: functools.reduce(operator.add,[cls({
		     tuple(dual_bases[vector_space_index][tensor_index[vector_space_index]] for vector_space_index in range(
		               0, len(dual_bases))):
		     f(*[
		         vectorspace_bases[vector_space_index]
		         [tensor_index[vector_space_index]]
		         for vector_space_index in range(0, len(vectorspace_bases))
		     ])
		 }) for tensor_index in itertools.product(
		    *[range(0, len(vectorspace_base)) for vectorspace_base in vectorspace_bases])],cls())

	@classmethod
	def mixed_tensor(cls, vectorspace_base, rank, dual_base=None):
		contravariant_rank, covariant_rank = rank
		dual_base = cls.standard_base_dual_vectorspace(
		    vectorspace_base) if dual_base is None else dual_base
		return cls.multilinear_mapping_tensor_expansion(
		    *[dual_base] * contravariant_rank,
		    *[vectorspace_base] * covariant_rank)

	@classmethod
	def kronecker_delta(cls, vectorspace_base):
		r"""Returns kronecker delta
		(GUESS) :math:`\boldsymbol{\delta} = \sum_{i,j} e_j^{*}(e_i) e_i^{**} \otimes e_j^{*}`
		:param dimension: dimension of vector space
		:return: kronecker delta as a mixed tensor
		"""
		return cls.mixed_tensor(vectorspace_base,
		                        (1, 1))(lambda cov, con: cov(con))

	@classmethod
	def symbolic(cls, symbol, vectorspace_base, rank):
		"""[summary]
		
		:param symbol: Example: "A"
		:param symbol: [str]
		:param vectorspace_base: e.g. tensor.standard_base_vectorspace(dimension) or sympy.symbols("e_{0:3}")
		:type vectorspace_base: [type]
		:param rank: [description]
		:type rank: [type]
		:return: [description]
		:rtype: [type]
		"""

		def latex_vectorspace_base_vector(vectorspace_base, dual_base, v):
			return ''.join([
			    "^{",
			    str(dual_base.index(v) if v in dual_base else " "), "}", "_{",
			    str(
			        vectorspace_base.index(v)
			        if v in vectorspace_base else " "), "}"
			])

		def latex_tensor_base_vector(vectorspace_base, dual_base, V):
			return ''.join([
			    latex_vectorspace_base_vector(vectorspace_base, dual_base, v)
			    for v in V
			])

		def make_symbol(symbol, vectorspace_base, dual_base, V):
			return sympy.Symbol((symbol + "{indices}").format(
			    indices=latex_tensor_base_vector(vectorspace_base, dual_base,
			                                     V)))

		dual_base = cls.standard_base_dual_vectorspace(vectorspace_base)
		return cls.mixed_tensor(vectorspace_base, rank, dual_base)(lambda *tensor_base_vector,symbol=symbol,vectorspace_base=vectorspace_base,dual_base=dual_base:
		make_symbol(symbol, vectorspace_base, dual_base, tensor_base_vector))

	@classmethod
	def same_coefficient(cls, vectorspace_base, rank, coefficient=0):
		return cls.mixed_tensor(vectorspace_base,
		                        rank)(lambda *tensor_base_vector: coefficient)

	def without_zeros(self, zero_coefficient=0):
		return type(self)({
		    base_vector: coefficient
		    for base_vector, coefficient in self.items()
		    if coefficient != zero_coefficient
		})

	def latex(self):
		return r' + '.join([
		    r' \cdot '.join([
		        r"({0})".format(coefficient),
		        r' \otimes '.join(["{0}".format(v) for v in base])
		        if base else r"1"  # scalar 𝟙 
		    ]) for base, coefficient in self.items()
		])

	def __str__(self):
		return LatexNodes2Text().latex_to_text(self.latex())
