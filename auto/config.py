from pathlib import Path

_base_path = Path(__file__).resolve().parent.parent / "data"

EDGES_PATH = _base_path / "export.csv"
VERTICES_PATH = _base_path / "vertices.txt"
COUNTRIES_INFO_PATH = _base_path / "countries_info.csv"

