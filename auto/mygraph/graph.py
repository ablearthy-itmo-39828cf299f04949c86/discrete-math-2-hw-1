from typing import TypeVar, Generic, List, Tuple, Set, Dict, Iterable
from collections import defaultdict, deque
from pathlib import Path

T = TypeVar('T')

def _build_adj_list(edges: Iterable[Tuple[T, T]]) -> Dict[T, List[T]]:
    ret = defaultdict(list)
    for u, v in edges:
        ret[u].append(v)
        ret[v].append(u)
    return ret

class Subgraph:
    def __init__(self, indices: List[int], edges: Set[Tuple[int, int]]):
        self._indices: List[int] = indices
        self._edges: Set[Tuple[int, int]] = edges
        self._adj_list: Dict[int, List[int]] = _build_adj_list(edges)

    @property
    def indices(self):
        return self._indices

    @property
    def edges(self):
        return self._edges

    @property
    def adj_list(self):
        return self._adj_list

    def adj_nodes(self, idx: int) -> List[int]:
        return self._adj_list[idx]

class Graph(Generic[T]):
    def __init__(self, vertices: List[T], edges: List[Tuple[T, T]]):
        self._vertices = vertices
        self._vertices_map = {v: i for i, v in enumerate(vertices)}
        self._edges = [(self._vertices_map[u], self._vertices_map[v]) for u, v in edges]
        self._adj_list = _build_adj_list(self._edges)
        self._connected_components: List[Subgraph] = None

    def get_vertex_id_by_name(self, name: T):
        return self._vertices_map[name]

    @property
    def adj_list(self):
        return self._adj_list

    @property
    def vertices(self):
        return self._vertices

    @property
    def connected_components(self):
        if self._connected_components is None:
            self._connected_components = _get_connected_components(self)
        return self._connected_components

    def adj_nodes(self, idx: int) -> List[int]:
        return self._adj_list[idx]

def _get_connected_components(g: Graph) -> List["Subgraph"]:
    subgraphs = []
    visited = [False] * len(g.vertices)
    for i in range(len(g.vertices)):
        if visited[i]:
            continue
        visited[i] = True
        q = deque([i])
        indices = [i]
        edges = set()
        while q:
            v = q.popleft()
            for u in g.adj_nodes(v):
                if (u, v) not in edges and (v, u) not in edges:
                    edges.add((u, v))
                if visited[u]:
                    continue
                visited[u] = True
                q.append(u)
                indices.append(u)
        subgraphs.append(Subgraph(indices=indices, edges=edges))
    return subgraphs

def load_graph(vertices_fp: Path, edges_fp: Path) -> Graph[str]:
    with vertices_fp.open() as f:
        vertices = [x.strip() for x in f.readlines() if x.strip()]

    with edges_fp.open() as f:
        edges = [tuple(x.strip().split('\t')) for x in f.readlines() if x.strip()]

    return Graph(vertices=vertices, edges=edges)
