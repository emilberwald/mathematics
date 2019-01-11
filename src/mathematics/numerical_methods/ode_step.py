import operator
import numpy as np
import scipy as sp
import scipy.optimize
import collections
from math import sqrt


class Lobatto:
	#Attempts to follow http://homepage.math.uiowa.edu/~ljay/publications.dir/Lobatto.pdf
	@staticmethod
	def pack(a, b, c):
		X = np.hstack((np.ravel(a), np.ravel(b), np.ravel(c)))
		return X

	@staticmethod
	def unpack(X):
		s = int(sqrt(len(X) + 1) - 1)
		a = X[:-2 * s].reshape(s, s)
		b = X[-2 * s:-s]
		c = X[-s:]
		return a, b, c

	@classmethod
	def assumption_B(cls, p):
		def null_system_for_assumption(X):
			a, b, c = cls.unpack(X)
			s = len(c)
			result = [sum([b[j] * (c[j]**(k - 1.0)) for j in range(s)]) - 1.0 / k for k in range(1, p + 1)]
			return result

		return null_system_for_assumption

	@classmethod
	def assumption_C(cls, q):
		def null_system_for_assumption(X):
			a, b, c = cls.unpack(X)
			s = len(c)
			result = [sum([(c[j]**(k - 1)) * a[i, j] for j in range(s)]) - (c[i]**k) / k for i in range(s) for k in range(1, q + 1)]
			return result

		return null_system_for_assumption

	@classmethod
	def assumption_D(cls, r):
		def null_system_for_assumption(X):
			a, b, c = cls.unpack(X)
			s = len(c)
			result = [
				sum([b[i] * (c[i]**(k - 1.0)) * a[i, j] for i in range(s)]) - (b[j] / k) * (1.0 - (c[j])**k) for j in range(s)
				for k in range(1, r + 1)
			]
			return result

		return null_system_for_assumption

	@classmethod
	def assumption_IIIC(cls, s):
		def create_system(soft=lambda x, cmp, y: cmp(x, y)):
			def system(X):
				a, b, c = cls.unpack(X)
				result = np.hstack((
					[soft(c[0], operator.eq, 0.0), soft(c[-1], operator.eq, 1.0)],
					[soft(0, operator.le, ci) for ci in c],
					[soft(ci, operator.le, 1.0) for ci in c],
					[soft(c[i], operator.lt, c[i + 1]) for i in range(len(c) - 1)],
					[soft(ai[0], operator.eq, b[0]) for ai in a],
					[soft(asj, operator.eq, bj) for asj, bj in zip(a[-1], b)],
					[soft(x, operator.eq, 0.0) for x in cls.assumption_B(2 * len(c) - 2)(X)],
					[soft(x, operator.eq, 0.0) for x in cls.assumption_C(len(c) - 1)(X)],
					[soft(x, operator.eq, 0.0) for x in cls.assumption_D(len(c) - 1)(X)],
				))
				return result

			return system

		def try_to_minimize(a, b, c, epsilon=1e-1):
			soft_min = lambda lhs, cmp, rhs: (not (cmp(lhs, rhs))) * np.linalg.norm(lhs - rhs)
			system_to_minimize = lambda x: np.linalg.norm(create_system(soft_min)(x))
			sol = sp.optimize.minimize(system_to_minimize, cls.pack(a, b, c))
			if (sol.success):
				cost = system_to_minimize(sol.x)
				a, b, c = cls.unpack(sol.x)
				return a, b, c, cost
			else:
				if 'x' in sol:
					cost = system_to_minimize(sol.x)
					if cost < epsilon:
						a, b, c = cls.unpack(sol.x)
						return a, b, c, cost, sol.success

		def try_to_find_kernel(a, b, c):
			soft_0 = lambda lhs, cmp, rhs: (not (cmp(lhs, rhs))) * np.linalg.norm(lhs - rhs)
			system_to_find_kernel = lambda x: create_system(soft_0)(x)
			#Need to choose a solver that allows for the output to be different than the input
			sol = sp.optimize.root(system_to_find_kernel, cls.pack(a, b, c), method='lm')
			if (sol.success):
				residual = system_to_find_kernel(sol.x)
				a, b, c = cls.unpack(sol.x)
				return a, b, c, residual, sol.success

		a = [[0.0 for i in range(s)] for j in range(s)]
		b = [0.0 for i in range(s)]
		c = [0.0 for i in range(s)]
		for i in range(2):
			result_0 = try_to_find_kernel(a, b, c)
			if (result_0):
				a, b, c, residual_0, success = result_0
				c[0] = 0.0
				c[-1] = 1.0
				reqs = create_system()(cls.pack(a, b, c))
				if (all(reqs) or success):
					break

			result_min = try_to_minimize(a, b, c)
			if (result_min):
				a, b, c, residual_min, success = result_min
				c[0] = 0.0
				c[-1] = 1.0
				reqs = create_system()(cls.pack(a, b, c))
				if (all(reqs) or success):
					break
		return a.tolist(), b.tolist(), c.tolist()

	@staticmethod
	def hardcoded_IIIC(p):
		result= (butcher_tableu['lobatto_iiic']['butcher_matrix'][p], butcher_tableu['lobatto_iiic']['weights'][p], butcher_tableu[
			'lobatto_iiic']['abscissae'][p])
		return result





