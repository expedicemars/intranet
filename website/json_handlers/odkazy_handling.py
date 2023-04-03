import json
from website.paths import odkazy_path

def pridat_odkaz(popis: str, odkaz: str) -> None:
    with open(odkazy_path()) as file:
        file = json.load(file)
    file.append({
        "popis": popis,
        "odkaz": odkaz
    })
    with open(odkazy_path(), "w") as f:
        f.write(json.dumps(file, indent=4))

def get_odkazy() -> list:
    with open(odkazy_path()) as file:
        return json.load(file)

def smazat_odkaz_by_id(i):
    with open(odkazy_path()) as file:
        file = json.load(file)
    file.pop(int(i))
    with open(odkazy_path(), "w") as f:
        f.write(json.dumps(file, indent=4))