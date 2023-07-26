import json
import website.paths as p
from website.json_handlers.logs_handling import log
from datetime import date
from website.json_handlers.dostupne_omezeni import get_dostupne_odbornosti


"""
Tyhle soubory nejsou součástí version control, generujou se při spuštění appky.
"""

def check_known_bugs_file() -> None:
    bugs_path = p.known_bugs_path()
    if bugs_path.exists():
        log("soubor known bugs už existuje.")
    else:
        bugs_path.touch()
        with open(bugs_path, "w") as file:
            file.write(json.dumps([]))
        log("zakládám soubor known bugs na " + str(bugs_path))
        

def check_logs_files() -> None:
    app_logs_path = p.app_logs_file_path()
    if app_logs_path.exists():
        log("(tento) soubor na app logy už existuje.")
    else:
        app_logs_path.touch()
        log("vytvářím (tento) soubor na app logy na " + str(app_logs_path))
    
    admin_logs_path = p.admin_logs_file_path()
    if admin_logs_path.exists():
        log("Soubor na admin logy už existuje.")
    else:
        admin_logs_path.touch()
        log("Vytvářím soubor na admin logy na " + str(admin_logs_path))
    


def check_mailing_list() -> None:
    mailing_list_path = p.mailing_list_path()
    if mailing_list_path.exists():
        log("soubor pro mailing list už existuje.")
    else:
        mailing_list_path.touch()
        with open(mailing_list_path, "w") as file:
            file.write(json.dumps([]))
        log("vytvářim mailing list na " + str(mailing_list_path))


def check_velitel_odbornosti_data() -> None:
    path = p.velitel_odbornosti_data_path()
    if path.exists():
        log("soubor velitel_odbornosti už existuje.")
    else:
        path.touch()
        with open(path, "w") as file:
            file.write(json.dumps({o["system_name"]:"" for o in get_dostupne_odbornosti()}, indent=4))
        log("Zakládam soubor na velitele odborností na " + str(path))

def check_user_data_folder() -> None:
    path = p.user_data_folder_path()
    if path.exists():
        log("Složka pro user data existuje.")
    else:
        path.mkdir()
        log("Vytvořena složka pro user data na "+ str(path))

def check_zadani_folders() -> None:
    path = p.zadani_folder_path()
    if path.exists():
        log("Složka pro zadání už existuje.")
    else:
        path.mkdir()
        for odbornost in get_dostupne_odbornosti():
            _path = path / odbornost["system_name"]
            _path.mkdir()
        log("Vytvořena složka pro zadání na "+str(path))

def check_poznamky() -> None:
    path = p.poznamky_path()
    if path.exists():
        log("Soubor na poznámky už existuje.")
    else:
        path.touch()
        with open(path, "w") as file:
            file.write(json.dumps([], indent=4))
        log("Založen soubor na poznámky na " + str(path))

def check_pohovory() -> None:
    path = p.pohovory_path()
    if path.exists():
        log("Soubor na pohovory už existuje.")
    else:
        path.touch()
        with open(path, "w") as file:
            file.write(json.dumps([], indent=4))
        log("Založen soubor na pohovory na " + str(path))

def check_exporty() -> None:
    path = p.exporty_path()
    if path.exists():
        log("Složka pro export už existuje.")
    else:
        path.mkdir()
        log("Vytvořena složka pro export na "+str(path))
        
def check_odkazy() -> None:
    path = p.odkazy_path()
    if path.exists():
        log("Soubor na odkazy už existuje.")
    else:
        path.touch()
        with open(path, "w") as file:
            file.write(json.dumps([], indent=4))
        log("Založen soubor na pohovory na " + str(path))
        
def check_prubeh_rocniku() -> None:
    path = p.prubeh_rocniku_path()
    if path.exists():
        log("Soubor na průběh ročníku už existuje.")
    else:
        path.touch()
        with open(path, "w") as file:
            file.write(json.dumps({"datum_konce_registrace":str(date.today()),"otevrena_registrace":False,"viditelna_zadani":False}, indent=4))
        log("Založen soubor na pohovory na " + str(path))