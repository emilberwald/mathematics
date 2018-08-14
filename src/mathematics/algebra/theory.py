def underset(over, under):
	return r" {{ \underset{{ {under} }}{{ {over} }} }}".format(
	    over=over, under=under)


def overset(over, under):
	return r" {{ \overset{{ {over} }}{{ {under} }} }}".format(
	    over=over, under=under)


def subscript(over, under, right=True):
	return r" {{ {over} }}_{{ {under} }} ".format(
	    over=over, under=under
	) if right else r"{{ {{}}_{{ {under} }} {{ {over} }} }}".format(
	    over=over, under=under)


def underbrace(over, under):
	return underset(r"\underbrace{{ {over} }}".format(over=over), under)


class Element():
	def __init__(self, algebraic_structure, index=None, restriction=None):
		self.algebraic_element = underset(
		    (str(algebraic_structure.lower()) if index is None else subscript(
		        str(algebraic_structure).lower(), str(index))),
		    str(algebraic_structure)
		    if restriction is None else str(restriction))

	def __str__(self) -> str:
		return self.algebraic_element


class Operation():
	def __init__(self,
	             *domains,
	             codomain=None,
	             infix=None,
	             prefix=None,
	             postfix=None):
		if codomain:
			if domains:
				self.prefix = r"" if prefix is None else overset(
				    r" \times ".join(domains),
				    underset(str(prefix), str(codomain)))
				self.infix = r"" if infix is None else overset(
				    r" \times ".join(domains),
				    underset(str(infix), str(codomain)))
				self.postfix = r"" if postfix is None else overset(
				    r" \times ".join(domains),
				    underset(str(postfix), str(codomain)))
			else:
				self.prefix = r"" if prefix is None else underset(
				    str(prefix), str(codomain))
				self.infix = r"" if infix is None else underset(
				    str(infix), str(codomain))
				self.postfix = r"" if postfix is None else underset(
				    str(postfix), str(codomain))
		else:
			self.prefix = r"" if prefix is None else str(prefix)
			self.infix = r"" if infix is None else str(infix)
			self.postfix = r"" if postfix is None else str(postfix)

	def __call__(self, *args: Element) -> str:
		return self.prefix + self.infix.join([str(arg)
		                                      for arg in args]) + self.postfix


class Quantifier():
	def __init__(self, quantifier):
		self.quantifier = str(quantifier)

	def __call__(self, *args: Element):
		return r"".join(
		    [r" " + self.quantifier + r" " + str(arg) + r" " for arg in args])


forall = Quantifier(r" \forall ")
exists = Quantifier(r" \exists ")
exists_unique = Quantifier(r" !\exists ")
equals = Operation(infix=r" = ")
nequals = Operation(infix=r" \neq ")
land = Operation(infix=r" \land ")


def element_of(algebraic_structure, *args):
	return underbrace(" ".join([str(arg) for arg in args]),
	                  str(algebraic_structure))


def expression(expr, *quantifiers) -> str:
	return r" \left( " + "".join([
	    str(quantifier) for quantifier in quantifiers
	]) + (r"\colon\quad" if quantifiers else r"") + str(expr) + r" \right) "


def closure(algebraic_structure, op) -> str:
	A = str(algebraic_structure)
	op = Operation(codomain=A, infix=op)
	args = [Element(A, k) for k in range(0, 2)]
	return expression(element_of(A, op(*args)), forall(*args))


def associative(algebraic_structure, op) -> str:
	A = str(algebraic_structure)
	op = Operation(codomain=A, infix=op)
	a = [Element(A, k) for k in range(0, 3)]
	return expression(
	    equals(
	        op(expression(op(a[0], a[1])), a[2]), op(*a),
	        op(a[0], expression(op(a[1], a[2])))), forall(*a))


def identity_element(algebraic_structure, op, id):
	A = str(algebraic_structure)
	op = Operation(codomain=A, infix=op)
	id = Operation(codomain=A, prefix=id)
	a = Element(A)
	return expression(
	    equals(op(id(), a), a, op(a, id())), exists_unique(id()), forall(a))


def inverse_element(algebraic_structure, op, id, restriction=None):
	A = str(algebraic_structure)
	op = Operation(codomain=A, infix=op)
	id = Operation(codomain=A, prefix=id)
	a = [Element(A, k, restriction=restriction) for k in range(0, 2)]
	return expression(
	    equals(op(a[0], a[1]), id(), op(a[1], a[0])), exists_unique(id()),
	    forall(a[0]), exists(a[1]))


