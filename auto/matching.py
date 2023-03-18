from mygraph import Graph, Subgraph, load_graph, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

import z3
import itertools

def matching_solver(g: Graph, comp: Subgraph):
    s = z3.Optimize()

    max_matching_size = z3.Int("max_matching_size")
    cv = z3.BoolVector("indices", len(comp.edges))
    s.add(z3.Sum([z3.If(v, 1, 0) for v in cv]) == max_matching_size)

    edges = list(comp.edges)
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            if any(a == b for a, b in itertools.product(edges[i], edges[j])):
                s.add(z3.Or(cv[i] == False, cv[j] == False))

    s.maximize(max_matching_size)
    return s, cv, edges, max_matching_size

def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)

    mcc = max(g.connected_components, key=lambda x:len(x.indices))

    s, is_in_matching, edges, size = matching_solver(g, mcc)

    if s.check() != z3.sat:
        print("unsat")
        exit(1)
    
    m = s.model()
    print(f"--- Maximium matching size = {m[size].as_long()} ---")
    is_in_matching = [z3.is_true(m[i]) for i in is_in_matching]

    for (u, v), b in zip(edges, is_in_matching):
        cc1 = ccs.to_country_code[g.vertices[u]]
        cc2 = ccs.to_country_code[g.vertices[v]]
        sign = '+' if b else '-'
        print(f"{sign} {cc1}-{cc2}")

if __name__ == "__main__":
    main()
