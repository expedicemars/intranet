from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from website.models.chyba import Chyba
from website.models.user import User
from website.json_handlers.admin_handling import is_admin
from website.mails.mail_handler import mail_sender
from website import db
import json


default_views = Blueprint("default_views", __name__)

@default_views.route("/")
@default_views.route("/home")
def home():
    if current_user.is_authenticated:
        if is_admin(current_user.email):
            admin = True
        else:
            admin = False
    else:
        admin = False
    return render_template("home.html", admin = admin)


@default_views.route("/nahlasit_bug", methods=["GET", "POST"])
def nahlasit_bug():
    if request.method == "GET":
        return render_template("nahlasit_chybu.html")
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


@default_views.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "GET":
        return render_template("account.html", current_user=current_user)
    else:
        token = current_user.get_reset_token()
        mail_sender(mail_identifier="potvrzeni_emailu", target=current_user.email, data=token)
        flash("E-mail byl odeslán. Zkontrolujte si svou schránku.", category="info")
        return redirect(url_for("default_views.account"))

@default_views.route("/account/<token>", methods=["GET"])
@login_required
def account_verified(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("Obnovovací link vypršel, nebo je jinak neplatný.", category="info")
        return redirect(url_for("default_views.account"))
    else:
        user.confirmed = True
        db.session.commit()
        return redirect(url_for("default_views.account"))


@default_views.route("/known_bugs")
def known_bugs():
    return render_template("zname_chyby.html")

        