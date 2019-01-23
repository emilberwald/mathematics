import functools
import enum
import numpy as np


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
    """
	:param permutation: permutation in 'one line notation' (https://en.wikipedia.org/wiki/Permutation#One-line_notation),
                        e.g. if (0,1,2) -> (2,1,0) under the permutation then the permutation is (2,1,0)

    :return:            returns the decomposition into disjoint cycles (as a set of tuples).
                        https://en.wikipedia.org/wiki/Iterated_function#Definition
                        Iterate 0:                  f^0 = id
                        Iterate n+1:                f^{n+1}(x) = f(f^{n}(x))
                        Periodic orbit:             f^{n+m}(x) = f^{n}(x)
                            Periodic point: x
                            Smallest value m for a given periodic point x is called the period of the orbit.
                        https://en.wikipedia.org/wiki/Cycle_detection
                        Here we learn that in general for function iterates over a finite set there might be a starting subsequence that is not
                        repeated and that there will be an periodic orbit (repeating sequence, cycle, loop, ...).

                        A cycle is a periodic orbit, with the iterated function being the permutation. 
                        Any element of the iterated sequence is a periodic point, so there is an equivalence class of cycles
                        that represent the same iterated sequence modulo starting point.
                        A canonical order is a way to choose representatives from these equivalence classes by choosing starting point
                        in an ordered fashion.
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
    return {
        canonical_order([iterate + offset for iterate in cycle]) for cycle in cycles
    }


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
        k = min(transposition)
        l = max(transposition)
        # move k to l:
        for s in range(k, l):
            adjacent_transpositions.add(canonical_order((s, s + 1)))
            # move l from l-1 to k:
        for s in range(l - 1, k, -1):
            adjacent_transpositions.add(canonical_order((s - 1, s)))
    return adjacent_transpositions


def inversions_domainpair(permutation):
    """:math:`\{(i,j) \colon i<j \land \pi(i)>\pi(j)\}`
	NOTE: called pair of  places in wikipedia"""
    return {
        (i, j)
        for i in range(0, len(permutation))
        for j in range(0, len(permutation))
        if (i < j) and (permutation[i] > permutation[j])
    }


def inversions_codomainpair(permutation):
    """ :math:`\{(\pi(i),\pi(j)) \colon i<j \land \pi(i)>\pi(j)\}`
	NOTE: called pair of elements in wikipedia
	"""
    return {
        (permutation[i], permutation[j])
        for i in range(0, len(permutation))
        for j in range(0, len(permutation))
        if (i < j) and (permutation[i] > permutation[j])
    }


def inversion_vector(permutation):
    """https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)#Inversion_related_vectors
	"""
    pairs = inversions_codomainpair(permutation)
    return [sum([pair[1] == i for pair in pairs]) for i in sorted(permutation)]


def left_inversion_count(permutation):
    """l[i] is the number of elements where permutation[0:i] is greater than permutation[i] 
	"""
    return [
        sum(np.array(permutation[0:i]) > permutation[i])
        for i in range(0, len(permutation))
    ]


def right_inversion_count(permutation):
    """Lehmer code
	r[i] is the number of elements where permutation[i] is smaller than permutation[i+1:] 
	"""
    return [
        sum(permutation[i] > np.array(permutation[i + 1 :]))
        for i in range(0, len(permutation))
    ]


def permutation_symbol(*permutation):
    return functools.reduce(
        lambda x, y: x * y,
        [
            np.sign(permutation[j] - permutation[i])
            for i in range(0, len(permutation))
            for j in range(i + 1, len(permutation))
        ],
    )


@enum.unique
class ParityMethod(enum.Enum):
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
