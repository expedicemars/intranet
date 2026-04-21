from website import db
from website.models.user import User
from typing import List
from datetime import datetime
from website.helpers.pretty_date import pretty_datetime

class Hodnoceni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="hodnoceni")
    admin_id = db.Column(db.Integer)
    vecnost = db.Column(db.Integer)
    originalita = db.Column(db.Integer)
    komunikace = db.Column(db.Integer)
    motivovanost = db.Column(db.Integer)
    sebevedomi = db.Column(db.Integer)
    flexibilita = db.Column(db.Integer)
    sebehodnoceni = db.Column(db.Integer)
    k_faktor = db.Column(db.Integer)
    dojem = db.Column(db.Text)
    datum_zalozeni = db.Column(db.DateTime, default=datetime.now)


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "admin_id": self.admin_id,
            "admin_email": User.get_by_id(self.admin_id).email,
            "vecnost": self.vecnost,
            "originalita": self.originalita,
            "komunikace": self.komunikace,
            "motivovanost": self.motivovanost,
            "sebevedomi": self.sebevedomi,
            "flexibilita": self.flexibilita,
            "sebehodnoceni": self.sebehodnoceni,
            "k_faktor": self.k_faktor,
            "dojem": self.dojem,
            "datum_zalozeni": pretty_datetime(self.datum_zalozeni)
        }
    
    @staticmethod
    def zapsat_hodnoceni(form_dict, user_id, admin_id):
        h = Hodnoceni(
            user_id=user_id,
            admin_id=admin_id,
            vecnost=form_dict["vecnost"],
            originalita=form_dict["originalita"],
            komunikace=form_dict["komunikace"],
            motivovanost=form_dict["motivovanost"],
            sebevedomi=form_dict["sebevedomi"],
            flexibilita=form_dict["flexibilita"],
            sebehodnoceni=form_dict["sebehodnoceni"],
            k_faktor=form_dict["k_faktor"],
            dojem = form_dict["dojem"]
        )
        db.session.add(h)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id) -> "Hodnoceni":
        return db.session.get(Hodnoceni, int(id))
    
    def smazat(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod  
    def get_by_user_id(id) -> List["Hodnoceni"]:
        return db.session.scalars(db.select(Hodnoceni).where(Hodnoceni.user_id == id)).all()
    
    @staticmethod
    def get_all() -> List["Hodnoceni"]:
        return db.session.scalars(db.select(Hodnoceni)).all()
        