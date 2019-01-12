def underset(over, under):
    return r" {{ \underset{{ {under} }}{{ {over} }} }}".format(over=over, under=under)


def overset(over, under):
    return r" {{ \overset{{ {over} }}{{ {under} }} }}".format(over=over, under=under)


def subscript(over, under, right=True):
    return (
        r" {{ {over} }}_{{ {under} }} ".format(over=over, under=under)
        if right
        else r"{{ {{}}_{{ {under} }} {{ {over} }} }}".format(over=over, under=under)
    )


def underbrace(over, under):
    return underset(r"\underbrace{{ {over} }}".format(over=over), under)


class Element:
    def __init__(self, algebraic_structure, index=None, restriction=None):
        self.algebraic_element = underset(
            (
                str(algebraic_structure.lower())
                if index is None
                else subscript(str(algebraic_structure).lower(), str(index))
            ),
            str(algebraic_structure) if restriction is None else str(restriction),
        )

    def __str__(self) -> str:
        return self.algebraic_element


class Operation:
    def __init__(
        self, *domains, codomain=None, infix=None, prefix=None, postfix=None, owner=None
    ):
        def construct_symbol(*domains, owner=None, symbol=None):
            if symbol:
                if domains:
                    if owner:
                        return overset(
                            r" \times ".join(domains), underset(str(symbol), str(owner))
                        )
                    else:
                        return overset(r" \times ".join(domains), str(symbol))
                else:
                    if owner:
                        return underset(str(symbol), str(owner))
                    else:
                        return str(symbol)
            else:
                return r""

        self.codomain = str(codomain) if codomain else codomain
        self.domains = [str(domain) if domain else domain for domain in domains]
        self.owner = str(owner) if owner else owner
        self.prefix = construct_symbol(*domains, owner=self.owner, symbol=prefix)
        self.infix = construct_symbol(*domains, owner=self.owner, symbol=infix)
        self.postfix = construct_symbol(*domains, owner=self.owner, symbol=postfix)

    def __call__(self, *args: Element) -> str:
        over = self.prefix + self.infix.join([str(arg) for arg in args]) + self.postfix
        if self.codomain:
            return underbrace(over, self.codomain)
        else:
            return over


class Quantifier:
    def __init__(self, quantifier):
        self.quantifier = str(quantifier)

    def __call__(self, *args: Element):
        return r"".join(
            [r" " + self.quantifier + r" " + str(arg) + r" " for arg in args]
        )


forall = Quantifier(r" \forall ")
exists = Quantifier(r" \exists ")
exists_unique = Quantifier(r" !\exists ")
equals = Operation(infix=r" = ")
nequals = Operation(infix=r" \neq ")
land = Operation(infix=r" \land ")


def expression(expr, *quantifiers) -> str:
    return (
        r" \left( "
        + "".join([str(quantifier) for quantifier in quantifiers])
        + (r" \colon\quad " if quantifiers else r"")
        + str(expr)
        + r" \right) "
    )


def closure(algebraic_structure, op) -> str:
    A = str(algebraic_structure)
    op = Operation(codomain=A, infix=op)
    args = [Element(A, k) for k in range(0, 2)]
    return expression(op(*args), forall(*args))


def associative(algebraic_structure, op) -> str:
    A = str(algebraic_structure)
    op = Operation(codomain=A, infix=op)
    a = [Element(A, k) for k in range(0, 3)]
    return expression(
        equals(op(op(a[0], a[1]), a[2]), op(*a), op(a[0], op(a[1], a[2]))), forall(*a)
    )


def compatible_left_identity_element(
    id_algebraic_structure, algebraic_structure, op, id_op
):
    op = Operation(
        id_algebraic_structure,
        algebraic_structure,
        codomain=algebraic_structure,
        infix=op,
    )
    id_op = Operation(owner=id_algebraic_structure, prefix=id_op)
    a = Element(algebraic_structure)
    return expression(equals(op(id_op(), a), a), exists(id_op()), forall(a))


