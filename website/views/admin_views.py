import json
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from website import db
from website.models.chyba import Chyba
from website.models.user import User
from website.helpers.mailing_list import promazat_mailing_list
from website.helpers.user_filter import user_filter, seznam_generator
from website.roles.role_handler import get_access_rights
from website.json_handlers.logs_handling import delete_logs,  delete_alogs, alog
from website.json_handlers.poznamky_handling import zapsat_poznamky
from website.json_handlers.pohovory_handling import pridat_pohovory, smazat_termin
from website.paths.paths import terminy_path,faze_path, velitel_odbornosti_data_path, zadani_folder_path


admin_views = Blueprint("admin_views",__name__)

@admin_views.route("/")
@admin_views.route("/dashboard")
def admin_dashboard():
    rights = get_access_rights(current_user)
    if "admin" in rights:
        return render_template("admin_dashboard.html", pocet_bugu = Chyba.pocet_neresenych(), roles=rights)
    else:
        abort(401)


@admin_views.route("/poznamky", methods=["GET","POST"])
def poznamky():
    rights = get_access_rights(current_user)
    if "admin" in rights:
        if request.method == "GET":
            return render_template("admin_poznamky.html", roles=rights, username = current_user.jmeno, date=datetime.date.today())
        else:
            zapsat_poznamky(json.loads(request.form.get("result")))
            flash("Změny uloženy.", category="success")
            return redirect(url_for("admin_views.poznamky"))
    else:
        abort(401)


@admin_views.route("/planovane_featury")
def planovane_featury():
    rights = get_access_rights(current_user)
    if "admin" in rights:
       return render_template("admin_planovane_featury.html", roles=rights)
    else:
        abort(401)


@admin_views.route("/historie_verzi")
def historie_verzi():
    rights = get_access_rights(current_user)
    if "admin" in rights:
        return render_template("admin_historie_verzi.html", roles=rights)
    else:
        abort(401)


@admin_views.route("/uprava_znamych_bugu", methods=["GET","POST"])
def uprava_znamych_bugu():
    rights = get_access_rights(current_user)
    if "editing_bugs_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_uprava_znamych_chyb.html", roles=rights)
        else:
            Chyba.save_po_upravach(json.loads(request.form.get("result")))
            alog("Uprava záznamů na bugtrackeru.")
            return redirect(url_for("admin_views.admin_dashboard"))
    else:
        abort(401)
    

@admin_views.route("/app_logs", methods=["GET","POST"])
def app_logs():
    rights = get_access_rights(current_user)
    if "editing_logs_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_app_logs.html", roles=rights)
        else:
            delete_logs()
            alog("Vymazani app logu.")
            flash("Soubor s app logy byl promazán.",category="success")
            return redirect(url_for("admin_views.admin_dashboard"))
    else:
        abort(401)
    

@admin_views.route("/admin_logs", methods=["GET","POST"])
def admin_logs():
    rights = get_access_rights(current_user)
    if "editing_logs_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_admin_logs.html", roles=rights)
        else:
            delete_alogs()
            alog("Vymazani admin logu.")
            flash("Soubor s admin logy byl promazán.",category="success")
            return redirect(url_for("admin_views.admin_dashboard"))
    else:
        abort(401)


@admin_views.route("/registrovani_uzivatele", methods=["GET","POST"])
def registrovani_uzivatele():
    rights = get_access_rights(current_user)
    if "editing_users_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_registrovani_uzivatele.html", roles=rights)
        else:
            if request.form.get("dummy"):
                u = User.generate_random()
                alog("Generování nového dummy usera s id=" + str(u.id))
                return redirect(url_for("admin_views.detail_usera", id=u.id))
            else:
                result = request.form.get("result")
                return redirect(url_for("admin_views.detail_usera",id=int(result)))
    else:
        abort(401)
    
