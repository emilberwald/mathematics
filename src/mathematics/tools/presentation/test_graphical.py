import sys
import unittest
from parameterized import parameterized
from .graphical import *
from ..testing import user_verdict

#	def exec_(self):
#		return QDialog.exec_(self)


class TestLatexWalker(unittest.TestCase):
	@parameterized.expand([(traversal, presentation)
	                       for traversal in list(LatexWalker.Traversal)
	                       for presentation in
	                       (LatexNode.Presentation.UNICODE_APPROXIMATION, )])
	def test_LatexWalker_unicode(self, traversal, presentation):
		LatexNode.presentation = presentation
		V = "V"
		R = "R"
		A = "A"
		plus = Operation(A, A, codomain=A, symbol="+", algebraic_structure=A)
		scalprod = Operation(
		    R, A, codomain=A, symbol=" \cdot ", algebraic_structure=V)
		result_graph = plus(scalprod("r_0", "a_0"), scalprod("r_1", "a_1"))
		result = LatexWalker(traversal)(result_graph)

		verdict = user_verdict.get_textverdict(
		    sys._getframe().f_code.co_name, result, timeout=60)
		self.assertTrue(verdict, msg=result)

	@parameterized.expand([(traversal, presentation)
	                       for traversal in list(LatexWalker.Traversal) for
	                       presentation in (LatexNode.Presentation.URL_IMG_PNG,
	                                        LatexNode.Presentation.TEXT)])
	def test_LatexWalker_image(self, traversal, presentation):
		V = "V"
		R = "R"
		A = "A"
		plus = Operation(A, A, codomain=A, symbol="+", algebraic_structure=A)
		scalprod = Operation(
		    R, A, codomain=A, symbol=" \cdot ", algebraic_structure=V)
		result_graph = plus(scalprod("r", "a_0"), scalprod("r", "a_1"))

		LatexNode.presentation = presentation
		result_text = LatexWalker(traversal)(result_graph)
		if presentation == LatexNode.Presentation.TEXT:
			LatexNode.presentation = LatexNode.Presentation.URL_IMG_PNG
			result_image = LatexNode("$$" + result_text + "$$").as_default()
			verdict = user_verdict.get_mediaverdict(
			    sys._getframe().f_code.co_name, result_image, timeout=60)
			self.assertTrue(verdict)
			result_image.unlink()
		verdict = user_verdict.get_textverdict(
		    sys._getframe().f_code.co_name, result_text, timeout=60)
		self.assertTrue(verdict, msg=result_text)


if __name__ == '__main__':
	unittest.main()