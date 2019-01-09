import numpy as np
import scipy as sp
import scipy.optimize


class RungeKutta:
	r"""Creates a runge kutta method with Butcher Tableu
		.. math::
			y_{n+1}		= y_n + h \sum_{i=1}^s b_i   k_i
			k_i = f\left( t_n + c_i h,\ y_{n} + h \sum_{j=1}^s a_{ij} k_j \right), \quad i = 1, \ldots, s.
			y^*_{n+1}	= y_n + h \sum_{i=1}^s b^*_i k_i
			e_{n+1} = y_{n+1} - y^*_{n+1} = h\sum_{i=1}^s (b_i - b^*_i) k_i
	"""

	@staticmethod
	def general_k(a, c, F, t0, y0, delta_t):
		def system_for_k(k):
			return [F(t0 + c[i] * delta_t, y0 + delta_t * sum([a[i, j] * k[j] for j in range(len(k))])) - k[i] for i in range(len(c))]

		return sp.optimize.root(system_for_k, np.ones_like(c)).x

	@staticmethod
	def explicit_k(a, c, F, t0, y0, delta_t):
		k = np.zeros_like(c)
		for i in range(len(c)):
			k[i] = F(t0 + c[i] * delta_t, y0 + delta_t * sum([a[i, j] * k[j] for j in range(len(k))]))
		return k

	@classmethod
	def solve_for_k(cls, a, c, F, t0, y0, delta_t):
		if np.allclose(a, np.tril(a, -1)) and np.allclose(c, [0] + c[1:]):
			return cls.explicit_k(a, c, F, t0, y0, delta_t)
		else:
			return cls.general_k(a, c, F, t0, y0, delta_t)

	@staticmethod
	def consistent_c(a):
		return [sum([aij for aij in ai]) for ai in a]

	@staticmethod
	def step(b, F, y0, delta_t, k):
		return y0 + delta_t * sum([b[i] * k[i] for i in range(len(b))])

	@staticmethod
	def error_estimate(b, bstar, delta_t, k):
		return delta_t * sum([(b[i] - bstar[i]) * k[i] for i in range(len(b))])

	def __init__(self, F, t0, y0, a, b, c=None):
		self.a = a
		self.b = b
		self.c = c if c is None else self.consistent_c(a)
		self.F = F
		self.t0 = t0
		self.y0 = y0

	def __call__(self, delta_t):
		k = self.solve_for_k(self.a, self.c, self.F, self.t0, self.y0, delta_t)
		return self.step(self.b, self.F, self.y0, delta_t, k)


class PredictorCorrector:
	def __init__(self, predictor, corrector):
		self.predictor = predictor
		self.corrector = corrector

	def __call__(self, F, t0, y0, delta_t=None):
		delta_t = delta_t if delta_t is None else np.spacing(t0)