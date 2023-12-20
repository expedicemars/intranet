from website.paths import mailing_list_path
import json
from datetime import datetime
from website.helpers.pretty_date import pretty_datetime

def get_mailing_list() -> list[dict]:
    with open(mailing_list_path()) as file:
        file = json.load(file)
        new = sorted(file, key = lambda x: datetime.fromisoformat(x["timestamp"]), reverse=True)
        return new

def pridat_mail_do_mailing_listu(mail: str) -> None:
    mails = get_mailing_list()
    timestamp = datetime.now()
    new = {
        "email": mail,
        "timestamp": timestamp.isoformat(),
        "pretty": pretty_datetime(timestamp)
    }
    mails.append(new)
    with open(mailing_list_path(), "w") as file:
        file.write(json.dumps(mails, indent=4))

def odebrat_mail_z_mailing_listu(mail: str) -> None:
    mails = get_mailing_list()
    new_mails = []
    for m in mails:
        if m["email"] != mail:
            new_mails.append(m)
            print(m, mail)
    with open(mailing_list_path(), "w") as file:
        file.write(json.dumps(new_mails, indent=4))