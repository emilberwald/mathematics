from mathematics.number_theory.combinatorics import integer_partitions

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

	@staticmethod
	def standard_base_dual_vectorspace(vector_base, result_type=int):
		return tuple(
			dual(vector_base, result_type, i)
			for i in range(0, len(vector_base)))

	@staticmethod
	def standard_base_vectorspace(dimension):
		return tuple(integer_partitions(dimension, 1))