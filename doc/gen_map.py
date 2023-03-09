def parse_coord(coord):
    sign = 1 if coord[-1]  == 'N' or coord[-1] == 'E' else -1
    new_coord = ""
    for x in coord:
        if x.isdigit() or x in "NSWE":
            new_coord += x
        else:
            new_coord += ' '
    lst = new_coord.split(' ')
    c = int(lst[0]) + int(lst[1]) / 60
    return sign * c

def main():
    with open("vertices.txt", "r") as f:
        data = [x.strip().split(' ') for x in f.readlines() if x.strip()]
        data = [list(filter(lambda x: x, line)) for line in data]
        data = [ (' '.join(line[:-3]), line[-3], line[-2], line[-1]) for line in data]

    with open("vertices-latex.txt", "r") as f:
        latex_vertices = [x.strip().split(' ') for x in f.readlines() if x.strip()]


    with open("export.csv", "r") as f:
        edges = [x.strip().split('\t') for x in f.readlines() if x.strip()]

    codes = {country: code for country, code, _, _ in data}
    for code, x, y in latex_vertices:
        print(f"\\node[countrynode] ({code}) at ({x}, {y}) {{{code}}};")

    for u, v in edges:
        cu, cv = codes[u], codes[v]
        print(f"\\draw[myline] ({cu}) -- ({cv});")


if __name__ == "__main__":
    main()
