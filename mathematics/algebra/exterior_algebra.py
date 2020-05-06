import itertools as _itertools
import math as _math
from ..algebra.matrix import Matrix
from ..algebra.tensor import Tensor
from ..algebra.clifford import Clifford
from ..number_theory.combinatorics import sign, parity, apply_permutation, riffle_shuffles, permutation_symbol

# clifford algebra with Q = 0?


def exterior_product(a: Tensor, b: Tensor):
    k = len(a.keys())
    m = len(b.keys())
    result = Tensor()
    for permutation in riffle_shuffles(range(0, k), range(k, k + m)):
        addend = parity(permutation)
        for akey in apply_permutation(list(a.keys()), permutation[0:k]):
            addend = addend * a[akey]
        for bkey in apply_permutation(list(b.keys()), [p - k for p in permutation[k:]]):
            addend = addend * b[bkey]
        result = result + addend


# hodge star and so on


def hodge_star(g: Matrix, a: Clifford, n: int):
    """
    hodge_star [summary]

    NOTE: this will not work at all unless the keys are tuples of integers zero indexed ... TODO: figure out how to generalise

    :param g: Metric for V, note it is not for dual V*, if you want that you need to sharpen the metric (if I understood this? https://www.homotopico.com/2019/06/10/hodge-star.html)
    :type g: Matrix
    :param a: [description]
    :type a: Clifford
    :param volume: [description]
    :type volume: Clifford
    """
    result = Clifford()
    akeys = list(a.keys())
    for permutation in _itertools.permutations(range(0, n)):
        head = tuple(permutation[0 : len(akeys)])
        tail = tuple(permutation[len(akeys) :])
        if head in akeys:
            result[tail] = (
                1.0
                / (
                    _math.sqrt(abs(Matrix.determinant(g)))
                    * _math.gamma(len(akeys) + 1)
                    * _math.gamma(n - len(akeys) + 1)
                )
                * a[head]
                * permutation_symbol(*permutation)
            )


def hodge_star_inverse(g: Matrix, a: Clifford, n: int):
    k = len(a.keys())
    s = sign(Matrix.determinant(g))
    return ((-1) ** (k * (n - k))) * s * hodge_star(g, a, n)


#def codifferential(g: Matrix, a: Clifford, n: int):
#    k = len(a.keys())
#    return (-1) ** k * hodge_star_inverse(g, exterior_derivative(hodge_star(g, a, n)), n)
