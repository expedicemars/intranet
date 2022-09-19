from flask import Blueprint, abort, send_file, flash, redirect, url_for
from flask_login import current_user
import json
from website.models.chyba import Chyba
from website.models.user import User
from website.json_handlers.logs_handling import get_logs, get_alogs
from website.roles.role_handler import get_access_rights, dostupna_omezeni
from website.paths.paths import terminy_path, faze_path, velitel_odbornosti_data_path, user_data_folder_path, zadani_folder_path, default_profilovka_path, poznamky_path
from website.helpers.mailing_list import get_mails_from_mailing_list
from website.helpers.get_user_files import get_motivak_by_id, get_prace_filenames, get_profilovka_by_id
from website.json_handlers.pohovory_handling import get_pohovory
from website.helpers.pretty_date import pretty_date

sender = Blueprint("sender", __name__)


@sender.route("/send_noauth/<string:query>")
def send_noauth(query):
    if query == "chyby":
        return json.dumps(Chyba.get_all())
    elif query == "registrace":
        with open(terminy_path()) as file:
            file = json.load(file)
            for t in file:
                if t["popis"] == "registrace":
                    return json.dumps(t)
    else:
        return f"Query {query} not found."

@sender.route("send_admin/<string:query>")
def send_admin(query):
    rights = get_access_rights(current_user)
    if query == "app_logs":
        if "editing_logs_allowed" in rights:
            return json.dumps(get_logs())
        else:
            abort(401)
    elif query == "admin_logs":
        if "editing_logs_allowed" in rights:
            return json.dumps(get_alogs())
        else:
            abort(401)
    elif query == "users_from_db":
        if "editing_users_allowed" in rights or "editing_admins_allowed" in rights:
            return json.dumps([user.get_full_info() for user in User.query.all()])
        else:
            abort(401)
    elif "detail_usera_" in query:
        if "editing_users_allowed" in rights or "editing_admins_allowed" in rights:
            id = int(query.replace("detail_usera_", ""))
            u = User.query.get(id)
            return u.get_full_info()
        else:
            abort(401)
    elif "role" in query:
        if "editing_admins_allowed" in rights:
            zadane_id = int(query.replace("role_",""))
            return json.dumps(get_access_rights(User.query.get(zadane_id))) 
        else:
            abort(401)
    elif query == "vsechny_omezeni":
        if "editing_admins_allowed" in rights:
            return json.dumps(dostupna_omezeni)
        else:
            abort(401)
    elif query == "emaily_admin_editoru":
        if "admin" in rights:
            result = ""
            for u in User.query.all():
                if "editing_admins_allowed" in get_access_rights(u):
                    result += u.email
                    result += " "
            return result
        else:
            abort(401)
    elif query == "faze":
        if "prepinani_fazi_allowed" in rights:
            with open(faze_path()) as file:
                return json.dumps(json.load(file))
        else:
            abort(401)
    elif query == "mailing_list":
        if "prepinani_fazi_allowed" in rights:
            return json.dumps(get_mails_from_mailing_list())
        else:
            abort(401)
    elif query == "velitel_odbornosti_data":
        if "velitel_odbornosti" in rights:
            with open(velitel_odbornosti_data_path()) as file:
                return json.dumps(json.load(file))
        else:
            abort(401)
    elif query == "upozornit_na_zadani":
        if "prepinani_fazi_allowed" in rights:
                
            # getne maily registrovanejch useru
            result = []
            for u in User.query.all():
                u_rights = get_access_rights(u)
                if "user" in u_rights and "admin" not in u_rights:
                    result.append(u.email)
            return json.dumps(result)
        else:
            abort(401)
    elif query == "odbornosti_kterym_velim":
        if "velitel_odbornosti" in rights:
            return json.dumps([y.replace("velitel_odbornosti_", "") for y in filter(lambda x: "velitel_odbornosti_" in x, get_access_rights(current_user))])
        else:
            abort(401)
    elif query == "data_pro_motivaky_a_prace":
        if "editing_users_allowed" in rights:

            """
            Getne seznam uživatelů, jejich ID, data o tom, zda maj motivák, jména souborů prací a hodnocoení motiváku
            """
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
                    p =  p / "prace"
                    for file in p.iterdir():
                        zaznam["prace"].append(file.name)
                    zaznam["hodnoceni"] = u.hodnoceni_motivaku
                    result.append(zaznam)
            return json.dumps(result)
        else:
            abort(401)
    elif query == "poznamky":
        if "admin" in rights:
            with open(poznamky_path()) as file:
                return json.dumps(json.load(file))
        else:
            abort(401)
    elif query == "pohovory":
        if "editing_pohovory" in rights:
            result = []
            for p in get_pohovory():
                zaznam = {}
                zaznam["iso"] = p.isoformat()
                zaznam["pretty"] = pretty_date(p)
                result.append(zaznam)
            return json.dumps(result)
        else:
            abort(401)


@sender.route("/send_user/<string:query>")
def send_user(query: str):
    rights = get_access_rights(current_user)
    if query == "terminy":
        if "user" in rights or "admin" in rights: # připouštim oba, protože i úpravy termínů posílaj request sem
            with open(terminy_path()) as file:
                return json.dumps(json.load(file))
        else:
            abort(401)
    elif query == "info":
        if "user" in rights:
            return current_user.get_basic_info()
        else:
            abort(401)
    elif query == "kontakt_na_meho_velitele_odbornosti":
        if "user" in rights:
            if current_user.odbornost == "zatím nevybraná":
                return "nevybrano"
            else:
                with open(velitel_odbornosti_data_path()) as file:
                    file = json.load(file)
                return file[current_user.odbornost]
        else:
            abort(401)


@sender.route("/send_profilovka")
def send_profilovka_minimal():
    return send_profilovka(current_user.id)

@sender.route("/send_profilovka/<int:id>")
def send_profilovka(id):
    rights = get_access_rights(current_user)
    if "editing_users_allowed" in rights:
        return get_profilovka_by_id(id)
    elif "user" in rights:
        if id == current_user.id:
            return get_profilovka_by_id(id)
        else:
            abort(401)
    else:
        abort(401)


@sender.route("/send_prace_file/<string:name>")
def send_prace_file_minimal(name):
    return send_prace_file(current_user.id, name)


@sender.route("/send_prace_file/<int:id>/<string:filename>")
def send_prace_file(id, filename: str):
    rights = get_access_rights(current_user)
    if "editing_users_allowed" in rights:
        p = user_data_folder_path() / str(id) / "prace" / filename
        if p.exists():
            return send_file(p)
        else:
            flash("Tenhle soubor neexistuje", category="error")
            return redirect(url_for("default_views.home"))
    elif "user" in rights:
        if id == current_user.id:
            p = user_data_folder_path() / str(id) / "prace" / filename
            if p.exists():
                return send_file(p)
            else:
                flash("Tenhle soubor neexistuje", category="error")
                return redirect(url_for("default_views.home"))
        else:
            abort(401)
    else:
        abort(401)


@sender.route("/send_prace_filenames")
def send_prace_filenames_minimal():
    return send_prace_filenames(current_user.id)


@sender.route("/send_prace_filenames/<int:id>")
def send_prace_filenames(id):
    rights = get_access_rights(current_user)
    if "editing_users_allowed" in rights:
        return get_prace_filenames(id)
    elif "user" in rights:
        if id == current_user.id:
            return get_prace_filenames(id)
        else:
            abort(401)
    else:
        abort(401)


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


