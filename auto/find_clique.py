from mygraph import Graph, load_graph, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

from typing import Iterable

import itertools


def _check_clique(g: Graph, indices: Iterable[int]) -> bool:
    s = set(indices)
    return all((s - {i}) <= set(g.adj_nodes(i)) for i in indices)

def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)
    max_connected_component = max(g.connected_components, key=lambda x:len(x.indices))
    degrees = {idx : len(max_connected_component.adj_nodes(idx)) for idx in max_connected_component.indices}

    k = 5
    for k in range(4, 10):
        for v in max_connected_component.indices:
            others = [u for u in max_connected_component.adj_nodes(v) if degrees[u] >= k]
            if len(others) + 1 >= k:
                vertices = others + [v]
                for suspect in itertools.combinations(vertices, k):
                    if _check_clique(g, suspect):
                        print(f"{[ccs.to_country_code[g.vertices[r]] for r in suspect]} is a clique ({k = })")

if __name__ == "__main__":
    main()
