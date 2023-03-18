from mygraph import Graph, load_graph, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

from typing import Tuple
from collections import deque

def _find_blocks(g: Graph) -> Tuple[list[set[int]], set[int]]:
    levels = [-1] * len(g.vertices)
    heights = [-1] * len(g.vertices)

    cut_vertices = set()

    components = []

    def dfs(cur, parent):
        levels[cur] = heights[cur] = 0 if parent == -1 else heights[parent] + 1
        children = 0

        nodes = {cur}

        for u in g.adj_nodes(cur):
            if u == parent:
                continue

            if heights[u] == -1:
                tmp = dfs(u, cur)
                levels[cur] = min(levels[cur], levels[u])
                if heights[cur] <= levels[u] and parent != -1:
                    cut_vertices.add(cur)
                    components.append(tmp | {cur})
                    nodes |= {cur}
                else:
                    nodes |= tmp
                children += 1
            else:
                levels[cur] = min(levels[cur], heights[u])

        if parent == -1 and children > 1:
            cut_vertices.add(cur)
            components.append(nodes)
        elif parent == -1 and nodes:
            components.append(nodes)

        return nodes

    for i in range(len(g.vertices)):
        if heights[i] != -1:
            continue
        dfs(i, -1)
    return components, cut_vertices


def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)

    blocks, cut_vertices = _find_blocks(g)
    for block in blocks:
        cuts = cut_vertices & block
        named_cuts = [ccs.to_country_code[g.vertices[c]] for c in cuts]
        named_block = [ccs.to_country_code[g.vertices[c]] for c in block]
        print('-' * 10)
        print(f"{len(block) = }")
        print(f"cuts = {','.join(named_cuts)}")
        print(f"block = {','.join(named_block)}")

if __name__ == "__main__":
    main()
