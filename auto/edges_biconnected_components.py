from mygraph import Graph, load_graph, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

from typing import Tuple
from collections import deque

def _find_edge_biconnected_components(g: Graph) -> Tuple[list[set[int]], set[Tuple[int, int]]]:
    levels = [-1] * len(g.vertices)
    heights = [-1] * len(g.vertices)

    bridges = set()
    components = []

    def dfs(cur, parent):
        levels[cur] = heights[cur] = 0 if parent == -1 else heights[parent] + 1
        children = 0

        vertices = set([cur])

        for u in g.adj_nodes(cur):
            if u == parent:
                continue

            if heights[u] == -1:
                tmp = dfs(u, cur)
                levels[cur] = min(levels[cur], levels[u])
                if heights[cur] < levels[u]:
                    bridges.add((cur, u))
                    components.append(tmp)
                else:
                    vertices |= tmp
                children += 1
            else:
                levels[cur] = min(levels[cur], heights[u])

        if parent == -1 and vertices:
            components.append(vertices)
        return vertices

    for i in range(len(g.vertices)):
        if heights[i] != -1:
            continue
        dfs(i, -1)
    return components, bridges


def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)

    blocks, bridges = _find_edge_biconnected_components(g)
    print([f"{ccs.to_country_code[g.vertices[a]]}--{ccs.to_country_code[g.vertices[b]]}" for a, b in bridges])
    for block in blocks:
        named_block = [f"{ccs.to_country_code[g.vertices[a]]}" for a in block]
        print('-' * 10)
        print(f"{len(block) = }")
        print(f"block = {','.join(named_block)}")

if __name__ == "__main__":
    main()