def commutative(algebraic_structure, op):
	A = str(algebraic_structure)
	op = Operation(codomain=A, infix=op)
	a = [Element(A, k) for k in range(0, 2)]
	return expression(equals(op(*a), op(*reversed(a))), forall(*a))


def idempotent(algebraic_structure, op):
	A = str(algebraic_structure)
	op = Operation(codomain=A, infix=op)
	a = Element(A)
	return expression(equals(op(a, a), a), forall(a))


def latin_square(algebraic_structure, op):
	A = str(algebraic_structure)
	op = Operation(codomain=A, infix=op)
	a = [Element(A, k) for k in range(0, 4)]
	a = Element(A, 0)
	b = Element(A, 1)
	x_L = Element(A, "L")
	x_R = Element(A, "R")
	return expression(
	    land(equals(op(x_L, a), b), equals(op(a, x_R), b)), forall(a, b),
	    exists_unique(x_L, x_R))


def left_zero(algebraic_structure, op, absorbing_element):
	A = str(algebraic_structure)
	op = Operation(codomain=A, infix=op)
	annihalator = Operation(codomain=A, prefix=absorbing_element)
	a = Element(A)
	return expression(equals(op(annihalator(), a), annihalator()), forall(a))


def right_zero(algebraic_structure, op, absorbing_element):
	A = str(algebraic_structure)
	op = Operation(codomain=A, infix=op)
	annihalator = Operation(codomain=A, prefix=absorbing_element)
	a = Element(A)
	return expression(equals(op(a, annihalator()), annihalator()), forall(a))


def left_distributivity(algebraic_structure, distributor_op, distributee_op):
	A = str(algebraic_structure)
	distributor_op = Operation(codomain=A, infix=distributor_op)
	distributee_op = Operation(codomain=A, infix=distributee_op)
	a = [Element(A, k) for k in range(0, 3)]
	return expression(
	    equals(
	        distributor_op(a[0], expression(distributee_op(a[1], a[2]))),
	        distributee_op(
	            distributor_op(a[0], a[1]), distributor_op(a[0], a[2]))),
	    forall(*a))


def right_distributivity(algebraic_structure, distributor_op, distributee_op):
	A = str(algebraic_structure)
	distributor_op = Operation(codomain=A, infix=distributor_op)
	distributee_op = Operation(codomain=A, infix=distributee_op)
	a = [Element(A, k) for k in range(0, 3)]
	return expression(
	    equals(
	        distributor_op(expression(distributee_op(a[1], a[2])), a[0]),
	        distributee_op(
	            distributor_op(a[1], a[0]), distributor_op(a[2], a[0]))),
	    forall(*a))


def identities_different(algebraic_structure, *identities):
	A = str(algebraic_structure)
	identities = [
	    Operation(codomain=A, prefix=identity)() for identity in identities
	]
	return nequals(*identities)


def absorption_law(algebraic_structure, meet, join):
	A = str(algebraic_structure)
	meet = Operation(codomain=A, infix=meet)
	join = Operation(codomain=A, infix=join)
	a = [Element(A, k) for k in range(0, 2)]
	return expression(
	    equals(
	        meet(a[0], expression(join(a[0], a[1]))), a[0],
	        join(a[0], expression(meet(a[0], a[1])))), forall(*a))


def set_action(actor, actee, op):
	actor = str(actor)
	actee = str(actee)
	op = Operation(actor, actee, codomain=actee, infix=op)
	r = Element(actor)
	a = Element(actee)
	return expression(element_of(actee, op(r, a)), forall(r), forall(a))


if __name__ == "__main__":
	print(r"\\closure\\", closure("A", "+"))
	print(r"\\associative\\", associative("A", "+"))
	print(r"\\identity\\", identity_element("A", "+", "0"))
	print(r"\\inverse\\", inverse_element("A", "+", "0"))
	print(r"\\commutative\\", commutative("A", "+"))
	print(r"\\idempotent\\", idempotent("A", "+"))
	print(r"\\latin square\\", latin_square("A", "+"))
	print(r"\\left zero\\", left_zero("A", "\cdot", "0"))
	print(r"\\right zero\\", right_zero("A", "\cdot", "0"))
	print(r"\\left distributivity\\", left_distributivity("A", "\cdot", "+"))
	print(r"\\right distributivity\\", right_distributivity("A", "\cdot", "+"))
	print(r"\\identities different\\", identities_different("A", "0", "1"))
	print(r"\\absorption law\\", absorption_law("A", " \land ", " \lor "))
	print(r"\\set action\\", set_action("R", "A", " \cdot "))
