from flask_login import UserMixin
from website import db
from flask import current_app
import jwt
import json
from website.paths.paths import user_data_folder_path
from shutil import rmtree
from website.helpers.pretty_date import pretty_date
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
    souhlas_rodicu = db.Column(db.Boolean, default=False)
    odbornost = db.Column(db.String(100), default="zatím nevybraná")
    datum_narozeni = db.Column(db.String(100))
    progress = db.Column(db.String(100), default="Domácí kolo")
    role = db.Column(db.Text, default=json.dumps(["user"]))
    tricko = db.Column(db.String(100))
    dozvedeli = db.Column(db.String(100))
    admin_poznamka = db.Column(db.String(1000))
    hodnoceni_motivaku = db.Column(db.String(5000))
    uzamcene_zmeny = db.Column(db.Boolean, default=False)
    alergie = db.Column(db.String(1000))
    skola = db.Column(db.String(1000))
    datum_registrace = db.Column(
        db.String(100), default=datetime.now().isoformat())
    datum_pohovoru = db.Column(db.String(100))
    meeting_link = db.Column(db.String(1000))

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
        info["hodnoceni_motivaku"] = self.hodnoceni_motivaku
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
            "souhlas_rodicu": self.souhlas_rodicu,
            "odbornost": self.odbornost,
            "datum_narozeni": self.datum_narozeni,
            "progress": self.progress,
            "role": self.role,
            "tricko": self.tricko,
            "dozvedeli": self.dozvedeli,
            "alergie": self.alergie,
            "skola": self.skola,
            "datum_registrace": pretty_date(self.datum_registrace),
            "datum_pohovoru": pretty_date(self.datum_pohovoru),
            "meeting_link": self.meeting_link
        }

    def odstranit(self):
        db.session.delete(self)
        db.session.commit()
        osobni_slozka = user_data_folder_path() / str(self.id)
        rmtree(osobni_slozka)

    @staticmethod
    def generate_random() -> "User":
        import random
        import datetime

        def biased_coin() -> bool:
            return random.randint(0, 100) < 70

        # povinne veci
        u = User()
        db.session.add(u)
        db.session.commit()
        user_folder_path = user_data_folder_path() / str(u.id)
        prace_path = user_folder_path / "prace"
        user_folder_path.mkdir()
        prace_path.mkdir()
        u.email = "dummy_email_" + str(u.id)
        u.confirmed = True
        u.role = json.dumps(["user"])

        # veci co muzou byt nahodne
        if biased_coin():
            u.jmeno = "dummy_jmeno_" + str(u.id)
        if biased_coin():
            u.adresa = "dummy_adresa_" + str(u.id)
        if biased_coin():
            u.telcislo = "dummy_telcislo_" + str(u.id)
        if biased_coin():
            u.mail_rodicu = "dummy_mail_rodicu_" + str(u.id)
        if biased_coin():
            u.odbornost = random.choice(
                ["biolog", "konstrukter", "inzenyr", "fyzik", "popularizator"])
        if biased_coin():
            u.datum_narozeni = datetime.date.today().isoformat()
        if biased_coin():
            u.progress = random.choice(
                ["Domácí kolo", "Semifinále", "Finále", "Simulace"])
        if biased_coin():
            u.tricko = random.choice(["XS", "S", "M", "L", "XL"])
        if biased_coin():
            u.dozvedeli = "dummy_dozvedeli"
        if biased_coin():
            u.admin_poznamka = "dummy_admin_poznamka"
        if biased_coin():
            u.hodnoceni_motivaku = "dummy_hodnoceni_motivaku"
        if biased_coin():
            u.uzamcene_zmeny = random.choice([True, False])
        if biased_coin():
            u.alergie = "dummy_alergie"
        if biased_coin():
            u.skola = "dummy_skola"
        if biased_coin():
            motivak_path = user_data_folder_path() / str(u.id) / "motivak.txt"
            motivak_path.touch()
        if biased_coin():
            prace_path = user_data_folder_path() / str(u.id) / "prace" / "pr.txt"
            prace_path.touch()
        if biased_coin():
            profilovka = user_data_folder_path() / str(u.id) / "profilovka.jpg"
            profilovka.touch()
        if biased_coin():
            u.datum_pohovoru = datetime.datetime.utcnow().isoformat()
        if biased_coin():
            u.datum_registrace = (datetime.datetime.utcnow(
            ) - datetime.timedelta(days=365)).isoformat()

        db.session.add(u)
        db.session.commit()
        return u
