"""
kdyz jsem potreboval jednorazove upravit usery v databazi, tak User model nesel importnout. Se spustenou appkou to pujde lepe.
"""
from flask import Blueprint
from  website.models.user import User
from website import db


trigger = Blueprint("trigger", __name__)

@trigger.route("/mimoradna_uprava_useru_13_9")
def uprava_useru():
    """
    11. 9. jsem pridal uzamcene_zmeny, ted to musim vsem existujicim uctum defaultnout na false

    stejne tak defaultuju vsem userum progress na novej default, "Domácí kolo"
    """
    for u in User.query.all():
        if u.uzamcene_zmeny is None:
            u.uzamcene_zmeny = False
            db.session.add(u)
            db.session.commit()
        else:
            print("User " + str(u.id) + " uz mel jinou hodnotu uzamcene_zmeny")
        if u.progress is None:
            u.progress = "Domácí kolo"
            db.session.add(u)
            db.session.commit()
        else:
            print("User " + str(u.id) + " uz mel jinou hodnotu progressu")
    return "done"

