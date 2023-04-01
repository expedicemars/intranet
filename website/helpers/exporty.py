from openpyxl import Workbook
from website.paths.paths import exporty_path, mailing_list_path, pohovory_path, poznamky_path, terminy_path, velitel_odbornosti_data_path, zadani_folder_path, admin_logs_file_path, app_logs_file_path, prohlaseni_path, user_data_folder_path
from website.helpers.pretty_date import pretty_date
from website.roles.role_handler import get_access_rights
from datetime import datetime
from website.models.user import User
from website import db
import json
from zipfile import ZipFile

def exportovat() -> None:
    time_of_export = datetime.now()
    filename = time_of_export.strftime("%Y_%m_%d-%H_%M_%S")
    folder_name = time_of_export.isoformat()
    folder = exporty_path() / folder_name
    folder.mkdir()
    xlsx_path = folder / "data.xlsx"
    zip_filename = "zaloha_iEM_" + filename + ".zip"
    zip_path = folder / zip_filename

    wb = Workbook()
    wb.remove(wb.active)
    ws1 = wb.create_sheet("Účastníci")
    names = [
        "id",
        "E-mail",
        "confirmed",
        "Jméno",
        "Adresa",
        "Telefoní číslo",
        "E-mail rodičů",
        "Souhlas rodičů",
        "Odbornost",
        "Datum narození",
        "Progress",
        "Role",
        "Tričko",
        "Jak se o nás dozvěděli",
        "Admin poznámka",
        "Hodnocení motiváku",
        "Uzamčené změny",
        "Alergie",
        "Škola",
        "Datum registrace",
        "Datum pohovoru",
        "Meeting link"
        ]
    for i, name in enumerate(names):
        ws1.cell(1,i+1, value=name)
    for i, u in enumerate(User.query.all()):
        ws1.cell(i+2,1,value=u.id)
        ws1.cell(i+2,2,value=u.email)
        ws1.cell(i+2,3,value=u.confirmed)
        ws1.cell(i+2,4,value=u.jmeno)
        ws1.cell(i+2,5,value=u.adresa)
        ws1.cell(i+2,6,value=u.telcislo)
        ws1.cell(i+2,7,value=u.mail_rodicu)
        ws1.cell(i+2,8,value=u.souhlas_rodicu)
        ws1.cell(i+2,9,value=u.odbornost)
        ws1.cell(i+2,10,value=u.datum_narozeni)
        ws1.cell(i+2,11,value=u.progress)
        ws1.cell(i+2,12,value=u.role)
        ws1.cell(i+2,13,value=u.tricko)
        ws1.cell(i+2,14,value=u.dozvedeli)
        ws1.cell(i+2,15,value=u.admin_poznamka)
        ws1.cell(i+2,16,value=u.hodnoceni_motivaku)
        ws1.cell(i+2,17,value=u.uzamcene_zmeny)
        ws1.cell(i+2,18,value=u.alergie)
        ws1.cell(i+2,19,value=u.skola)
        ws1.cell(i+2,20,value=u.datum_registrace)
        ws1.cell(i+2,21,value=u.datum_pohovoru)
        ws1.cell(i+2,22,value=u.meeting_link)
    
    ws2 = wb.create_sheet("Mailing list")
    with open(mailing_list_path()) as file:
        file = json.load(file)
    for i, mail in enumerate(file):
        ws2.cell(i+1,1,mail)

    ws3 = wb.create_sheet("Pohovory")
    with open(pohovory_path()) as file:
        file = json.load(file)
    ws3.cell(1,1,"Datum")
    ws3.cell(1,2,"Účastník")
    for i, zaznam in enumerate(file):
        ws3.cell(i+2,1,pretty_date(zaznam["iso"]))
        ws3.cell(i+2,2,zaznam["user"])
    
    ws4 = wb.create_sheet("Poznámky")
    with open(poznamky_path()) as file:
        file = json.load(file)
    ws4.cell(1,1,"Autor")
    ws4.cell(1,2,"Datum")
    ws4.cell(1,3,"Poznámka")
    for i, zaznam in enumerate(file):
        ws4.cell(i+2,1,zaznam["autor"])
        ws4.cell(i+2,2,zaznam["datum"])
        ws4.cell(i+2,3,zaznam["msg"])
    
    
    ws5 = wb.create_sheet("Kontakty na velitele odborností")
    with open(velitel_odbornosti_data_path()) as file:
        file = json.load(file)
    ws5.cell(1,1,"Odbornost")
    ws5.cell(1,2,"Kontakt")
    for i, key in enumerate(file.keys()):
        ws5.cell(i+2,1,key)
        ws5.cell(i+2,2,file[key])

    wb.save(xlsx_path)

    with ZipFile(zip_path, mode="a") as archive:
        archive.write(xlsx_path, arcname=xlsx_path.name)
        archive.write(admin_logs_file_path(), arcname=admin_logs_file_path().name)
        archive.write(app_logs_file_path(), arcname=app_logs_file_path().name)
        archive.write(prohlaseni_path(), arcname=prohlaseni_path().name)
        archive.write(terminy_path(), arcname=terminy_path().name)
        for p in user_data_folder_path().rglob("*"):
            archive.write(p, arcname=p.relative_to(user_data_folder_path().parent))
        for p in zadani_folder_path().rglob("*"):
            archive.write(p, arcname=p.relative_to(zadani_folder_path().parent))

def promazat() -> None:
    """
    Promaže vše, co bylo exportováno, krom mailing listu.
    """
    for folder in zadani_folder_path().iterdir():
        if folder.name == ".DS_Store":
            pass
        else:
            for file in folder.iterdir():
                if file.name == ".DS_Store":
                    pass
                else:
                    file.unlink()
    with open(admin_logs_file_path(), "w") as file:
        file.write("")
    with open(pohovory_path(), "w") as file:
        file.write(json.dumps([], indent=4))
    with open(poznamky_path(), "w") as file:
        file.write(json.dumps([], indent=4))
    with open(terminy_path(),"w") as file:
        file.write(json.dumps([
            {
                "popis": "registrace",
                "date": "2022-01-01"
            }
        ]))
    with open(velitel_odbornosti_data_path(), "w") as file:
        file.write(json.dumps({
            "biolog": "",
            "fyzik": "",
            "konstrukter": "",
            "inzenyr": "",
            "popularizator": ""
        }, indent=4))
    
    for u in User.query.all():
        u: User
        if "admin" not in get_access_rights(u):
            u.odstranit()
        else:
            u.datum_pohovoru = ""
            db.session.add(u)
            db.session.commit()
        


    
