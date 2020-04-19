import dataclasses
from typing import Any, Tuple


class PredicateLogicSymbols:
    NOT = "¬"
    AND = "∧"
    OR = "∨"
    FORALL = "∀"
    EXISTS = "∃"


@dataclasses.dataclass(frozen=True)
class Term:
    pass


@dataclasses.dataclass(frozen=True)
class Variable(Term):
    identifier: str


@dataclasses.dataclass(frozen=True)
class FunctionSymbol(Term):
    identifier: str
    arguments: Tuple[Term]

    def __str__(self):
        return f"{self.identifier}({','.join([str(arg) for arg in self.arguments])})"


@dataclasses.dataclass(frozen=True)
class Formula:
    identifier: str

    def __str__(self):
        return self.identifier

    def substitute(self, original, substitute):
        return self

    def is_free(self, term):
        return True


@dataclasses.dataclass(frozen=True)
class AtomicFormula(Formula):
    identifier: str
    terms: Tuple[Term, ...]

    def __str__(self):
        return f"{self.identifier}[{','.join([str(arg) for arg in self.terms])}]"

    def substitute(self, original, substitute):
        return dataclasses.replace(self, terms=[substitute if term == original else term for term in self.terms])


@dataclasses.dataclass(frozen=True)
class LogicFormula(Formula):
    identifier: str
    formulas: Tuple[Formula, ...]

    def __str__(self):
        return f"{self.identifier}⟦{','.join([str(arg) for arg in self.formulas])}⟧"

    def substitute(self, original, substitute):
        return dataclasses.replace(
            self, formulas=[formula.substitute(original, substitute) for formula in self.formulas]
        )

    def is_free(self, term):
        return all(wff.is_free(term) for wff in self.formulas)


@dataclasses.dataclass(frozen=True)
class BindingFormula(Formula):
    identifier: str
    binding: Variable
    formulas: Tuple[Formula, ...]

    def substitute(self, original, substitute):
        if self.binding == original:
            raise ValueError("substitute N/A")

        return dataclasses.replace(
            self, formulas=[formula.substitute(original, substitute) for formula in self.formulas]
        )

    def is_free(self, term):
        return all(wff.is_free(term) for wff in self.formulas)

    def __str__(self):
        return f"{self.identifier}⟨{self.binding}|{','.join([str(arg) for arg in self.formulas])}⟩"


@dataclasses.dataclass(frozen=True)
class Sequent:
    antecedents: Tuple[Formula, ...]
    consequents: Tuple[Formula, ...]

    def __str__(self):
        return (
            ",".join(["'" + str(wff) + "'" for wff in self.antecedents])
            + "⊢"
            + ",".join(["'" + str(wff) + "'" for wff in self.consequents])
        )


