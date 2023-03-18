from mygraph import Graph, Subgraph, load_graph, load_country_codes
from config import EDGES_PATH, VERTICES_PATH, COUNTRIES_INFO_PATH

def main():
    ccs = load_country_codes(COUNTRIES_INFO_PATH)
    g = load_graph(vertices_fp=VERTICES_PATH, edges_fp=EDGES_PATH)
    mcc = max(g.connected_components, key=lambda x: len(x.indices))

    print("Enter size of the walk: ", end='')
    size = int(input())
    print("Enter shortcodes of countries separated by newline:")
    walk = [input() for _ in range(size + 1)]

    visited = {v: False for v in mcc.indices}

    for i in range(1, len(walk)):
        prev = g.get_vertex_id_by_name(ccs.from_country_code[walk[i - 1]])
        cur = g.get_vertex_id_by_name(ccs.from_country_code[walk[i]])
        visited[prev] = True
        if cur not in g.adj_nodes(prev):
            print(f"No edge between {walk[i - 1]} and {walk[i]}")
            exit(1)

    if not all(visited.values()):
        not_visited = [g.vertices[i] for i, b in visited.items() if not b]
        print(f"Some vertices are not visited: {not_visited}")
        exit(1)

    print("OK")

if __name__ == "__main__":
    main()
