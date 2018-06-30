from mathematics.notation.multi_index import multi_index
from mathematics.number_theory.combinatorics import integer_partitions


def taylor_expansion_partial_derivative_coefficients_at_point(dx, order):
	"""key-wise sum for several different points, each unsummed expansion weighed, solve for weights, given that only the sum in the basis of the derivative/key of interest should be equal to one. or something. to get finite difference schema."""
	return {
	    partial_derivative_orders: (dx**multi_index(partial_derivative_orders))
	    / multi_index(partial_derivative_orders).factorial()
	    for n in range(0, order + 1)
	    for partial_derivative_orders in integer_partitions(len(dx), n)
	}
