from flask import Blueprint
import json
from website.models.chyba import Chyba
from website.json_handlers.prubeh_rocniku_handling import get_datum_konce_registrace
from website.json_handlers.dostupne_omezeni import get_dostupne_odbornosti
from website.json_handlers.prubeh_rocniku_handling import get_koordinator_internetovych_kol
from website.helpers.pretty_date import pretty_datetime

import datetime



noauth_api = Blueprint("noauth_api", __name__)

@noauth_api.route("/chyby")
def chyby():
    return json.dumps(Chyba.get_all())

@noauth_api.route("/registrace")
def registrace():
    return get_datum_konce_registrace()

@noauth_api.route("/registrace_pretty")
def registrace_pretty():
    date = datetime.datetime.fromisoformat(get_datum_konce_registrace())
    td = datetime.timedelta(hours=23, minutes=59)
    return pretty_datetime(date + td)

@noauth_api.route("/dostupne_odbornosti")
def dostupne_odbornosti():
    return json.dumps(get_dostupne_odbornosti())

@noauth_api.route("/velitel_internetovych_kol_mail")
def velitel_internetovych_kol_mail():
    return get_koordinator_internetovych_kol()


