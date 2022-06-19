from flask import Blueprint, abort
from flask_login import current_user
import json
from website.models.chyba import Chyba
from website.models.user import User
from website.json_handlers.logs_handling import get_logs
from website.roles.role_handler import get_access_rights, dostupna_omezeni
from website.paths.paths import terminy_path, faze_path
from website.hepers.mailing_list import get_mails_from_mailing_list


sender = Blueprint("sender", __name__)


@sender.route("/send_noauth/<string:query>")
def send_noauth(query):
    if query == "chyby":
        return json.dumps(Chyba.get_all())
    else:
        return f"Query {query} not found."

@sender.route("send_admin/<string:query>")
def send_admin(query):
    rights = get_access_rights(current_user)
    if query == "logs":
        if "editing_logs_allowed" in rights:
            return json.dumps(get_logs())
        else:
            abort(401)
    elif query == "users_from_db":
        if "editing_users_allowed" in rights or "editing_admins_allowed" in rights:
            return json.dumps([user.get_basic_info() for user in User.query.all()])
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

@sender.route("/send_user/<string:query>")
def send_user(query):
    rights = get_access_rights(current_user)
    if query == "terminy":
        if "user" in rights:
            with open(terminy_path()) as file:
                return json.dumps(json.load(file))
        else:
            abort(401)