@admin_views.route("/detail_usera/<int:id>", methods=["GET","POST"])
def detail_usera(id):
    rights = get_access_rights(current_user)
    if "editing_users_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_detail_usera.html", roles = rights, id=id)
        else:
            if request.form.get("smazat"):
                User.query.get(id).odstranit()
                alog("Smazání usera " + str(id) + ".")
                flash("User byl smazán", category="success")
                return redirect(url_for("admin_views.registrovani_uzivatele"))
            elif request.form.get("result"):
                data = json.loads(request.form.get("result"))
                if len(data["admin_poznamka"]) > 1000:
                    flash("Admin poznámka je moc dlouhá, sori. Může bejt max 1000 znaků.", category="error")
                    return redirect(url_for("admin_views.detail_usera", id=id))
                if len(data["meeting_link"]) > 1000:
                    flash("Meeting link je moc dlouhý, sori. Může bejt max 1000 znaků.", category="error")
                    return redirect(url_for("admin_views.detail_usera", id=id))
                if data["uzamcene_zmeny"] == "true":
                    data["uzamcene_zmeny"] = True
                if data["uzamcene_zmeny"] == "false":
                    data["uzamcene_zmeny"] = False
                
                if data["souhlas_rodicu"] == "true":
                    data["souhlas_rodicu"] = True
                if data["souhlas_rodicu"] == "false":
                    data["souhlas_rodicu"] = False

                u = User.query.get(id)
                if u.progress == data["progress"]:
                    pass
                else:
                    u.progress = data["progress"]
                    alog(f"Změna progressu uživatele {id} na { u.progress }.")

                if u.uzamcene_zmeny == data["uzamcene_zmeny"]:
                    pass
                else:
                    u.uzamcene_zmeny = data["uzamcene_zmeny"]
                    alog(f"Změna uzamčení změn uživatele {id} na { u.uzamcene_zmeny }.")
                
                if u.admin_poznamka == data["admin_poznamka"]:
                    pass
                else:
                    u.admin_poznamka = data["admin_poznamka"]
                    alog(f"Změna admin poznámky uživatele {id}.")
                
                if u.souhlas_rodicu == data["souhlas_rodicu"]:
                    pass
                else:
                    u.souhlas_rodicu = data["souhlas_rodicu"]
                    alog(f"Změna souhlasu rodičů uživatele {id} na { u.souhlas_rodicu }.")

                if u.meeting_link == data["meeting_link"]:
                    pass
                else:
                    u.meeting_link = data["meeting_link"]
                    alog(f"Změna meeting linku uživatele {id}.")
                
                db.session.add(u)
                db.session.commit()
                flash("Záznam o userovi upraven", category="success")
                return redirect(url_for("admin_views.registrovani_uzivatele"))
            else:
                return "divna query"
    else:
        abort(401)
    

@admin_views.route("/jmenovat_adminy", methods=["GET","POST"])
def jmenovat_adminy():
    rights = get_access_rights(current_user)
    if "editing_admins_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_jmenovat_adminy.html", roles=rights)
        else:
            return redirect(url_for("admin_views.vybrat_role_adminovi", id=int(request.form.get("result"))))
    else:
        abort(401)

@admin_views.route("/jmenovat_adminy/<int:id>", methods=["GET","POST"])
def vybrat_role_adminovi(id):
    rights = get_access_rights(current_user)
    if "editing_admins_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_vybrat_role_adminovi.html", user=User.query.get(id), roles=rights)
        else:
            if request.form.get("detail"):
                return redirect(url_for("admin_views.detail_usera", id=request.form.get("detail")))
            else:
                nove_role = json.loads(request.form.get("result"))
                u = User.query.get(id)
                if u.role == json.dumps(nove_role):
                    pass
                else:
                    u.role = json.dumps(nove_role)
                    alog(f"Změněny role uživatele {id} na {json.dumps(nove_role)}")
                db.session.add(u)
                db.session.commit()
                flash("Role byly upraveny.", category="success")
                return redirect(url_for("admin_views.jmenovat_adminy"))
            
    else:
        abort(401)


@admin_views.route("/stanovit_terminy", methods=["GET","POST"])
def stanovit_terminy():
    rights = get_access_rights(current_user)
    if "stanovit_terminy_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_stanovit_terminy.html", roles=rights)
        else:
            with open(terminy_path(), "w") as file:
                file.write(json.dumps(json.loads(request.form.get("result")), indent=4))
            alog("Úprava termínů.")
            flash("Termíny byly upraveny.", category="success")
            return redirect(url_for("admin_views.admin_dashboard"))
    else:
        abort(401)


@admin_views.route("/prepinat_faze", methods=["GET","POST"])
def prepinat_faze():
    rights = get_access_rights(current_user)
    if "prepinani_fazi_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_prepinat_faze.html", roles=rights)
        else:
            if request.form.get("smazat_mailing_list"):
                flash("Mailing list byl promazán.", category="info")
                promazat_mailing_list()
                alog("Mailing list byl promazán.")
                return redirect(url_for("admin_views.prepinat_faze"))
            else:
                with open(faze_path()) as file:
                    faze = json.load(file)
                aktualni_faze = list(filter(lambda x: x["active"], faze))[0]
                aktualni_faze["active"] = False
                pozadavek = request.form.get("result")
                if pozadavek == "dalsi":
                    nova_faze = list(filter(lambda x: x["nazev"] == aktualni_faze["nasledujici"], faze))[0]
                else:
                    nova_faze = list(filter(lambda x: x["nasledujici"] == aktualni_faze["nazev"], faze))[0]
                alog("Změna fáze na " + nova_faze["nazev"] + ".")
                nova_faze["active"] = True
                with open(faze_path(), "w") as file:
                    file.write(json.dumps(faze, indent=4))
                return redirect(url_for("admin_views.prepinat_faze"))
    else:
        abort(401)

