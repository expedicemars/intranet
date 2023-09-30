import json
import datetime
from shutil import rmtree
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from website import db
from website.helpers.require_role_decorator import require_role_on_current_user
from website.models.chyba import Chyba
from website.models.user import User
from website.models.hodnoceni import Hodnoceni
from website.models.motivacni_call import Motivacni_call
from website.json_handlers.mailing_list import set_mailing_list
from website.helpers.user_filter import seznam_generator
from website.helpers.exporty import exportovat, promazat
from website.helpers.pretty_date import pretty_datetime
from website.role_handler import get_access_rights
from website.json_handlers.logs_handling import delete_logs,  delete_alogs, alog
from website.json_handlers.poznamky_handling import zapsat_poznamky
from website.json_handlers.odkazy_handling import pridat_odkaz, smazat_odkaz_by_id
from website.json_handlers.prubeh_rocniku_handling import set_nove_datum_konce_registrace, set_nove_datum_zacatku_registrace, toggle_registrace, get_registrace_otevrena, toggle_zadani, get_zadani_viditelne, zapsat_koordinatora_i_kol, toggle_info_o_konferenci, get_info_o_konferenci_viditelne, zapsat_info_o_konferenci
from website.json_handlers.dostupne_omezeni import get_dostupne_odbornosti
from website.json_handlers.velitele_odbornosti_handling import zapsat_kontakt
from website.paths import zadani_folder_path, prohlaseni_path, exporty_path, sablony_folder_path, vzorove_vypracovani_path


admin_views = Blueprint("admin_views",__name__)

@admin_views.route("/", methods=["GET","POST"])
@admin_views.route("/dashboard", methods=["GET","POST"])
@require_role_on_current_user("admin")
def admin_dashboard():
    if request.method == "GET":
        flash("Vítej a porozhlédni se tu. Zatím nejlépe shrnuté a popsané fíčury jsou dole v patičce v Přehledu fíčur systému.", category="success")
        return render_template("admin_dashboard.html", roles=get_access_rights())
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
        result = request.form.get("result")
        return redirect(url_for("admin_views.detail_usera",id=int(result)))
        
    
