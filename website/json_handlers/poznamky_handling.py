import json
from website.paths import poznamky_path

def zapsat_poznamky(list_poznamek: list) -> None:
    with open(poznamky_path(), "w") as new:
        new.write(json.dumps(list_poznamek, indent=4))



