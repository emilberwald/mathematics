"""
This module aims to aid in writing mathematics, keeping track of the
domain and codomain of operators
"""

import base64
import enum
import io
import itertools
import multiprocessing
import pathlib
import subprocess
import tempfile

import graphviz
import networkx
import pylatexenc.latex2text
import sympy
import sympy.printing


def underset(over, under):
    return f" {{ \\underset{{ {under} }}{{ {over} }} }} "


def overset(over, under):
    return f" {{ \\overset{{ {over} }}{{ {under} }} }} "


def underbrace(over, under):
    return underset(f" \\underbrace{{ {over} }} ", under)


def overbrace(over, under):
    return f" {{ \\overbrace{{ {over} }}{{ {under} }} }} "


def subscript(subscript):
    return f" {{}}_{{ {subscript} }}"


def superscript(superscript):
    return f" {{}}^{{ {superscript} }}"


class LatexNode:
    """
	Convert from latex code to other formats.
	"""

    @enum.unique
    class Presentation(enum.Enum):
        TEXT = (enum.auto(),)
        UNICODE_APPROXIMATION = (enum.auto(),)
        HTML_IMG_PNG = (enum.auto(),)
        HTML_IMG_PNG_EMBEDDED = (enum.auto(),)
        URL_IMG_PNG = (enum.auto(),)

    class Folder(enum.Enum):
        TMP = (enum.auto(),)
        CWD = (enum.auto(),)

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
        return pylatexenc.latex2text.LatexNodes2Text().latex_to_text(self.latex)

    def as_png(self) -> bytes:
        buffer = io.BytesIO()
        sympy.printing.preview(self.latex, output="png", euler=False, viewer="BytesIO", outputbuffer=buffer)
        latex_png_data = buffer.getvalue()
        buffer.close()
        return latex_png_data

    def as_png_b64(self) -> str:
        return base64.b64encode(self.as_png()).decode()

    def as_html_img_embedded_png(self) -> str:
        latex_png_b64 = self.as_png_b64()
        return '<img src="data:image/png;base64,' + latex_png_b64 + '"/>'

    def as_url_png(self, path) -> pathlib.Path:
        sympy.printing.preview(self.latex, output="png", euler=False, viewer="file", filename=path)
        return pathlib.Path(path)

    def as_url_png_tmp(self, cwd=False) -> pathlib.Path:
        if cwd:
            file = tempfile.NamedTemporaryFile(suffix=".png", delete=False, dir=pathlib.Path.cwd())
        else:
            file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        file.close()
        return self.as_url_png(file.name)

    def as_html_img_url_png_tmp(self, cwd=False) -> str:
        png_filename = self.as_url_png_tmp(cwd=cwd)
        return '<img src="' + str(png_filename) + '"/>'

    def as_xelatex_pdf_url(self) -> pathlib.Path:
        with tempfile.NamedTemporaryFile(suffix=".tex") as file:
            file.write(self.latex)
            file.close()
            subprocess.call(
                ["xelatex", "--output-directory", file.parent, "-interaction=nonstopmode", file.name,]
            )
            return pathlib.Path(file.name).joinpath(".pdf")


def get_roots(graph):
    return [node for node, degree in graph.in_degree() if degree == 0]


class Operation:
    identifier = multiprocessing.Value("i", 0)

    @staticmethod
    def get_fresh_identifier():
        with Operation.identifier.get_lock():
            Operation.identifier.value += 1
            return Operation.identifier.value

    def __init__(
        self, *domains, codomain=None, symbol=None, algebraic_structure=None, identity=None,
    ):
        self.domains = domains
        self.codomain = codomain
        self.algebraic_structure = algebraic_structure
        self.symbol = symbol
        self.identity = identity

    def __str__(self):
        def cartesian_product(*domains):
            return r" \times ".join([str(k) + superscript(len(list(g))) for k, g in itertools.groupby(domains)])

        symbol = str(self.symbol) if self.symbol else r""
        if self.algebraic_structure:
            symbol = underset(symbol, str(self.algebraic_structure))
        if self.domains and self.codomain:
            symbol = overset(r"\rightarrow ".join([cartesian_product(*self.domains), str(self.codomain)]), symbol,)
        elif self.domains:
            symbol = overset(cartesian_product(*self.domains), symbol)
        elif self.codomain:
            symbol = overset(r"\rightarrow " + str(self.codomain), symbol)
        return symbol

    def __call__(self, *args):
        graph = networkx.MultiDiGraph()
        operation = Operation(
            *self.domains,
            codomain=self.codomain,
            symbol=self.symbol,
            algebraic_structure=self.algebraic_structure,
            identity=Operation.get_fresh_identifier(),
        )
        graph.add_node(operation)
        for arg in args:
            if isinstance(arg, networkx.MultiDiGraph):
                graph = networkx.algorithms.compose(graph, arg)
                for root in get_roots(arg):
                    graph.add_edge(operation, root)
            else:
                graph.add_node(arg)
                graph.add_edge(operation, arg)
        return graph


def variable_binding_operator(symbol=None, variable=r"\text{t}", formula=r"\text{f}"):
    def bind_arguments(*bound):
        # the domain is a variable which is a kind of term, but v is so overused so used t instead.
        domains = [variable] * len(bound[:-1])
        if isinstance(bound[-1], networkx.Graph):
            roots = get_roots(bound[-1])
            if roots and len(roots) == 1 and isinstance(roots[-1], Operation):
                domains.append(roots[-1].codomain)
            else:
                domains.append(formula)
        else:
            domains.append(formula + "?")
        return Operation(*domains, codomain=formula, symbol=symbol)(*bound)

    return bind_arguments


