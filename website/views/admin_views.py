from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from website.models.chyba import Chyba
from website.models.user import User
from website.json_handlers.logs_handling import delete_logs
from website.paths.paths import terminy_path,faze_path, velitel_odbornosti_data_path, zadani_folder_path
import json
from website.roles.role_handler import get_access_rights
from website import db
from website.helpers.mailing_list import promazat_mailing_list


admin_views = Blueprint("admin_views",__name__)

@admin_views.route("/")
@admin_views.route("/dashboard")
def admin_dashboard():
    rights = get_access_rights(current_user)
    if "admin" in rights:
        return render_template("admin_dashboard.html", pocet_bugu = Chyba.pocet_neresenych(), roles=rights)
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
            return redirect(url_for("admin_views.admin_dashboard"))
    else:
        abort(401)
    

@admin_views.route("/logs_file", methods=["GET","POST"])
def logs_file():
    rights = get_access_rights(current_user)
    if "editing_logs_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_logs_file.html", roles=rights)
        else:
            delete_logs()
            flash("Soubor s logy byl promazán.",category="success")
            return redirect(url_for("admin_views.admin_dashboard"))
    else:
        abort(401)


@admin_views.route("/edit_users", methods=["GET","POST"])
def edit_users():
    rights = get_access_rights(current_user)
    if "editing_users_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_edit_users.html", roles=rights)
        else:
            result = request.form.get("result")
            return redirect(url_for("admin_views.detail_usera",id=int(result)))
    else:
        abort(401)
    
@admin_views.route("/edit_users/<int:id>", methods=["GET","POST"])
def detail_usera(id):
    rights = get_access_rights(current_user)
    if "editing_users_allowed" in rights:
        if request.method == "GET":
            return render_template("admin_detail_usera.html", roles = rights, id=id)
        else:
            if request.form.get("smazat"):
                User.query.get(id).odstranit()
                flash("User byl smazán", category="success")
                return redirect(url_for("admin_views.edit_users"))
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
            nove_role = json.loads(request.form.get("result"))
            u = User.query.get(id)
            u.role = json.dumps(nove_role)
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
                flash(f"Zadání odborosti {odbornost} je smazaný.", category="success")
            
            # ukládání souborů
            elif request.form.get("ulozit_zadani"):
                odbornost = request.form.get("ulozit_zadani")
                if all(request.files.getlist(f"{odbornost}_files")):
                    for file in request.files.getlist(f"{odbornost}_files"):
                        file.save(zadani_folder_path() / odbornost / file.filename)
                    flash("Zadání nahráno.", category="success")
                else:
                    flash("Nenahrál jsi žádné soubory.", category="info")


            # zapisování kontaktních dat
            else:
                inputs_ids_list = ["biolog", "konstrukter", "fyzik", "inzenyr", "popularizator"]
                with open(velitel_odbornosti_data_path()) as file:
                    velitel_odbornosti_data = json.load(file)
                for id in inputs_ids_list:
                    res = request.form.get(id)
                    if res is None:
                        pass
                    else:
                        velitel_odbornosti_data[id] = res
                with open(velitel_odbornosti_data_path(),"w") as file:
                    file.write(json.dumps(velitel_odbornosti_data, indent=4))


                flash("Data velitelů odborností byla upravena.", category="success")
            return redirect(url_for("admin_views.velitele_odbornosti"))

    else:
        abort(401)