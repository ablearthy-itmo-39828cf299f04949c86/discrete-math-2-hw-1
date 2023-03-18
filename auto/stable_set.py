from mygraph import Graph, Subgraph, load_graph, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

import z3

def stable_set_solver(g: Graph, comp: Subgraph):
    s = z3.Optimize()

    max_stable_set_size = z3.Int("max_stable_set_size")
    cv = z3.BoolVector("indices", len(comp.indices))
    s.add(z3.Sum([z3.If(v, 1, 0) for v in cv]) == max_stable_set_size)

    map_indices = {v:i for i, v in enumerate(comp.indices)}

    for v in comp.indices:
        for u in g.adj_nodes(v):
            s.add(z3.Or(cv[map_indices[u]] == False, cv[map_indices[v]] == False))

    s.maximize(max_stable_set_size)
    return s, cv, max_stable_set_size

def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)

    mcc = max(g.connected_components, key=lambda x:len(x.indices))

    s, is_in_stable_set, size = stable_set_solver(g, mcc)

    if s.check() != z3.sat:
        print("unsat")
        exit(1)
    
    m = s.model()
    print(f"--- Maximium stable set size = {m[size].as_long()} ---")
    is_in_stable_set = [z3.is_true(m[i]) for i in is_in_stable_set]
    countries = [g.vertices[c] for c, b in zip(mcc.indices, is_in_stable_set) if b]
    print([ccs.to_country_code[c] for c in countries])

if __name__ == "__main__":
    main()
