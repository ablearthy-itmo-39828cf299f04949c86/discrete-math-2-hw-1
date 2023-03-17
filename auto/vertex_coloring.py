from mygraph import Graph, load_graph, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

import z3

def vertex_coloring_solver(g: Graph):
    s = z3.Optimize()

    max_color_count = z3.Int("max_color_count")
    cv = z3.IntVector("colors", len(g.vertices))
    for x in cv:
        s.add(z3.And(1 <= x, x <= max_color_count))

    for v in range(len(g.vertices)):
        for u in g.adj_nodes(v):
            s.add(cv[u] != cv[v])

    s.minimize(max_color_count)
    return s, cv, max_color_count


def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)

    s, colors, min_color_count = vertex_coloring_solver(g)

    if s.check() == z3.sat:
        m = s.model()
        print(f"--- Minimum color count = {m[min_color_count].as_long()} ---")
        colors = [m[i].as_long() for i in colors]
        for country, color in zip(g.vertices, colors):
            print(f"{ccs.to_country_code[country]} - {color}")
    else:
        print("unsat")

if __name__ == "__main__":
    main()
