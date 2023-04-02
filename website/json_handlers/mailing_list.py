from website.paths.paths import mailing_list_path
import json

def get_mails_from_mailing_list() -> list:
    with open(mailing_list_path()) as file:
        return json.load(file)

def pridat_mail_do_mailing_listu(mail: str) -> None:
    mails = get_mails_from_mailing_list()
    mails.append(mail)
    with open(mailing_list_path(), "w") as file:
        file.write(json.dumps(mails, indent=4))

def set_mailing_list(mails: str) -> None:
    mails = mails.replace(" ", "").split(",")
    with open(mailing_list_path(), "w") as file:
        file.write(json.dumps(mails, indent=4))