def compatible_right_identity_element(
    algebraic_structure, id_algebraic_structure, op, id_op
):
    op = Operation(
        algebraic_structure,
        id_algebraic_structure,
        codomain=algebraic_structure,
        infix=op,
    )
    id_op = Operation(owner=id_algebraic_structure, prefix=id_op)
    a = Element(algebraic_structure)
    return expression(equals(op(id_op(), a), a), exists(id_op()), forall(a))


def compatible_two_sided_identity_element(
    algebraic_structure, id_algebraic_structure, op_l, op_r, id_op
):
    op_l = Operation(
        id_algebraic_structure,
        algebraic_structure,
        codomain=algebraic_structure,
        infix=op_l,
    )
    op_r = Operation(
        algebraic_structure,
        id_algebraic_structure,
        codomain=algebraic_structure,
        infix=op_r,
    )
    id_op = Operation(owner=id_algebraic_structure, prefix=id_op)
    a = Element(algebraic_structure)
    return expression(
        equals(op_l(id_op(), a), a, op_r(a, id_op())),
        exists_unique(id_op())
        if algebraic_structure == id_algebraic_structure
        else exists(id_op()),  # not sure, but hunch
        forall(a),
    )


def inverse_element(algebraic_structure, op, id, restriction=None):
    A = str(algebraic_structure)
    op = Operation(codomain=A, infix=op)
    id = Operation(owner=A, prefix=id)
    a = [Element(A, k, restriction=restriction) for k in range(0, 2)]
    return expression(
        equals(op(a[0], a[1]), id(), op(a[1], a[0])),
        exists_unique(id()),
        forall(a[0]),
        exists(a[1]),
    )


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
        land(equals(op(x_L, a), b), equals(op(a, x_R), b)),
        forall(a, b),
        exists_unique(x_L, x_R),
    )


def left_zero(algebraic_structure, op, absorbing_element):
    A = str(algebraic_structure)
    op = Operation(codomain=A, infix=op)
    annihalator = Operation(owner=A, prefix=absorbing_element)
    a = Element(A)
    return expression(equals(op(annihalator(), a), annihalator()), forall(a))


def right_zero(algebraic_structure, op, absorbing_element):
    A = str(algebraic_structure)
    op = Operation(codomain=A, infix=op)
    annihalator = Operation(owner=A, prefix=absorbing_element)
    a = Element(A)
    return expression(equals(op(a, annihalator()), annihalator()), forall(a))


def left_distributivity(
    distributor_algebraic_structor,
    distributee_algebraic_structure,
    distributor_op,
    distributee_op,
):
    R = str(distributor_algebraic_structor)
    A = str(distributee_algebraic_structure)
    distributor_op = Operation(R, A, codomain=A, infix=distributor_op)
    distributee_op = Operation(A, A, codomain=A, infix=distributee_op)
    a = [Element(R, k) if k == 0 else Element(A, k) for k in range(0, 3)]
    return expression(
        equals(
            distributor_op(a[0], distributee_op(a[1], a[2])),
            distributee_op(distributor_op(a[0], a[1]), distributor_op(a[0], a[2])),
        ),
        forall(*a),
    )


def right_distributivity(
    distributor_algebraic_structor,
    distributee_algebraic_structure,
    distributor_op,
    distributee_op,
):
    R = str(distributor_algebraic_structor)
    A = str(distributee_algebraic_structure)
    distributor_op = Operation(A, R, codomain=A, infix=distributor_op)
    distributee_op = Operation(A, A, codomain=A, infix=distributee_op)
    a = [Element(R, k) if k == 0 else Element(A, k) for k in range(0, 3)]
    return expression(
        equals(
            distributor_op(distributee_op(a[1], a[2]), a[0]),
            distributee_op(distributor_op(a[1], a[0]), distributor_op(a[2], a[0])),
        ),
        forall(*a),
    )


def identities_different(algebraic_structure, *identities):
    A = str(algebraic_structure)
    identities = [Operation(owner=A, prefix=identity)() for identity in identities]
    return nequals(*identities)


