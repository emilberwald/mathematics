import networkx


def axiom(sequent: networkx.MultiDiGraph, A):
    result = networkx.MultiDiGraph()
    result.add_nodes_from(sequent.nodes())
    result.add_edges_from(sequent.edges())
    result.add_node(A)
    result.add_edge(A, A)
    return result


def cut(sequent0: networkx.MultiDiGraph, sequent1: networkx.MultiDiGraph, A):
    lhs0_nodes = set(sequent0.predecessors(A))
    rhs0_cut = {
        rhs0_node
        for lhs0_node in lhs0_nodes
        for rhs0_node in sequent0.successors(lhs0_node)
        if rhs0_node != A
    }
    rhs1_nodes = set(sequent1.successors(A))
    lhs1_cut = {
        lhs1_node
        for rhs1_node in rhs1_nodes
        for lhs1_node in sequent1.predecessors(rhs1_node)
        if lhs1_node != A
    }
    result = networkx.MultiDiGraph()
    result.add_nodes_from(lhs0_nodes + rhs0_cut + lhs1_cut + rhs1_nodes)
    result.add_edges_from(
        [(lhs, rhs) for lhs in lhs0_nodes + lhs1_cut for rhs in rhs0_cut + rhs1_nodes]
    )
    return result


def left_or(sequent, A_or_B):
    """Assumes the node in question is the tuple A,_or_,B = A_or_B
	"""
    assert A_or_B in sequent.nodes()
    result = [networkx.MultiDiGraph(), networkx.MultiDiGraph()]
    result[0].add_node(A)
    result[1].add_node(B)
    A, _or_, B = A_or_B
    for rhs_nodes in sequent.successors(A_or_B):
        for rhs_node in rhs_nodes:
            result[0].add_node(rhs_node)
            result[0].add_edge(A, rhs_node)
            result[1].add_node(rhs_node)
            result[1].add_edge(B, rhs_node)
            for lhs_nodes in sequent.predecessors(rhs_node):
                for lhs_node in (
                    lhs_node for lhs_node in lhs_nodes if lhs_node != A_or_B
                ):
                    result[0].add_node(lhs_node)
                    result[0].add_edge(lhs_node, rhs_node)
                    result[1].add_node(lhs_node)
                    result[1].add_edge(lhs_node, rhs_node)
    return result
