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

    covered = z3.BoolVector("covered", len(comp.indices))
    in_set = z3.BoolVector("in_set", len(edges))

    indices_map = {v:i for i, v in enumerate(comp.indices)}

    min_edge_cover_len = z3.Int("min_edge_cover_len")

    s.add(z3.Sum([z3.If(v, 1, 0) for v in in_set]) == min_edge_cover_len)

    s.add(z3.And(covered))

    for i, (u, v) in enumerate(edges):
        s.add(z3.Implies(in_set[i] == True, covered[indices_map[u]] == True))
        s.add(z3.Implies(in_set[i] == True, covered[indices_map[v]] == True))

    for v in comp.indices:
        edge_ids = [_find_edge(comp, v, u) for u in g.adj_nodes(v)]
        s.add(z3.Implies(covered[indices_map[v]] == True, z3.Or([in_set[idx] == True for idx in edge_ids])))

    s.minimize(min_edge_cover_len)
    return s, in_set, edges, min_edge_cover_len


def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)
    mcc = max(g.connected_components, key=lambda x: len(x.indices))

    s, in_set, edges, size = vertex_cover_solver(g, mcc)

    if s.check() != z3.sat:
        print("unsat")
        exit(1)

    m = s.model()
    print(f"--- Minimum edge cover size = {m[size].as_long()} ---")
    in_set = [z3.is_true(m[i]) for i in in_set]
    for (u, v), b in zip(edges, in_set):
        cc1 = ccs.to_country_code[g.vertices[u]]
        cc2 = ccs.to_country_code[g.vertices[v]]
        sign = '+' if b else '-'
        print(f"{sign} {cc1}--{cc2}")

if __name__ == "__main__":
    main()
