from flask import Blueprint
import json
from website.models.chyba import Chyba
from website.json_handlers.prubeh_rocniku_handling import get_datum_konce_registrace, get_datum_zacatku_registrace
from website.json_handlers.dostupne_omezeni import get_dostupne_odbornosti
from website.json_handlers.prubeh_rocniku_handling import get_koordinator_internetovych_kol
from website.helpers.pretty_date import pretty_datetime

import datetime



noauth_api = Blueprint("noauth_api", __name__)

@noauth_api.route("/chyby")
def chyby():
    return json.dumps(Chyba.get_all())

@noauth_api.route("/konec_registrace")
def konec_registrace():
    return get_datum_konce_registrace()


@noauth_api.route("/zacatek_registrace")
def zacatek_registrace():
    return get_datum_zacatku_registrace()

@noauth_api.route("/zacatek_registrace_pretty")
def zacatek_registrace_pretty():
    date = datetime.datetime.fromisoformat(get_datum_zacatku_registrace())
    td = datetime.timedelta(hours=23, minutes=59)
    return pretty_datetime(date + td)

@noauth_api.route("/konec_registrace_pretty")
def konec_registrace_pretty():
    date = datetime.datetime.fromisoformat(get_datum_konce_registrace())
    td = datetime.timedelta(hours=23, minutes=59)
    return pretty_datetime(date + td)

@noauth_api.route("/mit")
def mit():
    zacatek = datetime.datetime.fromisoformat(get_datum_zacatku_registrace())
    konec = datetime.datetime.fromisoformat(get_datum_konce_registrace())
    dnes = datetime.datetime.now()
    if dnes < zacatek:
        return "bude mít"
    elif dnes < konec:
        return "má"
    else:
        return "měl"

@noauth_api.route("/dostupne_odbornosti")
def dostupne_odbornosti():
    return json.dumps(get_dostupne_odbornosti())

@noauth_api.route("/velitel_internetovych_kol_mail")
def velitel_internetovych_kol_mail():
    return get_koordinator_internetovych_kol()


