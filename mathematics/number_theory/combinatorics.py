import enum as _enum
import functools as _functools
import math as _math
import operator as _operator


def sign(x):
    return _math.copysign(1, x) if x else 0


def integer_partitions(number_of_elements, total_sum):
    if number_of_elements == 1:
        yield (total_sum,)
    else:
        for i in range(0, total_sum + 1):
            for j in integer_partitions(number_of_elements - 1, total_sum - i):
                yield (i,) + j


def canonical_order(cycle):
    shift = cycle.index(min(cycle))
    return tuple(cycle[i % len(cycle)] for i in range(shift, shift + len(cycle)))


def permutation_to_cycles(permutation):
    r"""
	:param permutation: permutation in 'one line notation'
						(see https://en.wikipedia.org/wiki/Permutation#One-line_notation),
						e.g. if permutation(0,1,2) -> (2,1,0) then ``permutation`` is (2,1,0)

	:return:			returns the decomposition into disjoint cycles (as a set of tuples).
						https://en.wikipedia.org/wiki/Iterated_function#Definition
						Iterate 0:				  f^0 = id
						Iterate n+1:				f^{n+1}(x) = f(f^{n}(x))
						Periodic orbit:			 f^{n+m}(x) = f^{n}(x)
							Periodic point: x
							Smallest ``m`` for periodic point ``x`` is the ``period of the orbit``.
						https://en.wikipedia.org/wiki/Cycle_detection
						Function iterates over a finite set might have a starting subsequence that
						is not repeated, but will always have a periodic orbit (repeating sequence,
						cycle, loop, ...).

						A cycle is a periodic orbit, with the permutation as the iterated function.
						Any element of the iterated sequence is a periodic point, so there is an
						equivalence class of cycles that represent the same iterated sequence
						modulo starting point.
						A canonical order is a way to choose representatives from these equivalence
						classes by choosing a starting point in an ordered fashion.
	"""

    codomain = list(permutation)
    offset = min(codomain)
    shifted_codomain = [v - offset for v in codomain]

    cycles = list()
    for starting_point in shifted_codomain:
        if any([starting_point in cycle for cycle in cycles]):
            continue
        else:
            cycle = list()
            cycle.append(starting_point)
            while True:
                iterate = shifted_codomain[cycle[-1]]
                if iterate != cycle[0]:
                    cycle.append(iterate)
                    continue
                else:
                    break
            cycles.append(cycle)
    return {canonical_order([iterate + offset for iterate in cycle]) for cycle in cycles}


def permutation_to_transpositions(permutation):
    """[summary]
		One-cycles are ignored; it does not add a dummy (x,x) two-cycle
	:param permutation: [description]
	:type permutation: [type]
	:return: [description]
	:rtype: [type]
	"""

    cycles = permutation_to_cycles(permutation)
    transpositions = set()
    for cycle in cycles:
        for k in range(1, len(cycle)):
            transpositions.add(canonical_order([cycle[0], cycle[k]]))
    return transpositions


def permutation_to_adjacent_transpositions(permutation):
    transpositions = permutation_to_transpositions(permutation)
    adjacent_transpositions = set()
    for transposition in transpositions:
        x_0 = min(transposition)
        x_1 = max(transposition)
        # move from x_0 to x_1 (...>x_0>....<x_1<...) -> (...x_0...<<,>x_1>...):
        for position in range(x_0, x_1):
            adjacent_transpositions.add(canonical_order((position, position + 1)))
            # move from x_1-1 to x_0 (...x_0...<<,>x_1>...) -> (...<x_0<...,>x_1>...):
        for position in range(x_1 - 1, x_0, -1):
            adjacent_transpositions.add(canonical_order((position - 1, position)))
    return adjacent_transpositions


def inversions_domainpair(permutation):
    r""":_math:`\{(i,j) \colon i<j \land \pi(i)>\pi(j)\}`
	NOTE: called pair of  places in wikipedia"""
    return {
        (i, j)
        for i in range(0, len(permutation))
        for j in range(0, len(permutation))
        if (i < j) and (permutation[i] > permutation[j])
    }


def inversions_codomainpair(permutation):
    r""" :_math:`\{(\pi(i),\pi(j)) \colon i<j \land \pi(i)>\pi(j)\}`
	NOTE: called pair of elements in wikipedia
	"""
    return {
        (permutation[i], permutation[j])
        for i in range(0, len(permutation))
        for j in range(0, len(permutation))
        if (i < j) and (permutation[i] > permutation[j])
    }


def inversion_vector(permutation):
    """https://en.wikipedia.org/wiki/Inversion_(discrete__mathematics)#Inversion_related_vectors
	"""
    pairs = inversions_codomainpair(permutation)
    return [sum([pair[1] == i for pair in pairs]) for i in sorted(permutation)]


def left_inversion_count(permutation):
    """l[i] is the number of elements where permutation[0:i] is greater than permutation[i]
	"""
    return [sum(p > permutation[i] for p in permutation[0:i]) for i in range(0, len(permutation))]


def right_inversion_count(permutation):
    """Lehmer code
	r[i] is the number of elements where permutation[i] is smaller than permutation[i+1:]
	"""
    return [sum(permutation[i] > p for p in permutation[i + 1 :]) for i in range(0, len(permutation))]


def permutation_symbol(*permutation):
    return _functools.reduce(
        lambda x, y: x * y,
        [
            sign(permutation[j] - permutation[i])
            for i in range(0, len(permutation))
            for j in range(i + 1, len(permutation))
        ],
    )


@_enum.unique
class ParityMethod(_enum.Enum):
    permutation_symbol = 1
    transpositions = 2
    inversions = 3


def parity(permutation, method: ParityMethod = ParityMethod.permutation_symbol):
    if method == ParityMethod.permutation_symbol:
        return permutation_symbol(*permutation)
    elif method == ParityMethod.transpositions:
        return (-1) ** (len(permutation_to_transpositions(permutation)))
    elif method == ParityMethod.inversions:
        return (-1) ** (sum(left_inversion_count(permutation)))
    else:
        raise NotImplementedError()


def apply_permutation(t, permutation):
    yield from (t[pi] for pi in permutation)


def riffle_shuffles(P, Q, op=None):
    """
	Returns riffle shuffles, also called (p-q)-shuffles.
	Notation as operator: P ⧢ Q

	https://en.wikipedia.org/wiki/Shuffle_algebra#Shuffle_product
	https://en.wikipedia.org/wiki/Riffle_shuffle_permutation

	:param P:   first set in shuffle. Needs to be slicable.
	:param Q:   second set in shuffle. Needs to be slicable.
	:param op:  if None, addition is used to combine elements during the riffle shuffle.
	"""
    op = _operator.add if op is None else op
    shuffles = list()
    if P and Q:
        shuffles.extend([op(P[0:1], riffle_shuffle) for riffle_shuffle in riffle_shuffles(P[1:], Q)])
        shuffles.extend([op(Q[0:1], riffle_shuffle) for riffle_shuffle in riffle_shuffles(P, Q[1:])])
    elif P:
        shuffles.append(P)
    elif Q:
        shuffles.append(Q)
    return shuffles
