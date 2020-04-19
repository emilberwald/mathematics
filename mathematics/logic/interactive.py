if __package__:
    from .sequent_calculus import *
else:
    from sequent_calculus import *
from typing import Sequence
import networkx

PROMPT = "\n>"


def get_required(text):
    while True:
        if symbol := input(text + PROMPT):
            print(symbol)
            return symbol


def get_optional(text):
    symbol = input(text + PROMPT)
    print(symbol)
    return symbol


def get_variable():
    return Variable(get_required("<variable>").lower())


def get_function():
    symbol = get_required("<function symbol>").lower()
    arguments = list()
    while argument := get_term():
        arguments.append(argument)
    return FunctionSymbol(symbol, arguments)


def get_term():
    print("<<term>>")
    commands = ("(v)ariable", "(f)unction symbol")
    while command := get_optional(f"{'|'.join(commands)}").lower():
        if command == "v":
            return get_variable()
        elif command == "f":
            return get_function()
        else:
            return None


def get_formulas():
    terms = list()
    formulas = list()
    commands = ("(t)erm", "(a)tomic", "(l)ogical", "(b)inding", "(g)eneric", "(c)lear")
    while (command := get_optional(f"terms:\t{terms}\nformulas:\t{formulas}\n{'|'.join(commands)}").lower()) :
        if command == "t":
            term = get_term()
            if term:
                terms.append(term)
        elif command == "c":
            terms.clear()
            formulas.clear()
        elif command == "a":
            while connective := get_required(f"=|...").upper():
                if connective in (symbol.name.upper() for symbol in PredicateLogicSymbols):
                    print(f"atomic formula does not allow: '{connective}'")
                    continue
                included: Sequence[Term] = list()
                for term in terms:
                    if input(f"<Enter> to include '{term}'"):
                        included.append(term)
                terms = [term for term in terms if term not in included]
                formulas.append(AtomicFormula(connective, tuple(included)))
                break
        elif command == "l":
            while op := get_required(f"{'|'.join(e for e in PredicateLogicSymbols)}").upper():
                if op in (symbol.name.upper() for symbol in PredicateLogicSymbols):
                    connective = PredicateLogicSymbols[op].value
                else:
                    print(f"compound formula does not allow: '{op}'")
                    continue
                included: Sequence[Formula] = list()
                for formula in formulas:
                    if get_optional(f"<Enter> to include '{formula}'"):
                        included.append(formula)
                formulas = [formula for formula in formulas if formula not in included]
                formulas.append(LogicFormula(connective, tuple(included)))
                break
        elif command == "b":
            while op := get_required(f"{'|'.join(e for e in QuantifierSymbols)}|...").upper():
                if op in (symbol.name.upper() for symbol in QuantifierSymbols):
                    connective = QuantifierSymbols[connective].value
                elif op in (symbol.name for symbol in PredicateLogicSymbols):
                    print(f"binding formula does not allow: '{op}'")
                    continue
                else:
                    connective = op

                included: Sequence[Formula] = list()
                for formula in formulas:
                    if input(f"<Enter> to include:\t{formula}"):
                        included.append(formula)

                while True:
                    if symbol := get_required("<binding variable>").lower():
                        tentative = Variable(symbol)
                        if all(wff.is_free(tentative) for wff in included):
                            formulas.append(BindingFormula(connective, tentative, tuple(included)))
                            break

                formulas = [formula for formula in formulas if formula not in included]
                break
        elif command == "g":
            symbol = get_required("<symbol>")
            formulas.append(Formula(symbol))
    return tuple(formulas)


def summarize(G: networkx.MultiDiGraph):
    print("<<summarise>>")
    for index, node in enumerate(x for x in G.nodes() if G.out_degree(x) == 0):
        print(f"{index}\t{node}")


def select(G: networkx.MultiDiGraph):
    summarize(G)
    print("<<select:iterate>>")
    for node in enumerate(x for x in G.nodes() if G.out_degree(x) == 0):
        if chosen := get_optional(f"<Enter> to ignore: {node}"):
            return node


def axiom(G: networkx.MultiDiGraph):
    axioms = ("(i)nitial", "(w)eakening", "(s)ubstitute")
    while command := get_required(f"{'|'.join(axioms)}").lower():
        print()
        if command == "i":
            wffs = get_formulas()
            G.add_node(Sequent(wffs, wffs))
            return
        elif command == "w":
            sequent = select(G)
            if sequent:
                sides = {"(l)eft", "(r)ight"}
                while side := get_required(f"{'|'.join(sides)}") in sides:
                    if side == "l":
                        print("<<weakening left side>>")
                        wffs = get_formulas()

                        weakened = sequent
                        for wff in wffs:
                            weakened = InferenceRules.l_weakening(weakened, wff)
                        G.add_node(weakened)
                        G.add_edge(sequent, weakened, label="(l_weakening)")
                        return
                    elif side == "r":
                        print("<<weakening right side>>")
                        wffs = get_formulas()

                        weakened = sequent
                        for wff in wffs:
                            weakened = InferenceRules.r_weakening(weakened, wff)
                        G.add_node(weakened)
                        G.add_edge(sequent, weakened, label="(r_weakening)")
                        return
        elif command == "s":
            raise NotImplementedError()


if __name__ == "__main__":
    G = networkx.MultiDiGraph()
    commands = ("(a)xiom", "(i)nference rule", "(s)tructural rule")
    while command := get_optional("|".join(commands)).lower():
        if command == "a":
            axiom(G)
        elif command == "i":
            raise NotImplementedError()
        elif command == "s":
            raise NotImplementedError()
        print(summarize(G))
