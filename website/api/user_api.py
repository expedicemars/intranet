from flask import Blueprint
from flask_login import current_user
import json
import datetime
from website.helpers.pretty_date import pretty_date, pretty_datetime
from website.helpers.require_role_decorator import require_progress_na_ucastnikovi, require_role_on_current_user
from website.json_handlers.pohovory_handling import get_neobsazene_pohovory
from website.paths import velitel_odbornosti_data_path
from website.json_handlers.dostupne_omezeni import get_dostupne_odbornosti




user_api = Blueprint("user_api", __name__)

@user_api.route("/confirmed")
@require_role_on_current_user("user")
def confirmed():
    return json.dumps({"confirmation_status": current_user.confirmed})


@user_api.route("/uzamcene_zmeny")
@require_role_on_current_user("user")
def uzamcene_zmeny():
    return json.dumps({"status": current_user.uzamcene_zmeny})


@user_api.route("/volne_pohovory")
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("První kontakt")
def volne_pohovory():
    result = []
    for p in get_neobsazene_pohovory():
        if datetime.datetime.fromisoformat(p["iso"]) - datetime.timedelta(hours=48) > datetime.datetime.now():
            zaznam = {}
            zaznam["iso"] = p["iso"]
            zaznam["pretty"] = pretty_datetime(p["iso"])
            result.append(zaznam)
    return json.dumps(result)


@user_api.route("/datum_pohovoru")
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("První kontakt")
def datum_pohovoru():
    result = {
        "datum": pretty_datetime(current_user.datum_pohovoru),
        "link": current_user.meeting_link
        }
    return json.dumps(result)


@user_api.route("/kontakt_na_velitele_odbornosti/<string:odb>")
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Domácí projekt")
def kontakt_na_velitele_odbornosti(odb):
    with open(velitel_odbornosti_data_path()) as file:
        file = json.load(file)
    try:
        result = file[odb]
    except KeyError:
        return "Tahle odbornost neexistuje."
    if result == "":
        return "Tato odbornost kontakt ještě nezadala."
    else:
        return result


@user_api.route("/info")
@require_role_on_current_user("user")
def info():
    return current_user.get_info_na_ucet_stranku()


@user_api.route("/dostupne_odbornosti")
@require_progress_na_ucastnikovi("Domácí projekt")
@require_role_on_current_user("user")
def dostupne_odbornosti():
    return json.dumps(get_dostupne_odbornosti())


@user_api.route("/odpovedi_motivaku")
@require_role_on_current_user(["user"])
def odpovedi_motivaku():
    if current_user.motivacni_dotaznik:
        return current_user.motivacni_dotaznik
    else:
        return json.dumps([{"id": i, "odpoved": ""} for i in range(1,15)])