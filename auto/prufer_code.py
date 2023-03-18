from mygraph import Graph, Subgraph, load_graph, load_distances, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

from typing import Tuple
from collections import deque, defaultdict

import queue
import heapq

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

def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)
    mcc = max(g.connected_components, key=lambda x: len(x.indices))
    distances = load_distances(COUNTRIES_INFO_PATH, EDGES_PATH)
    index_based_distances = _get_index_based_distances(g, distances)
    mst, _ = _find_mst(mcc, index_based_distances)

    degrees = [(len(mst.adj_nodes(i)), ccs.to_country_code[g.vertices[i]], i) for i in mst.indices]
    heapq.heapify(degrees)

    edges = mst.adj_list.copy()
    result = []

    while len(degrees) > 2:
        deg, _, idx = heapq.heappop(degrees)
        n = edges[idx][0]
        result.append(n)
        del edges[idx][0]
        del edges[result[-1]][edges[result[-1]].index(idx)]
        nidx = [i for i, x in enumerate(degrees) if x[2] == n][0]
        degrees[nidx] = (degrees[nidx][0] - 1, degrees[nidx][1], degrees[nidx][2])
        newitem = degrees[nidx]

        while nidx > 0:
            ppos = (nidx - 1) >> 1
            p = degrees[ppos]
            if newitem < p:
                degrees[nidx] = p
                nidx = ppos
                continue
            break
        degrees[nidx] = newitem

    print(' '.join([ccs.to_country_code[g.vertices[c]] for c in result]))


if __name__ == "__main__":
    main()
