from mygraph import Graph, Subgraph, load_graph, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

import z3

from typing import Tuple

def _get_unique_edges(comp: Subgraph) -> list[Tuple[int, int]]:
    ret = set()
    for u, v in comp.edges:
        if (u, v) not in ret and (v, u) not in ret:
            ret.add((u, v))

    return list(ret)

def _find_edge(comp: Subgraph, u: int, v: int) -> int:
    for i, e in enumerate(comp.edges):
        if e == (u, v) or e == (v, u):
            return i
    return -1

def vertex_cover_solver(g: Graph, comp: Subgraph):
    s = z3.Optimize()

    edges = _get_unique_edges(comp)

    covered = z3.BoolVector("covered", len(edges))
    in_set = z3.BoolVector("in_set", len(comp.indices))

    indices_map = {v:i for i, v in enumerate(comp.indices)}

    min_vertex_cover_len = z3.Int("min_vertex_cover_len")

    s.add(z3.Sum([z3.If(v, 1, 0) for v in in_set]) == min_vertex_cover_len)

    s.add(z3.And(covered))

    for v in comp.indices:
        for u in g.adj_nodes(v):
            idx = _find_edge(comp, u, v)
            s.add(z3.Or(covered[idx] == in_set[indices_map[u]], covered[idx] == in_set[indices_map[v]]))

    s.minimize(min_vertex_cover_len)
    return s, in_set, min_vertex_cover_len


def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)
    mcc = max(g.connected_components, key=lambda x: len(x.indices))

    s, in_set, size = vertex_cover_solver(g, mcc)

    if s.check() != z3.sat:
        print("unsat")
        exit(1)

    m = s.model()
    print(f"--- Minimum vertex cover size = {m[size].as_long()} ---")
    in_set = [z3.is_true(m[i]) for i in in_set]
    for i, b in zip(mcc.indices, in_set):
        cc = ccs.to_country_code[g.vertices[i]]
        sign = '+' if b else '-'
        print(f"{sign} {cc}")

if __name__ == "__main__":
    main()
