from flask import Blueprint
import json
from website.models.chyba import Chyba
from website.json_handlers.prubeh_rocniku_handling import get_datum_konce_registrace
from website.helpers.pretty_date import pretty_date



noauth_api = Blueprint("noauth_api", __name__)

@noauth_api.route("/chyby")
def chyby():
    return json.dumps(Chyba.get_all())

@noauth_api.route("/registrace")
def registrace():
    return get_datum_konce_registrace()

@noauth_api.route("/registrace_pretty")
def registrace_pretty():
    return pretty_date(get_datum_konce_registrace())


