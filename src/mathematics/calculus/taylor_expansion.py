import itertools
import operator
import functools
from collections import Counter
from mathematics.notation.multi_index import multi_index
from mathematics.number_theory.combinatorics import integer_partitions


def multilinear_mapping(*args, **kwargs):
	r"""

	:param *args: interpreted as vectors from vector spaces in the order of apperance: math:`\mathbf{x}_0,\ldots,\mathbf{x}_k`
	:param \**['bases']:
		Generator for an ordered base for each arg in args,
		.. highlight:: python
			([base_vector for base_vector in base] for base_vectors in bases)
		default:
			The default assumes that the vectors are lists.
			.. highlight:: python
				bases = ([[1 if i == k else 0 for i in range(0,len(arg))] for k in range(0,len(arg))] for arg in args)
	:param \**['dual_bases']:
		Generator for an ordered dual base for each arg in args,
		.. highlight:: python
			([dual_base_vector(arg) for dual_base_vector in dual_base] for arg, dual_base in zip(args, dual_bases))
		should become a generator for tuples of pairings (dual_base_vector,arg)
		default:
			The default assumes that the vectors are indexable:
			.. highlight:: python
				#corresponds to cartesian, (e^i,v) = (e^i,v^ke_k) = v^i = arg[i], v = arg in args:
				dual_bases = ((lambda v, k=k: v[k] for k in range(0, len(arg))) for arg in args)
	:return: [description]
	:rtype: [type]
	"""
	if 'bases' in kwargs:
		bases = kwargs['bases']
	else:
		bases = ([[1 if i == k else 0 for i in range(0, len(arg))]
		          for k in range(0, len(arg))] for arg in args)
	if 'dual_bases' in kwargs:
		dual_bases = kwargs['dual_bases']
	else:
		dual_bases = ((lambda v, k=k: v[k] for k in range(0, len(arg)))
		              for arg in args)
	return lambda f, bases=bases, dual_bases = dual_bases, args = args: functools.reduce(
	 operator.add,
	 ( operator.mul(
	   functools.reduce(operator.mul,itertools.product(*[dual_base_vector(arg) for dual_base_vector in dual_base])),
	   f(base)) for arg, base, dual_base in zip(args, bases, dual_bases)))


def Differential(domain_dimension, differential_order):
	for iterated_partial_derivative_list in itertools.product(
	    range(0, domain_dimension), differential_order):
		pass
	#zero indexing, e_0, ..., e_{domain_dimension-1}
	partial_derivative_orders = Counter(iterated_partial_derivative_list)
	factorials = (gamma(ai + 1) for ai in self)
	result = next(factorials, 1.0)
	for factorial in factorials:
		result *= factorial
	return result


def taylor_expansion_partial_derivative_coefficients_at_point(dx, order):
	"""key-wise sum for several different points, each unsummed expansion weighed, solve for weights, given that only the sum in the basis of the derivative/key of interest should be equal to one. or something. to get finite difference schema."""
	return {
	    partial_derivative_orders: (dx**multi_index(partial_derivative_orders))
	    / multi_index(partial_derivative_orders).factorial()
	    for n in range(0, order + 1)
	    for partial_derivative_orders in integer_partitions(len(dx), n)
	}
