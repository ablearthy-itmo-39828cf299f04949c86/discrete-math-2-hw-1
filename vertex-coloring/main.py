from z3 import *

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

def get_vertex_coloring_model(k, graph):
    s = Solver()

    norm = normalize(graph)
    edges = get_edges(graph, norm)

    cv = []
    for v in norm.keys():
        var = Int(v)
        s.add(And(0 <= var, var <= k - 1))
        cv.append(var)

    for u, v in edges:
        s.add(cv[u] != cv[v])
    return s

def main():
    graph = load_graph("export.csv")
    for k in range(4, 1, -1):
        s = get_vertex_coloring_model(k, graph)
        if s.check() == sat:
            model = s.model()
            print(f"success: {k = }")
            print({v.name(): model[v] for v in model})
        else:
            print(f"fail: {k = } :(")
            break

if __name__ == "__main__":
    main()
