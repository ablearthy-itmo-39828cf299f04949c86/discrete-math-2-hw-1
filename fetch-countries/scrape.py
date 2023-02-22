import httpx
from bs4 import BeautifulSoup
from pathlib import Path


def fetch_or_get_cached(url, path):
    if path.is_file():
        with open(path, "rb") as f:
            content = f.read()
            return content
    else:
        content = httpx.get(url).content
        with open(path, "wb") as f:
            f.write(content)
        return content


def fetch_europe_countries():
    countries = {}
    URL = "https://simple.wikipedia.org/wiki/List_of_European_countries"
    CACHED_PATH = Path(__file__).parent / Path("cached_europe.html")
    content = fetch_or_get_cached(URL, CACHED_PATH)
    soup = BeautifulSoup(content, "lxml")
    table = soup.select_one("table.wikitable.sortable")
    if table is None:
        print("An error occured while fetching land borders table")
        exit(1)
    for row in table.select("tbody tr"):
        elems = row.select("td")
        if len(elems) != 5:
            continue
        country = [el.text.strip() for el in elems[0].select("a") if el.get("title") is not None and el.select_one("img") is None]
        country = elems[0].text.strip() if not country else country[0]
        countries[country] = elems[-1].text.strip()
    return countries




def fetch_land_borders():
    ret = {}
    URL = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_number_of_land_borders"
    CACHED_PATH = Path(__file__).parent / Path("cached.html")
    content = fetch_or_get_cached(URL, CACHED_PATH)

    soup = BeautifulSoup(content, "lxml")
    table = soup.select_one("table.wikitable")
    if table is None:
        print("An error occured while fetching land borders table")
        exit(1)

    for row in table.select("tbody tr"):
        elems = row.select("td")
        if len(elems) != 6:
            continue
        if elems[0].text.strip().startswith("United Kingdom (plus British Overseas Territories and Crown Dependencies)") or elems[0].text.strip().startswith("Cyprus"):
            continue
        # if elems[0].select_one("div.mw-collapsible"):
        #     print(elems[0].text.strip())
        # src_country = None
        # src_country = [x.get("title").strip() for x in elems[0].select("a") if x.get("title") is not None][0]
        src_country = (elems[0].select_one("b") or elems[0]).text.strip()
        dest_countries = [x.text.strip() for x in elems[-1].select("a") if x.get("title") is not None]
        ret[src_country] = dest_countries
    return ret


def main():
    aliases = {'France, Metropolitan': 'France'}
    edges = []
    countries = fetch_europe_countries()
    borders = fetch_land_borders()

    for a, b in aliases.items():
        borders[b] = borders[a]

    for country in countries:
        if country in borders:
            for b in borders[country]:
                if b in countries:
                    edges.append((b, country))

    visited = []
    with open("edges.csv", "w") as f:
        for u, v in edges:
            if (v, u) in visited:
                continue
            visited.append((u, v))
            f.write(f"{u}\t{v}\n")

    with open("vertices.txt", "w") as f:
        for c in countries:
            f.write(f"{c}\n")




if __name__ == "__main__":
    main()
