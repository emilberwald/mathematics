import networkx
import multiprocessing
import io
import sympy.printing
import sympy
import base64
import tempfile
import pathlib
import pylatexenc.latex2text
import enum
import subprocess
import graphviz


def underset(over, under):
	return r" {{ \underset{{ {under} }}{{ {over} }} }} ".format(
	    over=over, under=under)


def overset(over, under):
	return r" {{ \overset{{ {over} }}{{ {under} }} }} ".format(
	    over=over, under=under)


def underbrace(over, under):
	return underset(r" \underbrace{{ {over} }} ".format(over=over), under)


def overbrace(over, under):
	return r" {{ \overbrace{{ {over} }}{{ {under} }} }} ".format(
	    over=over, under=under)


def subscript(subscript):
	return r" {{}}_{{ {subscript} }} ".format(subscript=subscript)


def superscript(superscript):
	return r" {{}}^{{ {superscript} }} ".format(superscript=superscript)


class LatexNode():
	"""
	Convert from latex code to other formats.
	"""

	@enum.unique
	class Presentation(enum.Enum):
		TEXT = enum.auto(),
		UNICODE_APPROXIMATION = enum.auto(),
		HTML_IMG_PNG = enum.auto(),
		HTML_IMG_PNG_EMBEDDED = enum.auto(),
		URL_IMG_PNG = enum.auto(),

	class Folder(enum.Enum):
		TMP = enum.auto(),
		CWD = enum.auto(),

	presentation = Presentation.TEXT
	folder = Folder.CWD

	def __init__(self, latex):
		self.latex = str(latex)

	def as_default(self):
		if self.presentation and self.folder:
			if self.presentation == LatexNode.Presentation.TEXT:
				return self.latex
			elif self.presentation == LatexNode.Presentation.UNICODE_APPROXIMATION:
				return self.as_unicode_approximation()
			elif self.presentation == LatexNode.Presentation.HTML_IMG_PNG:
				if self.folder == LatexNode.Folder.CWD:
					return self.as_html_img_url_png_tmp(cwd=True)
				elif LatexNode.Folder.TMP == self.folder:
					return self.as_html_img_url_png_tmp(cwd=False)
				else:
					raise NotImplementedError()
			elif self.presentation == LatexNode.Presentation.URL_IMG_PNG:
				if self.folder == LatexNode.Folder.CWD:
					return self.as_url_png_tmp(cwd=True)
				elif self.folder == LatexNode.Folder.TMP:
					return self.as_url_png_tmp(cwd=False)
				else:
					raise NotImplementedError()
			elif self.presentation == LatexNode.Presentation.HTML_IMG_PNG_EMBEDDED:
				return self.as_html_img_embedded_png()
			else:
				raise NotImplementedError()
		else:
			raise NotImplementedError()

	def as_unicode_approximation(self):
		return pylatexenc.latex2text.LatexNodes2Text().latex_to_text(
		    self.latex)

	def as_png(self) -> bytes:
		buffer = io.BytesIO()
		sympy.printing.preview(
		    self.latex,
		    output='png',
		    euler=False,
		    viewer='BytesIO',
		    outputbuffer=buffer)
		latex_png_data = buffer.getvalue()
		buffer.close()
		return latex_png_data

	def as_png_b64(self) -> str:
		return base64.b64encode(self.as_png()).decode()

	def as_html_img_embedded_png(self) -> str:
		latex_png_b64 = self.as_png_b64()
		return '<img src="data:image/png;base64,' + latex_png_b64 + '"/>'

	def as_url_png(self, path) -> pathlib.Path:
		sympy.printing.preview(
		    self.latex,
		    output='png',
		    euler=False,
		    viewer='file',
		    filename=path)
		return pathlib.Path(path)

	def as_url_png_tmp(self, cwd=False) -> pathlib.Path:
		if cwd:
			f = tempfile.NamedTemporaryFile(
			    suffix=".png", delete=False, dir=pathlib.Path.cwd())
		else:
			f = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
		f.close()
		return self.as_url_png(f.name)

	def as_html_img_url_png_tmp(self, cwd=False) -> str:
		png_filename = self.as_url_png_tmp(cwd=cwd)
		return '<img src="' + png_filename + '"/>'

	def as_xelatex_pdf_url(self) -> pathlib.Path:
		with tempfile.NamedTemporaryFile(suffix=".tex") as f:
			f.write(self.latex)
			f.close()
			subprocess.call([
			    "xelatex", "--output-directory", f.parent,
			    "-interaction=nonstopmode", f.name
			])
			return pathlib.Path(f.name).joinpath(".pdf")


def get_roots(graph):
	return [node for node, degree in graph.in_degree() if degree == 0]


