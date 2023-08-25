from flask import Blueprint
from flask_login import current_user
import json
import datetime
from website.helpers.pretty_date import pretty_datetime
from website.helpers.require_role_decorator import require_progress_na_ucastnikovi, require_role_on_current_user
from website.models.motivacni_call import Motivacni_call
from website.models.user import User
from website.paths import velitel_odbornosti_data_path, vzorove_vypracovani_path



user_api = Blueprint("user_api", __name__)

@user_api.route("/confirmed")
@require_role_on_current_user("user")
def confirmed():
    return json.dumps({"confirmation_status": current_user.confirmed})


@user_api.route("/uzamcene_zmeny")
@require_role_on_current_user("user")
def uzamcene_zmeny():
    return json.dumps({"status": current_user.uzamcene_zmeny})


@user_api.route("/volne_pohovory")
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Motivační call")
def volne_pohovory():
    result = []
    for p in Motivacni_call.get_neobsazene_cally():
        if p.datum_a_cas - datetime.timedelta(hours=48) > datetime.datetime.now():
            zaznam = {}
            zaznam["id"] = p.id
            zaznam["pretty"] = pretty_datetime(p.datum_a_cas)
            result.append(zaznam)
    return json.dumps(result)


@user_api.route("/datum_motivacniho_callu")
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Motivační call")
def datum_motivacniho_callu():
    m = Motivacni_call.get_by_user_id(current_user.id)
    result = {
        "datum": pretty_datetime(m.datum_a_cas) if m else None,
        "link": m.meeting_link if m else None
        }
    return json.dumps(result)


@user_api.route("/kontakt_na_velitele_odbornosti/<string:odb>")
@require_role_on_current_user("user")
@require_progress_na_ucastnikovi("Domácí projekt")
def kontakt_na_velitele_odbornosti(odb):
    with open(velitel_odbornosti_data_path()) as file:
        file = json.load(file)
    try:
        result = file[odb]
    except KeyError:
        return "Tahle odbornost neexistuje."
    if result == "":
        return "Tato odbornost kontakt ještě nezadala."
    else:
        return result


@user_api.route("/info")
@require_role_on_current_user("user")
def info():
    data = current_user.get_info_na_ucet_stranku()
    m = Motivacni_call.get_by_user_id(current_user.id)
    if m:
        data["datum_motivacniho_callu"] = pretty_datetime(m.datum_a_cas)
    else:
        data["datum_motivacniho_callu"] = None
    return data


@user_api.route("/odpovedi_motivaku")
@require_role_on_current_user(["user"])
def odpovedi_motivaku():
    if current_user.motivacni_dotaznik:
        return current_user.motivacni_dotaznik
    else:
        return json.dumps([{"id": i, "odpoved": ""} for i in range(1,15)])
    

@user_api.route("/vzorove_vypracovani_existuje")
@require_role_on_current_user(["user"])
def vzorove_vypracovani_existuje():
    return json.dumps({"existuje": vzorove_vypracovani_path().exists()})

@user_api.route("/dalsi_kroky")
@require_role_on_current_user(["user"])
def dalsi_kroky():
    u: User
    u = current_user
    if not u.odevzdany_motivacni_dotaznik:
        return "Pro tvé další kroky Expedicí od tebe teď potřebujeme vyplnění motivačního formuláře. Ten není nutné odeslat rovnou, uložené odpovědi si můžeš nechat rozmyslet a formulář odeslat později. Čím dřív ho ale dostaneme, tím dříve si budeš moct zvolit termín motivačního callu. Je také potřeba průběžně vyplňovat (tuto) stránku svého účtu."
    elif not Motivacni_call.get_by_user_id(u.id):
        return "Čeká tě motivační call s některými našimi organizátory. Jde o neformální online popovídání, při kterém se s tebou seznámíme a ty zase poznáš pár minulých účastníků Expedice. Pro účast na callu si musíš vybrat jeden z vypsaných termínů. Jestliže nejsou žádné termíny vypsané nebo se ti nehodí, brzy zveřejníme další. Pokud by to trvalo dlouho, omlouváme se. Můžeš nám kdykoli napsat, například s návrhem času, který ti vyhovuje. "
    elif Motivacni_call.get_by_user_id(u.id).datum_a_cas > datetime.datetime.now():
        return "Čeká tě motivační call, termín už máš vybraný. Nejpozději do zvoleného času uvidíš na intranetu odkaz, kde se bude call odehrávat. Těšíme se!"
    elif u.odbornost == "zatím nevybraná":
        return "Teď tě čeká domácí práce. Vyber si jednu z pěti odborností podle toho, které nejlépe vystihuje tvé zájmy.  Začít s prací můžeš kdykoli, velitelé odborostí jsou ti kdykoli k dispozici a moc rádi odpoví na tvé otázky. <br>Finální zařazení do odbornosti proběhne ve chvíli, kdy odevzdáš shrnutí práce."
    elif not u.ma_nahranou_praci():
        return "Na online konferenci budeš prezentovat svou domácí práci. Nyní čekáme na to, než celou práci odevzdáš. Máš na to čas do půlnoci před konferencí."
    else:
        return "Informace o konferenci a dalších kolech budeš dostávat e-mailem. Tak na viděnou!"