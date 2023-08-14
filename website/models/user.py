from flask_login import UserMixin
from website import db
from flask import current_app
import jwt
import json
from website.paths import user_data_folder_path
from shutil import rmtree
from website.helpers.pretty_date import pretty_datetime, pretty_date
from website.helpers.get_user_files import get_prace_filenames, get_shrnuti_filename
from website.json_handlers.pohovory_handling import odhlasit_usera_by_id
from website.json_handlers.dostupne_omezeni import get_odbornost_by_system_name
from datetime import datetime, timezone, timedelta
from pathlib import Path

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
    progress = db.Column(db.String(100), default="Motivační formulář")
    role = db.Column(db.Text, default=json.dumps(["user"]))
    tricko = db.Column(db.String(100))
    dozvedeli = db.Column(db.String(100))
    admin_poznamka = db.Column(db.String(1000))
    uzamcene_zmeny = db.Column(db.Boolean, default=False)
    alergie = db.Column(db.String(1000))
    skola = db.Column(db.String(1000))
    datum_registrace = db.Column((db.DateTime), default=datetime.now)
    datum_pohovoru = db.Column(db.DateTime)
    meeting_link = db.Column(db.String(1000))
    motivacni_dotaznik = db.Column(db.Text)
    odevzdany_motivacni_dotaznik = db.Column(db.Boolean)
    osloveni_1p = db.Column(db.String(200))
    osloveni_5p = db.Column(db.String(200))
    zajmeno = db.Column(db.String(200))

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
    
    def get_info_na_ucet_stranku(self) -> dict:
        return {
            "jmeno": self.jmeno,
            "email": self.email,
            "adresa": self.adresa,
            "telcislo": self.telcislo,
            "datum_narozeni": self.datum_narozeni.isoformat() if self.datum_narozeni else None,
            "mail_rodicu": self.mail_rodicu,
            "dozvedeli": self.dozvedeli,
            "alergie": self.alergie,
            "skola": self.skola,
            "confirmed": "Ano" if self.confirmed else "Ne",
            "odbornost": get_odbornost_by_system_name(self.odbornost)["prvnipjc"] if self.odbornost != "zatím nevybraná" else "zatím nevybraná",
            "progress": self.progress,
            "tricko": self.tricko,
            "datum_registrace": pretty_datetime(self.datum_registrace),
            "datum_pohovoru": pretty_datetime(self.datum_pohovoru),
            "osloveni_1p": self.osloveni_1p,
            "osloveni_5p": self.osloveni_5p,
            "zajmeno": self.zajmeno
        }
    
    def get_info_na_detail_usera(self) -> dict:
        return {
            "jmeno": self.jmeno,
            "datum_narozeni": pretty_date(self.datum_narozeni.isoformat()) if self.datum_narozeni else None,
            "email": self.email,
            "telcislo": self.telcislo,
            "adresa": self.adresa,
            "confirmed": self.confirmed,
            "id": self.id,
            "tricko": self.tricko,
            "mail_rodicu": self.mail_rodicu,
            "odbornost": self.odbornost,
            "dozvedeli": self.dozvedeli,
            "alergie": self.alergie,
            "skola": self.skola,
            "datum_registrace": pretty_datetime(self.datum_registrace),
            "datum_pohovoru": pretty_datetime(self.datum_pohovoru),
            "progress": self.progress,
            "meeting_link": self.meeting_link,
            "admin_poznamka": self.admin_poznamka,
            "uzamcene_zmeny": "Ano" if self.uzamcene_zmeny else "Ne",
            "uzamcene_zmeny_bool": self.uzamcene_zmeny,
            "motivacni_formular": json.loads(self.motivacni_dotaznik) if self.odevzdany_motivacni_dotaznik else None,
            "osloveni_1p": self.osloveni_1p,
            "osloveni_5p": self.osloveni_5p,
            "zajmeno": self.zajmeno
        }
        

    def odstranit(self):
        db.session.delete(self)
        db.session.commit()
        osobni_slozka = user_data_folder_path() / str(self.id)
        rmtree(osobni_slozka)


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
    def get_all() ->list:
        return db.session.scalars(db.select(User)).all()

    @staticmethod
    def get_all_by_role(role) -> list:
        result = []
        for u in User.get_all():
            if role in json.loads(u.role):
                result.append(u)
        return result
    
    def ulozit_odpovedi(self, form):
        if self.motivacni_dotaznik is None:
            self.motivacni_dotaznik = [{"id": i, "odpoved": ""} for i in range(1,15)]
        else:
            self.motivacni_dotaznik = json.loads(self.motivacni_dotaznik)
        for key, value in form.items():
            try:
                key = int(key)
            except ValueError:
                continue
            
            if key in range(1,15):
                for entry in self.motivacni_dotaznik:
                    if entry["id"] == key:
                        entry["odpoved"] = value
        self.motivacni_dotaznik = json.dumps(self.motivacni_dotaznik)
        db.session.add(self)
        db.session.commit()
    
    def odhlasit_z_motivacniho_callu(self):
        self.datum_pohovoru = None
        db.session.add(self)
        db.session.commit()
        admin = odhlasit_usera_by_id(self.id)
        return admin        
    
    def ma_nahranou_praci(self):
        filenames = json.loads(get_prace_filenames(self.id))
        return bool(filenames)
    
    def smazat_praci(self):
        path = user_data_folder_path() / str(self.id) / "prace"
        for file in path.iterdir():
            file.unlink()

    def smazat_shrnuti(self):
        filename = get_shrnuti_filename(self.id)
        if filename["filename"]:
            p: Path = user_data_folder_path() / str(self.id) / filename["filename"]
            p.unlink()
        self.odbornost = "zatím nevybraná"
        db.session.add(self)
        db.session.commit()
    
        
    def odebrat_motivacni_formular(self):
        self.motivacni_dotaznik = None
        self.odevzdany_motivacni_dotaznik = False
        db.session.add(self)
        db.session.commit()
    
    def znovu_zpristupnit_motivacni_formular(self):
        self.odevzdany_motivacni_dotaznik = False
        self.progress = "Motivační formulář"
        db.session.add(self)
        db.session.commit()
        
        