def absorption_law(algebraic_structure, meet, join):
    A = str(algebraic_structure)
    meet = Operation(codomain=A, infix=meet)
    join = Operation(codomain=A, infix=join)
    a = [Element(A, k) for k in range(0, 2)]
    return expression(
        equals(meet(a[0], join(a[0], a[1])), a[0], join(a[0], meet(a[0], a[1]))),
        forall(*a),
    )


def set_action(actor, actee, op):
    actor = str(actor)
    actee = str(actee)
    op = Operation(actor, actee, codomain=actee, infix=op)
    r = Element(actor)
    a = Element(actee)
    return expression(op(r, a), forall(r), forall(a))


def compatible_3args(
    A, O=None, OO=None, OOO=None, P=None, PP=None, PP_P=None, P_PP=None
):
    """
	op01_2(*[op01(a0,     a1) ,a2	])
	=
	op0_12(*[     a0,op12(a1  ,a2)	]))
	"""
    a = [Element(A[k], k) for k in range(0, len(A))]
    if not O:
        O = A
    if not OO:
        OO = [None for k in range(len(A) - 1)]
    if not OOO:
        OOO = None
    if P:
        p = [Operation(A[k], codomain=O[k], prefix=P[k]) for k in range(len(P))]
    else:
        p = [lambda x: x, lambda x: x, lambda x: x]
    if PP:
        pp = [
            Operation(O[k], O[k + 1], codomain=OO[k], infix=PP[k])
            for k in range(len(PP))
        ]
    else:
        pp = [lambda x, y: (x, y), lambda x, y: (x, y)]
    if PP_P:
        pp_p = Operation(OO[0], O[2], codomain=OOO, infix=PP_P)
    else:
        pp_p = lambda x, y: r" ( {0} , {1} ) ".format(x, y)
    if P_PP:
        p_pp = Operation(O[0], OO[1], codomain=OOO, infix=P_PP)
    else:
        p_pp = lambda x, y: r" ( {0} , {1} ) ".format(x, y)
    return expression(
        equals(
            pp_p(pp[0](p[0](a[0]), p[1](a[1])), p[2](a[2])),
            p_pp(p[0](a[0]), pp[1](p[1](a[1]), p[2](a[2]))),
        ),
        forall(*a),
    )


if __name__ == "__main__":
    print(r"\\closure\\", closure("A", "+"))
    print(r"\\associative\\", associative("A", "+"))
    print(
        r"\\identity\\", compatible_two_sided_identity_element("A", "A", "+", "+", "0")
    )
    print(r"\\inverse\\", inverse_element("A", "+", "0"))
    print(r"\\commutative\\", commutative("A", "+"))
    print(r"\\idempotent\\", idempotent("A", "+"))
    print(r"\\latin square\\", latin_square("A", "+"))
    print(r"\\left zero\\", left_zero("A", "\cdot", "0"))
    print(r"\\right zero\\", right_zero("A", "\cdot", "0"))
    print(r"\\left distributivity\\", left_distributivity("A", "A", "\cdot", "+"))
    print(r"\\right distributivity\\", right_distributivity("A", "A", "\cdot", "+"))
    print(r"\\identities different\\", identities_different("A", "0", "1"))
    print(r"\\absorption law\\", absorption_law("A", " \land ", " \lor "))
    print(r"\\set action\\", set_action("R", "A", " \cdot "))
    print(r"\\left distributivity\\", left_distributivity("R", "A", "\cdot", "+"))
    print(r"\\right distributivity\\", right_distributivity("R", "A", "\cdot", "+"))
    print(
        r"\\compatability of scalar multiplication with ring multiplication\\",
        compatible_3args(
            (r"R", r"R", r"A"),
            OO=["R", "A"],
            OOO="A",
            PP=["\cdot", "\cdot"],
            P_PP="\cdot",
            PP_P="\cdot",
        ),
    )

    print(
        r"\\compatability of scalar multiplication with ring unit\\",
        compatible_left_identity_element("R", "A", "\cdot", "1"),
    )

