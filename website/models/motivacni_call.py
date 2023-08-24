from website import db
from datetime import datetime, timedelta
from typing import List
from website.helpers.pretty_date import pretty_datetime

class Motivacni_call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    admin_id = db.Column(db.Integer)
    datum_a_cas = db.Column(db.DateTime)
    meeting_link = db.Column(db.String(1000))

    @staticmethod
    def pridat_pohovory(start_datetime: datetime, end_datetime: datetime, admin) ->  None:
        nove_terminy: List[datetime] = []
        nove_terminy.append(start_datetime)
        dt = timedelta(minutes=15)
        while nove_terminy[-1] < end_datetime:
            nove_terminy.append(nove_terminy[-1] + dt)
        
        for t in nove_terminy:
            m = Motivacni_call(
                admin_id = admin.id,
                datum_a_cas = t
            )
            db.session.add(m)
        db.session.commit()
    
    @staticmethod
    def get_by_user_id(id) -> "Motivacni_call":
        return db.session.scalars(db.select(Motivacni_call).where(Motivacni_call.user_id == id)).first()
    
    @staticmethod
    def get_neobsazene_cally() -> List["Motivacni_call"]:
        return db.session.scalars(db.select(Motivacni_call).where(Motivacni_call.user_id == None)).all() # sqlalchemy neumí is None syntax...

    @staticmethod 
    def get_by_id(id) -> "Motivacni_call":
        return db.session.get(Motivacni_call, int(id))
    
    @staticmethod
    def get_all() -> List["Motivacni_call"]:
        return db.session.scalars(db.select(Motivacni_call)).all()
    
    @staticmethod
    def odhlasit_usera_by_user_id(id) -> int:
        m = Motivacni_call.get_by_user_id(id)
        m.user_id = None
        admin_id = m.admin_id
        db.session.add(m)
        db.session.commit()
        return admin_id
    
    def zapsat_usera(self, user_id: int) -> bool:
        if self.user_id:
            return False
        else:
            self.user_id = user_id
            db.session.add(self)
            db.session.commit()
            return True
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f"Call {pretty_datetime(self.datum_a_cas)}"


        
