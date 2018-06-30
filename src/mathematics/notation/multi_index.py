from math import gamma
from autologging import traced


@traced
class multi_index(tuple):
	@classmethod
	def __prepare__(mcs, *args, **kwargs):
		return {}

	def __new__(mcs, *args, **kwargs):
		return super().__new__(mcs, *args, **kwargs)

	def __add__(self, b):
		return multi_index((ai + bi for ai, bi in zip(self, b)))

	def __radd__(self, b):
		return self.__add__(b)

	def __sub__(self, b):
		return multi_index((ai - bi for ai, bi in zip(self, b)))

	def __abs__(self):
		r"""Calculates magnitude
		
		:param self: :math:`\alpha`
		:return: :math:`| \alpha | = \alpha_1 + \alpha_2 + \cdots + \alpha_n`
		:rtype: [type]
		"""

		return sum(self)

	def __rpow__(self, a):
		r"""Calculates power
		
		:param self: :math:`\alpha`
		:param a: vector
		:type a: [type]
		:return: :math:`x^\alpha = x_1^{\alpha_1} x_2^{\alpha_2} \ldots x_n^{\alpha_n}`
		:rtype: [type]
		"""

		powers = (ai**bi for ai, bi in zip(a, self))
		result = next(powers, 1.0)
		for power in powers:
			result *= power
		return result

	def factorial(self):
		r"""Calculates factorial
		
		:param self: :math:`\alpha`
		:return: :math:`\alpha ! = \alpha_1! \cdot \alpha_2! \cdots \alpha_n!`
		:rtype: [type]
		"""

		factorials = (gamma(ai + 1) for ai in self)
		result = next(factorials, 1.0)
		for factorial in factorials:
			result *= factorial
		return result

	def binomial_coefficient(self, b):
		r"""Calculates binomial coefficient

		:param self: :math:`\alpha`
		:param b: :math:`\beta`
		:type b: [type]
		:return: :math:`\binom{\alpha}{\beta} = \binom{\alpha_1}{\beta_1}\binom{\alpha_2}{\beta_2}\cdots\binom{\alpha_n}{\beta_n} = \frac{\alpha!}{\beta!(\alpha-\beta)!}`
		:rtype: [type]
		"""
		print("multi_index.binomial_coefficient({0},{1})".format(self, b))
		b = multi_index(b)
		return self.factorial() / (b.factorial() * (self - b).factorial())

	def multinomial_coefficient(self):
		r"""Calculates multinomial coefficient
	
		:param self: :math:`\alpha`
		:return: :math:`\binom{k}{\alpha} = \frac{k!}{\alpha_1! \alpha_2! \cdots \alpha_n! } = \frac{k!}{\alpha!}`
		:rtype: [type]
		"""
		return gamma(abs(self) + 1) / self.factorial()
