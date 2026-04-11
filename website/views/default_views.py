import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from website.models.chyba import Chyba
from website.role_handler import get_access_rights, get_user_progress, get_info_o_konf_viditelne
from website.json_handlers.prubeh_rocniku_handling import get_zadani_viditelne, get_aktualni_faze, get_datum_zacatku_registrace_pretty, get_datum_konce_registrace_pretty
from website.mail_handler import mail_sender


default_views = Blueprint("default_views", __name__)

@default_views.route("/")
@default_views.route("/home")
def home():
    return render_template("guest/home.html", 
                           roles = get_access_rights(), 
                           user_progress = get_user_progress(),
                           zverejnena_zadani = get_zadani_viditelne(),
                           konf_viditelne = get_info_o_konf_viditelne(),
                           aktualni_faze_system_name = get_aktualni_faze()["system_name"],
                           datum_zacatku_registrace = get_datum_zacatku_registrace_pretty(),
                           datum_konce_registrace = get_datum_konce_registrace_pretty())


@default_views.route("/nahlasit_bug", methods=["GET", "POST"])
def nahlasit_bug():
    if request.method == "GET":
        return render_template("guest/nahlasit_chybu.html", roles = get_access_rights(), user_progress=get_user_progress(), konf_viditelne = get_info_o_konf_viditelne())
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
        mail_sender("novej_bug", "josef.latj@gmail.com")
        return redirect(url_for("default_views.known_bugs"))


@default_views.route("/known_bugs")
def known_bugs():
    return render_template("guest/zname_chyby.html", roles = get_access_rights(), user_progress=get_user_progress(), konf_viditelne = get_info_o_konf_viditelne())

@default_views.route("/kontakty")
def kontakty():
    return render_template("guest/kontakty.html", roles = get_access_rights(), user_progress=get_user_progress(), konf_viditelne = get_info_o_konf_viditelne())

@default_views.route("/repre_test")
def repre_test():
    return render_template("guest/repre_test.html", roles = get_access_rights())