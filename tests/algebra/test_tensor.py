import itertools

import numpy as np
import pytest

from mathematics.algebra.tensor import *
from mathematics.algebra.create import *


class TestTensor:
    @pytest.mark.timeout(1)
    def test_tensor(self):
        basis = tuple(sympy.symbols("e_{0:3}"))
        dual_basis = tuple(sympy.symbols("e^{0:3}"))

        def slot_to_dual(e):
            if e in basis:
                return dual_basis[basis.index(e)]
            if e in dual_basis:
                return basis[dual_basis.index(e)]
            raise NotImplementedError()

        AMap = mixed_tensor(Tensor, "A", basis, (1, 1), slot_to_dual)

        def multilinear_map(x, y):
            return Tensor({sympy.Symbol("w_0"): 2 * x, sympy.Symbol("w_1"): 2 * y})

        A = AMap(multilinear_map)
        A2 = A * A
        pass
