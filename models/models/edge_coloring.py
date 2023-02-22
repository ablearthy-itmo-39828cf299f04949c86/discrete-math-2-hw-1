import z3
import itertools

def edge_coloring_model(edges):
    s = z3.Optimize()
    max_edges_count = z3.Int("max_edges_count")

    cv = z3.IntVector("colors", len(edges))
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            if any(map(lambda x: x[0] == x[1], itertools.product(edges[i], edges[j]))):
                s.add(cv[i] != cv[j])

    s.minimize(max_edges_count)
    return s
