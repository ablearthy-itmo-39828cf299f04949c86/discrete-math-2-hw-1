from collections import defaultdict, deque


def to_list(edges):
    edges_map = defaultdict(list)
    for u,v in edges:
        edges_map[u].append(v)
        edges_map[v].append(u)
    return edges_map

def get_degrees(vertices, edges):
    degrees = {v: 0 for v in vertices}
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    return degrees

def get_components(vertices_count, edges):
    result = []

    edges_map = to_list(edges)
    visited = [False] * vertices_count
    for v in range(vertices_count):
        if visited[v]:
            continue
        tmp_v = []
        tmp_e = set()
        q = deque([v])
        while q:
            cur = q.popleft()
            visited[cur] = True
            tmp_v.append(cur)
            for u in edges_map[cur]:
                if (u, cur) not in tmp_e:
                    tmp_e.add((cur, u))
                if not visited[u]:
                    visited[u] = True
                    q.append(u)
        result.append((tmp_v, tmp_e))
    return result


def get_eccentricity(edges, v):
    visited = set()
    q = deque([(v, 0)])
    edges_map = to_list(edges)

    e = 0
    while q:
        node, dist = q.popleft()
        e = max(e, dist)
        visited.add(node)
        for u in edges_map[node]:
            if u not in visited:
                visited.add(u)
                q.append((u, dist + 1))
    return e


def get_eccentricities(edges, vertices):
    return {v: get_eccentricity(edges, v) for v in vertices}


def main():
    with open("vertices.txt", "r") as f:
        vertices = [x.strip() for x in f.readlines() if x.strip()]

    with open("export.csv", "r") as f:
        edges = [x.strip().split('\t') for x in f.readlines() if x.strip()]

    vertices_ids = {v : i for i, v in enumerate(vertices)}
    edges_ids = [(vertices_ids[u], vertices_ids[v]) for u, v in edges]

    print(len(edges_ids))

    for vs, es in get_components(len(vertices), edges_ids):
        degrees = get_degrees(vs, es)
        min_idx, min_deg = min(degrees.items(), key=lambda x: x[1])
        max_idx, max_deg = max(degrees.items(), key=lambda x: x[1])

        print(f"--- |V| = {len(vs)}, |E| = {len(es)} ---")
        print(f"Min degree: {vertices[min_idx]} - {min_deg}")
        print(f"Max degree: {vertices[max_idx]} - {max_deg}")

        eccentricities = get_eccentricities(es, vs)
        print({vertices[idx]: e for idx, e in eccentricities.items()})

        radius = min(eccentricities.values())
        diam = max(eccentricities.values())
        center = [vertices[idx] for idx, e in eccentricities.items() if e == radius]

        print(f"Radius: {radius}")
        print(f"Diameter: {diam}")
        print(f"Center: {center}")



if __name__ == "__main__":
    main()
