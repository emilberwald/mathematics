import statistics
from itertools import chain, combinations, tee


def powerset(iterable):
    """
	https://docs.python.org/3/library/itertools.html#recipes
	NOTE: finite sets only

	:param iterable:
	:return:
	"""
    xs = list(iterable)
    return chain.from_iterable(combinations(xs, n) for n in range(len(xs) + 1))


def pairwise_disjoint(*sets):
    """
	https://stackoverflow.com/a/44786707
	NOTE: finite sets only

	:param sets:
	:return:
	"""
    return sum(len(u) for u in sets) == len(set().union(*sets))


def preimage(domain, function, codomain):
    return {arg for arg in domain if function(arg) in codomain}


class MeasurableSpace:
    def __init__(self, X, Σ):
        """
		NOTE: finite sets only

		:param X: a set
		:param Σ: a (subset of (the set of all subsets of X))
					its elements are called measurable sets
		"""
        assert X in Σ
        for A in Σ:
            assert (X - A) in Σ
        for A in powerset(X):
            if all(Ai in Σ for Ai in A):
                assert A in Σ
        self.X = X
        self.Σ = Σ

    def set(self):
        return self.X

    def sigma_algebra_on_set(self):
        return self.Σ

    def measurable_sets(self):
        yield from self.Σ


class MeasureSpace:
    def __init__(self, domain: MeasurableSpace, measure):
        for measurable_set in domain.measurable_sets():
            if measurable_set == set():
                assert measure(measurable_set) == 0
            else:
                assert measure(measurable_set) >= 0
        for subset in powerset(domain.measurable_sets()):
            if pairwise_disjoint(*subset):
                assert measure(set().union(*subset)) == sum(measure(s) for s in subset)
        self.XΣ = domain
        self.μ = measure

    def measurable_space(self):
        return self.XΣ

    def measure(self):
        return μ


class ProbabilitySpace(MeasureSpace):
    def __init__(self, domain: MeasurableSpace, measure):
        super().__init__(domain, measure)
        assert self.measure_space.measure()(self.measure_space.measurable_space().set()) == 1


def function_is_measurable(domain: MeasurableSpace, function, codomain: MeasurableSpace):
    return all(
        preimage(domain.set(), function, codomain_measurable_set) in domain.sigma_algebra_on_set()
        for codomain_measurable_set in codomain.measurable_sets()
    )


def integral(measurable_integration_region, measure_space: MeasureSpace, *level_set_value_pair):
    return sum(
        value * measure_space.measure()(measurable_integration_region.intersection(level_set))
        for level_set, value in level_set_value_pair
    )


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def lebesgue_integral_limit_sequence(
    preimage_mapping,
    codomain_partitioned_into_measurable_subsets,
    measurable_codomain_subset_representative_element_chooser=statistics.mean,
):
    """

	:param preimage_mapping: maps a measurable subset to its preimage
	:param codomain_partitioned_into_measurable_subsets:
		codomain partitioned into measurable sets.
	:param measurable_codomain_subset_representative_element_chooser:
	   maps from one of the sets in the partition to a value from that set.
	:return:
	"""
    for measurable_codomain_subset in codomain_partitioned_into_measurable_subsets:
        measurable_codomain_subset_representative_element_chooser(measurable_codomain_subset) * preimage_mapping(
            measurable_codomain_subset
        )
