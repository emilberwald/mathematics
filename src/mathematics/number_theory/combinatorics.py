import itertools


def integer_partitions(number_of_elements, total_sum):
	if number_of_elements == 1:
		yield (total_sum, )
	else:
		for i in range(0, total_sum + 1):
			for j in integer_partitions(number_of_elements - 1, total_sum - i):
				yield (i, ) + j


def permutation_to_cycles(permutation):
	"""
	:param permutation: [description]
	:type permutation: [type]
	"""
	codomain = list(permutation)
	offset = min(codomain)
	shifted_codomain = [v - offset for v in codomain]

	cycles = list()
	for s in shifted_codomain:
		if any([s in cycle for cycle in cycles]):
			continue
		else:
			cycle = list()
			cycle.append(s)
			while True:
				value = shifted_codomain[cycle[-1]]
				if value != cycle[0]:
					cycle.append(value)
					continue
				else:
					break
			cycles.append(cycle)
	return {tuple(v + offset for v in cycle) for cycle in cycles}


def permutation_to_transpositions(permutation):
	cycles = permutation_to_cycles(permutation)
	transpositions = set()
	for cycle in cycles:
		for k in range(
		    1,
		    len(cycle)):  # ignore "one-cycles", or add a dummy (x,x) two-cycle
			transpositions.add((cycle[0], cycle[k]))
	return transpositions


def permutation_to_adjacent_transpositions(permutation):
	transpositions = permutation_to_transpositions(permutation)
	adjacent_transpositions = set()
	for transposition in transpositions:
		k = min(transposition)
		l = max(transposition)
		#move k to l:
		for s in range(k, l):
			adjacent_transpositions.add((s, s + 1))
		#move l from l-1 to k:
		for s in range(l - 1, k, -1):
			adjacent_transpositions.add((s - 1, s))
	return adjacent_transpositions
