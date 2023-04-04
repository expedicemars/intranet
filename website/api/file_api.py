from flask import Blueprint, send_file
from flask_login import current_user
import json
from website.helpers.require_role_decorator import require_role_on_current_user
from website.paths import user_data_folder_path, zadani_folder_path, prohlaseni_path, exporty_path
from website.helpers.get_user_files import get_prace_filenames, get_profilovka_by_id
from website.helpers.pretty_date import pretty_date, pretty_datetime


file_api = Blueprint("file_api", __name__)

@file_api.route("/prohlaseni_rodicu")
@require_role_on_current_user(["user","admin"])
def prohlaseni_rodicu():
    return send_file(prohlaseni_path())

@file_api.route("/user_profilovka")
@require_role_on_current_user("user")
def user_profilovka():
    return get_profilovka_by_id(current_user.id)

@file_api.route("/admin_profilovka/<int:id>")
@require_role_on_current_user("editing_users_allowed")
def admin_profilovka(id):   
    return get_profilovka_by_id(id)

@file_api.route("/vlastni_prace/<string:name>")
@require_role_on_current_user("user")
def vlastni_prace(name):
    p = user_data_folder_path() / str(current_user.id) / "prace" / name
    return send_file(p)

@file_api.route("/cizi_prace/<int:id>/<string:name>")
@require_role_on_current_user("editing_users_allowed")
def cizi_prace(id, name: str):
        p = user_data_folder_path() / str(id) / "prace" / name
        return send_file(p)
    
@file_api.route("/send_filenames_vlastni_prace")
@require_role_on_current_user("user")
def send_filenames_vlastni_prace():
    return get_prace_filenames(current_user.id)

@file_api.route("/send_filenames_cizi_prace/<int:id>")
@require_role_on_current_user("editing_users_allowed")
def send_filenames_cizi_prace(id):
    return get_prace_filenames(id)

@file_api.route("/filenames_vsech_zadani_v_odbornosti/<string:odbornost>")
@require_role_on_current_user(["user","admin"])
def filenames_vsech_zadani_v_odbornosti(odbornost):
    odbornost_path = zadani_folder_path() / odbornost
    result = []
    for file in odbornost_path.iterdir():
        result.append(file.name)
    return json.dumps(result)

@file_api.route("/zadani_file/<string:odbornost>/<string:filename>")
@require_role_on_current_user(["user","admin"])
def zadani_file(odbornost, filename):
    return send_file(zadani_folder_path() / odbornost / filename)

@file_api.route("/zadani_filenames_me_odbornosti")
@require_role_on_current_user(["user","admin"])
def zadani_filenames_me_odbornosti():
    return filenames_vsech_zadani_v_odbornosti(current_user.odbornost)

@file_api.route("/zadani_file_me_odbornosti/<string:filename>")
@require_role_on_current_user(["user","admin"])
def zadani_file_me_odbornost(filename):
    return zadani_file(current_user.odbornost, filename)


@file_api.route("/exporty_filenames")
@require_role_on_current_user("editing_prubeh_rocniku")
def exporty():
    result = []
    for p in exporty_path().iterdir():
        zaznam = {}
        if p.name == ".DS_Store":
            pass
        else:
            zaznam["datum"] = pretty_datetime(p.name)
            zaznam["iso"] = p.name
            for file in p.iterdir():
                if file.suffix == ".zip":
                    zaznam["filename"] = file.name
            result.append(zaznam)
    return json.dumps(result)


@file_api.route("/export/<string:filename>")
@require_role_on_current_user("editing_users_allowed")
def export(filename):
    for p in exporty_path().rglob("*.zip"):
            if p.name == filename:
                return send_file(p)