@admin_views.route("/velitele_odbornosti", methods=["GET","POST"])
def velitele_odbornosti():
    rights = get_access_rights(current_user)
    if "velitel_odbornosti" in rights:
        if request.method == "GET":
            return render_template("admin_velitele_odbornosti.html", roles=rights)
        else:
            # mazani souboru
            if request.form.get("smazat_zadani"):
                odbornost = request.form.get("smazat_zadani")
                path = zadani_folder_path() / odbornost
                for file in path.iterdir():
                    file.unlink()
                alog(f"Smazání zadání odbornosti {odbornost}.")
                flash(f"Zadání odborosti {odbornost} je smazaný.", category="success")
            
            # ukládání souborů
            elif request.form.get("ulozit_zadani"):
                odbornost = request.form.get("ulozit_zadani")
                if all(request.files.getlist(f"{odbornost}_files")):
                    for file in request.files.getlist(f"{odbornost}_files"):
                        file.save(zadani_folder_path() / odbornost / file.filename)
                    flash("Zadání nahráno.", category="success")
                    alog(f"Nahrání nového zadání pro odbornost {odbornost}.")
                else:
                    flash("Nenahrál jsi žádné soubory.", category="info")


            # zapisování kontaktních dat
            else:
                inputs_ids_list = ["biolog", "konstrukter", "fyzik", "inzenyr", "popularizator"]
                zmeneno = []
                with open(velitel_odbornosti_data_path()) as file:
                    velitel_odbornosti_data = json.load(file)
                for id in inputs_ids_list:
                    res = request.form.get(id)
                    if res is None:
                        pass
                    else:
                        if velitel_odbornosti_data[id] == res:
                            pass
                        else:
                            zmeneno.append(id)
                            velitel_odbornosti_data[id] = res
                with open(velitel_odbornosti_data_path(),"w") as file:
                    file.write(json.dumps(velitel_odbornosti_data, indent=4))
                alog("Úprava kontaktních údajů pro odbornosti: " + str(zmeneno))
                flash("Data velitelů odborností byla upravena.", category="success")
            return redirect(url_for("admin_views.velitele_odbornosti"))

    else:
        abort(401)


@admin_views.route("/generovat_seznamy/", methods=["GET","POST"])
def generovat_seznamy():
    rights = get_access_rights(current_user)
    if "editing_users_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_generovat_seznamy.html", roles=rights)
        else:
            alog("Generování seznamu účastníků podle: " + request.form.get("result") + ".")
            kriteria = json.loads(request.form.get("result"))
            users = user_filter(kriteria)
            data = seznam_generator(users, kriteria["vypsat"])
            return json.dumps(data)
    else:
        abort(401)

@admin_views.route("/motivaky_a_prace", methods=["GET","POST"])
def motivaky_a_prace():
    rights = get_access_rights(current_user)
    if "editing_users_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_motivaky_a_prace.html", roles=rights)
        else:
            result = json.loads(request.form.get("result"))
            zmeneno = []
            for zaznam in result:
                user = User.query.get(zaznam["id"])
                if user.hodnoceni_motivaku == zaznam["hodnoceni"]:
                    pass
                else:
                    user.hodnoceni_motivaku = zaznam["hodnoceni"]
                    db.session.add(user)
                    db.session.commit()
                    zmeneno.append(user.id)
            alog(f"Změna hodnocení motiváku u uživatelů {str(zmeneno)}.")
            flash("Hodnocení motiváků uložena.", category="success")
            return redirect(url_for("admin_views.admin_dashboard"))

    else:
        abort(401)



@admin_views.route("/pohovory", methods=["GET","POST"])
def pohovory():
    rights = get_access_rights(current_user)
    if "editing_pohovory" in rights:
        if request.method == "GET":
            return render_template("admin_pohovory.html", roles=rights)
        else:
            if request.form.get("pridat_termin"):
                date = request.form.get("date")
                start_time = request.form.get("start_time")
                end_time = request.form.get("end_time")
                start_datetime = date + " " + start_time
                end_datetime = date + " " + end_time
                try:
                    start_datetime = datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M")
                    end_datetime = datetime.datetime.strptime(end_datetime, "%Y-%m-%d %H:%M")
                except ValueError:
                    flash("Pravděpodobně nebylo zadáno datum.", category="error")
                    return redirect(url_for("admin_views.pohovory"))
                if start_datetime > end_datetime:
                    flash("Časy, kkteré byly zadány, nedávaly smysl. Zkus to znova.", category="error")
                    return redirect(url_for("admin_views.pohovory"))
                else:
                    pridat_pohovory(start_datetime=start_datetime, end_datetime=end_datetime)
                    flash("Termíny vypsány.", category="success")
                    return redirect(url_for("admin_views.pohovory"))
            elif request.form.get("smazat"):
                vysledek = smazat_termin(datetime.datetime.fromisoformat(request.form.get("smazat")))
                if vysledek:
                    flash("Termín smazán.", category="success")
                else:
                    flash("Tento termín si mezitím někdo zapsal, nejde tedy smazat.", category="error")
                return redirect(url_for("admin_views.pohovory"))

    else:
        abort(401)