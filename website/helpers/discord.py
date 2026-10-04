import os
import requests
from website.helpers.pretty_date import pretty_datetime


def send_discord_message(message: str) -> None:
    """Send a message to a Discord webhook."""
    url = os.getenv("DISCORD_WEBHOOK_URL")
    
    data = {
        "content": message
    }
    
    response = requests.post(url, json=data)
    if response.status_code != 204:
        raise Exception(f"Failed to send message to Discord webhook. Status code: {response.status_code}, Response: {response.text}")


def discord_odevzdany_formular(current_user) -> None:
    url = os.getenv("HOME_URL") + f"/admin/detail_usera/{current_user.id}"
    message = f"Odevzdaný nový motivační formulář od {current_user.get_full_name()}. [Odkaz na profil]({url})"
    send_discord_message(message)


def discord_zapis_na_call(current_user, call) -> None:
    url = os.getenv("HOME_URL") + "/admin/motivacni_call"
    message = f"Uživatel {current_user.get_full_name()} se zapsal na motivační call. Datum callu: {pretty_datetime(call.datum_a_cas)}, vypsal: {call.admin.get_full_name()}. [Odkaz na cally]({url})"
    send_discord_message(message)


def discord_nova_pripominka(pripominka) -> None:
    url = os.getenv("HOME_URL") + "/admin/uprava_znamych_bugu"
    message = f"Nová připomínka od {pripominka.autor}: {pripominka.popis}. [Odkaz na připomínky]({url})"
    send_discord_message(message)


def discord_nove_shrnuti(current_user, odb) -> None:
    url = os.getenv("HOME_URL") + f"/admin/detail_usera/{current_user.id}"
    message = f"Uživatel {current_user.get_full_name()} odevzdal nové shrnutí práce pod odborost {odb}. [Odkaz na profil]({url})"
    send_discord_message(message)