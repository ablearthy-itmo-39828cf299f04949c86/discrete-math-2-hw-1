from mygraph import Graph, load_graph, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

import z3
import itertools

def edge_coloring_solver(g: Graph):
    s = z3.Optimize()

    min_edges_color = z3.Int("min_edges_color")

    unique_edges = set()
    for v, neighbours in g.adj_list.items():
        for u in neighbours:
            if (v, u) not in unique_edges and (u, v) not in unique_edges:
                unique_edges.add((v, u))

    unique_edges = list(unique_edges)
    cv = z3.IntVector("colors", len(unique_edges))

    for x in cv:
        s.add(z3.And(1 <= x, x <= min_edges_color))

    for i in range(len(unique_edges)):
        for j in range(i + 1, len(unique_edges)):
            if any(a == b for a, b in itertools.product(unique_edges[i], unique_edges[j])):
                s.add(cv[i] != cv[j])

    s.minimize(min_edges_color)
    return s, cv, unique_edges, min_edges_color


def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)

    s, colors, edges, min_color_count = edge_coloring_solver(g)

    if s.check() == z3.sat:
        m = s.model()
        print(f"--- Minimum color count = {m[min_color_count].as_long()} ---")
        colors = [m[i].as_long() for i in colors]
        for (u, v), color in zip(edges, colors):
            cc1 = ccs.to_country_code[g.vertices[u]]
            cc2 = ccs.to_country_code[g.vertices[v]]
            print(f"{cc1}-{cc2} - {color}")
    else:
        print("unsat")

if __name__ == "__main__":
    main()
