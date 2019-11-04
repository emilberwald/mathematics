import functools as _functools
import operator as _operator


class TupleVector(tuple):
    """
    Vector where basis is index in tuple
    """

    @staticmethod
    def __binop(lhs, op, rhs):
        try:
            return type(lhs)(op(lhsi, rhsi) for lhsi, rhsi in zip(lhs, rhs))
        except:
            return type(lhs)(op(lhsi, rhs) for lhsi in lhs)

    def __call__(self, *args, **kwargs):
        try:
            return type(self)(selfi(*args, **kwargs) for selfi in self)
        except:
            return type(self)(selfi(arg, **kwargs) for selfi, arg in zip(self, args))

    def __add__(self, rhs):
        return type(self).__binop(self, _operator.__add__, rhs)

    def __sub__(self, rhs):
        return type(self).__binop(self, _operator.__sub__, rhs)

    def __mul__(self, rhs):
        raise NotImplementedError()

    def __truediv__(self, rhs):
        return type(self).__binop(self, _operator.__truediv__, rhs)

    def __rmul__(self, lhs):
        # this is wrong if it is supposed to be noncommutative module
        return type(self).__binop(self, _operator.__mul__, lhs)

    def __abs__(self):
        return (
            _functools.reduce(_operator.add, (abs(selfi) ** 2 for selfi in self)) ** 0.5
        )
