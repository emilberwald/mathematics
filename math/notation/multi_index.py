from number_theory.combinatorics import *
from math import gamma

class multi_index(tuple):
	@classmethod
	def __prepare__(mcs, *args, **kwargs):
		print("multi_index.__prepare__({0},{1},{2})".format(mcs,args,kwargs))
		return {}
	def __new__(mcs, *args, **kwargs):
		print("multi_index.__new__({0},{1},{2})".format(mcs,args,kwargs))
		return super().__new__(mcs, *args, **kwargs)
	def __call__(cls, *args, **kwargs):
		print("multi_index.__call__({0},{1},{2})".format(cls,args,kwargs))
		return super().__call__(*args, **kwargs)
	def __add__(self,b):
		print("multi_index.__add__({0},{1})".format(self,b))
		return multi_index((ai + bi for ai,bi in zip(self,b)))
	def __radd__(self,b):
		print("multi_index.__radd__({0},{1})".format(self,b))
		return self.__add__(b)
	def __sub__(self,b):
		print("multi_index.__sub__({0},{1})".format(self,b))
		return multi_index((ai - bi for ai,bi in zip(self,b)))
	def __abs__(self):
		print("multi_index.__abs__({0})".format(self))
		return sum(self)
	def __rpow__(self,a):
		print("multi_index.__rpow__({0},{1})".format(self,a))
		powers = (ai ** bi for ai,bi in zip(a,self))
		result = next(powers,1.0)
		for power in powers:
			result *= power
		return result
	def factorial(self):
		print("multi_index.factorial({0})".format(self))
		factorials = (gamma(ai + 1) for ai in self)
		result = next(factorials,1.0)
		for factorial in factorials:
			result *= factorial
		return result
	def binomial_coefficient(self,b):
		print("multi_index.binomial_coefficient({0},{1})".format(self,b))
		b = multi_index(b)
		return self.factorial() / (b.factorial() * (a - b).factorial())
	def multinomial_coefficient(self):
		print("multi_index.multinomial_coefficient({0})".format(self))
		return gamma(abs(self) + 1) / self.factorial()

def unsummed_taylor_expansion_partial_derivative_coefficients_at_point(dx,order):
	"""key-wise sum for several different points, each unsummed expansion weighed, solve for weights, given that only the sum in the basis of the derivative/key of interest should be equal to one. or something. to get finite difference schema."""
	return {partial_derivative_orders: (dx ** multi_index(partial_derivative_orders)) / multi_index(partial_derivative_orders).factorial() for n in range(0,order + 1) for partial_derivative_orders in integer_partitions(len(dx),n)}
