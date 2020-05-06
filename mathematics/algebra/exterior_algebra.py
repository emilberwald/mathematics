import itertools as _itertools

from ..algebra.tensor import Tensor
from ..number_theory.combinatorics import parity, apply_permutation, riffle_shuffles

#clifford algebra with Q = 0?

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