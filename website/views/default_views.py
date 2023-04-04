import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from website.models.chyba import Chyba
from website.role_handler import get_access_rights, get_user_progress
from website.json_handlers.prubeh_rocniku_handling import get_registrace_otevrena


default_views = Blueprint("default_views", __name__)

@default_views.route("/")
@default_views.route("/home")
def home():
    print(current_user)
    return render_template("home.html", roles = get_access_rights(current_user), otevrena_registrace = get_registrace_otevrena(), user_progress=get_user_progress())


@default_views.route("/nahlasit_bug", methods=["GET", "POST"])
def nahlasit_bug():
    if request.method == "GET":
        return render_template("nahlasit_chybu.html", roles = get_access_rights(current_user), user_progress=get_user_progress())
    else:
        popis=request.form.get("popis")
        if len(popis) > 1000:
            flash("Popis chyby byl delší než 1000 znaků. Zkuste to prosím vyjádřit stručněji.", category="error")
            return redirect(url_for("default_views.nahlasit_bug"))
        c = Chyba(
            autor=current_user.email if request.form.get(
                "include_name") else "Anonym",
            popis=request.form.get("popis")
        )
        c.pridat_do_chyb()
        return redirect(url_for("default_views.known_bugs"))


@default_views.route("/known_bugs")
def known_bugs():
    return render_template("zname_chyby.html", roles = get_access_rights(current_user), user_progress=get_user_progress())