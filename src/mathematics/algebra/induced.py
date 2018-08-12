def induced_symmetric_bilinar_form(quadratic_form):
	def symmetric_bilinear_form(u, v):
		return 1 / 4 * (quadratic_form(u + v) - quadratic_form(u - v))

	return symmetric_bilinear_form
