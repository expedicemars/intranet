from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from website.models.user import User
from website.mails.mail_handler import mail_sender
from website import db
from website.roles.role_handler import get_access_rights
import json
from website.paths.paths import user_data_folder_path
from website.hepers.get_aktualni_faze import je_zadani_pristupne

user_views = Blueprint("user_views", __name__)



@user_views.route("/ucet", methods=["GET", "POST"])
def ucet():
    if "user" in get_access_rights(current_user):
        if request.method == "GET":
            return render_template("ucet.html", current_user = current_user, roles = get_access_rights(current_user))
        else:
            if request.form.get("overeni_emailu"):
                token = current_user.get_reset_token()
                mail_sender(mail_identifier="potvrzeni_emailu", target=current_user.email, data=token)
                flash("E-mail byl odeslán. Zkontrolujte si svou schránku.", category="info")
                return redirect(url_for("user_views.ucet"))
            elif request.form.get("img"):
                #zkusit smazat starou
                path = user_data_folder_path() / str(current_user.id)
                for file in path.iterdir():
                    if file.stem == "profiovka":
                        profilovka_path = path / file.name
                        profilovka_path.unlink()
                        break
                #nahrát novou
                fotka = request.files.get("img_file")
                if len(fotka.filename.split(".")) == 2:
                    pripona = fotka.filename.split(".")[1]
                    filename = "profiovka" + "." + pripona
                    cesta = user_data_folder_path() / str(current_user.id) / filename
                    cesta.touch()
                    fotka.save(cesta)
                    flash("Fotka nahrána.", category="success")
                    return redirect(url_for("user_views.ucet"))
                else:
                    flash("Prosím, pojmenuj soubor tak, aby název obsahoval jen jednu tečku, a to u přípony.", category="success")
                    return redirect(url_for("user_views.ucet"))
            else:
                data = json.loads(request.form.get("result"))
                current_user.jmeno = data["jmeno"]
                current_user.adresa = data["adresa"]
                current_user.telcislo = data["telcislo"]
                current_user.datum_narozeni = data["datum_narozeni"]
                current_user.mail_rodicu = data["mail_rodicu"]
                if current_user.email != data["email"]:
                    current_user.email = data["email"]
                    current_user.confirmed = False
                    flash("Protože jsi změnil mail, musíš ho znovu ověřit.", category="info")
                db.session.add(current_user)
                db.session.commit()
                flash("Změny byly uloženy.", category="success")
                return redirect(url_for("user_views.ucet"))
    else:
        abort(401)


@user_views.route("/ucet/<token>", methods=["GET"])
def ucet_overeny(token):
    if "user" in get_access_rights(current_user):
        user = User.verify_reset_token(token)
        if user is None:
            flash("Obnovovací link vypršel, nebo je jinak neplatný.", category="info")
            return redirect(url_for("user_views.ucet"))
        else:
            user.confirmed = True
            db.session.commit()
            return redirect(url_for("user_views.ucet"))
    else:
        abort(401)

@user_views.route("/terminy")
def terminy():
    if "user" in get_access_rights(current_user):
        return render_template("terminy.html", roles=get_access_rights(current_user))
    else:
        abort(401)

@user_views.route("/odbornost", methods=["GET","POST"])
def odbornost():
    if "user" in get_access_rights(current_user):
        if request.method == "GET":
            if current_user.odbornost == "zatím nevybraná":
                nevybrano = True
            else:
                nevybrano = False
            return render_template("odbornost.html", zadani_pristupne =je_zadani_pristupne() , nevybrano=nevybrano, roles=get_access_rights(current_user))
        else:
            current_user.odbornost = request.form["result"]
            db.session.add(current_user)
            db.session.commit()
            flash("Odbornost vybrána!", category="success")
            return redirect(url_for("user_views.ucet"))
    else:
        abort(401)
