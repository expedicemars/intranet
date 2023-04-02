from flask import Blueprint
from flask_login import current_user
import json
from website.helpers.pretty_date import pretty_date
from website.helpers.require_role_decorator import require_role_on_current_user
from website.json_handlers.pohovory_handling import get_neobsazene_pohovory
from website.paths.paths import velitel_odbornosti_data_path




user_api = Blueprint("user_api", __name__)

@user_api.route("/confirmed")
@require_role_on_current_user("user")
def confirmed():
    return json.dumps({
                "confirmation_status": current_user.confirmed
            })


@user_api.route("/volne_pohovory")
@require_role_on_current_user("user")
def volne_pohovory():
    result = []
    for p in get_neobsazene_pohovory():
        zaznam = {}
        zaznam["iso"] = p["iso"]
        zaznam["pretty"] = pretty_date(p["iso"])
        result.append(zaznam)
    return json.dumps(result)


@user_api.route("/datum_pohovoru")
@require_role_on_current_user("user")
def datum_pohovoru():
    result = {
        "datum": pretty_date(current_user.datum_pohovoru),
        "link": current_user.meeting_link
        }
    return json.dumps(result)


@user_api.route("/kontakt_na_meho_velitele_odbornosti")
@require_role_on_current_user("user")
def kontakt_na_meho_velitele_odbornosti():
    if current_user.odbornost == "zatím nevybraná":
        return "nevybrano"
    else:
        with open(velitel_odbornosti_data_path()) as file:
            file = json.load(file)
        return file[current_user.odbornost]


@user_api.route("/info")
@require_role_on_current_user("user")
def info():
    return current_user.get_basic_info()


# @user_api.route("/confirmed")
# @require_role_on_current_user("user")
# def confirmed():
#     return


