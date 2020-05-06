import itertools as _itertools
import math as _math
from ..algebra.matrix import Matrix
from ..algebra.tensor import Tensor
from ..number_theory.combinatorics import parity, apply_permutation, riffle_shuffles

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

# def hodge_star(g : Matrix, a : Tensor):
#    k = len(a.keys())
#    (*a)_{i_{k+1}, ..., i_n} = _math.sqrt(abs(Matrix.determinant(g)))/_math.gamma(k+1) * a^{i_1, ..., i_k} * \eps_{i_1, ..., i_k, ..., i_n}
