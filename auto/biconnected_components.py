from mygraph import Graph, load_graph, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

from collections import deque

def _get_cut_vertices(g: Graph) -> set[int]:
    levels = [-1] * len(g.vertices)
    heights = [-1] * len(g.vertices)

    result = set()

    def dfs(cur, parent):
        levels[cur] = heights[cur] = 0 if parent == -1 else heights[parent] + 1
        children = 0

        for u in g.adj_nodes(cur):
            if u == parent:
                continue

            if heights[u] == -1:
                dfs(u, cur)
                levels[cur] = min(levels[cur], levels[u])
                if heights[cur] <= levels[u] and parent != -1:
                    result.add(cur)
                children += 1
            else:
                levels[cur] = min(levels[cur], heights[u])

        if parent == -1 and children > 1:
            result.add(cur)

    for i in range(len(g.vertices)):
        if heights[i] != -1:
            continue
        dfs(i, -1)
    return result

def _find_blocks(g: Graph):
    cut_vertices = _get_cut_vertices(g)
    visited = [False] * len(g.vertices)

    ret = []

    for i in range(len(g.vertices)):
        if visited[i] or i in cut_vertices:
            continue
        indices = set([i])
        q = deque([i])
        while q:
            v = q.popleft()
            if v in cut_vertices:
                continue
            visited[v] = True
            for u in g.adj_nodes(v):
                if visited[u] and u not in cut_vertices:
                    continue
                indices.add(u)
                q.append(u)
                visited[u] = True

        ret.append(indices)
    return ret

def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)

    blocks = _find_blocks(g)
    cut_vertices = _get_cut_vertices(g)
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
