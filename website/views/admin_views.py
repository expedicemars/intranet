from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from website.models.chyba import Chyba
from website.models.user import User
from website.json_handlers.logs_handling import delete_logs
import json
from website.roles.role_handler import get_access_rights
from website import db


admin_views = Blueprint("admin_views",__name__)

@admin_views.route("/")
@admin_views.route("/dashboard")
def admin_dashboard():
    roles = get_access_rights(current_user)
    if "admin" in roles:
        flash("Zkouška error hlášky", category="error")
        flash("Zkouška success hlášky", category="success")
        flash("Zkouška info hlášky", category="info")
        print(roles)
        return render_template("admin_dashboard.html", pocet_bugu = Chyba.pocet_neresenych(), roles=roles)
    else:
        abort(401)


@admin_views.route("/planovane_featury")
def planovane_featury():
    if "admin" in get_access_rights(current_user):
       return render_template("admin_planovane_featury.html", roles=get_access_rights(current_user))
    else:
        abort(401)


@admin_views.route("/historie_verzi")
def historie_verzi():
    if "admin" in get_access_rights(current_user):
        return render_template("admin_historie_verzi.html", roles=get_access_rights(current_user))
    else:
        abort(401)


@admin_views.route("/uprava_znamych_bugu", methods=["GET","POST"])
def uprava_znamych_bugu():
    if "editing_bugs_allowed" in get_access_rights(current_user):
        if request.method == "GET":
            return render_template("admin_uprava_znamych_chyb.html", roles=get_access_rights(current_user))
        else:
            Chyba.save_po_upravach(json.loads(request.form.get("result")))
            return redirect(url_for("admin_views.admin_dashboard"))
    else:
        abort(401)
    

@admin_views.route("/logs_file", methods=["GET","POST"])
def logs_file():
    if "editing_logs_allowed" in get_access_rights(current_user):
        if request.method == "GET":
            return render_template("admin_logs_file.html", roles=get_access_rights(current_user))
        else:
            delete_logs()
            return redirect(url_for("admin_views.admin_dashboard"))
    else:
        abort(401)


@admin_views.route("/edit_users", methods=["GET","POST"])
def edit_users():
    if "editing_users_allowed" in get_access_rights(current_user):
        if request.method == "GET":
            return render_template("admin_edit_users.html", roles=get_access_rights(current_user))
        else:
            result = request.form.get("result")
            user_na_odstraneni = User.query.get(int(result))
            if "admin" in user_na_odstraneni.role:
                flash("Nemůžeš odstranit admina.", category="error")
                return redirect(url_for("admin_views.edit_users"))
            else:
                user_na_odstraneni.odstranit()
                flash("User smazán", category="success")
                return redirect(url_for("admin_views.admin_dashboard"))
    else:
        abort(401)

@admin_views.route("/jmenovat_adminy", methods=["GET","POST"])
def jmenovat_adminy():
    if "editing_admins_allowed" in get_access_rights(current_user):
        if request.method == "GET":
            return render_template("admin_jmenovat_adminy.html", roles=get_access_rights(current_user))
        else:
            return redirect(url_for("admin_views.vybrat_role_adminovi", id=int(request.form.get("result"))))
    else:
        abort(401)

@admin_views.route("/jmenovat_adminy/<int:id>", methods=["GET","POST"])
def vybrat_role_adminovi(id):
    if "editing_admins_allowed" in get_access_rights(current_user):
        if request.method == "GET":
            return render_template("admin_vybrat_role_adminovi.html", user=User.query.get(id), roles=get_access_rights(current_user))
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
