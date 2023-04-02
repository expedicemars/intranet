from flask import Blueprint, abort, send_file, flash, redirect, url_for
from flask_login import current_user
import json
from website.helpers.require_role_decorator import require_role_on_current_user
from website.json_handlers.logs_handling import get_logs, get_alogs
from website.json_handlers.prubeh_rocniku_handling import get_registrace_otevrena
from website.json_handlers.odkazy_handling import get_odkazy
from website.helpers.pretty_date import pretty_date
from website.paths.paths import velitel_odbornosti_data_path, user_data_folder_path, zadani_folder_path, default_profilovka_path, poznamky_path, prohlaseni_path, exporty_path, prubeh_rocniku_path
from website.models.user import User
from website.json_handlers.pohovory_handling import get_pohovory, get_neobsazene_pohovory
from website.roles.role_handler import get_access_rights, dostupna_omezeni
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


@admin_api.route("/odkazy")
@require_role_on_current_user("admin")
def odkazy():
    return get_odkazy()


@admin_api.route("/exporty")
@require_role_on_current_user("editing_prubeh_rocniku")
def exporty():
    result = []
    for p in exporty_path().iterdir():
        zaznam = {}
        if p.name == ".DS_Store":
            pass
        else:
            zaznam["datum"] = pretty_date(p.name)
            zaznam["iso"] = p.name
            for file in p.iterdir():
                if file.suffix == ".zip":
                    zaznam["filename"] = file.name
            result.append(zaznam)
    return json.dumps(result)


@admin_api.route("/prohlaseni_rodicu_existuje")
@require_role_on_current_user("admin")
def prohlaseni_rodicu_existuje():
    return json.dumps({"existuje": prohlaseni_path().exists()})


@admin_api.route("/pohovory")
@require_role_on_current_user("editing_pohovory")
def pohovory():
    result = []
    for p in get_pohovory():
        zaznam = {}
        zaznam["iso"] = p["iso"]
        zaznam["pretty"] = pretty_date(p["iso"])
        zaznam["user"] = p["user"]
        if p["user"]:
            u = User.query.get(int(p["user"]))
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


@admin_api.route("/data_pro_motivaky_a_prace")
@require_role_on_current_user("editing_users_allowed")
def data_pro_motivaky_a_prace():
    result = []
    for u in User.query.all():
        if "admin" in get_access_rights(u):
            pass
        else:
            zaznam = {}
            zaznam["jmeno"] = u.jmeno
            zaznam["id"] = u.id
            p = user_data_folder_path() / str(u.id)
            for file in p.iterdir():
                if file.stem == "motivak":
                    zaznam["motivak"] = True
                    break
            else:
                zaznam["motivak"] = False
            zaznam["prace"] = []
            p = p / "prace"
            for file in p.iterdir():
                zaznam["prace"].append(file.name)
            zaznam["hodnoceni"] = u.hodnoceni_motivaku
            result.append(zaznam)
    return json.dumps(result)


@admin_api.route("/odbornosti_kterym_velim")
@require_role_on_current_user("velitel_odbornosti")
def odbornosti_kterym_velim():
    return json.dumps([y.replace("velitel_odbornosti_", "") for y in filter(lambda x: "velitel_odbornosti_" in x, get_access_rights(current_user))])


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
    for u in User.query.all():
        if "editing_admins_allowed" in get_access_rights(u):
            result += u.email
            result += " "
    return result


@admin_api.route("/vsechny_omezeni")
@require_role_on_current_user("editing_admins_allowed")
def vsechny_omezeni():
    return json.dumps(dostupna_omezeni)


@admin_api.route("/role/<int:id>")
@require_role_on_current_user("editing_admins_allowed")
def role(id):
    return json.dumps(get_access_rights(User.query.get(id)))


@admin_api.route("/detail_usera/<int:id>")
@require_role_on_current_user(["editing_users_allowed", "editing_admins_allowed"])
def detail_usera(id):
    u = User.query.get(id)
    return u.get_full_info()


@admin_api.route("/users_from_db")
@require_role_on_current_user(["editing_users_allowed", "editing_admins_allowed"])
def users_from_db():
    return json.dumps([user.get_full_info() for user in User.query.all()])