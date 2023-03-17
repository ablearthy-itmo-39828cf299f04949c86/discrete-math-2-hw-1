from pathlib import Path
from typing import NamedTuple
import csv

class CountryCodes(NamedTuple):
    from_country_code: dict[str, str]
    to_country_code: dict[str, str]

def load_country_codes(fp: Path) -> CountryCodes:
    from_country_code = dict()
    to_country_code = dict()
    with fp.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            code, country = row['code'], row['country']
            from_country_code[code] = country
            to_country_code[country] = code
    return CountryCodes(from_country_code, to_country_code)
