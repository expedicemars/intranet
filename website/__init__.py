from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
from website.helpers.check_files import check_known_bugs_file, check_logs_files, check_mailing_list, check_velitel_odbornosti_data, check_user_data_folder, check_zadani_folders, check_poznamky, check_pohovory, check_exporty, check_odkazy, check_prubeh_rocniku, check_informace
from .paths import user_database_path, env_path
from .json_handlers.logs_handling import log
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=env_path())

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()


def create_app():
    check_logs_files()
    log("=== START appky ===")
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    db_username = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    db_adress = os.environ.get("DB_ADRESS")
    db_driver = os.environ.get("DB_DRIVER")
    db_name = os.environ.get("DB_NAME")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{db_driver}://{db_username}:{db_password}@{db_adress}/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
    app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")


    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .models.user import User
    from .models.chyba import Chyba
    # with app.app_context():
    #     if not user_database_path().exists():
    #         db.create_all()
    #         log("Vytvořena databáze na " + str(user_database_path()))
    #     else:
    #         log("Databáze uživatelů už existuje.")
    with app.app_context():
        db.create_all()

    from .views.default_views import default_views
    from .views.auth_views import auth_views
    from .views.admin_views import admin_views
    from .views.user_views  import user_views
    from .api.admin_api import admin_api
    from .api.noauth_api import noauth_api
    from .api.user_api import user_api
    from .api.file_api import file_api


    app.register_blueprint(default_views, url_prefix="/")
    app.register_blueprint(user_views, url_prefix="/")
    app.register_blueprint(auth_views, url_prefix="/auth")
    app.register_blueprint(admin_views, url_prefix = "/admin")
    app.register_blueprint(admin_api, url_prefix="/admin_api")
    app.register_blueprint(noauth_api, url_prefix="/noauth_api")
    app.register_blueprint(user_api, url_prefix="/user_api")
    app.register_blueprint(file_api, url_prefix="/file_api")

    
    check_known_bugs_file()
    check_mailing_list()
    check_velitel_odbornosti_data()
    check_user_data_folder()
    check_zadani_folders()
    check_poznamky()
    check_pohovory()
    check_exporty()
    check_odkazy()
    check_prubeh_rocniku()
    check_informace()
    


    login_manager.login_view = "auth_views.login"

    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, id)
    
    from website.role_handler import get_access_rights 

    @app.errorhandler(404)
    def not_found(e):
        return render_template("not_found.html", roles = get_access_rights()), 404

    @app.errorhandler(401)
    def not_authorised(e):
        return render_template("not_authorised.html", roles = get_access_rights()), 401

    return app
