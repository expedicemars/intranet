from website.paths.paths import faze_path
import json

def get_aktualni_faze() -> dict:
    with open(faze_path()) as file:
        faze = json.load(file)
        return list(filter(lambda x: x["active"], faze))[0]

def je_registrace_otevrena() -> bool:
    aktualni_faze = get_aktualni_faze()
    if aktualni_faze["nazev"] in ["uzavrene_registrace", "ukonceny_rocnik"]:
        otevreny = False
    else:
        otevreny = True
    return otevreny
