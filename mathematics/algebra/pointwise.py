import functools
import itertools
import math
import operator
import sys


class Pointwise:
    def __init__(self, function):
        self.function = function

    def __repr__(self):
        return repr(self.function) + "-pointwise"

    def __call__(self, *args, **kwargs):
        if callable(self.function):
            return self.function(*args, **kwargs)
        else:
            return self.function

    @staticmethod
    def __op(lhs, op, *args, **kwargs):
        return op(lhs(*args, **kwargs))

    @staticmethod
    def __binop(lhs, op, rhs, *args, **kwargs):
        return op(lhs(*args, **kwargs), rhs(*args, **kwargs))

    def __abs__(self):
        def __abs(*args, **kwargs):
            return type(self).__op(self, operator.abs, *args, **kwargs)

        return type(self)(__abs)

    def __neg__(self):
        def __neg(*args, **kwargs):
            return type(self).__op(self, operator.__neg__, *args, **kwargs)

        return type(self)(__neg)

    def __pos__(self):
        def __pos(*args, **kwargs):
            return type(self).__op(self, operator.__pos__, *args, **kwargs)

        return type(self)(__pos)

    def __rmul__(self, lhs):
        def __rmul(*args, **kwargs):
            return (lhs(*args, **kwargs) if callable(lhs) else lhs) * self(
                *args, **kwargs
            )

        return type(self)(__rmul)

    def __lt__(self, rhs):
        # assert isinstance(rhs, Pointwise)
        def __lt(*args, **kwargs):
            return type(self).__binop(self, operator.__lt__, rhs, *args, **kwargs)

        return type(self)(__lt)

    def __le__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __le(*args, **kwargs):
            return type(self).__binop(self, operator.__le__, rhs, *args, **kwargs)

        return type(self)(__le)

    def __eq__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __eq(*args, **kwargs):
            return type(self).__binop(self, operator.__eq__, rhs, *args, **kwargs)

        return type(self)(__eq)

    def __ne__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __ne(*args, **kwargs):
            return type(self).__binop(self, operator.__ne__, rhs, *args, **kwargs)

        return type(self)(__ne)

    def __ge__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __ge(*args, **kwargs):
            return type(self).__binop(self, operator.__ge__, rhs, *args, **kwargs)

        return type(self)(__ge)

    def __gt__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __gt(*args, **kwargs):
            return type(self).__binop(self, operator.__gt__, rhs, *args, **kwargs)

        return type(self)(__gt)

    def __add__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __add(*args, **kwargs):
            return type(self).__binop(self, operator.__add__, rhs, *args, **kwargs)

        return type(self)(__add)

    def __and__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __and(*args, **kwargs):
            return type(self).__binop(self, operator.__and__, rhs, *args, **kwargs)

        return type(self)(__and)

    def __floordiv__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __floordiv(*args, **kwargs):
            return type(self).__binop(self, operator.__floordiv__, rhs, *args, **kwargs)

        return type(self)(__floordiv)

    def __mod__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __mod(*args, **kwargs):
            return type(self).__binop(self, operator.__mod__, rhs, *args, **kwargs)

        return type(self)(__mod)

    def __mul__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __mul(*args, **kwargs):
            return type(self).__binop(self, operator.__mul__, rhs, *args, **kwargs)

        return type(self)(__mul)

    def __or__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __or(*args, **kwargs):
            return type(self).__binop(self, operator.__or__, rhs, *args, **kwargs)

        return type(self)(__or)

    def __pow__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __pow(*args, **kwargs):
            return type(self).__binop(self, operator.__pow__, rhs, *args, **kwargs)

        return type(self)(__pow)

    def __sub__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __sub(*args, **kwargs):
            return type(self).__binop(self, operator.__sub__, rhs, *args, **kwargs)

        return type(self)(__sub)

    def __truediv__(self, rhs):
        # assert isinstance(rhs, Pointwise)

        def __truediv(*args, **kwargs):
            return type(self).__binop(self, operator.__truediv__, rhs, *args, **kwargs)

        return type(self)(__truediv)

    def after(self, rhs):
        """
        compose
        """
        # assert isinstance(rhs, Pointwise)

        def __after(*args, **kwargs):
            try:
                return self(*rhs(*args, **kwargs))
            except:
                return self(rhs(*args, **kwargs))

        return type(self)(__after)

    def before(self, rhs):
        """
        precompose
        """
        # assert isinstance(rhs, Pointwise)

        def __before(*args, **kwargs):
            try:
                return rhs(*self(*args, **kwargs))
            except:
                return rhs(self(*args, **kwargs))

        return type(self)(__before)
