"""
Tímhle skriptem můžu jmenovat registrovanýho usera adminem na základě e-mailu.
"""

from website import create_app, db
import json
from website.models.user import User

e_mail_na_jmenovani = "josef.latj@gmail.com"

app = create_app()
with app.app_context():
    user_na_jmenovani = User.query.filter_by(email=e_mail_na_jmenovani).first()
    if user_na_jmenovani is None:
        print("Zadaný email v db neexistuje, asi ho musíš nejdřív registrovat.")
    else:
        user_na_jmenovani.role = json.dumps(["admin", "editing_admins_allowed"])
        db.session.commit()
        print("Success")