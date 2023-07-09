import json
import datetime
from shutil import rmtree
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from website import db
from website.helpers.require_role_decorator import require_role_on_current_user
from website.models.chyba import Chyba
from website.models.user import User
from website.json_handlers.mailing_list import set_mailing_list
from website.helpers.user_filter import seznam_generator
from website.helpers.exporty import exportovat, promazat
from website.helpers.pretty_date import pretty_date, pretty_datetime
from website.role_handler import get_access_rights
from website.json_handlers.logs_handling import delete_logs,  delete_alogs, alog
from website.json_handlers.poznamky_handling import zapsat_poznamky
from website.json_handlers.pohovory_handling import pridat_pohovory, smazat_termin
from website.json_handlers.odkazy_handling import pridat_odkaz, smazat_odkaz_by_id
from website.json_handlers.prubeh_rocniku_handling import set_nove_datum_konce_registrace, toggle_registrace, get_registrace_otevrena
from website.json_handlers.info_handling import ulozit_info
from website.paths import velitel_odbornosti_data_path, zadani_folder_path, prohlaseni_path, exporty_path


admin_views = Blueprint("admin_views",__name__)

@admin_views.route("/", methods=["GET","POST"])
@admin_views.route("/dashboard", methods=["GET","POST"])
@require_role_on_current_user("admin")
def admin_dashboard():
    if request.method == "GET":
        flash("Vítej a porozhlédni se tu. Zatím nejlépe shrnuté a popsané fíčury jsou dole v patičce v Přehledu fíčur systému.", category="success")
        return render_template("admin_dashboard.html", pocet_bugu = Chyba.pocet_neresenych(), roles=get_access_rights())
    else:
        mailing_list = request.form.get("mailing_list")
        set_mailing_list(mailing_list)
        flash("Změna mailing listu uložena.", category="success")
        alog("Úprava mailing listu.")
        return redirect(url_for("admin_views.admin_dashboard"))


@admin_views.route("/poznamky", methods=["GET","POST"])
@require_role_on_current_user("admin")
def poznamky():
    if request.method == "GET":
        return render_template("admin_poznamky.html", roles=get_access_rights(), username = current_user.jmeno, date=datetime.date.today())
    else:
        zapsat_poznamky(json.loads(request.form.get("result")))
        flash("Změny uloženy.", category="success")
        return redirect(url_for("admin_views.poznamky"))


@admin_views.route("/planovane_featury")
@require_role_on_current_user("admin")
def planovane_featury():
       return render_template("admin_planovane_featury.html", roles=get_access_rights())


@admin_views.route("/historie_verzi")
@require_role_on_current_user("admin")
def historie_verzi():
        return render_template("admin_historie_verzi.html", roles=get_access_rights())


@admin_views.route("/uprava_znamych_bugu", methods=["GET","POST"])
@require_role_on_current_user("editing_bugs_allowed")
def uprava_znamych_bugu():
    if request.method == "GET":
        return render_template("admin_uprava_znamych_chyb.html", roles=get_access_rights())
    else:
        Chyba.save_po_upravach(json.loads(request.form.get("result")))
        alog("Uprava záznamů na bugtrackeru.")
        return redirect(url_for("admin_views.admin_dashboard"))
    

@admin_views.route("/app_logs", methods=["GET","POST"])
@require_role_on_current_user("editing_logs_allowed")
def app_logs():
    if request.method == "GET":
        return render_template("admin_app_logs.html", roles=get_access_rights())
    else:
        delete_logs()
        alog("Vymazani app logu.")
        flash("Soubor s app logy byl promazán.",category="success")
        return redirect(url_for("admin_views.admin_dashboard"))
    

@admin_views.route("/admin_logs", methods=["GET","POST"])
@require_role_on_current_user("editing_logs_allowed")
def admin_logs():
    if request.method == "GET":
        return render_template("admin_admin_logs.html", roles=get_access_rights())
    else:
        delete_alogs()
        alog("Vymazani admin logu.")
        flash("Soubor s admin logy byl promazán.",category="success")
        return redirect(url_for("admin_views.admin_dashboard"))


@admin_views.route("/registrovani_uzivatele", methods=["GET","POST"])
@require_role_on_current_user("editing_users_allowed")
def registrovani_uzivatele():
    if request.method == "GET":
        return render_template("admin_registrovani_uzivatele.html", roles=get_access_rights())
    else:
        if request.form.get("dummy"):
            u = User.generate_random()
            alog("Generování nového dummy usera s id=" + str(u.id))
            return redirect(url_for("admin_views.detail_usera", id=u.id))
        else:
            result = request.form.get("result")
            return redirect(url_for("admin_views.detail_usera",id=int(result)))
        
    
