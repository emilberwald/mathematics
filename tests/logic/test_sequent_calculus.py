from mathematics.logic.sequent_calculus import Sequent, InferenceRules, Formula, LogicFormula, PredicateLogicSymbols
from mathematics.tools.decorators import timeout
import pytest


class TestSequentCalculus:
    # @timeout(handler=lambda: pytest.skip("timeout"), seconds=1.0)
    def test_law_of_excluded_middle(self):
        LK = InferenceRules
        A = Formula("A")
        step = LK.initiate(A)
        step = LK.r_negation_l(step)
        step = LK.r_or_r_formula(step, A)
        step = LK.r_permute(step, [1, 0])
        step = LK.r_or_formula_r(step, LogicFormula(PredicateLogicSymbols.NOT, (A,)))
        step = LK.contract(step)
        assert step == (
            Sequent(
                tuple(), (LogicFormula(PredicateLogicSymbols.OR, (A, LogicFormula(PredicateLogicSymbols.NOT, (A,)))),)
            )
        )
