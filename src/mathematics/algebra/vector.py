__all__ = ["vector"]


class vector(tuple):
	@classmethod
	def __prepare__(mcs, *args, **kwargs):
		return {}

	def __new__(mcs, *args, **kwargs):
		return super().__new__(mcs, *args, **kwargs)

	def __add__(self, b):
		return vector((ai + bi for ai, bi in zip(self, b)))

	def __radd__(self, b):
		return self.__add__(b)

	def __sub__(self, b):
		return vector((ai - bi for ai, bi in zip(self, b)))

	def __rmul__(self, a):
		r"""scalar product
		
		:param self: vector
		:param a: scalar
		:type a: [type]
		:return: :math:`a\cdot \mathbf{x} = a \cdot (x^ke_k) =  (ax^k) e_k`
		:rtype: [type]
		"""

		return vector((a * bi for bi in self))

	def __rmatmul__(self, A):
		return
