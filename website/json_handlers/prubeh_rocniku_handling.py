from website.paths import prubeh_rocniku_path, info_o_konferenci_path
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

def toggle_registrace() -> None:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    f["otevrena_registrace"] = False if f["otevrena_registrace"] else True
    with open(prubeh_rocniku_path(), "w") as file:
        file.write(json.dumps(f, indent=4))

def get_registrace_otevrena() -> bool:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    return f["otevrena_registrace"]

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