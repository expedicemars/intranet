from flask import Blueprint
import json
from website.models.chyba import Chyba
from website.models.user import User
from website.json_handlers.logs_handling import get_logs
from website.roles.role_handler import get_access_rights, dostupna_omezeni


sender = Blueprint("sender", __name__)


@sender.route("/send_noauth/<string:query>")
def send_noauth(query):
    if query == "chyby":
        return json.dumps(Chyba.get_all())
    else:
        return f"Query {query} not found."

@sender.route("send_admin/<string:query>")
def send_admin(query):
    if query == "logs":
        return json.dumps(get_logs())
    elif query == "users_from_db":
        return json.dumps([user.get_basic_info() for user in User.query.all()])
    elif "role" in query:
        zadane_id = int(query.replace("role_",""))
        return json.dumps(get_access_rights(User.query.get(zadane_id))) 
    elif query == "vsechny_omezeni":
        return json.dumps(dostupna_omezeni)