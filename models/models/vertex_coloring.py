import z3

def vertex_coloring_model(edges, vertices_count):
    s = z3.Optimize()

    max_color_count = z3.Int("max_color_count")
    cv = z3.IntVector("colors", vertices_count)
    for x in cv:
        s.add(z3.And(1 <= x, x <= max_color_count))

    for u, v in edges:
        s.add(cv[u] != cv[v])

    s.minimize(max_color_count)
    return s
