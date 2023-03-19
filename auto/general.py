from mygraph import Graph, Subgraph, load_graph, load_distances, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

from typing import Tuple
from collections import deque, defaultdict

import queue


def get_ecc(g: Graph, v: int) -> int:
    e = 0
    visited = [False] * len(g.vertices)
    q = deque([(v, 0)])
    while q:
        node, dist = q.popleft()
        visited[node] = True
        e = max(e, dist)
        for u in g.adj_nodes(node):
            if not visited[u]:
                visited[u] = True
                q.append((u, dist + 1))
    return e

def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)
    mcc = max(g.connected_components, key=lambda x: len(x.indices))

    print(f"|V| = {len(g.vertices)}, |E| = {sum([len(x) for x in g.adj_list.values()]) // 2}")

    degrees = [len(g.adj_nodes(i)) for i in range(len(g.vertices))]
    eccs = [get_ecc(g, i) for i in range(len(g.vertices))]

    mcc_degrees = {i: degrees[i] for i in mcc.indices}
    mcc_eccs = {i: eccs[i] for i in mcc.indices}

    print(f"Min degree: {min(mcc_degrees.values())}")
    print(f"Max degree: {max(mcc_degrees.values())}")

    radius = min(mcc_eccs.values())
    diam = max(mcc_eccs.values())
    center = [k for k, v in mcc_eccs.items() if v == radius]

    print(f"Radius: {radius}")
    print(f"Diameter: {diam}")
    print(f"Center: {','.join([ccs.to_country_code[g.vertices[c]] for c in center])}")


if __name__ == "__main__":
    main()
