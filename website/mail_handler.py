from website import mail
from flask_mail import Message
from flask import render_template, url_for, flash
import os
from socket import gaierror


def mail_sender(mail_identifier, target, data=None) -> None:
    """
    Will send email, if parameters filled correctly
    """
    if isinstance(target, str):
        target = [target]
    target = list(set(target))
    try:
        if mail_identifier == "reset_password":
            msg = Message("Změna hesla pro Expedici Mars",
                        sender=os.environ.get("MAIL_USERNAME"),
                        recipients=target)
            msg.html = render_template("mails/reset_password.html", url=url_for("auth_views.reset_password", token = data, _external = True))
            mail.send(msg)

        if mail_identifier == "potvrzeni_emailu":
            msg = Message("Potvrzení e-mailu Expedice Mars",
                        sender=os.environ.get("MAIL_USERNAME"),
                        recipients=target)
            msg.html = render_template("mails/potvrzeni_emailu.html", url=url_for("user_views.ucet_overeny", token = data, _external = True))
            mail.send(msg)
        
        if mail_identifier == "novy_prvni_kontakt":
            msg = Message("Někdo se zapsal na první kontakt",
                        sender=os.environ.get("MAIL_USERNAME"),
                        recipients=target)
            msg.html = render_template("mails/novy_prvni_kontakt.html", url = url_for("admin_views.pohovory", _external = True))
            mail.send(msg)
            
        if mail_identifier == "odhlaseni_prvniho_kontaktu":
            msg = Message("Někdo se odhlásil z prvního kontaktu",
                        sender=os.environ.get("MAIL_USERNAME"),
                        recipients=target)
            msg.html = render_template("mails/odhlaseni_z_prvniho_kontaktu.html", url = url_for("admin_views.pohovory", _external = True))
            mail.send(msg)
            
        if mail_identifier == "nove_shrnuti_prace":
            msg = Message("Někdo odevzdal shrnutí své práce",
                        sender=os.environ.get("MAIL_USERNAME"),
                        recipients=target)
            msg.html = render_template("mails/nove_shrnuti_prace.html", url = url_for("admin_views.detail_usera", id=data, _external = True))
            mail.send(msg)
        
        if mail_identifier == "novej_bug":
            msg = Message("Nový bug na EM intranetu",
                        sender=os.environ.get("MAIL_USERNAME"),
                        recipients=target)
            msg.html = render_template("mails/nove_shrnuti_prace.html", url = url_for("admin_views.uprava_znamych_bugu", _external = True))
            mail.send(msg)
        
    except gaierror:
        flash(f"Gaierror, pravděpodobně nejsi online. E-mail se neposlal. Mail identifier: {mail_identifier}, target: {target}", category="info")
        
    
