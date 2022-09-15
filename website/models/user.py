from flask_login import UserMixin
from website import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json
from website.paths.paths import user_data_folder_path
from shutil import rmtree


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
	odbornost = db.Column(db.String(100), default = "zatím nevybraná")
	datum_narozeni=db.Column(db.String(100))
	progress = db.Column(db.String(100), default = "Domácí kolo")
	role = db.Column(db.Text, default=json.dumps(["user"]))
	tricko = db.Column(db.String(100))
	dozvedeli = db.Column(db.String(100))
	admin_poznamka = db.Column(db.String(1000))
	hodnoceni_motivaku = db.Column(db.String(5000))
	uzamcene_zmeny = db.Column(db.Boolean, default=False)
	alergie = db.Column(db.String(1000))
	skola = db.Column(db.String(1000))


	def get_reset_token(self, expires_sec = 9000) -> str:
		s = Serializer(current_app.config["SECRET_KEY"],  expires_sec)
		return s.dumps({"user_id": self.id}).decode("utf-8") 

	@staticmethod
	def verify_reset_token(token) -> "User":
		s = Serializer(current_app.config["SECRET_KEY"])
		try:
			user_id = s.loads(token)["user_id"]
		except:
			return None
		return User.query.get(user_id)

	def get_full_info(self) -> dict:
		return {
			"id": self.id,
			"email":self.email,
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
			"admin_poznamka": self.admin_poznamka,
			"hodnoceni_motivaku": self.hodnoceni_motivaku,
			"uzamcene_zmeny": self.uzamcene_zmeny,
			"alergie": self.alergie,
			"skola": self.skola
		}
	
	def get_basic_info(self) -> dict:
		return {
			"id": self.id,
			"email":self.email,
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
			"skola": self.skola
		}

	def odstranit(self):
		osobni_slozka = user_data_folder_path() / str(self.id)
		rmtree(osobni_slozka)
		db.session.delete(self)
		db.session.commit()

