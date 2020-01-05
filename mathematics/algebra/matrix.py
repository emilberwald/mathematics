import functools as _functools
import itertools as _itertools
import operator as _operator
import collections as _collections
import copy as _copy
from typing import Union, List

from ..number_theory.combinatorics import parity


def flatten(it, skip=(str, bytes)):
    for el in it:
        if isinstance(el, _collections.abc.Iterable) and not isinstance(el, skip):
            yield from flatten(el)
        else:
            yield el


def find_row_pivot_no(f, no):
    nof_rows = len(f)
    for pivot_row_no in range(no, nof_rows):
        if all(abs(f[pivot_row_no][no]) >= abs(f[row_no][no]) for row_no in range(no, nof_rows)):
            return pivot_row_no


def row_pivoting(f, no):
    nof_rows = len(f)
    permutation = [[float(row_no == col_no) for col_no in range(0, nof_rows)] for row_no in range(0, nof_rows)]
    pivot_row = find_row_pivot_no(f, no)
    if pivot_row != no:
        permutation[pivot_row], permutation[no] = permutation[no], permutation[pivot_row]
    return permutation, None


def complete_pivoting(f, no):
    nof_rows = len(f)
    nof_cols = max(len(row) for row in f)
    left_permutation = [[float(row_no == col_no) for col_no in range(0, nof_rows)] for row_no in range(0, nof_rows)]
    right_permutation = [[float(row_no == col_no) for col_no in range(0, nof_cols)] for row_no in range(0, nof_cols)]

    _, (pivot_row, pivot_col) = max(
        ((_, (i, j)) for i, row in enumerate(f) for j, _ in enumerate(row)),
        key=lambda p: (abs(p[0]), (-p[1][0], -p[1][1]))
        if all((ix >= no for ix in p[1]))
        else (-float("inf"), (-p[1][0], -p[1][1])),
    )

    left_permutation[pivot_row], left_permutation[no] = (
        left_permutation[no],
        left_permutation[pivot_row],
    )

    right_permutation[pivot_col], right_permutation[no] = right_permutation[no], right_permutation[pivot_col]

    return left_permutation, right_permutation


def doolittle_scheme(U, no):
    if U[no][no] == 0:
        return None
    else:
        nof_rows = len(U)
        elimination = [[float(row_no == col_no) for col_no in range(0, nof_rows)] for row_no in range(0, nof_rows)]
        for forward_row_no in range(no + 1, nof_rows):
            elimination[forward_row_no][no] = -U[forward_row_no][no] / U[no][no]
        return elimination, None


def gauss_jordan_scheme(U, no):
    def find_pivot(U, no):
        nof_rows = len(U)
        nof_cols = max(len(row) for row in U)
        for col_no in range(no, nof_cols):
            for row_no in range(no, nof_rows):
                if U[row_no][col_no] != 0:
                    return (row_no, col_no, nof_rows, nof_cols)

    if pivot := find_pivot(U, no):
        pivot_row, pivot_col, nof_rows, _ = pivot
        elimination_col = min(nof_rows - 1, pivot_col)
        left_elimination = [[float(row_no == col_no) for col_no in range(0, nof_rows)] for row_no in range(0, nof_rows)]
        for row_no in range(0, nof_rows):
            left_elimination[row_no][elimination_col] = -U[row_no][pivot_col] / U[pivot_row][pivot_col]
        return left_elimination, None
    return None


def reduced_row_echelon(U, no):
    nof_rows = len(U)
    nof_cols = max(len(row) for row in U)
    min_nof = min(nof_rows, nof_cols)
    if 1 + no == min_nof:
        left_rescale = [[float(row_no == col_no) for col_no in range(0, nof_rows)] for row_no in range(0, nof_rows)]
        for row_no, row in enumerate(U):
            for col in row:
                if col != 0:
                    left_rescale[row_no][row_no] = 1.0 / col
                    break
        return left_rescale, None
    else:
        return None