@admin_views.route("/detail_usera/<int:id>", methods=["GET","POST"])
@require_role_on_current_user("editing_users_allowed")
def detail_usera(id):
    if request.method == "GET":
        return render_template("admin_detail_usera.html", roles=get_access_rights(), id=id)
    else:
        u = User.get_by_id(id)
        if request.form.get("odebrat_motivacni_call"): #není tu check na to, zda m = None, protože disabluju tlačítko pomocí JS.
            m = Motivacni_call().get_by_user_id(id)
            m.user_id = None
            m.meeting_link = None
            db.session.add(m)
            db.session.commit()
            alog(f"Vymazána volba motivačního callu usera {u.email}")
            flash("Volba motivačního callu byla promazána.", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))
        
        elif request.form.get("progress_button"):
            p = request.form.get("progress")
            if u.progress == p:
                flash("Progres uživatele nezměněn, vybral jsi stejný progress.", category="info")
            else:
                u.progress = p
                u.save()
                alog(f"Změna progressu uživatele {u.email} na { p }.")
                flash(f"Progress uživatele změněn na {p}", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))
    
        elif request.form.get("odbornost_button"):
            odbornosti = get_dostupne_odbornosti()
            odbornosti.append({
                "system_name":"zatím nevybraná",
                "prvnipjc": "zatím nevybraná"
            })
            o_dict = list(filter(lambda x: x["system_name"] == request.form.get("odbornost"), odbornosti))[0]
            if u.odbornost == o_dict["system_name"]:
                flash("Odbornost uživatele nezměněna, vybral si stejnou.", category="info")
            else:
                u.odbornost = o_dict["system_name"]
                u.save()
                alog(f"Změna odbornosti uživatele {u.email} na { o_dict['prvnipjc'] }.")
                flash(f"Odbornost uživatele změněna na { o_dict['prvnipjc']}.", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))

        elif request.form.get("admin_poznamka_button"):
            admin_poznamka = request.form.get("admin_poznamka")
            if len(admin_poznamka) > 1000:
                flash("Admin poznámka je moc dlouhá, sori. Může bejt max 1000 znaků.", category="error")
                return redirect(url_for("admin_views.detail_usera", id=id))
            if admin_poznamka == "":
                admin_poznamka = None
            if u.admin_poznamka == admin_poznamka:
                flash("Admin poznámka uživatele nezměněna, byla stejná.", category="info")
            else:
                u.admin_poznamka = admin_poznamka
                u.save()
                flash("Změna admin poznámky.", category="success")
                alog(f"Změna admin poznámky uživatele {u.email}.")
            return redirect(url_for("admin_views.detail_usera", id=id))
        
        elif request.form.get("meeting_button"):
            meeting_link = request.form.get("meeting_link")
            if len(meeting_link) > 1000:
                flash("Meeting link je moc dlouhý. Může bejt max 1000 znaků.", category="error")
                return redirect(url_for("admin_views.detail_usera", id=id))
            if meeting_link == "":
                meeting_link = None
            m = Motivacni_call.get_by_user_id(id)
            if not m:
                flash("Nemůžeš upravovat meeting link, tento uživatel není zapsaný na žádném callu.", category="info")
                return redirect(url_for("admin_views.detail_usera", id=id))
            if m.meeting_link == meeting_link:
                flash("Meeting link uživatele nezměněn, byla stejný.", category="info")
            else:
                m.meeting_link = meeting_link
                m.save()
                flash("Změna meeting linku.", category="success")
                alog(f"Změna meeting linku uživatele {u.email}.")
            return redirect(url_for("admin_views.detail_usera", id=id))
        
            
        elif request.form.get("odebrat_motivacni_formular"):
            u.odebrat_motivacni_formular()
            alog(f"Vymazán motivační formulář usera {u.email}")
            flash("Motivační formulář byl promazán.", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))
        
        elif request.form.get("zpristupnit_motivacni_formular"):
            u.znovu_zpristupnit_motivacni_formular()
            alog(f"Znovu zpřístupněn motivační formulář usera {u.email}")
            flash("Motivační formulář byl znovu zpřístupněn.", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))

        elif request.form.get("hodnoceni"):
            return redirect(url_for("admin_views.hodnoceni", id=id))
        
        elif request.form.get("uzamcene_zmeny_udaju"):
            u.uzamcene_zmeny_udaju = not u.uzamcene_zmeny_udaju
            u.save()
            alog(f"Uzamčení změn údajů akatualizováno na {u.uzamcene_zmeny_udaju}")
            flash("Uzamčení změn údajů aktualizováno.", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))
        
        elif request.form.get("uzamcene_zmeny_callu"):
            u.uzamcene_zmeny_callu = not u.uzamcene_zmeny_callu
            u.save()
            alog(f"Uzamčení změn callů akatualizováno na {u.uzamcene_zmeny_callu}")
            flash("Uzamčení změn callů aktualizováno.", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))
        
        elif request.form.get("uzamcene_zmeny_prace"):
            u.uzamcene_zmeny_prace = not u.uzamcene_zmeny_prace
            u.save()
            alog(f"Uzamčení změn práce akatualizováno na {u.uzamcene_zmeny_prace}")
            flash("Uzamčení změn práce aktualizováno.", category="success")
            return redirect(url_for("admin_views.detail_usera", id=id))
        
        elif id_hodnoceni := request.form.get("smazat_hodnoceni"):
            Hodnoceni.get_by_id(id_hodnoceni).smazat()
            flash("Hodnocení smazáno", category="success")
            alog(f"Smazáno hodnocení od uživatele {u.email}")
            return redirect(url_for("admin_views.detail_usera", id=id))
        
        elif request.form.get("smazat"):
            if "admin" in json.loads(u.role):
                alog(f"Pokus o smazání admina {u.email}")
                flash("Nemůžeš mazat adminy!", category="error")
                return redirect(url_for("admin_views.registrovani_uzivatele"))
            else:
                u.odstranit()
                alog("Smazání usera " + str(id) + ".")
                flash("User byl smazán", category="success")
                return redirect(url_for("admin_views.registrovani_uzivatele"))



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
        elif request.form.get("ulozit_datum_otevreni"):
            datum = request.form.get("datum_otevreni")
            set_nove_datum_zacatku_registrace(datum)
            alog(f"Úprava termmínu začátku registrace na {datum}.")
            flash("Termín začátku registrace byl upraven.", category="success")
        elif request.form.get("ulozit_datum_uzavreni"):
            datum = request.form.get("datum_uzavreni")
            set_nove_datum_konce_registrace(datum)
            alog(f"Úprava termínu konce registrace na {datum}.")
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
        elif request.form.get("toggle_zadani"):
            toggle_zadani()
            alog(f"Změna viditelnosti zadání na {get_zadani_viditelne()}")
            flash(f"Stav viditelnosti zadání změnen na {get_zadani_viditelne()}", category="success")
        elif request.form.get("koordinator_internetovych_kol_button"):
            kontakt = request.form.get("koordinator_internetovych_kol")
            zapsat_koordinatora_i_kol(kontakt)
            alog(f"Změněn kontakt na koordinátora internetových kol na {kontakt}.")
            flash("Kontakt na koordinátora internetových kol změněn.", category="success")
        elif request.form.get("toggle_info_o_konferenci"):
            toggle_info_o_konferenci()
            alog(f"Změna viditelnosti stránky o online konferenci na {get_info_o_konferenci_viditelne()}")
            flash(f"Stav viditelnosti infa o online konferenci změnen na {get_info_o_konferenci_viditelne()}", category="success")
        return redirect(url_for("admin_views.prubeh_rocniku"))        

