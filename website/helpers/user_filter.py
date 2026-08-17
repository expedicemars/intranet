from website.models.user import User
from website.models.hodnoceni import Hodnoceni
from website.models.motivacni_call import Motivacni_call
from website.models.hodnoceni import Hodnoceni
from typing import List
from website.paths import user_data_folder_path
from website.helpers.pretty_date import pretty_datetime, pretty_date

def user_filter(kriteria: dict) -> List[User]:
    users: list[User] = User.get_all()
    
    if kriteria["filtrovat_orgy"]:
        users = filter(lambda x: "admin" in x.role, users)
    else:
        users = filter(lambda x: "admin" not in x.role, users)
    
   # odbornost 
    if kriteria["odbornost"] == "jakakoli":
        pass
    elif kriteria["odbornost"] == "bez_odbornosti":
        users = filter(lambda x: x.odbornost == "zatím nevybraná", users)
    else:
        users = filter(lambda x: x.odbornost in kriteria["odbornost"], users)
        
    #původ
    if kriteria["puvod"] == "jakykoli":
        pass
    else:
        users = filter(lambda x: x.puvod in kriteria["puvod"], users)
    
    
    # postup
    if kriteria["postup"] == "jakykoli":
        pass
    else:
        users = filter(lambda x: x.progress in kriteria["postup"], users)
    
    #uzamcene_zmeny
    if kriteria["uzamcenost_zmen"] == "jakakoli":
        pass
    else:
        if "uzamcene_zmeny_callu" in kriteria["uzamcenost_zmen"]:
            users = filter(lambda x: x.uzamcene_zmeny_callu, users)
        if "uzamcene_zmeny_prace" in kriteria["uzamcenost_zmen"]:
            users = filter(lambda x: x.uzamcene_zmeny_prace, users)
        if "uzamcene_zmeny_udaju" in kriteria["uzamcenost_zmen"]:
            users = filter(lambda x: x.uzamcene_zmeny_udaju, users)
    
    # odevzdavani     
    if kriteria["odevzdavani"] == "nezalezi":
        pass
    elif kriteria["odevzdavani"] == "motivak_chybi":
        users = filter(lambda x: not x.datetime_odevzdani_motivaku, users)
    elif kriteria["odevzdavani"] == "motivak":
        users = filter(lambda x: x.datetime_odevzdani_motivaku and not x.datetime_odevzdani_shrnuti_prace, users)
    elif kriteria["odevzdavani"] == "chybi_shrnuti":
        users = filter(lambda x: x.progress == "Domácí projekt" and not x.datetime_odevzdani_shrnuti_prace, users)
    elif kriteria["odevzdavani"] == "shrnuti":
        users = filter(lambda x: x.datetime_odevzdani_shrnuti_prace, users)
    elif kriteria["odevzdavani"] == "chybi_prezentace":
        users = filter(lambda x: x.datetime_odevzdani_shrnuti_prace and not x.datetime_odevzdani_prezentace, users)

    # přítomnost na kolech   
    if kriteria["pritomnost"] == "nezalezi":
        pass
    elif kriteria["pritomnost"] == "konference":
        users = filter(lambda x: x.pritomen_na_konferenci, users)
    elif kriteria["pritomnost"] == "primi":
            users = filter(lambda x: x.pritomen_na_primi, users)
            
            
    # k-faktor
    users_pred_filtrem_k_faktor = users
    users = []
    if kriteria["k_faktor"] == "nezalezi":
        users = users_pred_filtrem_k_faktor
    else:
        for u in users_pred_filtrem_k_faktor:
            maximum = 0
            hodnoceni = Hodnoceni.get_by_user_id(u.id)
            for h in hodnoceni:
                if h.k_faktor > maximum:
                    maximum = h.k_faktor
            if maximum == int(kriteria["k_faktor"]):
                users.append(u)
    

    def ma_profilovku(user):
        path = user_data_folder_path() / str(user.id)
        for file in path.iterdir():
            if file.stem == "profilovka":
                return True
        else:
            return False
        
    def ma_datum_motivacniho_callu(user):
        m = Motivacni_call.get_by_user_id(user.id)
        if m:
            return True
        else:
            return False
    
    def ma_meeting_link(user):
        m = Motivacni_call.get_by_user_id(user.id)
        if m:
            if m.meeting_link in [None, ""]:
                return False
            else:
                return True
        else:
            return False
        
    if kriteria["udaj_ma"] == "profilovka":
        users = filter(lambda x: ma_profilovku(x), users)
    elif kriteria["udaj_ma"] == "jmeno":
        users = filter(lambda x: x.jmeno not in [None,""], users)
    elif kriteria["udaj_ma"] == "prijmeni":
        users = filter(lambda x: x.prijmeni not in [None,""], users)
    elif kriteria["udaj_ma"] == "adresa":
        users = filter(lambda x: x.adresa not in [None, ""], users)
    elif kriteria["udaj_ma"] == "telcislo":
        users = filter(lambda x: x.telcislo not in [None, ""], users)
    elif kriteria["udaj_ma"] == "mail_rodicu":
        users = filter(lambda x: x.mail_rodicu not in [None, ""], users)
    elif kriteria["udaj_ma"] == "datum_narozeni":
        users = filter(lambda x: x.datum_narozeni not in [None, ""], users)
    elif kriteria["udaj_ma"] == "rok_maturity":
        users = filter(lambda x: x.rok_maturity not in [None, ""], users)
    elif kriteria["udaj_ma"] == "puvod":
        users = filter(lambda x: x.puvod not in [None, ""], users)
    elif kriteria["udaj_ma"] == "tricko":
        users = filter(lambda x: x.tricko not in [None, ""], users)
    elif kriteria["udaj_ma"] == "dozvedeli":
        users = filter(lambda x: x.dozvedeli not in [None, ""], users)
    elif kriteria["udaj_ma"] == "alergie":
        users = filter(lambda x: x.alergie not in [None, ""], users)
    elif kriteria["udaj_ma"] == "skola":
        users = filter(lambda x: x.skola not in [None, ""], users)
    elif kriteria["udaj_ma"] == "datum_motivacniho_callu":
        users = filter(lambda x: ma_datum_motivacniho_callu(x), users)
    elif kriteria["udaj_ma"] == "meeting_link":
        users = filter(lambda x: ma_meeting_link(x), users)
    elif kriteria["udaj_ma"] == "hodnoceni": 
        users = filter(lambda x: Hodnoceni.get_by_user_id(x.id), users)
    elif kriteria["udaj_ma"] == "osloveni_1p":
        users = filter(lambda x: x.osloveni_1p not in [None, ""], users)
    elif kriteria["udaj_ma"] == "osloveni_5p":
        users = filter(lambda x: x.osloveni_5p not in [None, ""], users)
    elif kriteria["udaj_ma"] == "zajmeno":
        users = filter(lambda x: x.zajmeno not in [None, ""], users)
    
    if kriteria["udaj_nema"] == "profilovka":
        users = filter(lambda x: not ma_profilovku(x), users)
    elif kriteria["udaj_nema"] == "jmeno":
        users = filter(lambda x: x.jmeno in [None,""], users)
    elif kriteria["udaj_nema"] == "prijmeni":
        users = filter(lambda x: x.prijmeni in [None,""], users)
    elif kriteria["udaj_nema"] == "adresa":
        users = filter(lambda x: x.adresa in [None, ""], users)
    elif kriteria["udaj_nema"] == "telcislo":
        users = filter(lambda x: x.telcislo in [None, ""], users)
    elif kriteria["udaj_nema"] == "mail_rodicu":
        users = filter(lambda x: x.mail_rodicu in [None, ""], users)
    elif kriteria["udaj_nema"] == "datum_narozeni":
        users = filter(lambda x: x.datum_narozeni in [None, ""], users)
    elif kriteria["udaj_nema"] == "rok_maturity":
        users = filter(lambda x: x.rok_maturity in [None, ""], users)
    elif kriteria["udaj_nema"] == "puvod":
        users = filter(lambda x: x.puvod in [None, ""], users)
    elif kriteria["udaj_nema"] == "tricko":
        users = filter(lambda x: x.tricko in [None, ""], users)
    elif kriteria["udaj_nema"] == "dozvedeli":
        users = filter(lambda x: x.dozvedeli in [None, ""], users)
    elif kriteria["udaj_nema"] == "alergie":
        users = filter(lambda x: x.alergie in [None, ""], users)
    elif kriteria["udaj_nema"] == "skola":
        users = filter(lambda x: x.skola in [None, ""], users)
    elif kriteria["udaj_nema"] == "datum_motivacniho_callu":
        users = filter(lambda x: not ma_datum_motivacniho_callu(x), users)
    elif kriteria["udaj_nema"] == "meeting_link":
        users = filter(lambda x: not ma_meeting_link(x), users)
    elif kriteria["udaj_nema"] == "hodnoceni": 
        users = filter(lambda x: not Hodnoceni.get_by_user_id(x.id), users)
    elif kriteria["udaj_nema"] == "osloveni_1p":
        users = filter(lambda x: x.osloveni_1p in [None, ""], users)
    elif kriteria["udaj_nema"] == "osloveni_5p":
        users = filter(lambda x: x.osloveni_5p in [None, ""], users)
    elif kriteria["udaj_nema"] == "zajmeno":
        users = filter(lambda x: x.zajmeno in [None, ""], users)
    
    # list to je, abych to moh projíždět víckrát potom
    users = list(users)
    
    # řazení
    def none_safe_prijmeni(user: User) -> str:
        return user.prijmeni if user.prijmeni else ""
        
    
    if kriteria["razeni"] == "prijmeni":
        users = sorted(users, key = lambda u: none_safe_prijmeni(u))
    elif kriteria["razeni"] == "registrace":
        users = sorted(users, key = lambda u: u.datum_registrace)
    
    return users


