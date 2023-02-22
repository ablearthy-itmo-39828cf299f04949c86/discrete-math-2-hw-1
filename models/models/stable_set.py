import z3

def stable_set_model(edges, max_vertices_count):
    s = z3.Optimize()

    max_stable_set_size = z3.Int("max_stable_set_size")

    cv = z3.BoolVector("indices", max_vertices_count)
    s.add(z3.Sum([z3.If(v, 1, 0) for v in cv]) == max_stable_set_size)

    for u, v in edges:
        s.add(z3.Or(cv[u] == False, cv[v] == False))

    s.maximize(max_stable_set_size)
    return s