class InferenceRules:
    @staticmethod
    def initiate(formula: Formula):
        return Sequent((formula,), (formula,))

    @staticmethod
    def cut(lhs: Sequent, rhs: Sequent):
        common = set(lhs.consequents) & set(rhs.antecedents)
        if not common:
            raise ValueError(f"Cut({lhs,rhs}) N/A")

        return Sequent(
            antecedents=lhs.antecedents + tuple(wff for wff in rhs.antecedents if wff not in common),
            consequents=tuple(wff for wff in lhs.consequents if wff not in common) + rhs.consequents,
        )

    @staticmethod
    def l_weakening(sequent: Sequent, wff: Formula):
        return Sequent(antecedents=sequent.antecedents + (wff,), consequents=sequent.consequents)

    @staticmethod
    def r_weakening(sequent: Sequent, wff: Formula):
        return Sequent(antecedents=sequent.antecedents, consequents=(wff,) + sequent.consequents)

    @staticmethod
    def contract(sequent: Sequent):
        return Sequent(tuple(sorted(set(sequent.antecedents))), tuple(sorted(set(sequent.consequents))))

    @staticmethod
    def l_permute(sequent: Sequent, permutation):
        if len(permutation) != len(set(permutation)) or len(set(permutation)) != len(sequent.antecedents):
            raise ValueError(f"PermuteL({sequent},{permutation}) N/A")

        return Sequent(tuple(sequent.antecedents[i] for i in permutation), sequent.consequents)

    @staticmethod
    def r_permute(sequent: Sequent, permutation):
        if len(permutation) != len(set(permutation)) or len(set(permutation)) != len(sequent.consequents):
            raise ValueError(f"PermuteL({sequent},{permutation}) N/A")

        return Sequent(sequent.antecedents, tuple(sequent.consequents[i] for i in permutation))

    @staticmethod
    def l_and_l_formula(sequent: Sequent, formula: Formula):
        """∧L1"""
        return Sequent(
            antecedents=tuple(sequent.antecedents[:-1]) + (LogicFormula("∧", (sequent.antecedents[-1], formula,)),),
            consequents=sequent.consequents,
        )

    @staticmethod
    def l_and_formula_l(sequent: Sequent, formula: Formula):
        """∧L2"""
        return Sequent(
            antecedents=tuple(sequent.antecedents[:-1]) + (LogicFormula("∧", (formula, sequent.antecedents[-1],)),),
            consequents=sequent.consequents,
        )

    @staticmethod
    def r_or_r_formula(sequent: Sequent, formula: Formula):
        """∨R1"""
        return Sequent(
            antecedents=sequent.antecedents,
            consequents=(LogicFormula("∨", (formula, sequent.consequents[0],)),) + tuple(sequent.consequents[1:]),
        )

    @staticmethod
    def r_or_formula_r(sequent: Sequent, formula: Formula):
        """∨R1"""
        return Sequent(
            antecedents=sequent.antecedents,
            consequents=(LogicFormula("∨", (sequent.consequents[0], formula,)),) + tuple(sequent.consequents[1:]),
        )

    @staticmethod
    def l_or_ll_rl(lhs: Sequent, rhs: Sequent):
        """∨L"""
        return Sequent(
            antecedents=tuple(lhs.antecedents[:-1])
            + tuple(rhs.antecedents[:-1])
            + (LogicFormula("∨", (lhs.antecedents[-1], rhs.antecedents[-1],)),),
            consequents=lhs.consequents + rhs.consequents,
        )

    @staticmethod
    def r_and_lr_rr(lhs: Sequent, rhs: Sequent):
        """∧R"""
        return Sequent(
            antecedents=lhs.antecedents + rhs.antecedents,
            consequents=(LogicFormula("∧", (lhs.consequents[0], rhs.consequents[0],)),)
            + tuple(lhs.consequents[1:])
            + tuple(rhs.consequents[1:]),
        )

    @staticmethod
    def l_conditional_lr_rr(lhs: Sequent, rhs: Sequent):
        """→L"""
        return Sequent(
            antecedents=tuple(lhs.antecedents[:-1])
            + tuple(rhs.antecedents[:-1])
            + (LogicFormula("→", (lhs.antecedents[-1], rhs.antecedents[-1],)),),
            consequents=lhs.consequents + rhs.consequents,
        )

    @staticmethod
    def r_conditional_l_r(sequent: Sequent):
        """→R"""
        return Sequent(
            antecedents=tuple(sequent.antecedents[:-1]),
            consequents=(LogicFormula("→", (sequent.antecedents[-1], sequent.consequents[0],)),)
            + tuple(sequent.consequents[1:]),
        )

    @staticmethod
    def l_negation_r(sequent: Sequent):
        """
            ¬L
            (crosses side right -> left)
        """
        return Sequent(
            antecedents=sequent.antecedents + (LogicFormula("¬", (sequent.consequents[0],)),),
            consequents=tuple(sequent.consequents[1:]),
        )

    @staticmethod
    def r_negation_l(sequent: Sequent):
        """
            ¬R
            (crosses side left -> right)
        """
        return Sequent(
            antecedents=tuple(sequent.antecedents[:-1]),
            consequents=(LogicFormula("¬", (sequent.antecedents[-1],)),) + sequent.consequents,
        )

    @staticmethod
    def substitution(sequent: Sequent, original: Term, substitute: Term):
        """Substitution Lemma"""
        return Sequent(
            antecedents=tuple(wff.substitute(original, substitute) for wff in sequent.antecedents),
            consequents=tuple(wff.substitute(original, substitute) for wff in sequent.consequents),
        )

    @staticmethod
    def l_binding(sequent: Sequent, symbol: str, variable: Variable):
        # TODO:
        # Is this correct?
        # Why is the substitution on the upper part in the inference rules?
        if not sequent.antecedents[-1].is_free(variable):
            raise ValueError(f"BindingL({sequent},{symbol},{variable}) N/A")

        return Sequent(
            antecedents=tuple(sequent.antecedents[:-1])
            + (BindingFormula(symbol, variable, (sequent.antecedents[-1],)),),
            consequents=sequent.consequents,
        )

    @staticmethod
    def r_binding(sequent: Sequent, symbol: str, variable: Variable):
        # TODO:
        # Is this correct?
        # Why is the substitution on the upper part in the inference rules?
        if not sequent.consequents[0].is_free(variable):
            raise ValueError(f"BindingR({sequent},{symbol},{variable}) N/A")

        return Sequent(
            antecedents=sequent.antecedents,
            consequents=(BindingFormula(symbol, variable, (sequent.consequents[0],)),) + tuple(sequent.consequents[1:]),
        )

    @staticmethod
    def l_existential_generalisation(sequent: Sequent, variable: Variable):
        """∃L"""
        return InferenceRules.l_binding(sequent, "∃", variable)

    @staticmethod
    def l_universal_generalisation(sequent: Sequent, variable: Variable):
        """∀L"""
        return InferenceRules.l_binding(sequent, "∀", variable)

    @staticmethod
    def r_existential_generalisation(sequent: Sequent, variable: Variable):
        """∃R"""
        return InferenceRules.r_binding(sequent, "∃", variable)

    @staticmethod
    def r_universal_generalisation(sequent: Sequent, variable: Variable):
        """∀R"""
        return InferenceRules.r_binding(sequent, "∀", variable)
