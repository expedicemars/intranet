from flask_login import UserMixin
from website import db
from flask import current_app
import jwt
import json
from website.paths import user_data_folder_path
from shutil import rmtree
from website.helpers.pretty_date import pretty_date, pretty_datetime
from datetime import datetime, timezone, timedelta


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    confirmed = db.Column(db.Boolean, default=False)
    jmeno = db.Column(db.String(100))
    adresa = db.Column(db.String(100))
    telcislo = db.Column(db.String(100))
    mail_rodicu = db.Column(db.String(100))
    odbornost = db.Column(db.String(100), default="zatím nevybraná")
    datum_narozeni = db.Column(db.Date)
    progress = db.Column(db.String(100), default="Registrován")
    role = db.Column(db.Text, default=json.dumps(["user"]))
    tricko = db.Column(db.String(100))
    dozvedeli = db.Column(db.String(100))
    admin_poznamka = db.Column(db.String(1000))
    uzamcene_zmeny = db.Column(db.Boolean, default=False)
    alergie = db.Column(db.String(1000))
    skola = db.Column(db.String(1000))
    datum_registrace = db.Column((db.DateTime), default=datetime.now())
    datum_pohovoru = db.Column(db.DateTime)
    meeting_link = db.Column(db.String(1000))
    motivacni_dotaznik = db.Column(db.Text)

    def get_reset_token(self, expires_sec=9000) -> str:
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec)
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return reset_token

    @staticmethod
    def verify_reset_token(token) -> "User":
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return None
        return db.session.get(User, data["user_id"])

    def get_full_info(self) -> dict:
        info = self.get_basic_info()
        info["admin_poznamka"] = self.admin_poznamka
        info["uzamcene_zmeny"] = self.uzamcene_zmeny
        return info

    def get_basic_info(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "confirmed": self.confirmed,
            "jmeno": self.jmeno,
            "adresa": self.adresa,
            "telcislo": self.telcislo,
            "mail_rodicu": self.mail_rodicu,
            "odbornost": self.odbornost,
            "datum_narozeni": self.datum_narozeni.isoformat() if self.datum_narozeni else None,
            "progress": self.progress,
            "role": self.role,
            "tricko": self.tricko,
            "dozvedeli": self.dozvedeli,
            "alergie": self.alergie,
            "skola": self.skola,
            "datum_registrace": pretty_datetime(self.datum_registrace),
            "datum_pohovoru": pretty_datetime(self.datum_pohovoru),
            "meeting_link": self.meeting_link
        }

    def odstranit(self):
        db.session.delete(self)
        db.session.commit()
        osobni_slozka = user_data_folder_path() / str(self.id)
        rmtree(osobni_slozka)
    
    def odebrat_odbornost(self):
        self.odbornost = "zatím nevybraná"
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def jmenovat_admina_by_email(email) -> "User":
        u = User.get_by_email(email)
        if u:
            u.role = json.dumps(["admin", "editing_admins_allowed"])
            db.session.add(u)
            db.session.commit()
            return "Success"
        else:
            return "Zadadný mail v db neexistuje"
    
    @staticmethod
    def get_by_id(id) -> "User":
        return db.session.get(User, int(id))
    
    @staticmethod
    def get_by_email(email) -> "User":
        return db.session.scalars(db.select(User).where(User.email == email)).first()

    @staticmethod
    def get_all():
        return db.session.scalars(db.select(User)).all()
    