@admin_views.route("/velitele_odbornosti", methods=["GET","POST"])
@require_role_on_current_user("velitel_odbornosti")
def velitele_odbornosti():
    if request.method == "GET":
        return render_template("admin_velitele_odbornosti.html", roles=get_access_rights())
    else:
        # mazani souboru
        if odbornost := request.form.get("smazat_zadani"):
            path = zadani_folder_path() / odbornost
            for file in path.iterdir():
                file.unlink()
            alog(f"Smazání zadání odbornosti {odbornost}.")
            flash(f"Zadání odborosti {odbornost} je smazaný.", category="success")
        
        # ukládání souborů
        elif odbornost := request.form.get("ulozit_zadani"):
            if all(request.files.getlist(f"{odbornost}_files")):
                for file in request.files.getlist(f"{odbornost}_files"):
                    file.save(zadani_folder_path() / odbornost / file.filename)
                flash("Zadání nahráno.", category="success")
                alog(f"Nahrání nového zadání pro odbornost {odbornost}.")
            else:
                flash("Nenahrál jsi žádné soubory.", category="info")


        # zapisování kontaktních dat
        elif odbornost := request.form.get("ulozit_kontakt"):
            zapsat_kontakt(odbornost=odbornost, data=request.form.get(odbornost))
            alog("Úprava kontaktních údajů pro odbornost " + odbornost)
            flash("Data velitelů odborností byla upravena.", category="success")
        return redirect(url_for("admin_views.velitele_odbornosti"))


@admin_views.route("/generovat_seznamy/", methods=["GET","POST"])
@require_role_on_current_user("editing_users_allowed")
def generovat_seznamy():
    if request.method == "GET":
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


@admin_views.route("/motivacni_call", methods=["GET","POST"])
@require_role_on_current_user("editing_pohovory")
def motivacni_call():
    if request.method == "GET":
        return render_template("admin_motivacni_call.html", roles=get_access_rights())
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
                return redirect(url_for("admin_views.motivacni_call"))
            if start_datetime > end_datetime:
                flash("Časy, kkteré byly zadány, nedávaly smysl. Zkus to znova.", category="error")
                return redirect(url_for("admin_views.motivacni_call"))
            else:
                Motivacni_call.pridat_pohovory(start_datetime=start_datetime, end_datetime=end_datetime, admin=current_user)
                flash("Termíny vypsány.", category="success")
                alog(f"Vypsání nových termínů na pohovory mezi {start_datetime} a {end_datetime}")
                return redirect(url_for("admin_views.motivacni_call"))
        elif r := request.form.get("smazat_ids_list"):
            ids_list = json.loads(r)
            skipped_some = False
            for id in ids_list:
                m: Motivacni_call
                m = Motivacni_call.get_by_id(id)
                if m.user_id:
                    skipped_some = True
                else:
                    m.delete()
            alog("Smazání vybraných termínů pohovorů")
            if skipped_some:
                flash("Na některé vybrané pohovory se mezitím někdo zapsal. Ostatní byly smazány.", category="info")
            else:
                flash("Termíny smazány.", category="success")
            return redirect(url_for("admin_views.motivacni_call"))
        elif request.form.get("smazat_48"):
            for m in Motivacni_call.get_all():
                if m.datum_a_cas - datetime.timedelta(hours=48) < datetime.datetime.now() and not m.user_id:
                    m.delete()
            alog("Smazání termínů bližších než 48 hodin.")
            flash("Termíny smazány.", category="success")
            return redirect(url_for("admin_views.motivacni_call"))


