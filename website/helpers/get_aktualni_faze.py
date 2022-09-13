from website.paths.paths import faze_path
import json

def get_aktualni_faze() -> str:
    with open(faze_path()) as file:
        faze = json.load(file)
        return list(filter(lambda x: x["active"], faze))[0]["nazev"]

def je_registrace_otevrena() -> bool:
    if get_aktualni_faze() in ["uzavrene_registrace", "ukonceny_rocnik"]:
        otevreny = False
    else:
        otevreny = True
    return otevreny

def je_zadani_pristupne() -> bool:
    if get_aktualni_faze() in ["zpristupnena_zadani", "uzavrene_registrace"]:
        pristupne = True
    else:
        pristupne = False
    print(pristupne)
    return pristupne
