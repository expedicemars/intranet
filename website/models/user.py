from flask_login import UserMixin
from website import db
from flask import current_app
import jwt
import json
from website.paths import user_data_folder_path
from shutil import rmtree
from website.helpers.pretty_date import pretty_datetime, pretty_date
from website.helpers.get_user_files import get_prace_filenames, get_shrnuti_filename
from website.json_handlers.dostupne_omezeni import get_odbornost_by_system_name
from datetime import datetime, timezone, timedelta
from pathlib import Path
from website.models.motivacni_call import Motivacni_call

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    confirmed = db.Column(db.Boolean, default=False)
    jmeno = db.Column(db.String(100))
    prijmeni = db.Column(db.String(100)) #-- done
    puvod = db.Column(db.String(100)) # done, nabývá hodnot cz nebo sk
    pritomen_na_konferenci = db.Column(db.Boolean, default=False) #done
    pritomen_na_primi = db.Column(db.Boolean, default=False) #done
    rok_maturity = db.Column(db.Integer) # done
    datetime_odevzdani_motivaku = db.Column(db.DateTime) # done
    datetime_odevzdani_shrnuti_prace = db.Column(db.DateTime) # done
    datetime_odevzdani_prezentace = db.Column(db.DateTime) # done#--
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
    uzamcene_zmeny_udaju = db.Column(db.Boolean, default=False)
    uzamcene_zmeny_callu = db.Column(db.Boolean, default=False)
    uzamcene_zmeny_prace = db.Column(db.Boolean, default=False)
    alergie = db.Column(db.String(1000))
    skola = db.Column(db.String(1000))
    datum_registrace = db.Column((db.DateTime), default=datetime.now)
    motivacni_dotaznik = db.Column(db.Text)
    odevzdany_motivacni_dotaznik = db.Column(db.Boolean)
    osloveni_1p = db.Column(db.String(200))
    osloveni_5p = db.Column(db.String(200))
    zajmeno = db.Column(db.String(200))
    
    def __repr__(self):
        return f"Uživatel {self.email}"

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
            "prijmeni": self.prijmeni,
            "email": self.email,
            "adresa": self.adresa,
            "telcislo": self.telcislo,
            "datum_narozeni": self.datum_narozeni.isoformat() if self.datum_narozeni else None,
            "rok_maturity": self.rok_maturity,
            "zeme_puvodu": self.puvod,
            "mail_rodicu": self.mail_rodicu,
            "dozvedeli": self.dozvedeli,
            "alergie": self.alergie,
            "skola": self.skola,
            "confirmed": "Ano" if self.confirmed else "Ne",
            "odbornost": get_odbornost_by_system_name(self.odbornost)["prvnipjc"] if self.odbornost != "zatím nevybraná" else "zatím nevybraná",
            "progress": self.progress,
            "tricko": self.tricko,
            "datum_registrace": pretty_datetime(self.datum_registrace),
            "datum_motivaku": pretty_datetime(self.datetime_odevzdani_motivaku),
            "datum_shrnuti": pretty_datetime(self.datetime_odevzdani_shrnuti_prace),
            "datum_prezentace": pretty_datetime(self.datetime_odevzdani_prezentace),
            "osloveni_1p": self.osloveni_1p,
            "osloveni_5p": self.osloveni_5p,
            "zajmeno": self.zajmeno,
            "dalsi_kroky": self.dalsi_kroky()
        }
    
    def get_info_na_detail_usera(self) -> dict:
        puvod = "neurčena"
        if self.puvod == "cz":
            puvod = "Česká republika"
        elif self.puvod == "sk":
            puvod = "Slovensko"
        return {
            "jmeno": self.jmeno,
            "prijmeni": self.prijmeni,
            "datum_narozeni": pretty_date(self.datum_narozeni.isoformat()) if self.datum_narozeni else None,
            "rok_maturity": self.rok_maturity,
            "zeme_puvodu": puvod,
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
            "datum_motivaku": pretty_datetime(self.datetime_odevzdani_motivaku),
            "datum_shrnuti": pretty_datetime(self.datetime_odevzdani_shrnuti_prace),
            "datum_prezentace": pretty_datetime(self.datetime_odevzdani_prezentace),
            "progress": self.progress,
            "admin_poznamka": self.admin_poznamka,
            "uzamcene_zmeny_callu": "Ano" if self.uzamcene_zmeny_callu else "Ne",
            "uzamcene_zmeny_prace": "Ano" if self.uzamcene_zmeny_prace else "Ne",
            "uzamcene_zmeny_udaju": "Ano" if self.uzamcene_zmeny_udaju else "Ne",
            "pritomen_na_konferenci": "Ano" if self.pritomen_na_konferenci else "Ne",
            "pritomen_na_primi": "Ano" if self.pritomen_na_primi else "Ne",
            "motivacni_formular": json.loads(self.motivacni_dotaznik) if self.odevzdany_motivacni_dotaznik else None,
            "osloveni_1p": self.osloveni_1p,
            "osloveni_5p": self.osloveni_5p,
            "zajmeno": self.zajmeno,
            "dalsi_kroky": self.dalsi_kroky()
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
        self.save()
    
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
        self.save()
    
        
    def odebrat_motivacni_formular(self):
        self.motivacni_dotaznik = None
        self.odevzdany_motivacni_dotaznik = False
        self.save()
    
    def znovu_zpristupnit_motivacni_formular(self):
        self.odevzdany_motivacni_dotaznik = False
        self.progress = "Motivační formulář"
        self.save()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def dalsi_kroky(self) -> str:
        if not self.odevzdany_motivacni_dotaznik:
            return "Pro tvé další kroky Expedicí od tebe teď potřebujeme vyplnění motivačního formuláře. Ten není nutné odeslat rovnou, uložené odpovědi si můžeš nechat rozmyslet a formulář odeslat později. Čím dřív ho ale dostaneme, tím dříve si budeš moct zvolit termín motivačního callu. Je také potřeba průběžně vyplňovat (tuto) stránku svého účtu."
        elif not Motivacni_call.get_by_user_id(self.id):
            return "Čeká tě motivační call s některými našimi organizátory. Jde o neformální online popovídání, při kterém se s tebou seznámíme a ty zase poznáš pár minulých účastníků Expedice. Pro účast na callu si musíš vybrat jeden z vypsaných termínů. Jestliže nejsou žádné termíny vypsané nebo se ti nehodí, brzy zveřejníme další. Pokud by to trvalo dlouho, omlouváme se. Můžeš nám kdykoli napsat, například s návrhem času, který ti vyhovuje. "
        elif Motivacni_call.get_by_user_id(self.id).datum_a_cas > datetime.now() and self.progress == "Motivační call":
            return "Čeká tě motivační call, termín už máš vybraný. Nejpozději do zvoleného času uvidíš na intranetu odkaz, kde se bude call odehrávat. Těšíme se!"
        elif self.progress == "Motivační call":
            return "Teď čekáš na to, než ti někdo z organizátorů zpřístupní výběr odbornosti. Mělo by se tak stát do několika dní po tvém motivačním callu."
        elif self.odbornost == "zatím nevybraná":
            return "Teď tě čeká domácí práce. Vyber si jednu z pěti odborností podle toho, která nejlépe vystihuje tvé zájmy. Začít s prací můžeš kdykoli, velitelé odborostí jsou ti neustále k dispozici a moc rádi odpoví na tvé otázky. <br>Finální zařazení do odbornosti proběhne ve chvíli, kdy odevzdáš shrnutí práce."
        elif not self.ma_nahranou_praci():
            return "Na online konferenci budeš prezentovat svou domácí práci. Nyní čekáme na to, než celou práci odevzdáš. Máš na to čas do půlnoci před konferencí."
        else:
            return "Informace o konferenci a dalších kolech budeš dostávat e-mailem. Tak na viděnou!"
        
    def pretty_name(self, surname_first:bool = False) -> str:
        if not self.prijmeni: # protože fstrig s None vypíše None
            self.prijmeni = ""
        if not self.jmeno:
            self.jmeno = ""
            
        if surname_first:
            return f"{self.prijmeni} {self.jmeno}"
        else:
            return f"{self.jmeno} {self.prijmeni}"