butcher_tableu = {
	'lobatto_iiic': {
	'butcher_matrix': {
	2: [
	[1 / 2, -1 / 2],
	[1 / 2, 1 / 2],
	],
	3: [
	[1 / 6, -1 / 3, 1 / 6],
	[1 / 6, 5 / 12, -1 / 12],
	[1 / 6, 2 / 3, 1 / 6],
	],
	4: [
	[1 / 12, -sqrt(5) / 12, sqrt(5) / 12, -1 / 12],
	[1 / 12, 1 / 4, (10 - 7 * sqrt(5)) / 60, sqrt(5) / 60],
	[1 / 12, (10 + 7 * sqrt(5)) / 60, 1 / 4, -sqrt(5) / 60],
	[1 / 12, 5 / 12, 5 / 12, 1 / 12],
	],
	5: [
	[1 / 20, -7 / 60, 2 / 15, -7 / 60, 1 / 20],
	[1 / 20, 29 / 180, (47 - 15 * sqrt(21)) / 315, (203 - 30 * sqrt(21)) / 1260, -3 / 140],
	[1 / 20, (329 + 105 * sqrt(21)) / 2880, 73 / 360, (329 - 105 * sqrt(21)) / 2880, 3 / 160],
	[1 / 20, (203 + 30 * sqrt(21)) / 1260, (47 + 15 * sqrt(21)) / 315, 29 / 180, -3 / 140],
	[1 / 20, 49 / 180, 16 / 45, 49 / 180, 1 / 20],
	],
	},
	'weights': {
	2: [1 / 2, 1 / 2],
	3: [1 / 6, 2 / 3, 1 / 6],
	4: [1 / 12, 5 / 12, 5 / 12, 1 / 12],
	5: [1 / 20, 49 / 180, 16 / 45, 49 / 180, 1 / 20],
	},
	'abscissae': {  #node coefficients that multiply h, f(x+c*h)
	2: [0, 1],
	3: [0, 1 / 2, 1],
	4: [0, 1/2-sqrt(5)/10, 1/2+sqrt(5)/10,1],
	5: [0, 1/2-sqrt(21)/14, 1/2, 1/2+sqrt(21)/14, 1],
	}
	},
}


class RungeKutta:
	r"""Creates a runge kutta method using a Butcher Tableu
		a := ButcherMatrix
		b := weights
		c := abscissae
		.. math::
			y_{n+1}		= y_n + h \sum_{i=1}^s b_i   k_i
			k_i = f\left( t_n + c_i h,\ y_{n} + h \sum_{j=1}^s a_{ij} k_j \right), \quad i = 1, \ldots, s.
			y^*_{n+1}	= y_n + h \sum_{i=1}^s b^*_i k_i
			e_{n+1} = y_{n+1} - y^*_{n+1} = h\sum_{i=1}^s (b_i - b^*_i) k_i
	"""

	@staticmethod
	def general_k(a, c, F, t0, y0, delta_t):
		def system_for_k(k):
			return [F(t0 + c[i] * delta_t, y0 + delta_t * sum([a[i][j] * k[j] for j in range(len(k))])) - k[i] for i in range(len(c))]

		sol = sp.optimize.root(system_for_k, np.ones_like(c))
		return sol.x

	@staticmethod
	def explicit_k(a, c, F, t0, y0, delta_t):
		k = np.zeros_like(c)
		for i in range(len(c)):
			k[i] = F(t0 + c[i] * delta_t, y0 + delta_t * sum([a[i][j] * k[j] for j in range(len(k))]))
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
		self.c = self.consistent_c(a) if c is None else c
		self.F = F
		self.t0 = t0
		self.y0 = y0
		self.k = None

	def __call__(self, delta_t):
		self.k = self.solve_for_k(self.a, self.c, self.F, self.t0, self.y0, delta_t)
		return self.step(self.b, self.F, self.y0, delta_t, self.k)


class PredictorCorrector:
	def __init__(self, predictor, corrector):
		self.predictor = predictor
		self.corrector = corrector

	def __call__(self, F, t0, y0, delta_t=None):
		delta_t = delta_t if delta_t is None else np.spacing(t0)