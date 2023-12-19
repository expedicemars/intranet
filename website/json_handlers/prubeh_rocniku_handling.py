from website.paths import prubeh_rocniku_path, info_o_konferenci_path, faze_path
import datetime
from website.helpers.pretty_date import pretty_datetime
import json

def set_nove_datum_konce_registrace(datum: str) -> None:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    f["datum_konce_registrace"] = datum
    with open(prubeh_rocniku_path(), "w") as file:
        file.write(json.dumps(f, indent=4))
        
def set_nove_datum_zacatku_registrace(datum: str) -> None:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    f["datum_zacatku_registrace"] = datum
    with open(prubeh_rocniku_path(), "w") as file:
        file.write(json.dumps(f, indent=4))

def get_datum_konce_registrace() -> str:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    return f["datum_konce_registrace"]

def get_datum_zacatku_registrace() -> str:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    return f["datum_zacatku_registrace"]

def get_datum_zacatku_registrace_pretty() -> str:
    date = datetime.datetime.fromisoformat(get_datum_zacatku_registrace())
    td = datetime.timedelta(hours=23, minutes=59)
    return pretty_datetime(date + td)

def get_datum_konce_registrace_pretty() -> str:
    date = datetime.datetime.fromisoformat(get_datum_konce_registrace())
    td = datetime.timedelta(hours=23, minutes=59)
    return pretty_datetime(date + td)


def toggle_zadani() -> None:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    f["viditelna_zadani"] = False if f["viditelna_zadani"] else True
    with open(prubeh_rocniku_path(), "w") as file:
        file.write(json.dumps(f, indent=4))


def get_zadani_viditelne() -> bool:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    return f["viditelna_zadani"]


def toggle_info_o_konferenci() -> None:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    f["info_o_konferenci_viditelne"] = False if f["info_o_konferenci_viditelne"] else True
    with open(prubeh_rocniku_path(), "w") as file:
        file.write(json.dumps(f, indent=4))


def get_info_o_konferenci_viditelne() -> bool:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    return f["info_o_konferenci_viditelne"]


def get_aktualni_faze() -> dict:
    with open(prubeh_rocniku_path()) as file:
        aktualni_faze_system_name =json.load(file)["aktualni_faze"]
    with open(faze_path()) as file:
        return list(filter(lambda x: x["system_name"] == aktualni_faze_system_name, json.load(file)))[0]


def set_aktualni_faze_system_name(name: str) -> None:
    with open(prubeh_rocniku_path()) as file:
        file = json.load(file)
    file["aktualni_faze"] = name
    with open(prubeh_rocniku_path(), "w") as new:
        new.write(json.dumps(file, indent=4))


def get_vsechny_faze() -> dict:
    with open(faze_path()) as file:
        return json.load(file)


def zapsat_koordinatora_i_kol(mail) -> None:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    f["koordinator_internetovych_kol"] = mail
    with open(prubeh_rocniku_path(), "w") as file:
        file.write(json.dumps(f, indent=4))


def get_koordinator_internetovych_kol():
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    try:
        return f["koordinator_internetovych_kol"]
    except KeyError:
        return ""
        
        
def get_info_o_konferenci():
    with open(info_o_konferenci_path()) as file:
        return file.read()
    

def zapsat_info_o_konferenci(data):
    with open(info_o_konferenci_path(), "w") as file:
        file.write(data)
        
        
def get_mezni_hodiny_pro_cally() -> int:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
        return int(f["hodiny_motivacni_call"])
    
    
def save_mezni_hodiny_pro_cally(h: int):
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    f["hodiny_motivacni_call"] = h
    with open(prubeh_rocniku_path(), "w") as file:
        file.write(json.dumps(f, indent=4))