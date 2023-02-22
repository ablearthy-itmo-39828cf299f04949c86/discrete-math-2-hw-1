import z3
import itertools

def matching_model(edges):
    s = z3.Optimize()
    max_matching_size = z3.Int("max_matching_size")

    cv = z3.BoolVector("cv", len(edges))
    s.add(z3.Sum([z3.If(v, 1, 0) for v in cv]) == max_matching_size)

    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            if any(map(lambda x: x[0] == x[1], itertools.product(edges[i], edges[j]))):
                s.add(z3.Or(cv[i] == False, cv[j] == False))
    s.maximize(max_matching_size)
    return s

