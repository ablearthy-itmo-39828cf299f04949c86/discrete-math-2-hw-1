from pathlib import Path
import csv
import math
from collections import defaultdict

def _transform_coord(s: str) -> float:
    sign = 1 if s[-1] == 'N' or s[-1] == 'E' else -1
    s = s[:-1]
    new_s = ''.join([x if x.isdigit() else '_' for x in s])
    d = 1
    r = 0
    for x in new_s.split('_'):
        if x:
            r += int(x) * d
            d /= 60
    return sign * r


def load_distances(info_fp: Path, edges_fp: Path):
    coords = {}
    with info_fp.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            country, lat, lon = row['country'], row['lat'], row['lon']
            lam = math.radians(_transform_coord(lat))
            phi = math.radians(_transform_coord(lon))
            coords[country] = (lam, phi)

    with edges_fp.open() as f:
        edges = [tuple(map(lambda x: x.strip(), x.strip().split('\t'))) for x in f.readlines() if x.strip()]

    ret = defaultdict(dict)
    for u, v in edges:
        lam1, phi1 = coords[u]
        lam2, phi2 = coords[v]
        dist = _calc_distance(lam1, phi1, lam2, phi2)
        ret[u][v] = dist
        ret[v][u] = dist
    return ret

def _calc_distance(lam1, phi1, lam2, phi2):
    r = 6371 * 1000
    d_phi = abs(phi2 - phi1)
    t = math.cos(lam1) * math.cos(lam2) * math.cos(d_phi) + math.sin(lam1) * math.sin(lam2)
    return r * math.acos(t)


