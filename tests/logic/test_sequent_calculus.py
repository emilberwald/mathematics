from mathematics.logic.sequent_calculus import (
    PredicateLogicSymbols,
    Term,
    Variable,
    FunctionSymbol,
    Formula,
    AtomicFormula,
    BindingFormula,
    LogicFormula,
    Sequent,
    InferenceRules,
)
from mathematics.tools.decorators import timeout
import pytest


class TestSequentCalculus:
    # @timeout(handler=lambda: pytest.skip("timeout"), seconds=1.0)
    def test_law_of_excluded_middle(self):
        LK = InferenceRules
        A = Formula("A")
        actual = LK.initiate(A)
        actual = LK.r_negation_l(actual)
        actual = LK.r_or_r_formula(actual, A)
        actual = LK.r_permute(actual, [1, 0])
        actual = LK.r_or_formula_r(actual, LogicFormula(PredicateLogicSymbols.NOT, (A,)))
        actual = LK.contract(actual)
        expected = Sequent(
            tuple(), (LogicFormula(PredicateLogicSymbols.OR, (A, LogicFormula(PredicateLogicSymbols.NOT, (A,))),),),
        )
        assert actual == expected

    def test_2(self):
        LK = InferenceRules
        x = Variable("x")
        y = Variable("y")
        p = AtomicFormula("p", (x, y,))
        actual = LK.initiate(p)
        actual = LK.l_forall(actual, x)
        actual = LK.r_exists(actual, y)
        actual = LK.l_exists(actual, y)
        actual = LK.r_forall(actual, x)
        expected = Sequent(
            (
                BindingFormula(
                    PredicateLogicSymbols.EXISTS, y, (BindingFormula(PredicateLogicSymbols.FORALL, x, (p,)),),
                ),
            ),
            (
                BindingFormula(
                    PredicateLogicSymbols.FORALL, x, (BindingFormula(PredicateLogicSymbols.EXISTS, y, (p,)),),
                ),
            ),
        )
        assert actual == expected