class Operation:
	identifier = multiprocessing.Value('i', 0)

	@staticmethod
	def get_fresh_identifier():
		with Operation.identifier.get_lock():
			Operation.identifier.value += 1
			return Operation.identifier.value

	def __init__(self,
	             *domains,
	             codomain=None,
	             symbol=None,
	             algebraic_structure=None,
	             id=None):
		self.domains = domains
		self.codomain = codomain
		self.algebraic_structure = algebraic_structure
		self.symbol = symbol
		self.id = id

	def __str__(self):
		symbol = str(self.symbol) if self.symbol else r""
		if self.algebraic_structure:
			symbol = underset(symbol, str(self.algebraic_structure))
		if self.domains and self.codomain:
			symbol = overset(
			    r"\rightarrow ".join([
			        r" \times ".join([str(domain) for domain in self.domains]),
			        str(self.codomain)
			    ]), symbol)
		elif self.domains:
			symbol = overset(
			    r" \times ".join([str(domain)
			                      for domain in self.domains]), symbol)
		elif self.codomain:
			symbol = overset(r"\rightarrow " + str(self.codomain), symbol)
		return symbol

	def __call__(self, *args):
		graph = networkx.MultiDiGraph()
		op = Operation(
		    *self.domains,
		    codomain=self.codomain,
		    symbol=self.symbol,
		    algebraic_structure=self.algebraic_structure,
		    id=Operation.get_fresh_identifier())
		graph.add_node(op)
		for arg in args:
			if isinstance(arg, networkx.Graph):
				graph = networkx.algorithms.compose(graph, arg)
				for root in get_roots(arg):
					graph.add_edge(op, root)
			else:
				graph.add_node(arg)
				graph.add_edge(op, arg)
		return graph


class LatexWalker:
	class Traversal(enum.Enum):
		PREFIX = 1,
		INFIX = 2,
		POSTFIX = 3,

	def __init__(self, traversal=Traversal.INFIX):
		self.traversal = traversal

	def __call__(self,
	             graph: networkx.MultiDiGraph,
	             root_join="\quad ",
	             fix_join="\quad , \quad "):
		def infix(*successors, root=" ", graph=networkx.MultiDiGraph()):
			if successors:
				if isinstance(root, Operation) and root.codomain:
					over = LatexNode(root).as_default().join([
					    infix(
					        *graph.successors(successor),
					        root=successor,
					        graph=graph) for successor in successors
					])
					under = LatexNode(root.codomain).as_default()
					return underbrace(over, under)
				else:
					return LatexNode(root).as_default().join([
					    infix(
					        *graph.succesors(successor),
					        root=successor,
					        graph=graph) for successor in successors
					])
			else:
				return LatexNode(root).as_default()

		roots = get_roots(graph)
		if LatexNode.presentation in (
		    LatexNode.Presentation.TEXT,
		    LatexNode.Presentation.UNICODE_APPROXIMATION):
			if self.traversal == LatexWalker.Traversal.INFIX:
				return root_join.join([
				    infix(*graph.successors(root), root=root, graph=graph)
				    for root in roots
				])
			elif self.traversal == LatexWalker.Traversal.PREFIX:
				#TODO: this method does not work well when there are nodes connected to several other nodes
				return root_join.join([
				    fix_join.join([
				        LatexNode(node).as_default()
				        for node in networkx.algorithms.dfs_preorder_nodes(
				            graph, root)
				    ]) for root in roots
				])
			elif self.traversal == LatexWalker.Traversal.POSTFIX:
				#TODO: this method does not work well when there are nodes connected to several other nodes
				return root_join.join([
				    fix_join.join([
				        LatexNode(node).as_default()
				        for node in networkx.algorithms.dfs_postorder_nodes(
				            graph, root)
				    ]) for root in roots
				])
			else:
				raise NotImplementedError()
		elif LatexNode.presentation in (LatexNode.Presentation.URL_IMG_PNG, ):
			remove_us = list()
			for node in graph.nodes():
				image = LatexNode("$$" + str(node) + "$$").as_default()
				graph.node[node]["label"] = ""
				graph.node[node]['image'] = str(image.name)
				graph.node[node]['imagepath'] = str(image.parent)
				remove_us.append(image)
			graph = networkx.relabel.convert_node_labels_to_integers(graph)
			if LatexNode.folder == LatexNode.Folder.CWD:
				f = tempfile.NamedTemporaryFile(
				    suffix=".dot", delete=False, dir=pathlib.Path.cwd())
				f.close()
				networkx.drawing.nx_pydot.write_dot(graph, f.name)
				result = pathlib.Path(graphviz.render('dot', 'png', f.name))
				remove_us.append(pathlib.Path(f.name))
			elif LatexNode.folder == LatexNode.Folder.TMP:
				f = tempfile.NamedTemporaryFile(suffix=".dot", delete=False)
				f.close()
				networkx.drawing.nx_pydot.write_dot(graph, f.name)
				result = pathlib.Path(graphviz.render('dot', 'png', f.name))
				remove_us.append(pathlib.Path(f.name))
			else:
				return NotImplementedError()
			for remove_me in remove_us:
				remove_me.unlink()
			return result
		else:
			#TODO: add possiblity to return a html page ?
			raise NotImplementedError()