from mygraph import Graph, Subgraph, load_graph, load_distances, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

from typing import Tuple
from collections import deque, defaultdict

import queue

def _get_index_based_distances(g: Graph, distances) -> dict[int, dict[int,int]]:
    index_map = {v:i for i, v in enumerate(g.vertices)}
    ret = defaultdict(dict)
    for v, tmp in distances.items():
        for u, d in tmp.items():
            ret[index_map[v]][index_map[u]] = d
            ret[index_map[u]][index_map[v]] = d
    return ret

def _find_mst(cc: Subgraph, index_based_distances: dict[int, dict[int,int]]) -> Tuple[Subgraph, dict[int, dict[int, int]]]:
    pq = queue.PriorityQueue()
    vertices = set([cc.indices[0]])
    edges = set()
    distances = defaultdict(dict)

    for v, d in index_based_distances[cc.indices[0]].items():
        pq.put((d, v, cc.indices[0]))

    while not pq.empty():
        d, v, p = pq.get()
        if v in vertices:
            continue
        edges.add((p, v))
        vertices.add(v)
        distances[p][v] = d
        distances[v][p] = d
        for u, d1 in index_based_distances[v].items():
            pq.put((d1, u, v))

    return Subgraph(list(vertices), edges), distances

def find_maximum_subtree_weight(tree: Subgraph, v: int, distances: dict[int, dict[int,int]]) -> float:
    def dfs(u, p):
        s = 0
        for r in tree.adj_nodes(u):
            if r == p:
                continue
            s += distances[u][r]
            s += dfs(r, u)
        return s

    sum_max = float("-inf")
    for u in tree.adj_nodes(v):
        sum_max = max(sum_max, dfs(u, v) + distances[u][v])
    return sum_max

def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)
    mcc = max(g.connected_components, key=lambda x: len(x.indices))
    distances = load_distances(COUNTRIES_INFO_PATH, EDGES_PATH)
    index_based_distances = _get_index_based_distances(g, distances)
    mst, mst_distances = _find_mst(mcc, index_based_distances)
    weights = {x: find_maximum_subtree_weight(mst, x, mst_distances) for x in mst.indices}
    country, weight = min(weights.items(), key=lambda x: x[1])
    print(f"Centroid: {ccs.to_country_code[g.vertices[country]]} ({weight})")


if __name__ == "__main__":
    main()
