import math
import unittest
import logging
from .ode_step import *


class TestLobatto(unittest.TestCase):
	def test_IIIC(self):
		x2 = Lobatto.assumption_IIIC(2)
		pass


class TestRungeKutta(unittest.TestCase):
	def test_implicit_runge_kutta(self):
		"""
		Four-stage, 3rd order, L-stable Diagonally Implicit Runge Kutta method
		  dy/dt = F(t,y) = K*y
		  t0 = 0
		  y0 = y(t0) = 1
		  y(t) = exp(K*t)
		 """
		a = np.array([
			[1 / 2, 0, 0, 0],
			[1 / 6, 1 / 2, 0, 0],
			[-1 / 2, 1 / 2, 1 / 2, 0],
			[3 / 2, -3 / 2, 1 / 2, 1 / 2],
		])
		b = np.array([3 / 2, -3 / 2, 1 / 2, 1 / 2])
		c = RungeKutta.consistent_c(a)

		Ks = np.hstack((np.random.uniform(-5, 0, 5), np.random.uniform(0, 5, 5)))
		for K in Ks:

			def F(t, y):
				return K * y

			t = [0]
			y = [1]
			expected_y = [1]
			delta_t = 0.001
			max_t = 2.0
			for i in range(0, int(max_t / delta_t)):
				y.append(RungeKutta(F, t[-1], y[-1], a, b, c)(delta_t))
				t.append(t[-1] + delta_t)
				expected_y.append(np.exp(K * t[-1]))
				error_estimate = expected_y[-1] - y[-1]
				np.testing.assert_almost_equal(
					y[-1],
					expected_y[-1],
					decimal=0,
					err_msg=
					f"K={K} e={error_estimate} h={delta_t} log_h(e)={math.log(abs(error_estimate if error_estimate else np.nextafter(error_estimate,error_estimate+1)),delta_t)} [t={t[-1]}, i={i}/{int(max_t/delta_t)}]"
				)

	def test_explicit_runge_kutta(self):
		#https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods#Use
		"""Ralston's method"""
		a = np.array([[0, 0], [2 / 3, 0]])
		b = np.array([1 / 4, 3 / 4])
		c = np.array([0, 2 / 3])

		def F(t, y):
			return np.tan(y) + 1

		t = [1]
		y = [1]
		delta_t = 0.025
		for i in range(0, 4):
			y.append(RungeKutta(F, t[-1], y[-1], a, b, c)(delta_t))
			t.append(t[-1] + delta_t)
		expected_t = [1, 1.025, 1.05, 1.075, 1.1]
		expected_y = [1, 1.066869388, 1.141332181, 1.227417567, 1.335079087]

		np.testing.assert_almost_equal(t, expected_t)
		np.testing.assert_almost_equal(y, expected_y)


if __name__ == '__main__':
	unittest.main()