class LatexWalker:
    class Traversal(enum.Enum):
        PREFIX = (1,)
        INFIX = (2,)
        POSTFIX = (3,)

    def __init__(self, traversal=Traversal.INFIX):
        self.traversal = traversal

    def __call__(self, graph: networkx.MultiDiGraph, root_join=r"\quad ", fix_join=r"\qquad "):
        def infix(*successors, root="", graph=networkx.MultiDiGraph()):
            if successors:
                if isinstance(root, Operation) and root.codomain:
                    if root.domains and len(root.domains) != 2:
                        # Special case (infix looks really bad when it does not have arity 2 and
                        # the domains look wrong)
                        over = (
                            r" \left( "
                            + LatexNode(root).as_default()
                            + r" \colon\quad "
                            + " , ".join(
                                [
                                    infix(*graph.successors(successor), root=successor, graph=graph,)
                                    for successor in successors
                                ]
                            )
                            + r" \right) "
                        )
                    else:
                        over = (
                            LatexNode(root)
                            .as_default()
                            .join(
                                [
                                    infix(*graph.successors(successor), root=successor, graph=graph,)
                                    for successor in successors
                                ]
                            )
                        )
                    under = LatexNode(root.codomain).as_default()
                    return underbrace(over, under)
                else:
                    return (
                        LatexNode(root)
                        .as_default()
                        .join(
                            [
                                infix(*graph.succesors(successor), root=successor, graph=graph,)
                                for successor in successors
                            ]
                        )
                    )
            else:
                return LatexNode(root).as_default()

        def prefix(*successors, root="", fix_join="", graph=networkx.MultiDiGraph()):
            if successors:
                if isinstance(root, Operation) and root.codomain:
                    over = fix_join.join(
                        [LatexNode(root).as_default()]
                        + [
                            prefix(*graph.successors(successor), root=successor, fix_join=fix_join, graph=graph,)
                            for successor in successors
                        ]
                    )
                    under = LatexNode(root.codomain).as_default()
                    return underbrace(over, under)
                else:
                    return fix_join.join(
                        [LatexNode(root).as_default()]
                        + [
                            prefix(*graph.successors(successor), root=successor, fix_join=fix_join, graph=graph,)
                            for successor in successors
                        ]
                    )
            else:
                return LatexNode(root).as_default()

        def postfix(*successors, root="", fix_join="", graph=networkx.MultiDiGraph()):
            if successors:
                if isinstance(root, Operation) and root.codomain:
                    over = fix_join.join(
                        [
                            postfix(*graph.successors(successor), root=successor, fix_join=fix_join, graph=graph,)
                            for successor in successors
                        ]
                        + [LatexNode(root).as_default()]
                    )
                    under = LatexNode(root.codomain).as_default()
                    return underbrace(over, under)
                else:
                    return fix_join.join(
                        [
                            postfix(*graph.successors(successor), root=successor, fix_join=fix_join, graph=graph,)
                            for successor in successors
                        ]
                        + [LatexNode(root).as_default()]
                    )
            else:
                return LatexNode(root).as_default()

        roots = get_roots(graph)
        if LatexNode.presentation in (LatexNode.Presentation.TEXT, LatexNode.Presentation.UNICODE_APPROXIMATION,):
            if self.traversal == LatexWalker.Traversal.INFIX:
                return root_join.join([infix(*graph.successors(root), root=root, graph=graph) for root in roots])
            elif self.traversal == LatexWalker.Traversal.PREFIX:
                return root_join.join(
                    [prefix(*graph.successors(root), root=root, fix_join=fix_join, graph=graph,) for root in roots]
                )
            elif self.traversal == LatexWalker.Traversal.POSTFIX:
                return root_join.join(
                    [postfix(*graph.successors(root), root=root, fix_join=fix_join, graph=graph,) for root in roots]
                )
            else:
                raise NotImplementedError()
        elif LatexNode.presentation in (LatexNode.Presentation.URL_IMG_PNG,):
            remove_us = list()
            for node in graph.nodes():
                image = LatexNode("$$" + str(node) + "$$").as_default()
                graph.node[node]["label"] = ""
                graph.node[node]["image"] = str(image.name)
                graph.node[node]["imagepath"] = str(image.parent)
                remove_us.append(image)
            graph = networkx.relabel.convert_node_labels_to_integers(graph)
            if LatexNode.folder == LatexNode.Folder.CWD:
                file = tempfile.NamedTemporaryFile(suffix=".dot", delete=False, dir=pathlib.Path.cwd())
                file.close()
                networkx.drawing.nx_pydot.write_dot(graph, file.name)
                result = pathlib.Path(graphviz.render("dot", "png", file.name))
                remove_us.append(pathlib.Path.cwd() / pathlib.Path(file.name))
            elif LatexNode.folder == LatexNode.Folder.TMP:
                file = tempfile.NamedTemporaryFile(suffix=".dot", delete=False)
                file.close()
                networkx.drawing.nx_pydot.write_dot(graph, file.name)
                result = pathlib.Path(graphviz.render("dot", "png", file.name))
                remove_us.append(pathlib.Path.cwd() / pathlib.Path(file.name))
            else:
                return NotImplementedError()
            for remove_me in remove_us:
                remove_me.unlink()
            return result
        else:
            # TODO: add possiblity to return a html page ?
            raise NotImplementedError()
