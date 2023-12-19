from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from website.models.user import User
from website.mail_handler import mail_sender
from website.json_handlers.mailing_list import get_mails_from_mailing_list, pridat_mail_do_mailing_listu
from website.paths import user_data_folder_path
from website.json_handlers.prubeh_rocniku_handling import get_aktualni_faze


auth_views = Blueprint("auth_views",__name__)

@auth_views.route("/login", methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("user_views.ucet"))
	if request.method == "GET":
		return render_template("auth_login.html")
	else:
		email = request.form.get("email")
		password = request.form.get("password")
		if len(email) > 100:
			flash("Zadaný e-mail byl určitě přiliš dlouhý.", category="error")
			return redirect(url_for("auth_views.login"))
		if len(password) > 300:    
			flash("Zadané heslo bylo určitě příliš dlouhé.", category="error")
			return redirect(url_for("auth_views.login"))
		user = User.get_by_email(email)
		if user and check_password_hash(user.password, password):
			login_user(user, remember=True)
			flash("úspěšné přihlášení", category="success")
			return redirect(url_for("user_views.ucet"))
		else:
			flash("E-mail nebo heslo byly špatně", category="error")
			return redirect(url_for("auth_views.login"))

@auth_views.route("/register", methods=["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("user_views.ucet"))   
	elif not get_aktualni_faze()["system_name"] == "otevrena_registrace":
		return redirect(url_for("auth_views.mailing_list"))
	else:
		if request.method == "GET":
				return render_template("auth_register.html")
		else:
			email = request.form.get("email")
			password = request.form.get("password")
			souhlas = request.form.get("souhlas")
			if len(email) > 100:
				flash("Zadaný e-mail byl delší než 100 znaků. Vyberte prosím kratší.", category="error")
				return redirect(url_for("auth_views.register"))
			if len(password) > 300 or len(password) <= 7:    
				flash("Zvolené heslo nemělo vyhovující délku. Vyberte prosím nějaké mezi 8 a 300 znaky.", category="error")
				return redirect(url_for("auth_views.register"))
			if souhlas != "on":
				flash("Nesouhlasil jsi s podmínkama uchovávání dat.", category="error")
				return redirect(url_for("auth_views.register"))

			user = User.get_by_email(email)
			if user:
				flash("Tento email je už zaregistrovaný. Použij prosím jiný", category="error")
				return redirect(url_for("auth_views.register"))
			else:
				user = User(email=email, password=generate_password_hash(password, method="sha256"))
				db.session.add(user)
				db.session.commit()
				login_user(user, remember=False)
				flash("Úspěšná registrace.", category="info")
				# create files
				user_folder_path = user_data_folder_path() / str(user.id)
				prace_path = user_folder_path / "prace"
				user_folder_path.mkdir()
				prace_path.mkdir()
				token = current_user.get_reset_token()
				mail_sender(mail_identifier="potvrzeni_emailu", target=current_user.email, data=token)
				return redirect(url_for("user_views.ucet"))

@auth_views.route("/mailing_list", methods=["GET","POST"])		
def mailing_list():
	if current_user.is_authenticated:
		return redirect(url_for("user_views.ucet"))   
	elif get_aktualni_faze()["system_name"] == "otevrena_registrace":
		return redirect(url_for("auth_views.register"))
	else:
		if request.method == "GET":
			return render_template("auth_registrace_uzavrene.html")
		else:
			email = request.form.get("email")
			if len(email) > 100:
				flash("Zadaný e-mail byl delší než 100 znaků. Vyberte prosím kratší.", category="error")
				return redirect(url_for("auth_views.register"))
			user = User.get_by_email(email)
			if user:
				flash("Tento email je už zaregistrovaný. Použij prosím jiný", category="error")
				return redirect(url_for("auth_views.register"))
			if email in get_mails_from_mailing_list():
				flash("Tenhle mail už v mailing listu máme - upozorníme tě, až to bude potřeba :).", category="info")
				return redirect(url_for("default_views.home"))
			pridat_mail_do_mailing_listu(email)
			flash("Tvůj e-mail byl přidán do mailing-listu. Dáme ti vědět, až začne další ročník.", category="success")
			return redirect(url_for("default_views.home"))


@auth_views.route("/logout")
def logout():
	if current_user.is_authenticated:
		logout_user()
		flash("Odhlášení proběhlo úspěšně :)", category="info")
		return redirect(url_for("default_views.home"))
	else:
		flash("HA! slídil :)", category="success")
		return redirect(url_for("default_views.home"))


@auth_views.route("/reset_password", methods=["GET","POST"])
def request_reset():
	if current_user.is_authenticated:
		return redirect(url_for("default_views.home"))
	if request.method == "GET":
		return render_template("auth_request_reset.html")
	else:
		email = request.form.get("email")
		if len(email) > 100:
			flash("Zadaný e-mail byl určitě moc dlouhý.", category="error")
			return redirect(url_for("auth_views.request_reset"))
		user = User.get_by_email(email)
		if user:
			mail_sender(mail_identifier="reset_password", target=email, data=user.get_reset_token())
		flash("Pokud existuje uživatel s tímto e-mailem, byl mu odeslán ověřovací e-mail.", category="info")
		return redirect(url_for("auth_views.login"))


@auth_views.route("/reset_password/<token>", methods=["GET","POST"])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for("user_views.ucet"))
	user = User.verify_reset_token(token)
	if user is None:
		flash("Obnovovací link vypršel, nebo je jinak neplatný.", category="info")
		return redirect(url_for("auth_views.request_reset"))
	if request.method == "GET":
		return render_template("auth_reset_password.html")
	else:
		user.password = generate_password_hash(request.form.get("password"), method="sha256")
		db.session.commit()
		flash("Heslo změněno, můžete se nyní přihlásit:", category="info")
		return redirect(url_for("auth_views.login"))


		
	





