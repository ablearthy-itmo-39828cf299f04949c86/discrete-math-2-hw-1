from mygraph import Graph, Subgraph, load_graph, load_distances
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

def sum_mst(mst: Subgraph, distances: dict[int, dict[int, int]]) -> int:
    s = 0
    q = deque([mst.indices[0]])
    visited = {x: False for x in mst.indices}
    while q:
        v = q.popleft()
        visited[v] = True
        for u in mst.adj_nodes(v):
            if not visited[u]:
                s += distances[v][u]
                visited[u] = True
                q.append(u)
    return s

def main():
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)
    mcc = max(g.connected_components, key=lambda x: len(x.indices))
    distances = load_distances(COUNTRIES_INFO_PATH, EDGES_PATH)
    index_based_distances = _get_index_based_distances(g, distances)
    mst, mst_distances = _find_mst(mcc, index_based_distances)
    print(f"Minimum sum: {sum_mst(mst, mst_distances)}")

if __name__ == "__main__":
    main()
