from website.models.user import User
from typing import List
from website.paths.paths import user_data_folder_path
from website.helpers.pretty_date import pretty_date
from datetime import datetime

def user_filter(kriteria: dict) -> List[User]:
    users = User.query.all()
    if kriteria["odbornost"] == "jakakoli":
        pass
    else:
        users = filter(lambda x: x.odbornost in kriteria["odbornost"], users)
    
    if kriteria["postup"] == "jakykoli":
        pass
    else:
        users = filter(lambda x: x.progress in kriteria["postup"], users)
    
    if kriteria["udaj"] == "motivak":
        def ma_motivak(user):
            path = user_data_folder_path() / str(user.id)
            for file in path.iterdir():
                if file.stem == "motivak":
                    return True
            else:
                return False
        users = filter(lambda x: not ma_motivak(x), users)
    if kriteria["udaj"] == "prace":
        def ma_praci(user):
            path = user_data_folder_path() / str(user.id) / "prace"
            if len(list(path.iterdir())) == 0:
                return False
            else:
                return True
        users = filter(lambda x: not ma_praci(x), users)
    if kriteria["udaj"] == "profilovka":
        def ma_profilovku(user):
            path = user_data_folder_path() / str(user.id)
            for file in path.iterdir():
                if file.stem == "profilovka":
                    return True
            else:
                return False
        users = filter(lambda x: not ma_profilovku(x), users)
    if kriteria["udaj"] == "jmeno":
        users = filter(lambda x: x.jmeno is None, users)
    if kriteria["udaj"] == "telcislo":
        users = filter(lambda x: x.telcislo is None, users)
    if kriteria["udaj"] == "adresa":
        users = filter(lambda x: x.adresa is None, users)
    if kriteria["udaj"] == "mail_rodicu":
        users = filter(lambda x: x.mail_rodicu is None, users)
    if kriteria["udaj"] == "odbornost":
        users = filter(lambda x: x.odbornost is None, users)
    if kriteria["udaj"] == "datum_narozeni":
        users = filter(lambda x: x.datum_narozeni is None, users)
    if kriteria["udaj"] == "tricko":
        users = filter(lambda x: x.tricko is None, users)
    if kriteria["udaj"] == "dozvedeli":
        users = filter(lambda x: x.dozvedeli is None, users)
    if kriteria["udaj"] == "alergie":
        users = filter(lambda x: x.alergie is None, users)
    if kriteria["udaj"] == "skola":
        users = filter(lambda x: x.skola is None, users)


    return users


def seznam_generator(users: List[User], vypsat_list) -> dict:
    users = list(users)
    vypsat_list.insert(0, "jmeno_vypsat")
    """
    struktura seznamu:
    {
        "emails": [
            "",
            "",
            ... emaily všech těch userů
        ],
        "keys": [
            "",
            "",
            ... vypsat_list 
        ]
        "users": [
            {
                ...
            },
            {
                ...
            }
        ]
    }
    """


    result = {}
    result["emails"] = [u.email for u in users]
    result["keys"] = vypsat_list
    result["users"] = []
    for u in users:
        zaznam = {}
        zaznam["id"] = u.id
        if "prazdny_vypsat" in vypsat_list:
            zaznam["prazdny_vypsat"] = ""
        if "jmeno_vypsat" in vypsat_list:
            zaznam["jmeno_vypsat"] = u.jmeno
        if "email_vypsat" in vypsat_list:
            zaznam["email_vypsat"] = u.email
        if "telcislo_vypsat" in vypsat_list:
            zaznam["telcislo_vypsat"] = u.telcislo
        if "adresa_vypsat" in vypsat_list:
            zaznam["adresa_vypsat"] = u.adresa
        if "mail_rodicu_vypsat" in vypsat_list:
            zaznam["mail_rodicu_vypsat"] = u.mail_rodicu
        if "odbornost_vypsat" in vypsat_list:
            zaznam["odbornost_vypsat"] = u.odbornost
        if "progress_vypsat" in vypsat_list:
            zaznam["progress_vypsat"] = u.progress
        if "tricko_vypsat" in vypsat_list:
            zaznam["tricko_vypsat"] = u.tricko
        if "dozvedeli_vypsat" in vypsat_list:
            zaznam["dozvedeli_vypsat"] = u.dozvedeli
        if "alergie_vypsat" in vypsat_list:
            zaznam["alergie_vypsat"] = u.alergie
        if "skola_vypsat" in vypsat_list:
            zaznam["skola_vypsat"] = u.skola
        if "admin_poznamka_vypsat" in vypsat_list:
            zaznam["admin_poznamka_vypsat"] = u.admin_poznamka
        if "hodnoceni_vypsat" in vypsat_list:
            zaznam["hodnoceni_vypsat"] = u.hodnoceni_motivaku
        if "registrace_vypsat" in vypsat_list:
            zaznam["registrace_vypsat"] = pretty_date(u.datum_registrace) 
        if "pohovor_vypsat" in vypsat_list:
            zaznam["pohovor_vypsat"] = pretty_date(u.datum_pohovoru)
        if "meeting_link_vypsat" in vypsat_list:
            zaznam["meeting_link_vypsat"] = u.meeting_link
        result["users"].append(zaznam)
    return result