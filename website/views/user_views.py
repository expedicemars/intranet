from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from website.models.user import User
from website.mails.mail_handler import mail_sender
from website import db
from website.roles.role_handler import get_access_rights

user_views = Blueprint("user_views", __name__)



@user_views.route("/account", methods=["GET", "POST"])
def account():
    if "user" in get_access_rights(current_user):
        if request.method == "GET":
            return render_template("account.html", current_user = current_user, roles = get_access_rights(current_user))
        else:
            token = current_user.get_reset_token()
            mail_sender(mail_identifier="potvrzeni_emailu", target=current_user.email, data=token)
            flash("E-mail byl odeslán. Zkontrolujte si svou schránku.", category="info")
            return redirect(url_for("user_views.account"))
    else:
        abort(401)


@user_views.route("/account/<token>", methods=["GET"])
def account_verified(token):
    if "user" in get_access_rights(current_user):
        user = User.verify_reset_token(token)
        if user is None:
            flash("Obnovovací link vypršel, nebo je jinak neplatný.", category="info")
            return redirect(url_for("user_views.account"))
        else:
            user.confirmed = True
            db.session.commit()
            return redirect(url_for("user_views.account"))
    else:
        abort(401)

@user_views.route("/terminy")
def terminy():
    if "user" in get_access_rights(current_user):
        return render_template("terminy.html", roles=get_access_rights(current_user))
    else:
        abort(401)