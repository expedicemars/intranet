from flask import Blueprint, abort, send_file, flash, redirect, url_for
from flask_login import current_user
import json
from website.roles.role_handler import get_access_rights
from website.paths.paths import user_data_folder_path, zadani_folder_path, prohlaseni_path, exporty_path
from website.helpers.get_user_files import get_motivak_by_id, get_prace_filenames, get_profilovka_by_id

sender = Blueprint("sender", __name__)


@sender.route("/send_zadani/<string:odbornost>/<string:name>")
def send_zadani(odbornost, name):
    rights = get_access_rights(current_user)
    if "user" in rights or "admin" in rights: # připouštim oba, protože i úpravy termínů posílaj request sem
        if name == "__jmena":
            p = zadani_folder_path() / odbornost
            res = []
            for file in p.iterdir():
                res.append(file.name)
            if len(res) == 0:
                return json.dumps(None)
            else:
                return json.dumps(res)
        else:
            return send_file(zadani_folder_path() / odbornost / name)
    else:
        abort(401)


@sender.route("/send_motivak")
def send_motivak_min():
    return send_motivak(current_user.id, "file")

@sender.route("/send_motivak/<int:id>/<string:style>")
def send_motivak(id, style):
    """
    posila file motivaku. Zaroven resi opravneni:
    ma-li current_user pouze roli user, musi sedet jeho ID s poslanym ID. Pokud ma roli editing_users_allowed, muze requestnout i cizi motivaky.
    id: user_id
    style: file/name
    """
    rights = get_access_rights(current_user)
    if "editing_users_allowed" in rights:
        return get_motivak_by_id(id, style)
    elif "user" in rights:
        if current_user.id == id:
            return get_motivak_by_id(id, style)
        else:
            abort(401)
    else:
        abort(401)

@sender.route("/send_zip/<string:filename>")
def send_zip(filename):
    if "editing_prubeh_rocniku" in get_access_rights(current_user):
        for p in exporty_path().rglob("*.zip"):
            if p.name == filename:
                return send_file(p)
    else:
        abort(401)
