import sys

import pytest

from .graphical import *
from ..testing import user_verdict, name_func


# 	def exec_(self):
# 		return QDialog.exec_(self)


class TestLatexWalkerText:
    @pytest.mark.parametrize(
        "traversal,presentation",
        [
            (traversal, presentation)
            for traversal in list(LatexWalker.Traversal)
            for presentation in (LatexNode.Presentation.UNICODE_APPROXIMATION,)
        ],
        ids=name_func,
    )
    @pytest.mark.slow
    def test_LatexWalker_unicode(self, traversal, presentation):
        LatexNode.presentation = presentation
        vector_space = "V"
        real_values = "R"
        abelian_group = "A"
        plus = Operation(
            abelian_group,
            abelian_group,
            codomain=abelian_group,
            symbol="+",
            algebraic_structure=abelian_group,
        )
        scalprod = Operation(
            real_values,
            abelian_group,
            codomain=abelian_group,
            symbol=r" \cdot ",
            algebraic_structure=vector_space,
        )
        result_graph = plus(scalprod("r_0", "a_0"), scalprod("r_1", "a_1"))
        result = LatexWalker(traversal)(result_graph)

        verdict = user_verdict.get_textverdict(
            sys._getframe().f_code.co_name, result, timeout=10
        )
        assert verdict


class TestLatexWalkerGraphics:
    @pytest.mark.parametrize(
        "traversal,presentation",
        [
            (traversal, presentation)
            for traversal in list(LatexWalker.Traversal)
            for presentation in (
                LatexNode.Presentation.URL_IMG_PNG,
                LatexNode.Presentation.TEXT,
            )
        ],
        ids=name_func,
    )
    @pytest.mark.slow
    def test_latexwalker_image(self, traversal, presentation):
        V = r"\mathbb{V}"
        R = r"\mathbb{R}"
        A = r"\mathbb{A}"

        forall = variable_binding_operator(symbol=r"\forall")
        plus = Operation(A, A, codomain=A, symbol="+", algebraic_structure=A)
        scalprod = Operation(R, A, codomain=A, symbol=r" \cdot ", algebraic_structure=V)
        result_graph = forall(
            "r", "a_0", "a_1", plus(scalprod("r", "a_0"), scalprod("r", "a_1"))
        )

        LatexNode.presentation = presentation
        if presentation in (
            LatexNode.Presentation.TEXT,
            LatexNode.Presentation.UNICODE_APPROXIMATION,
        ):
            result_text = LatexWalker(traversal)(result_graph)
            LatexNode.presentation = LatexNode.Presentation.URL_IMG_PNG
            result_image = LatexNode("$$" + result_text + "$$").as_default()
            verdict = user_verdict.get_mediaverdict(
                sys._getframe().f_code.co_name, result_image, timeout=10
            )
            result_image.unlink()
            assert verdict
        else:
            result_image = LatexWalker(traversal)(result_graph)
            verdict = user_verdict.get_mediaverdict(
                sys._getframe().f_code.co_name, result_image, timeout=10
            )
            result_image.unlink()
            assert verdict