@admin_views.route("/nahrat_soubory", methods=["GET","POST"])
@require_role_on_current_user("admin")
def nahrat_soubory():
    if request.method == "GET":
        return render_template("admin_nahrat_soubory.html", roles=get_access_rights())
    else:
        if request.form.get("souhlas"):
            file = request.files.get("souhlas_file")
            if file:
                file.name = "prohlaseni_rodicu.docx"
                file.save(prohlaseni_path())
                flash("Souhlas rodičů aktualizován.", category="success")
                alog("Nahraný nový soubor souhlasu rodičů.")
            else:
                flash("Nenahrál jsi žádný soubor.", category="error")
        elif request.form.get("vzor"):
            file = request.files.get("vzor_file")
            if file:
                file.name = "vzorove_vypracovani.docx"
                file.save(vzorove_vypracovani_path())
                flash("Vzorové vypracování aktualizováno.", category="success")
                alog("Nahraný nový soubor vzorového vypracování odbornostního kola.")
            else:
                flash("Nenahrál jsi žádný soubor.", category="error")
        else:
            for odb in get_dostupne_odbornosti():
                if request.form.get(odb["system_name"]):
                    file = request.files.get(odb["system_name"] + "_file")
                    if file:
                        file.name = odb["system_name"] + "_sablona.docx"
                        path = sablony_folder_path() / file.name
                        file.save(path)
                        flash(f"Šablona {odb['druhypmc']} aktualizována.", category="success")
                    else:
                        flash("Nenahrál jsi žádný soubor.", category="error")  
                    break
        return redirect(url_for("admin_views.nahrat_soubory"))

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
    
    
@admin_views.route("/organizatori", methods=["GET","POST"])
@require_role_on_current_user("editing_users_allowed")
def organizatori():
    if request.method == "GET":
        return render_template("admin_organizatori.html", roles=get_access_rights())
    else:
        result = request.form.get("result")
        return redirect(url_for("admin_views.detail_usera",id=int(result)))
    
    
@admin_views.route("/hodnoceni/<int:id>", methods=["GET","POST"])
@require_role_on_current_user("editing_users_allowed")
def hodnoceni(id):
    if request.method == "GET":
        return render_template("admin_hodnoceni.html", roles=get_access_rights(), jmeno=User.get_by_id(id).jmeno)
    else:
        Hodnoceni.zapsat_hodnoceni(request.form.to_dict(), id, current_user.id)
        flash("Hodnocení zapsáno", category="success")
        return redirect(url_for("admin_views.detail_usera", id=id))
    

@admin_views.route("/struktura_rozhovoru")
@require_role_on_current_user("admin")
def struktura_rozhovoru():
    return render_template("admin_struktura_rozhovoru.html", roles=get_access_rights())

@admin_views.route("/info_o_konferenci", methods=["GET","POST"])
@require_role_on_current_user("editing_prubeh_rocniku")
def info_o_konferenci():
    if request.method == "GET":
        return render_template("admin_info_o_konferenci.html", roles=get_access_rights())
    else:
        if request.form.get("content"):
            zapsat_info_o_konferenci(request.form.get("content"))
            alog("Změna informací o konferenci")
            flash("Info o konferenci změněno", category="success")
            return redirect(url_for("admin_views.prubeh_rocniku"))
        else:
            return request.form.to_dict()