import numpy as np
import scipy as sp
import scipy.optimize
import collections
from math import sqrt


class Lobatto:
	#Attempts to follow http://homepage.math.uiowa.edu/~ljay/publications.dir/Lobatto.pdf
	@staticmethod
	def pack(a,b,c):
		X = np.hstack((np.ravel(a),np.ravel(b),np.ravel(c)))
		return X
	@staticmethod
	def unpack(X):
		s = int(sqrt(len(X)+1)-1)
		a = X[:-2*s].reshape(s,s)
		b = X[-2*s:-s]
		c = X[-s:]
		return a,b,c
	@classmethod
	def assumption_B(cls,p):
		def null_system_for_assumption(X):
			a, b, c = cls.unpack(X)
			result = [k * sum([bj * (cj**(k - 1)) for bj, cj in zip(b, c)]) - 1 for k in range(1, p + 1)]
			return result

		return null_system_for_assumption

	@classmethod
	def assumption_C(cls,q):
		def null_system_for_assumption(X):
			a, b, c = cls.unpack(X)
			result = [k * sum([aij * (cj**(k - 1)) for aij, cj in zip(ai, c)]) - (ci**k) for ai, ci in zip(a, c) for k in range(1, q + 1)]
			return result

		return null_system_for_assumption

	@classmethod
	def assumption_D(cls,r):
		def null_system_for_assumption(X):
			a, b, c = cls.unpack(X)
			result= [
				k * sum([aij * ci**(k - 1) * bi for aij, bi, ci in zip(ai, b, c)]) + bj*(cj**k - 1) for ai, bj, cj in zip(a, b, c)
				for k in range(1, r + 1)
			]
			return result

		return null_system_for_assumption

	@classmethod
	def assumption_IIIC(cls, s):
		def null_system_for_assumption(X):
			a, b, c = cls.unpack(X)
			result= np.hstack(([ai[0] - b[0] for ai in a], [asj - bj for asj, bj in zip(a[-1], b)], cls.assumption_B(2 * len(c) - 2)(X),
				cls.assumption_C(len(c) - 1)(X), cls.assumption_D(len(c) - 1)(X)))
			return result
		a = [[1.0 for i in range(s)] for j in range(s)]
		b = [1.0 for i in range(s)]
		c = [1.0 for i in range(s)]
		#Need to choose a solver that allows for the output to be different than the input
		sol = sp.optimize.root(null_system_for_assumption, cls.pack(a,b,c), method='lm')
		result = cls.unpack(sol.x)
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
			return [F(t0 + c[i] * delta_t, y0 + delta_t * sum([a[i, j] * k[j] for j in range(len(k))])) - k[i] for i in range(len(c))]

		sol = sp.optimize.root(system_for_k, np.ones_like(c))
		return sol.x

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