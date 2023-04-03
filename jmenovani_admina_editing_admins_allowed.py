"""
Tímhle skriptem můžu jmenovat registrovanýho usera adminem na základě e-mailu.
"""

from website import create_app
import json
from website.models.user import User


e_mail_na_jmenovani = input("Napiš e-mail user na jmenování adminem: ")
print(e_mail_na_jmenovani)
app = create_app()
with app.app_context():
    print(User.jmenovat_admina_by_email(e_mail_na_jmenovani))