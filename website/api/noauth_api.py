from flask import Blueprint
import json
from website.models.chyba import Chyba
from website.json_handlers.prubeh_rocniku_handling import get_datum_konce_registrace, get_datum_zacatku_registrace
from website.json_handlers.dostupne_omezeni import get_dostupne_odbornosti, get_dostupne_progressy
from website.json_handlers.prubeh_rocniku_handling import get_koordinator_internetovych_kol, get_aktualni_faze, get_vsechny_faze


noauth_api = Blueprint("noauth_api", __name__)

@noauth_api.route("/chyby")
def chyby():
    return json.dumps(Chyba.get_all())


@noauth_api.route("/aktualni_faze")
def aktualni_faze():
    return json.dumps(get_aktualni_faze())


@noauth_api.route("/vsechny_faze")
def vsechny_faze():
    return json.dumps(get_vsechny_faze())


@noauth_api.route("/zacatek_registrace")
def zacatek_registrace():
    return get_datum_zacatku_registrace()


@noauth_api.route("/konec_registrace")
def konec_registrace():
    return get_datum_konce_registrace()


@noauth_api.route("/dostupne_odbornosti")
def dostupne_odbornosti():
    return json.dumps(get_dostupne_odbornosti())


@noauth_api.route("/dostupne_progressy")
def dostupne_progressy():
    return json.dumps(get_dostupne_progressy())


@noauth_api.route("/velitel_internetovych_kol_mail")
def velitel_internetovych_kol_mail():
    return get_koordinator_internetovych_kol()


