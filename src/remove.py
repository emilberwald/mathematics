# coding: utf8
import sympy
from mathematics.algebra.tensor import tensor
from mathematics.algebra.clifford import clifford

#pycallgraph ?

# class fileprinter:
# 	def __init__(self):
# 		self.text = "<trace>\n"

# 	def __call__(self, text):
# 		self.text += text + "\n"

# 	def flush(self):
# 		with open("output.xml", 'a', encoding='utf8') as f:
# 			f.write(self.text + "</trace>")
# 			self.text = ""

# fileprint = fileprinter()

# def tryprint(text, name):
# 	fileprint("<{name}>".format(name=name))
# 	try:
# 		fileprint("<![CDATA[{0}]]>".format(text))
# 	except Exception as e:
# 		fileprint("<![CDATA[{0}]]>".format(e))
# 	fileprint("</{name}>".format(name=name))

# def printcode(code):
# 	fileprint("<code>")
# 	tryprint(code.co_name, "co_name")
# 	tryprint(code.co_argcount, "co_argcount")
# 	tryprint(code.co_nlocals, "co_nlocals")
# 	tryprint(code.co_varnames, "co_varnames")
# 	tryprint(code.co_cellvars, "co_cellvars")
# 	tryprint(code.co_freevars, "co_freevars")
# 	tryprint(code.co_code, "co_code")
# 	tryprint(code.co_consts, "co_consts")
# 	tryprint(code.co_names, "co_names")
# 	tryprint(code.co_filename, "co_filename")
# 	tryprint(code.co_firstlineno, "co_firstlineno")
# 	tryprint(code.co_lnotab, "co_lnotab")
# 	tryprint(code.co_stacksize, "co_stacksize")
# 	tryprint(code.co_flags, "co_flags")
# 	fileprint("</code>")

# def printframe(frame):
# 	fileprint("<frame>")
# 	tryprint(frame.f_back, "f_back")
# 	printcode(frame.f_code)
# 	tryprint(frame.f_locals, "f_locals")
# 	tryprint(frame.f_globals, "f_globals")
# 	tryprint(frame.f_builtins, "f_builtins")
# 	tryprint(frame.f_lineno, "f_lineno")
# 	fileprint("</frame>")

# def tracer(frame, event, arg):
# 	def print_event(frame, event, arg, e):
# 		if (event == e):
# 			fileprint("<{0}>".format(e))
# 			printframe(frame)
# 			tryprint(arg, "arg")
# 			fileprint("</{0}>".format(e))

# 	print_event(frame, event, arg, "call")
# 	print_event(frame, event, arg, "line")
# 	print_event(frame, event, arg, "return")
# 	print_event(frame, event, arg, "exception")
# 	print_event(frame, event, arg, "opcode")
# 	return tracer

# import sys


def main():
	try:
		V = sympy.symbols("e_{0:3}")
		A = tensor.symbolic("A", V, (1, 1))
		x = tensor.symbolic("x", V, (1, 0))

		print(A.latex())
		print(x.latex())
		print(A(x).latex())

		V = sympy.symbols("e_{1:2}")
		a = clifford.symbolic("a", V, (1, 0))
		b = clifford.symbolic("b", V, (1, 0))
		print(a.latex())
		print(b.latex())
		print((a @ b).latex())
		#sys.settrace(tracer)
		#A + B
		#print((A + B).latex())
		#sys.settrace(None)
	finally:
		pass
		#fileprint.flush()


if __name__ == '__main__':
	main()
