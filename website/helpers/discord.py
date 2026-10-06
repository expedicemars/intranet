import os
import requests
from website.helpers.pretty_date import pretty_datetime
events_url = os.getenv("DISCORD_WEBHOOK_URL")
calls_url = os.getenv("DISCORD_CALL_LINK_URL")


def send_discord_message(message: str, url: str) -> None:
    """Send a message to a Discord webhook."""
    
    data = {
        "content": message
    }
    
    response = requests.post(url, json=data)
    if response.status_code != 204:
        raise Exception(f"Failed to send message to Discord webhook. Status code: {response.status_code}, Response: {response.text}")


def discord_odevzdany_formular(current_user) -> None:
    url = os.getenv("HOME_URL") + f"/admin/detail_usera/{current_user.id}"
    message = f"Odevzdaný nový motivační formulář od {current_user.get_full_name()}. [Odkaz na profil]({url})"
    send_discord_message(message, events_url)


def discord_zapis_na_call(current_user, call) -> None:
    url = os.getenv("HOME_URL") + "/admin/motivacni_call"
    message = f"Uživatel {current_user.get_full_name()} se zapsal na motivační call. Datum callu: {pretty_datetime(call.datum_a_cas)}, vypsal: {call.admin.get_full_name()}. [Odkaz na cally]({url})"
    send_discord_message(message, events_url)


def discord_nova_pripominka(pripominka) -> None:
    url = os.getenv("HOME_URL") + "/admin/uprava_znamych_bugu"
    message = f"Nová připomínka od {pripominka.autor}: {pripominka.popis}. [Odkaz na připomínky]({url})"
    send_discord_message(message, events_url)


def discord_nove_shrnuti(current_user, odb) -> None:
    url = os.getenv("HOME_URL") + f"/admin/detail_usera/{current_user.id}"
    message = f"Uživatel {current_user.get_full_name()} odevzdal nové shrnutí práce pod odborost {odb}. [Odkaz na profil]({url})"
    send_discord_message(message, events_url)


def discord_novy_link_na_call(current_user, call) -> None:
    message = f":notebook_with_decorative_cover: Motivační call {current_user.get_full_name()}: \n{pretty_datetime(call.datum_a_cas)}\n[Odkaz na call]({"https://" + call.meeting_link if not call.meeting_link.startswith("http") else call.meeting_link})"
    send_discord_message(message, calls_url)