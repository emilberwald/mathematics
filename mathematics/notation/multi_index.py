from math import gamma


class MultiIndex(tuple):
    @classmethod
    def __prepare__(cls, *_args, **_kwargs):
        return {}

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __add__(self, beta):
        return MultiIndex((alfa_i + beta_i for alfa_i, beta_i in zip(self, beta)))

    def __radd__(self, beta):
        return self.__add__(beta)

    def __sub__(self, beta):
        return MultiIndex((alfa_i - beta_i for alfa_i, beta_i in zip(self, beta)))

    def __abs__(self):
        r"""
        Calculates magnitude

        :param self: :math:`\alpha`
        :return: :math:`| \alpha | = \alpha_1 + \alpha_2 + \cdots + \alpha_n`
        :rtype: [type]
        """

        return sum(self)

    def __rpow__(self, alfa):
        r"""
        Calculates power

        :param self: :math:`\beta`
        :param alfa: vector
        :return: :math:`x^\beta = x_1^{\beta_1} x_2^{\beta_2} \ldots x_n^{\beta_n}`
        :rtype: [type]
        """

        powers = (alfa_i ** beta_i for alfa_i, beta_i in zip(alfa, self))
        result = next(powers, 1.0)
        for power in powers:
            result *= power
        return result

    def factorial(self):
        r"""
        Calculates factorial

        :param self: :math:`\alpha`
        :return: :math:`\alpha ! = \alpha_1! \cdot \alpha_2! \cdots \alpha_n!`
        :rtype: [type]
        """

        factorials = (gamma(ai + 1) for ai in self)
        result = next(factorials, 1.0)
        for factorial in factorials:
            result *= factorial
        return result

    def binomial_coefficient(self, beta):
        r"""
        Calculates binomial coefficient

        :param self: :math:`\alpha`
        :param beta: :math:`\beta`
        :type beta: [type]
        :return: ..math::
            \binom{\alpha}{\beta} =
            \binom{\alpha_1}{\beta_1}\binom{\alpha_2}{\beta_2}\cdots\binom{\alpha_n}{\beta_n}
            = \frac{\alpha!}{\beta!(\alpha-\beta)!}
        :rtype: [type]
        """
        beta = MultiIndex(beta)
        return self.factorial() / (beta.factorial() * (self - beta).factorial())

    def multinomial_coefficient(self):
        r"""
        Calculates multinomial coefficient

        :param self: :math:`\alpha`
        :return: ..math::
            \binom{k}{\alpha}=\frac{k!}{\alpha_1! \alpha_2! \cdots \alpha_n! }=\frac{k!}{\alpha!}
        :rtype: [type]
        """
        return gamma(abs(self) + 1) / self.factorial()
