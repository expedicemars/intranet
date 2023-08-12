from flask import Blueprint
from flask_login import current_user
import json
from website.helpers.require_role_decorator import require_role_on_current_user
from website.json_handlers.logs_handling import get_logs, get_alogs
from website.json_handlers.prubeh_rocniku_handling import get_registrace_otevrena, get_zadani_viditelne, get_koordinator_internetovych_kol
from website.json_handlers.odkazy_handling import get_odkazy
from website.helpers.pretty_date import pretty_datetime
from website.paths import velitel_odbornosti_data_path, poznamky_path, prohlaseni_path, sablony_folder_path
from website.models.user import User
from website.models.chyba import Chyba
from website.models.hodnoceni import Hodnoceni
from website.json_handlers.pohovory_handling import get_pohovory
from website.role_handler import get_access_rights
from website.json_handlers.dostupne_omezeni import get_dostupne_progressy, get_dostupne_role, get_dostupne_odbornosti
from website.json_handlers.mailing_list import get_mails_from_mailing_list


admin_api = Blueprint("admin_api", __name__)


@admin_api.route("/app_logs")
@require_role_on_current_user("editing_logs_allowed")
def app_logs():
    return json.dumps(get_logs())


@admin_api.route("/admin_logs")
@require_role_on_current_user("editing_logs_allowed")
def admin_logs():
    return json.dumps(get_alogs())


@admin_api.route("/je_registrace_otevrena")
@require_role_on_current_user("editing_prubeh_rocniku")
def je_registrace_otevrena():
    return str(get_registrace_otevrena())

@admin_api.route("/je_zadani_viditelne")
@require_role_on_current_user("editing_prubeh_rocniku")
def je_zadani_viditelne():
    return str(get_zadani_viditelne())


@admin_api.route("/odkazy")
@require_role_on_current_user("admin")
def odkazy():
    return get_odkazy()

@admin_api.route("koordinator_internetovych_kol")
@require_role_on_current_user("editing_prubeh_rocniku")
def koordinator_internetovych_kol():
    return get_koordinator_internetovych_kol()

@admin_api.route("/soubory_existuji")
@require_role_on_current_user("admin")
def soubory_existuji():
    result = {
        "prohlaseni_rodicu": prohlaseni_path().exists()
    }
    for odb in get_dostupne_odbornosti():
        filename = odb["system_name"] + "_sablona.docx"
        path = sablony_folder_path() / filename
        result[odb["system_name"]] = path.exists()
    return result


@admin_api.route("/pohovory")
@require_role_on_current_user("editing_pohovory")
def pohovory():
    result = []
    for p in get_pohovory():
        zaznam = {}
        zaznam["iso"] = p["iso"]
        zaznam["pretty"] = pretty_datetime(p["iso"])
        zaznam["user"] = p["user"]
        zaznam["admin"] = p["admin"]
        if p["user"]:
            u = User.get_by_id(p["user"])
            zaznam["jmeno"] = u.jmeno
            zaznam["link"] = u.meeting_link
            #  aby bylo clickable, i když nemá jméno ještě:
            if u.jmeno == "":
                zaznam["jmeno"] = "Dosud nevyplnil jméno"
        else:
            zaznam["jmeno"] = None
            zaznam["link"] = None

        result.append(zaznam)
    return json.dumps(result)


@admin_api.route("/poznamky")
@require_role_on_current_user("admin")
def poznamky():
    with open(poznamky_path()) as file:
        return json.dumps(json.load(file))


@admin_api.route("/odbornosti_kterym_velim")
@require_role_on_current_user("velitel_odbornosti")
def odbornosti_kterym_velim():
    return json.dumps([y.replace("velitel_odbornosti_", "") for y in filter(lambda x: "velitel_odbornosti_" in x, get_access_rights())])


@admin_api.route("/velitel_odbornosti_data")
@require_role_on_current_user("velitel_odbornosti")
def velitel_odbornosti_data():
    with open(velitel_odbornosti_data_path()) as file:
        return json.dumps(json.load(file))


@admin_api.route("/mailing_list")
@require_role_on_current_user("admin")
def mailing_list():
    return json.dumps(get_mails_from_mailing_list())


@admin_api.route("/emaily_admin_editoru")
@require_role_on_current_user("admin")
def emaily_admin_editoru():
    result = ""
    for u in User.get_all():
        if "editing_admins_allowed" in get_access_rights(u):
            result += u.email
            result += " "
    return result


@admin_api.route("/vsechny_omezeni")
@require_role_on_current_user("editing_admins_allowed")
def vsechny_omezeni():
    return json.dumps(get_dostupne_role())

@admin_api.route("/vsechny_progressy")
@require_role_on_current_user(["editing_users_allowed", "editing_admins_allowed"])
def vsechny_progressy():
    return json.dumps(get_dostupne_progressy())


@admin_api.route("/role/<int:id>")
@require_role_on_current_user("editing_admins_allowed")
def role(id):
    return json.dumps(get_access_rights(User.get_by_id(id)))


@admin_api.route("/detail_usera/<int:id>")
@require_role_on_current_user(["editing_users_allowed", "editing_admins_allowed"])
def detail_usera(id):
    u = User.get_by_id(id)
    return u.get_info_na_detail_usera()

@admin_api.route("/hodnoceni/<int:id>")
@require_role_on_current_user("editing_users_allowed")
def hodnoceni(id):
    return json.dumps([h.to_dict() for h in Hodnoceni.get_by_user_id(id)])


@admin_api.route("/ucastnici")
@require_role_on_current_user("editing_users_allowed")
def ucastnici():
    return json.dumps([{"id": u.id, "email": u.email, "jmeno": u.jmeno} for u in User.get_all() if "admin" not in json.loads(u.role)])

@admin_api.route("/organizatori")
@require_role_on_current_user("editing_users_allowed")
def organizatori():
    return json.dumps([{"id": u.id, "email": u.email, "jmeno": u.jmeno} for u in User.get_all() if "admin" in json.loads(u.role)])

@admin_api.route("/useri_na_jmenovani_adminu")
@require_role_on_current_user("editing_admins_allowed")
def useri_na_jmenovani_adminu():
    result = {
        "admins": [],
        "users": []
    }
    for u in User.get_all():
        if "admin" in json.loads(u.role):
            result["admins"].append({"id": u.id,"email": u.email, "jmeno": u.jmeno})
        else:
            result["users"].append({"id": u.id,"email": u.email, "jmeno": u.jmeno})
    return json.dumps(result)

@admin_api.route("/statistiky")
@require_role_on_current_user("admin")
def statistiky():
    ucastnici = [u for u in User.get_all() if "admin" not in json.loads(u.role)]
    
    result =  {
        "registrovanych": len(ucastnici),
        "domaci_kolo": len(list(filter(lambda x: x.progress in ["Domácí projekt", "Přípravná mise", "Simulovaná mise"], ucastnici))),
        "pripravna_mise": len(list(filter(lambda x: x.progress in ["Přípravná mise", "Simulovaná mise"], ucastnici))),
        "simulovana_mise": len(list(filter(lambda x: x.progress == "Simulovaná mise", ucastnici))),
        "pocet_bugu": Chyba.pocet_neresenych()
    }

    for odb in get_dostupne_odbornosti():
        result[odb["system_name"]] = len(list(filter(lambda x: x.odbornost == odb["system_name"], ucastnici)))

    return result