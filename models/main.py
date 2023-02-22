import z3
from models.edge_coloring import edge_coloring_model
from models.vertex_coloring import vertex_coloring_model
from models.stable_set import stable_set_model
from models.matching import matching_model

def load_graph(filename, vertices_filename):
    with open(filename, "r") as f:
        graph = [x.strip().split('\t') for x in f.readlines() if x]
    with open(vertices_filename, "r") as f:
        vertices = set([x.strip() for x in f.readlines() if x])
    return list(vertices), graph

def run_model(s):
    if s.check() == z3.sat:
        model = s.model()
        return {v.name(): model[v] for v in model}

def main():
    vertices, edges = load_graph("export.csv", "vertices.txt")
    mappings = {v: i for i, v in enumerate(vertices)}
    print(f"{len(vertices) = }, {len(edges) = }")
    normalized_edges = [(mappings[u], mappings[v]) for u, v in edges]
    s = vertex_coloring_model(normalized_edges, len(vertices))
    print(run_model(s))

if __name__ == "__main__":
    main()
