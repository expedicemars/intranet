from website import mail
from flask_mail import Message
from flask import render_template, url_for
import os


def mail_sender(mail_identifier, target, data=None) -> None:
    """
    Will send email, if parameters filled correctly
    """
    if mail_identifier == "reset_password":
        msg = Message("Změna hesla pro Expedici Mars",
                      sender=os.environ.get("MAIL_USERNAME"),
                      recipients=[target])
        msg.html = render_template("mails/reset_password.html", url=url_for("auth_views.reset_password", token = data, _external = True))
        mail.send(msg)

    if mail_identifier == "potvrzeni_emailu":
        msg = Message("Potvrzení e-mailu Expedice Mars",
                      sender=os.environ.get("MAIL_USERNAME"),
                      recipients=[target])
        msg.html = render_template("mails/potvrzeni_emailu.html", url=url_for("user_views.ucet_overeny", token = data, _external = True))
        mail.send(msg)
    
    if mail_identifier == "novy_prvni_kontakt":
        msg = Message("Někdo se zapsal na první kontakt",
                      sender=os.environ.get("MAIL_USERNAME"),
                      recipients=[target])
        msg.html = render_template("mails/novy_prvni_kontakt.html", url = url_for("admin_views.pohovory", _external = True))
        mail.send(msg)
    
