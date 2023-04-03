"""Jednorázový skript na jmenování všech userů na Registrován
    
"""

from website import create_app
import json
from website.models.user import User
from website import db

app = create_app()
with app.app_context():
    for u in db.session.scalars(db.select(User)).all():
        u.progress = "Registrován"
        db.session.add(u)
        db.session.commit()
        
print("Success")