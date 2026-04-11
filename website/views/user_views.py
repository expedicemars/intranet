from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_user
from website.helpers.require_role_decorator import require_role_on_current_user, require_progress_na_ucastnikovi, require_odbornost_na_ucastnikovi
from website.helpers.size_check import check_size
from website.models.user import User
from website.models.motivacni_call import Motivacni_call
from website.mail_handler import mail_sender
from website import db
from website.role_handler import get_access_rights, get_user_progress, get_info_o_konf_viditelne
from website.paths import user_data_folder_path
from website.json_handlers.dostupne_omezeni import get_dostupne_odbornosti, get_odbornost_by_system_name
import datetime
from pathlib import Path
from website.json_handlers.prubeh_rocniku_handling import get_koordinator_internetovych_kol

user_views = Blueprint("user_views", __name__)



@user_views.route("/ucet", methods=["GET", "POST"])
@require_role_on_current_user("user")
def ucet():
    if request.method == "GET":
        return render_template("ucastnik/ucet.html", current_user = current_user, roles=get_access_rights(), uzamcene_zmeny_udaju=current_user.uzamcene_zmeny_udaju, user_progress=get_user_progress(), konf_viditelne = get_info_o_konf_viditelne())
    else:
        if current_user.uzamcene_zmeny_udaju:
            flash("Máš uzamčené změny údajů, nesmíš nic měnit.")
            return redirect(url_for("user_views.ucet"))
        if request.form.get("overeni_emailu"):
            token = current_user.get_reset_token()
            mail_sender(mail_identifier="potvrzeni_emailu", target=current_user.email, data=token)
            flash("E-mail byl odeslán. Zkontroluj si svou schránku.", category="info")
            return redirect(url_for("user_views.ucet"))
        elif request.form.get("img"):
            files = check_size(request.files.getlist("img_file"), 5*1024*1024)
            if not files:
                flash("Soubor byl moc velký. Prosíme, nahraj fotku pod 5 MB.", category="error")
                return redirect(url_for("user_views.ucet"))
            
            fotka = files[0]
            
            #zkusit smazat starou
            path = user_data_folder_path() / str(current_user.id)
            for file in path.iterdir():
                if file.stem == "profilovka":
                    profilovka_path = path / file.name
                    profilovka_path.unlink()
                    break
            
            #nahrát novou
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
        else:
            data = request.form.to_dict()
            current_user.jmeno = data["jmeno"]
            current_user.prijmeni = data["prijmeni"]
            current_user.adresa = data["adresa"]
            current_user.telcislo = data["telcislo"]
            current_user.datum_narozeni = datetime.datetime.fromisoformat(data["datum_narozeni"]) if data["datum_narozeni"] else None
            current_user.rok_maturity = data["rok_maturity"] if data["rok_maturity"] else None
            current_user.puvod = data["zeme_puvodu"]
            current_user.mail_rodicu = data["mail_rodicu"]
            current_user.telcislo_rodicu = data["telcislo_rodicu"]
            current_user.tricko = data["tricko"]
            current_user.dozvedeli = data["dozvedeli"]
            current_user.skola = data["skola"]
            current_user.alergie = data["alergie"]
            current_user.osloveni_1p = data["osloveni_1p"]
            current_user.osloveni_5p = data["osloveni_5p"]
            current_user.zajmeno = data["zajmeno"]
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
    return render_template("ucastnik/info.html", roles = get_access_rights(), user_progress=get_user_progress(), odevzdany_formular = current_user.odevzdany_motivacni_dotaznik, konf_viditelne = get_info_o_konf_viditelne())


@user_views.route("/ucet/<token>", methods=["GET"])
def ucet_overeny(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("Ověřovací link vypršel, nebo je jinak neplatný.", category="info")
        return redirect(url_for("user_views.ucet"))
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("user_views.ucet"))
        
        
@user_views.route("/motivacni_call", methods=["GET","POST"])
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Motivační call")
def motivacni_call():
    if  request.method == "GET":
        return render_template("ucastnik/motivacni_call.html", roles=get_access_rights(), uzamcene_zmeny_callu = current_user.uzamcene_zmeny_callu, user_progress=get_user_progress(), konf_viditelne = get_info_o_konf_viditelne())
    else:
        if request.form.get("vybrat"):
            m: Motivacni_call
            m = Motivacni_call.get_by_id(request.form.get("vybrat"))
            vysledek = m.zapsat_usera(user_id = current_user.id)
            if vysledek:
                mail_sender("novy_motivacni_call", target=User.get_by_id(m.admin_id).email)
                flash("Termín vybrán.", category="success")
            else:
                flash("Tento termín si mezitím vybral někdo jiný. Prosím, vyber si další.", category="error")
            return redirect(url_for("user_views.motivacni_call"))
        elif request.form.get("zmenit"):
            admin_id = Motivacni_call.odhlasit_usera_by_user_id(current_user.id)
            mail_sender(mail_identifier="odhlaseni_motivacniho_callu", target=User.get_by_id(admin_id).email)
            flash("Termín byl odhlášen.", category="success")
            return redirect(url_for("user_views.motivacni_call"))
    
    