@admin_views.route("/detail_usera/<int:id>", methods=["GET","POST"])
@require_role_on_current_user("editing_users_allowed")
def detail_usera(id):
    if request.method == "GET":
        return render_template("admin_detail_usera.html", roles=get_access_rights(), id=id)
    else:
        u = User.get_by_id(id)
        if request.form.get("smazat"):
            if "admin" in json.loads(u.role):
                alog(f"Pokus o smazání admina {u.email}")
                flash("Nemůžeš mazat adminy!", category="error")
                return redirect(url_for("admin_views.registrovani_uzivatele"))
            else:
                u.odstranit()
                alog("Smazání usera " + str(id) + ".")
                flash("User byl smazán", category="success")
                return redirect(url_for("admin_views.registrovani_uzivatele"))
        elif request.form.get("odebrat_odbornost"):
            u.odebrat_odbornost()
            alog(f"Odebrána odbornost userovi {u.email}")
            flash("Odbornost byla odebrána", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))
        
        elif request.form.get("odebrat_motivacni_formular"):
            u.odebrat_motivacni_formular()
            alog(f"Vymazán motivační formulář usera {u.email}")
            flash("Motivační formulář byl promazán.", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))
    
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

            if u.meeting_link == data["meeting_link"]:
                pass
            else:
                u.meeting_link = data["meeting_link"]
                alog(f"Změna meeting linku uživatele {id}.")
            
            db.session.add(u)
            db.session.commit()
            flash("Záznam o userovi upraven", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))
        elif request.form.get("promazat_formular"):
            u.motivacni_dotaznik = None
            db.session.add(u)
            db.session.commit()
            flash("Motivační dotazník promazán.", category="success")
            alog(f"Promazán motivační dotazník uživatele {u.email}")
            return redirect(url_for("admin_views.detail_usera", id=id))
    

@admin_views.route("/jmenovat_adminy", methods=["GET","POST"])
@require_role_on_current_user("editing_admins_allowed")
def jmenovat_adminy():
        if request.method == "GET":
            return render_template("admin_jmenovat_adminy.html", roles=get_access_rights())
        else:
            return redirect(url_for("admin_views.vybrat_role_adminovi", id=int(request.form.get("result"))))

@admin_views.route("/jmenovat_adminy/<int:id>", methods=["GET","POST"])
@require_role_on_current_user("editing_admins_allowed")
def vybrat_role_adminovi(id):
    if request.method == "GET":
        return render_template("admin_vybrat_role_adminovi.html", user=User.get_by_id(id), roles=get_access_rights())
    else:
        if request.form.get("detail"):
            return redirect(url_for("admin_views.detail_usera", id=request.form.get("detail")))
        else:
            nove_role = json.loads(request.form.get("result"))
            u = User.get_by_id(id)
            if u.role == json.dumps(nove_role):
                pass
            else:
                u.role = json.dumps(nove_role)
                alog(f"Změněny role uživatele {id} na {json.dumps(nove_role)}")
            db.session.add(u)
            db.session.commit()
            flash("Role byly upraveny.", category="success")
            return redirect(url_for("admin_views.jmenovat_adminy"))


@admin_views.route("/prubeh_rocniku", methods=["GET","POST"])
@require_role_on_current_user("editing_prubeh_rocniku")
def prubeh_rocniku():
    if request.method == "GET":
        return render_template("admin_prubeh_rocniku.html", roles=get_access_rights())
    else:
        if request.form.get("ukoncit_rocnik_input"):
            promazat()
            alog("Byl promazán systém")
            flash("Promazání systému bylo úspěšné.", category="success")
            return redirect(url_for("admin_views.admin_dashboard"))
        elif request.form.get("ulozit_datum"):
            datum = request.form.get("registrace_date")
            set_nove_datum_konce_registrace(datum)
            alog(f"Úprava temrínu konce registrace na {datum}.")
            flash("Termín konce registrace byl upraven.", category="success")
        elif request.form.get("toggle_registraci"):
            toggle_registrace()
            alog(f"Změna otevření registrace na {get_registrace_otevrena()}")
            flash(f"Stav otevření registrace změnen na {get_registrace_otevrena()}", category="success")
        elif request.form.get("ulozit_mailing_list"):
            set_mailing_list(request.form.get("mailing_list"))
            alog("Upraven mailing list.")
            flash("Mailing list byl upraven.", category="success")
        elif request.form.get("generovat"):
            alog("Vygenerování exportu.")
            exportovat()
            flash("Export vytvořen, najdeš ho v seznamu starších exportů.", category="success")
        elif request.form.get("smazat_export"):
            name: str = request.form.get("smazat_export")
            p = exporty_path() / name
            rmtree(p)
            flash("Export byl smazán.", category="success")
            alog("Smazání exportu z "+ pretty_datetime(name))
        return redirect(url_for("admin_views.prubeh_rocniku"))        