class Matrix(list):
    def __init__(self, value: List[List[float]], *, deep=True):
        value = _copy.deepcopy(value) if deep else value
        super().__init__(value)

    @staticmethod
    def forward_substitution_for_lower_triangular_system(Fconst: List[List[float]], Fx: List[float], n: int):
        x: List[float] = list()
        for intra in range(0, n):
            if Fconst[intra][intra] == 0:
                raise ValueError("matrix is singular")
            x.append(Fx[intra] / Fconst[intra][intra])
            for post in range(intra + 1, n):
                Fx[post] = Fx[post] - Fconst[post][intra] * x[-1]
        return x

    @staticmethod
    def backward_substitution_for_upper_triangular_system(Fconst: List[List[float]], Fx: List[float], n: int):
        x: List[float] = list()
        for intra in range(n - 1, -1, -1):
            if Fconst[intra][intra] == 0:
                raise ValueError("matrix is singular")
            x.append(Fx[intra] / Fconst[intra][intra])
            for pre in range(0, intra):
                Fx[pre] = Fx[pre] - Fconst[pre][intra] * x[-1]
        return x

    @staticmethod
    def diag(*diags):
        nof_diags = len(diags)
        return [
            list(_itertools.chain(range(0, diag_no), (diag,), range(diag_no + 1, nof_diags)))
            for diag_no, diag in enumerate(diags)
        ]

    def inversed_lower_triangular(self, selfx: Union["Matrix", List[float]]):
        """
            Forward-Substitution for Lower Triangular System
            :param self:    lower triangular matrix (lhs)
            :param selfx:      column vector (rhs)
            self^{-1} * selfx
        """
        x = Matrix.forward_substitution_for_lower_triangular_system(
            self, list(flatten(selfx)) if isinstance(selfx, Matrix) else selfx, self.nof_diagonal_elements
        )
        return Matrix([x]).transpose if isinstance(selfx, Matrix) else x

    def inversed_upper_triangular(self, selfx: Union["Matrix", List[float]]):
        """
            Back-Substitution for Upper Triangular System
            :param self:    upper triangular matrix (lhs)
            :param fx:      column vector (rhs)
            self^{-1} * selfx
        """
        x = Matrix.backward_substitution_for_upper_triangular_system(
            self, list(flatten(selfx)) if isinstance(selfx, Matrix) else selfx, self.nof_diagonal_elements
        )
        return Matrix([x]).transpose if isinstance(selfx, Matrix) else x

    def gaussian_elimination(self, *, permutation_scheme, elimination_scheme, rescale_scheme):
        """

			https://math.stackexchange.com/a/1398058

			.. math::
				F x = fx

			Row operations:

			.. math::
				R F x = R fx

			Column operations:

			.. math::
				F C C^{-1} x = F x

			Row and column operations:

			.. math::
				R F C C^{-1} x = R fx

				U := R F C

			returns (U, R, C)
				- U - upper triangular matrix
				- R - is None if not used
				- C - is None if not used
		"""

        U = Matrix(self)
        R = None
        C = None

        for no in range(0, self.nof_diagonal_elements):
            if permutation_scheme and (permutations := permutation_scheme(U, no)):
                left_permutation, right_permutation = (
                    Matrix(permutation) if permutation else permutation for permutation in permutations
                )
                if left_permutation:
                    R = left_permutation if R is None else left_permutation @ R
                    U = left_permutation @ U
                if right_permutation:
                    C = right_permutation if C is None else C @ right_permutation
                    U = U @ right_permutation
            if elimination_scheme and (eliminations := elimination_scheme(U, no)):
                left_elimination, right_elimination = (
                    Matrix(elimination) if elimination else elimination for elimination in eliminations
                )
                if left_elimination:
                    U = left_elimination @ U
                    R = left_elimination if R is None else left_elimination @ R
                if right_elimination:
                    U = U @ right_elimination
                    C = right_elimination if C is None else C @ right_elimination
            if rescale_scheme and (rescales := rescale_scheme(U, no)):
                left_rescale, right_rescale = (Matrix(rescale) if rescale else rescale for rescale in rescales)
                if left_rescale:
                    U = left_rescale @ U
                    R = left_rescale if R is None else left_rescale @ R
                if right_rescale:
                    U = U @ right_rescale
                    R = right_rescale if R is None else R @ right_rescale
        return U, R, C

    def factor_lu_doolittle(self):
        L = self.zero
        U = self.zero
        for i in range(0, self.nof_diagonal_elements):
            for j in range(i, self.nof_diagonal_elements):
                U[i][j] = self[i][j] - sum([L[i][k] * U[k][j] for k in range(0, i)])
            for j in range(i, self.nof_diagonal_elements):
                if i == j:
                    L[i][j] = 1
                else:
                    L[j][i] = (self[j][i] - sum([L[j][k] * U[k][i] for k in range(0, i)])) / U[i][i]
        return L, U

    def factor_lu_crout(self):
        L = self.zero
        U = self.zero
        for i, j in self.diagonal_keys:
            U[i][j] = 1
        for i in range(0, self.nof_diagonal_elements):
            for j in range(i, self.nof_diagonal_elements):
                L[j][i] = self[j][i] - sum([L[j][k] * U[k][i] for k in range(0, i)])
            for j in range(i, self.nof_diagonal_elements):
                if L[i][i] == 0:
                    raise ValueError("L is singular")
                else:
                    U[i][j] = (self[i][j] - sum([L[i][k] * U[k][j] for k in range(0, i)])) / L[i][i]
        return L, U

    def inversed_lu_factorisation_by_gaussian_elimination_with_partial_pivoting(self, b: Union["Matrix", List[float]]):
        """
            :param self:
                linear transform in
                    self @ x = b
            :param x:
                solution to
                    self @ x = b
            :param b:
                rhs in
                    self @ x = b
            :returns:
                - x     - solution
                - P     permutation matrix
                - L     lower triangular matrix
                - U     upper triangular matrix

            See also :cite:`Heath2002`
        """
        LU = Matrix(self)
        permutation = list(range(0, LU.nof_diagonal_elements))
        for k in range(0, LU.nof_diagonal_elements - 1):
            p = find_row_pivot_no(LU, k)
            if p != k:
                LU[k], LU[p] = LU[p], LU[k]
                b[k], b[p] = b[p], b[k]
                permutation[k], permutation[p] = permutation[p], permutation[k]
            if LU[k][k] == 0:
                continue
            for i in range(k + 1, LU.nof_diagonal_elements):
                LU[i][k] = LU[i][k] / LU[k][k]
            for j in range(k + 1, LU.nof_diagonal_elements):
                for i in range(k + 1, LU.nof_diagonal_elements):
                    LU[i][j] = LU[i][j] - LU[i][k] * LU[k][j]
        P = Matrix.diag(*[1 for row in self])
        P = Matrix([P[i] for i in permutation], deep=False)
        L = Matrix(
            [
                [
                    LU[row_no][col_no] if col_no < row_no else 1 if col_no == row_no else 0 if col_no > row_no else None
                    for col_no in LU.col_nos
                ]
                for row_no in LU.row_nos
            ],
            deep=False,
        )
        U = Matrix(
            [
                [0 if col_no < row_no else LU[row_no][col_no] if col_no >= row_no else None for col_no in LU.col_nos]
                for row_no in LU.row_nos
            ],
            deep=False,
        )
        y = L.inversed_lower_triangular(b)
        x = U.inversed_upper_triangular(y)
        return x, P, L, U

    def inversed(self, fx, *, methods):
        if any(
            method
            in (self.gaussian_elimination, row_pivoting, complete_pivoting, doolittle_scheme, gauss_jordan_scheme)
            for method in methods
        ):
            permutation_scheme = complete_pivoting if complete_pivoting in methods else row_pivoting
            elimination_scheme = gauss_jordan_scheme if gauss_jordan_scheme in methods else doolittle_scheme
            rescale_scheme = reduced_row_echelon if reduced_row_echelon in methods else None
            U, R, C = self.gaussian_elimination(
                permutation_scheme=permutation_scheme,
                elimination_scheme=elimination_scheme,
                rescale_scheme=rescale_scheme,
            )
            Fx = fx if isinstance(fx, Matrix) else Matrix([fx]).transpose
            RFx = Fx if R is None else R @ Fx
            Cinvx = U.inversed_upper_triangular(RFx)
            x = Cinvx if C is None else C @ Cinvx
            x = x if isinstance(fx, Matrix) else list(flatten(x))
            return x
        else:
            return Matrix(Matrix.inverse(self)) @ fx

    @property
    def nof_rows(self):
        return len(self)

    @property
    def nof_cols(self):
        return max(len(row) for row in self)

    @property
    def nof_diagonal_elements(self):
        return min(self.nof_rows, self.nof_cols)

    @property
    def row_nos(self):
        yield from range(0, self.nof_rows)

    @property
    def col_nos(self):
        yield from range(0, self.nof_cols)

    @property
    def diagonal_keys(self):
        for diag_no in self.nof_diagonal_elements:
            yield (diag_no, diag_no)

    @property
    def indices_row_echelon_pivots(self):
        for row_no in self.row_nos:
            for col_no in list(self.col_nos)[::-1]:
                if self[row_no][col_no] != 0:
                    yield (row_no, col_no)
                    break

    @property
    def transpose(self):
        return Matrix(map(list, _itertools.zip_longest(*self)))

    @property
    def zero(self):
        return Matrix([[0 for col in row] for row in self])

    def __add__(self, b):
        return Matrix([[sum(x) for x in zip(*rows)] for rows in zip(self, b)])

    def __matmul__(self, b):
        return Matrix(
            [
                [sum(self_ik * bTjk for self_ik, bTjk in zip(self_i, bTj)) for bTj in Matrix(b).transpose]
                for self_i in self
            ]
        )

    @staticmethod
    def determinant(A):
        return _functools.reduce(
            _operator.add,
            [
                (parity(permutation) if len(permutation) > 1 else 1)
                * _functools.reduce(_operator.mul, [ai[permutation_i] for ai, permutation_i in zip(A, permutation)],)
                for permutation in _itertools.permutations(range(0, len(A)))
            ],
        )

    @staticmethod
    def submatrix(A, exclude_i, exclude_j):
        return [[aj for j, aj in enumerate(ai) if j != exclude_j] for i, ai in enumerate(A) if i != exclude_i]

    @staticmethod
    def minor(A, i, j):
        return Matrix.determinant(Matrix.submatrix(A, i, j))

    @staticmethod
    def cofactor(A, i, j):
        return (-1) ** (i + j) * Matrix.minor(A, i, j)

    @staticmethod
    def inverse(A):
        return [
            [Matrix.determinant(A) ** (-1) * Matrix.cofactor(A, j, i) for j, aj in enumerate(ai)]
            for i, ai in enumerate(A)
        ]
