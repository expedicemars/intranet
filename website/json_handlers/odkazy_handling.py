import json
from website.paths import odkazy_path

def get_odkazy() -> list:
    with open(odkazy_path()) as file:
        return json.load(file)

def pridat_odkaz(nazev: str, adresa: str, kategorie_system_name: str) -> None:
    odkazy = get_odkazy()
    kategorie = next(filter(lambda x: x["system_name"] == kategorie_system_name, odkazy))
    kategorie["odkazy"].append(
        {
            "nazev": nazev,
            "adresa": adresa
        }     
    )
    with open(odkazy_path(), "w") as f:
        f.write(json.dumps(odkazy, indent=4))


def smazat_odkaz_by_name(name):
    odkazy = get_odkazy()
    for kategorie in odkazy:
        for radek in kategorie["odkazy"]:
            if radek["nazev"] == name:
                kategorie["odkazy"].remove(radek)
    with open(odkazy_path(), "w") as f:
        f.write(json.dumps(odkazy, indent=4))