import json
import website.paths.paths as p
from website.json_handlers.logs_handling import log


"""
Tyhle soubory nejsou součástí version control, generujou se při spuštění appky.
"""

def check_known_bugs_file() -> None:
    bugs_path = p.known_bugs_path()
    if bugs_path.exists():
        log("Known bugs file already exists.")
    else:
        bugs_path.touch()
        with open(bugs_path, "w") as file:
            file.write(json.dumps([]))
        log("creating Known bugs file at " + str(bugs_path))
        

def check_logs_file() -> None:
    logs_path = p.log_file_path()
    if logs_path.exists():
        log("(this) log file already exists")
    else:
        logs_path.touch()
        log("creating (this) log file at  " + str(logs_path))


def check_mailing_list() -> None:
    mailing_list_path = p.mailing_list_path()
    if mailing_list_path.exists():
        log("Mailing list already exists.")
    else:
        mailing_list_path.touch()
        with open(mailing_list_path, "w") as file:
            file.write(json.dumps([]))
        log("Created mailing list at " + str(mailing_list_path))


def check_faze() -> None:
    faze_path = p.faze_path()
    if faze_path.exists():
        log("Fáze soubor already exists.")
    else:
        faze_path.touch()
        faze_default = [
            {
                "nazev": "otevrene_registrace",
                "popis": "Nov\u00ed u\u017eivatel\u00e9 se sm\u00ed registrovat, upravovat sv\u00e9 profily, nahr\u00e1vat motiv\u00e1ky. Roze\u0161le e-mail lidem, co \u010dekaj v mailing_listu",
                "nasledujici": "zpristupnena_zadani",
                "active": True
            },
            {
                "nazev": "zpristupnena_zadani",
                "popis": "Nov\u00ed u\u017eivatel\u00e9 se st\u00e1le sm\u00ed registrovat, registrovan\u00ed u\u017eivatel\u00e9 m\u016f\u017eou zvolit odbornost, nahl\u00ed\u017eet do zad\u00e1n\u00ed dom\u00e1c\u00edch kol nebo na deadliny.",
                "nasledujici": "uzavrene_registrace",
                "active": False
            },
            {
                "nazev": "uzavrene_registrace",
                "popis": "Nov\u00ed u\u017eivatel\u00e9 u\u017e se nemohou registrovat. P\u0159i registraci je to hod\u00ed na mailing_list, kterej bude d\u016fle\u017eitej potom. V t\u00e9to f\u00e1zi b\u011b\u017e\u00ed semi, fin\u00e1le, simulace, bal\u00f3n i eurotrip.",
                "nasledujici": "ukonceny_rocnik",
                "active": False
            },
            {
                "nazev": "ukonceny_rocnik",
                "popis": "Zaz\u00e1lohuje to data, vyma\u017ee u\u017eivatele, deadiny a obecn\u011b p\u0159iprav\u00ed na nov\u00fd ro\u010dn\u00edk. Otev\u0159\u00edt registrace?",
                "nasledujici": "otevrene_registrace",
                "active": False
            }
        ]
        with open(faze_path, "w") as file:
            file.write(json.dumps(faze_default, indent=4))
        log("Created faze at " + str(faze_path))


def check_terminy() -> None:
    terminy_path = p.terminy_path()
    if terminy_path.exists():
        log("Termíny soubor already exists.")
    else:
        terminy_path.touch()
        with open(terminy_path, "w") as file:
            # registrace tu bude vždycky
            file.write(json.dumps([
                {
                    "popis": "registrace",
                    "date": "2022-01-01"
                }
            ]))
        log("Created terminy at " + str(terminy_path))

def check_velitel_odbornosti_data() -> None:
    path = p.velitel_odbornosti_data_path()
    if path.exists():
        log("velitel_odbornosti data soubor už existuje.")
    else:
        path.touch()
        with open(path, "w") as file:
            file.write(json.dumps({
                "biolog": "",
                "fyzik": "",
                "konstrukter": "",
                "inzenyr": "",
                "popularizator": ""
            }, indent=4))
        log("Created terminy at " + str(path))

def check_user_data_folder() -> None:
    path = p.user_data_folder_path()
    if path.exists():
        log("Složka pro user data existuje.")
    else:
        path.mkdir()
        log("Vytvořena složka pro user data na "+ str(path))