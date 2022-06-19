from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
from website.hepers.check_files import check_known_bugs_file, check_logs_file, check_mailing_list
from .paths.paths import user_database_path
from .json_handlers.logs_handling import log

DB_NAME = "database.db"

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()


def create_app():
    check_logs_file()
    log("=== START appky ===")
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "5aaad9a24b756347536be2fc4b4a2c40a876cd0bd0dd782ecd7303bb1ba0dbbc"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["MAIL_SERVER"] = "smtp.googlemail.com"
    app.config["MAIL_PORT"] = "587"
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "josef.latj@gmail.com"
    app.config["MAIL_PASSWORD"] = "gewfrzvyateqfoya"


    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    def check_if_database_exists_else_create(app):
        if not user_database_path().exists():
            db.create_all(app=app)
            log("created db at " + str(user_database_path))
        else:
            log("user database already exists")

    from .views.default_views import default_views
    from .views.auth_views import auth_views
    from .views.admin_views import admin_views
    from .views.sender_endpoints import sender
    from .views.user_views  import user_views

    app.register_blueprint(default_views, url_prefix="/")
    app.register_blueprint(user_views, url_prefix="/")
    app.register_blueprint(auth_views, url_prefix="/auth")
    app.register_blueprint(admin_views, url_prefix = "/admin")
    app.register_blueprint(sender, url_prefix="/")

    from .models.user import User
    
    check_if_database_exists_else_create(app)
    check_known_bugs_file()
    check_mailing_list()

    login_manager.login_view = "auth_views.login"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from website.roles.role_handler import get_access_rights 

    @app.errorhandler(404)
    def not_found(e):
        return render_template("not_found.html", roles = get_access_rights(current_user)), 404

    @app.errorhandler(401)
    def not_found(e):
        return render_template("not_authorised.html", roles = get_access_rights(current_user)), 401

    return app