def seznam_generator(kriteria: dict) -> dict:
    users = user_filter(kriteria)
    vypsat_list = kriteria["vypsat"]
    """
    struktura seznamu:
    {
        "emails": [         - emaily vsech useru
            "",
            ""
        ],
        "keys": [           - seznam tech sloupecku k vypsani
            "",
            ""
        ]
        "users": [          - data, ktera maji byt vypsana o kazdem uzivateli
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
        zaznam["id_na_link"] = u.id
        puvod = "Nevyplněný"
        if u.puvod == "cz":
            puvod = "Česká republika"
        elif u.puvod == "sk":
            puvod = "Slovensko"
        
        if "prazdny" in vypsat_list:
            zaznam["prazdny"] = ""
        if "id" in vypsat_list:
            zaznam["id"] = u.id
        if "email" in vypsat_list:
            zaznam["email"] = u.email
        if "confirmed" in vypsat_list:
            zaznam["confirmed"] = u.confirmed
        if "jmeno" in vypsat_list:
            zaznam["jmeno"] = u.jmeno
        if "prijmeni" in vypsat_list:
            zaznam["prijmeni"] = u.prijmeni
        if "adresa" in vypsat_list:
            zaznam["adresa"] = u.adresa
        if "telcislo" in vypsat_list:
            zaznam["telcislo"] = u.telcislo
        if "mail_rodicu" in vypsat_list:
            zaznam["mail_rodicu"] = u.mail_rodicu
        if "telcislo_rodicu" in vypsat_list:
            zaznam["telcislo_rodicu"] = u.telcislo_rodicu
        if "odbornost" in vypsat_list:
            zaznam["odbornost"] = u.odbornost
        if "datum_narozeni" in vypsat_list:
            zaznam["datum_narozeni"] = pretty_date(u.datum_narozeni)
        if "vek" in vypsat_list:
            zaznam["vek"] = u.calculate_age()
        if "rok_maturity" in vypsat_list:
            zaznam["rok_maturity"] = u.rok_maturity
        if "puvod" in vypsat_list:
            zaznam["puvod"] = puvod
        if "progress" in vypsat_list:
            zaznam["progress"] = u.progress
        if "tricko" in vypsat_list:
            zaznam["tricko"] = u.tricko
        if "dozvedeli" in vypsat_list:
            zaznam["dozvedeli"] = u.dozvedeli
        if "admin_poznamka" in vypsat_list:
            zaznam["admin_poznamka"] = u.admin_poznamka
        if "uzamcene_zmeny_prace" in vypsat_list:
            zaznam["uzamcene_zmeny_prace"] = "Uzamčené" if u.uzamcene_zmeny_prace else "Odemčené"
        if "uzamcene_zmeny_udaju" in vypsat_list:
            zaznam["uzamcene_zmeny_udaju"] = "Uzamčené" if u.uzamcene_zmeny_udaju else "Odemčené"
        if "uzamcene_zmeny_callu" in vypsat_list:
            zaznam["uzamcene_zmeny_callu"] = "Uzamčené" if u.uzamcene_zmeny_callu else "Odemčené"
        if "alergie" in vypsat_list:
            zaznam["alergie"] = u.alergie
        if "skola" in vypsat_list:
            zaznam["skola"] = u.skola
        if "datum_registrace" in vypsat_list:
            zaznam["datum_registrace"] = pretty_datetime(u.datum_registrace) 
        if "datum_motivacniho_callu" in vypsat_list:
            m = Motivacni_call.get_by_user_id(u.id)
            zaznam["datum_motivacniho_callu"] = pretty_datetime(m.datum) if m else None
        if "meeting_link" in vypsat_list:
            m = Motivacni_call.get_by_user_id(u.id)
            zaznam["meeting_link"] = m.meeting_link if m else None
        if "odevzdany_motivacni_dotaznik" in vypsat_list:
            zaznam["odevzdany_motivacni_dotaznik"] = "Odevzdaný" if u.odevzdany_motivacni_dotaznik else "Ještě ne"
        if "osloveni_1p" in vypsat_list:
            zaznam["osloveni_1p"] = u.osloveni_1p
        if "osloveni_5p" in vypsat_list:
            zaznam["osloveni_5p"] = u.osloveni_5p
        if "zajmeno" in vypsat_list:
            zaznam["zajmeno"] = u.zajmeno
        if "datetime_odevzdani_motivaku" in vypsat_list:
            zaznam["datetime_odevzdani_motivaku"] = pretty_datetime(u.datetime_odevzdani_motivaku)
        if "datetime_odevzdani_prezentace" in vypsat_list:
            zaznam["datetime_odevzdani_prezentace"] = pretty_datetime(u.datetime_odevzdani_prezentace)
        if "datetime_odevzdani_shrnuti_prace" in vypsat_list:
            zaznam["datetime_odevzdani_shrnuti_prace"] = pretty_datetime(u.datetime_odevzdani_shrnuti_prace)
        result["users"].append(zaznam)
    return result