@user_views.route("/odbornost/<string:odb>", methods=["GET","POST"])
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Domácí projekt")
def odbornost(odb):
    if odb not in [o["system_name"] for o in get_dostupne_odbornosti()]:
        abort(404)
    current_odbornost = current_user.odbornost
    if current_odbornost != "zatím nevybraná" and odb != current_odbornost:
        abort(401)
    if request.method == "GET":
        return render_template("ucastnik/odbornost.html", 
                               roles=get_access_rights(), 
                               uzamcene_zmeny_prace = current_user.uzamcene_zmeny_prace, 
                               user_progress=get_user_progress(), 
                               odbornost=odb, 
                               odbornost_pretty = get_odbornost_by_system_name(odb)["prvnipjc"],
                               odbornost_uzivatele = current_odbornost, 
                               ma_nahranou_praci = current_user.ma_nahranou_praci(),
                               konf_viditelne = get_info_o_konf_viditelne())
    else:
        if request.form.get("ulozit_praci"):
            if all(files := request.files.getlist("nahrana_prace")):
                files = check_size(files, 20*1024*1024)
                if not files:
                    flash("Společná velikost souborů byla přes 20 MB.", category="error")
                else:
                    for file in request.files.getlist("nahrana_prace"):
                        prace_folder_path = user_data_folder_path() / str(current_user.id) / "prace"
                        file.save(prace_folder_path / file.filename)
                    current_user.datetime_odevzdani_prezentace = datetime.datetime.today()
                    db.session.add(current_user)
                    db.session.commit()
                    flash("Práce nahrána.", category="success")
            else:
                flash("Nenahrál jsi žádné soubory.", category="info")
            return redirect(url_for("user_views.odbornost", odb=odb))
        elif request.form.get("ulozit_shrnuti"):
            if all(files:=request.files.getlist("nahrane_shrnuti")): # musi to tak byt, protoze len(prazdneho) = 1
                if len(files) != 1:
                    flash("Nahrál jsi více souborů, než 1.")
                    return redirect(url_for("user_views.odbornost", odb=odb))
                files = check_size(files, 5*1024*1024)
                if not files:
                    flash("Soubor byl moc velký. Maximální velikost souboru je 5 MB.", category="error")
                    return redirect(url_for("user_views.odbornost", odb=odb))
                else: # ulozim origo a pak ho prejmenuju. taky tu probiha zapis do odbornosti
                    save_path: Path = user_data_folder_path() / str(current_user.id) / files[0].filename
                    files[0].save(save_path)
                    name_do_filename = current_user.prijmeni if current_user.prijmeni else current_user.email
                    filename = "shrnuti_" + name_do_filename + save_path.suffix
                    new_path = save_path.parent / filename
                    save_path.rename(new_path)
                    current_user.odbornost = odb
                    current_user.datetime_odevzdani_shrnuti_prace = datetime.datetime.today()
                    db.session.add(current_user)
                    db.session.commit()
                    target = [u.email for u in User.get_all_by_role("velitel_odbornosti_" + odb)]
                    target.append(get_koordinator_internetovych_kol())
                    mail_sender("nove_shrnuti_prace", target=target, data=current_user.id)
                    flash(f"Shrnutí nahráno, tímto proběhlo zapsání do odbornosti {odb}.", category="success")
                    return redirect(url_for("user_views.odbornost", odb=odb))
            else:
                flash("Nenahrál jsi žádné soubory.", category="info")
                return redirect(url_for("user_views.odbornost", odb=odb))
        elif request.form.get("smazat_praci"):
            current_user.smazat_praci()
            flash("Nahraná práce je smazána. Nezapomeň nahrát novou verzi :)", category="success")
            return redirect(url_for("user_views.odbornost", odb=odb))
        elif request.form.get("smazat_shrnuti"):
            current_user.smazat_shrnuti()
            current_user.smazat_praci()
            flash("Shrnutí bylo smazáno, můžeš si znovu vybrat odbornost.", category="success")
            return redirect(url_for("user_views.odbornost_vyber"))


@user_views.route("/odbornost_vyber")
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Domácí projekt")
def odbornost_vyber():
    if current_user.odbornost != "zatím nevybraná":
        return redirect(url_for("user_views.odbornost", odb = current_user.odbornost))
    else:
        return render_template("ucastnik/odbornost_vyber.html", roles=get_access_rights(), user_progress=get_user_progress(), konf_viditelne = get_info_o_konf_viditelne())

@user_views.route("/motivacni_formular>", methods=["GET","POST"])
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Motivační formulář")
def motivacni_formular():
    return redirect(url_for("user_views.motivacni_formular_numbered", blok_otazek = 1))

@user_views.route("/motivacni_formular/<int:blok_otazek>", methods=["GET","POST"])
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Motivační formulář")
def motivacni_formular_numbered(blok_otazek):
    if request.method == "GET":
        return render_template("ucastnik/motivacni_formular.html", roles=get_access_rights(), user_progress=get_user_progress(), blok_otazek=blok_otazek, odevzdany_formular=current_user.odevzdany_motivacni_dotaznik, konf_viditelne = get_info_o_konf_viditelne())
    else:
        if request.form.get("dalsi"):
            current_user.ulozit_odpovedi(request.form.to_dict())
            return redirect(url_for("user_views.motivacni_formular_numbered", blok_otazek=int(request.form.get("dalsi")) + 1))
        if request.form.get("predchozi"):
            current_user.ulozit_odpovedi(request.form.to_dict())
            return redirect(url_for("user_views.motivacni_formular_numbered", blok_otazek=int(request.form.get("predchozi")) - 1))
        if request.form.get("odeslat"):
            current_user.ulozit_odpovedi(request.form.to_dict())
            current_user.odevzdany_motivacni_dotaznik = True
            current_user.datetime_odevzdani_motivaku = datetime.datetime.now()
            current_user.progress = "Motivační call"
            db.session.add(current_user)
            db.session.commit()
            flash("Motivační formulář byl odevzdán.", category="success")
            return redirect(url_for("user_views.ucet"))
    
@user_views.route("/info_o_konferenci")
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Domácí projekt")
def info_o_konferenci():
    if get_info_o_konf_viditelne():
        return render_template("ucastnik/info_o_konferenci.html", roles=get_access_rights(), user_progress=get_user_progress(), konf_viditelne = get_info_o_konf_viditelne())
    else:
        abort(401)
            
