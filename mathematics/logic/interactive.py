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
    while (
        command := get_optional(
            f"terms:\t{[str(term) for term in terms]}\nformulas:\t{[str(formula) for formula in formulas]}\n{'|'.join(commands)}"
        ).lower()
    ) :
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
                    if get_optional(f"<Enter> to ignore\t'{term}'"):
                        included.append(term)

                formulas.append(AtomicFormula(connective, tuple(included)))
                terms = [term for term in terms if term not in included]
                break
        elif command == "l":
            logical_symbols = set(symbol.name.upper() for symbol in PredicateLogicSymbols) - set(
                symbol.name.upper() for symbol in QuantifierSymbols
            )
            while op := get_optional(f"{'|'.join(logical_symbols)}").upper():
                if op in logical_symbols:
                    connective = PredicateLogicSymbols[op].value
                    min_connective_arity = min_arity(PredicateLogicSymbols[op])
                else:
                    print(f"compound formula does not allow: '{op}'")
                    break

                included: Sequence[Formula] = list()
                for formula in formulas:
                    if get_optional(f"<Enter> to ignore:\t'{formula}'"):
                        included.append(formula)

                if min_connective_arity and not (len(included) >= min_connective_arity):
                    print(
                        f"compound formula arity wrong: '{len(included)}', should be at least: '{min_connective_arity}'."
                    )
                    continue

                formulas.append(LogicFormula(connective, tuple(included)))
                formulas = [formula for formula in formulas if formula not in included]
                break
        elif command == "b":
            if not formulas:
                print(f"no formulas to bind to.")
                continue

            while op := get_optional(f"{'|'.join(e.name.upper() for e in QuantifierSymbols)}|...").upper():
                if op in (symbol.name.upper() for symbol in QuantifierSymbols):
                    connective = QuantifierSymbols[op].value
                elif op in (symbol.name for symbol in PredicateLogicSymbols) or not op:
                    print(f"binding formula does not allow: '{op}'")
                    continue
                else:
                    connective = op

                included: Sequence[Formula] = list()
                for formula in formulas:
                    if get_optional(f"<Enter> to ignore:\t'{formula}'"):
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
