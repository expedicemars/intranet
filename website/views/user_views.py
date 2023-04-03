from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from website.helpers.require_role_decorator import require_role_on_current_user, require_progress_na_ucastnikovi
from website.models.user import User
from website.mail_handler import mail_sender
from website import db
from website.role_handler import get_access_rights
import json
from website.paths import user_data_folder_path
from website.json_handlers.pohovory_handling import zapsat_na_pohovor

user_views = Blueprint("user_views", __name__)



@user_views.route("/ucet", methods=["GET", "POST"])
@require_role_on_current_user("user")
def ucet():
    if request.method == "GET":
        return render_template("ucet.html", current_user = current_user, roles=get_access_rights(), uzamcene_zmeny=current_user.uzamcene_zmeny, user_progress=current_user.progress)
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
                if file.stem == "profilovka":
                    profilovka_path = path / file.name
                    profilovka_path.unlink()
                    break
            #nahrát novou
            fotka = request.files.get("img_file")
            if len(fotka.filename.split(".")) == 2:
                pripona = fotka.filename.split(".")[1]
                filename = "profilovka" + "." + pripona
                cesta = user_data_folder_path() / str(current_user.id) / filename
                cesta.touch()
                fotka.save(cesta)
                flash("Fotka nahrána.", category="success")
                return redirect(url_for("user_views.ucet"))
            else:
                flash("Prosím, pojmenuj soubor tak, aby název obsahoval jen jednu tečku, a to u přípony.", category="info")
                return redirect(url_for("user_views.ucet"))
        elif request.form.get("nahrat_motivak"):
            #zkusit smazat stary
            path = user_data_folder_path() / str(current_user.id)
            for file in path.iterdir():
                if file.stem == "motivak":
                    profilovka_path = path / file.name
                    profilovka_path.unlink()
                    break
            #nahrát novy
            file = request.files.get("motivak")
            if len(file.filename.split(".")) == 2:
                pripona = file.filename.split(".")[1]
                filename = "motivak" + "." + pripona
                cesta = user_data_folder_path() / str(current_user.id) / filename
                cesta.touch()
                file.save(cesta)
                flash("Morivák nahrán.", category="success")
                return redirect(url_for("user_views.ucet"))
            else:
                flash("Prosím, pojmenuj soubor tak, aby název obsahoval jen jednu tečku, a to u přípony.", category="info")
                return redirect(url_for("user_views.ucet"))
        else:
            data = json.loads(request.form.get("result"))
            current_user.jmeno = data["jmeno"]
            current_user.adresa = data["adresa"]
            current_user.telcislo = data["telcislo"]
            current_user.datum_narozeni = data["datum_narozeni"]
            current_user.mail_rodicu = data["mail_rodicu"]
            current_user.tricko = data["tricko"]
            current_user.dozvedeli = data["dozvedeli"]
            current_user.skola = data["skola"]
            current_user.alergie = data["alergie"]
            if current_user.email != data["email"]:
                current_user.email = data["email"]
                current_user.confirmed = False
                flash("Protože jsi změnil mail, musíš ho znovu ověřit.", category="info")
            db.session.add(current_user)
            db.session.commit()
            flash("Změny byly uloženy.", category="success")
            return redirect(url_for("user_views.ucet"))
        
@user_views.route("/info")
def info():
    return render_template("info.html", roles = get_access_rights(current_user), user_progress=current_user.progress)


@user_views.route("/ucet/<token>", methods=["GET"])
@require_role_on_current_user("user")
def ucet_overeny(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("Obnovovací link vypršel, nebo je jinak neplatný.", category="info")
        return redirect(url_for("user_views.ucet"))
    else:
        user.confirmed = True
        db.session.commit()
        return redirect(url_for("user_views.ucet"))
        
        
@user_views.route("/pohovory", methods=["GET","POST"])
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Online setkání")
def pohovory():
    if  request.method == "GET":
        return render_template("pohovory.html", roles=get_access_rights(current_user), uzamcene_zmeny = current_user.uzamcene_zmeny, user_progress=current_user.progress)
    else:
        if request.form.get("vybrat"):
            current_user.datum_pohovoru = request.form.get("vybrat")
            db.session.add(current_user)
            db.session.commit()
            vysledek = zapsat_na_pohovor(current_user.datum_pohovoru, current_user.id)
            if vysledek:
                flash("Termín vybrán.", category="success")
            else:
                flash("Tento termín si mezitím vybral někdo jiný. Prosím, vyber si další.", category="error")
            return redirect(url_for("user_views.pohovory"))
    
    
@user_views.route("/odbornost", methods=["GET","POST"])
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Domácí projekt")
def odbornost():
    if current_user.odbornost == "zatím nevybraná":
        return redirect(url_for("user_views.odbornost_vyber"))
    else:
        if request.method == "GET":
            return render_template("odbornost.html", roles=get_access_rights(current_user), uzamcene_zmeny = current_user.uzamcene_zmeny, user_progress=current_user.progress)
        else:
            if request.form.get("ulozit_praci"):
                if all(request.files.getlist("nahrana_prace")):
                    for file in request.files.getlist("nahrana_prace"):
                        prace_folder_path = user_data_folder_path() / str(current_user.id) / "prace"
                        file.save(prace_folder_path / file.filename)
                    flash("Práce nahrána.", category="success")
                else:
                    flash("Nenahrál jsi žádné soubory.", category="info")
            elif request.form.get("smazat_praci"):
                path = user_data_folder_path() / str(current_user.id) / "prace"
                for file in path.iterdir():
                    file.unlink()
                flash("Svou nahranou práci jsi smazal. Nezapomeň nahrát novou verzi :)", category="success")
            return redirect(url_for("user_views.odbornost"))


@user_views.route("/odbornost_vyber", methods=["GET","POST"])
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Domácí projekt")
def odbornost_vyber():
    if current_user.odbornost in ["biolog", "fyzik", "konstrukter", "inzenyr", "popularizator"]:
        return redirect(url_for("user_views.odbornost"))
    else:
        if request.method == "GET":
            return render_template("odbornost_vyber.html", roles=get_access_rights(current_user), user_progress=current_user.progress)
        else:
            current_user.odbornost = request.form.get("odbornost")
            db.session.add(current_user)
            db.session.commit()
            flash("Odbornost vybrána!", category="success")
            return redirect(url_for("user_views.odbornost"))