@admin_views.route("/velitele_odbornosti", methods=["GET","POST"])
@require_role_on_current_user("velitel_odbornosti")
def velitele_odbornosti():
    if request.method == "GET":
        return render_template("admin_velitele_odbornosti.html", roles=get_access_rights())
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


@admin_views.route("/generovat_seznamy/", methods=["GET","POST"])
@require_role_on_current_user("editing_users_allowed")
def generovat_seznamy():
    if request.method == "GET":
        flash("Tohe je ještě rozbitý.", category="error")
        return render_template("admin_generovat_seznamy.html", roles=get_access_rights())
    else:
        alog("Generování seznamu účastníků podle: " + request.form.get("result") + ".")
        kriteria = json.loads(request.form.get("result"))
        data = seznam_generator(kriteria)
        return json.dumps(data)

@admin_views.route("/prace", methods=["GET"])
@require_role_on_current_user("editing_users_allowed")
def prace():
    if request.method == "GET":
        return render_template("admin_prace.html", roles=get_access_rights())


@admin_views.route("/pohovory", methods=["GET","POST"])
@require_role_on_current_user("editing_pohovory")
def pohovory():
    if request.method == "GET":
        return render_template("admin_pohovory.html", roles=get_access_rights())
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
                alog(f"Vypsání nových termínů na pohovory mezi {start_datetime} a {end_datetime}")
                return redirect(url_for("admin_views.pohovory"))
        elif request.form.get("smazat"):
            isoformat = request.form.get("smazat")
            vysledek = smazat_termin(datetime.datetime.fromisoformat(isoformat))
            if vysledek:
                flash("Termín smazán.", category="success")
                alog(f"Smazání termínu pohovoru {isoformat}.")
            else:
                flash("Tento termín si mezitím někdo zapsal, nejde tedy smazat.", category="error")
            return redirect(url_for("admin_views.pohovory"))


@admin_views.route("/prohlaseni_rodicu", methods=["GET","POST"])
@require_role_on_current_user("admin")
def prohlaseni_rodicu():
    if request.method == "GET":
        return render_template("admin_prohlaseni_rodicu.html", roles=get_access_rights())
    else:
        file = request.files.get("souhlas")
        if file:
            file.name = "prohlaseni_rodicu.docx"
            file.save(prohlaseni_path())
            flash("Souhlas rodičů aktualizován.", category="success")
            alog("Nahraný nový soubor souhlasu rodičů.")
        else:
            flash("Nenahrál jsi žádný soubor.", category="error")
        return redirect(url_for("admin_views.admin_dashboard"))

@admin_views.route("/featury")
@require_role_on_current_user("admin")
def featury():
    return render_template("admin_featury.html", roles=get_access_rights())
    
@admin_views.route("/upravit_odkazy", methods=["GET","POST"])
@require_role_on_current_user("admin")
def upravit_odkazy():
    if request.method == "GET":
        return render_template("admin_upravit_odkazy.html", roles=get_access_rights())
    else:
        if request.form.get("smazat"):
            i = request.form.get("smazat")
            smazat_odkaz_by_id(i)
            flash("Odkaz odebrán", category="success")
            alog(f"Odebrán odkaz.")
        else:
            popis = request.form.get("popis")
            odkaz = request.form.get("odkaz")
            pridat_odkaz(popis=popis, odkaz=odkaz)
            flash("Odkaz přidán", category="success")
            alog(f"Přidán užitečný odkaz {odkaz}")
        return redirect(url_for("admin_views.upravit_odkazy"))
    

@admin_views.route("/info", methods=["GET","POST"])
@require_role_on_current_user("admin")
def info():
    if request.method == "GET":
        return render_template("admin_info.html", roles=get_access_rights())
    else:
        ulozit_info(request.form.to_dict())
        alog("Nové info pro účastníky.")
        flash("Informace byly uloženy.", category="success")
        return redirect(url_for("admin_views.info"))