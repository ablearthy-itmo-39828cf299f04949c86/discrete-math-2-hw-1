from z3 import *

import itertools

def load_graph(filename):
    with open(filename, "r") as f:
        return [x.strip().split('\t') for x in f.readlines() if x]

def normalize(graph):
    elems = set()
    for k, v in graph:
        elems.add(k)
        elems.add(v)
    lst = list(elems)
    return {v: i for i, v in enumerate(lst)}

def get_edges(graph, norm):
    edges = []
    for k, v in graph:
        edges.append((norm[k], norm[v]))
    return edges

def get_vertex_coloring_model(graph):
    s = Optimize()

    count = Int("count")
    norm = normalize(graph)
    edges = get_edges(graph, norm)

    cv = []
    for v in norm.keys():
        var = Int(v)
        s.add(And(1 <= var, var <= count))
        cv.append(var)

    for u, v in edges:
        s.add(cv[u] != cv[v])

    s.minimize(count)
    return s

def get_edge_coloring_model(graph):
    s = Optimize()

    count = Int("count")
    norm = normalize(graph)
    edges = get_edges(graph, norm)
    cv = IntVector("vec", len(edges))
    for x in cv:
        s.add(And(1 <= x, x <= count))
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            if any(map(lambda x: x[0] == x[1], itertools.product(edges[i], edges[j]))):
                s.add(cv[i] != cv[j])
    s.minimize(count)
    return s

def get_stable_set_model(graph):
    s = Optimize()

    count = Int("count")

    norm = normalize(graph)
    edges = get_edges(graph, norm)

    cv = [Bool(v) for v in norm.keys()]
    s.add(Sum([If(v, 1, 0) for v in cv]) == count)

    for u, v in edges:
        s.add(Or(cv[u] == False, cv[v] == False))

    s.maximize(count)
    return s

def get_matching_model(graph):
    s = Optimize()

    cnt = Int("count")

    norm = normalize(graph)
    edges = get_edges(graph, norm)

    cv = BoolVector("cv", len(edges))
    s.add(Sum([If(v, 1, 0) for v in cv]) == cnt)

    for i, p1 in enumerate(edges):
        for j, p2 in enumerate(edges):
            if i < j and (p1[0] == p2[0] or p1[0] == p2[1] or p1[1] == p2[0] or p1[1] == p2[1]):
                s.add(Or(cv[i] == False, cv[j] == False))
    s.maximize(cnt)
    return s

def test_vertex_coloring():
    graph = load_graph("export.csv")
    s = get_vertex_coloring_model(graph)
    if s.check() == sat:
        model = s.model()
        print({v.name(): model[v] for v in model})
    else:
        print("unsat")

def test_edge_coloring():
    graph = load_graph("export.csv")
    s = get_edge_coloring_model(graph)
    if s.check() == sat:
        model = s.model()
        print({v.name(): model[v] for v in model})
    else:
        print("unsat")

def test_stable_set():
    graph = load_graph("export.csv")
    s = get_stable_set_model(graph)

    if s.check() == sat:
        model = s.model()
        print({v.name(): model[v] for v in model})
    else:
        print(f"unsat")

def test_matching():
    graph = load_graph("export.csv")
    latest = None
    s = get_matching_model(graph)
    if s.check() == sat:
        model = s.model()
        print({v.name(): model[v] for v in model})
    else:
        print("unsat")


def main():
    test_vertex_coloring()
    # test_edge_coloring()
    # test_stable_set()
    # test_matching()

if __name__ == "__main__":
    main()
