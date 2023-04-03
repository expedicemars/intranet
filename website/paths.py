from pathlib import Path

def user_database_path() -> Path:
    return Path.cwd() / "instance" / "database.db"

def known_bugs_path() -> Path:
    return Path.cwd() / "data" / "known_bugs.json"

def app_logs_file_path() -> Path:
    return Path.cwd() / "data" / "app_logs.txt"

def admin_logs_file_path() -> Path:
    return Path.cwd() / "data" / "admin_logs.txt"

def mailing_list_path() -> Path:
    return Path.cwd() / "data"  / "mailing_list.json"

def user_data_folder_path() -> Path:
    return Path.cwd() / "user_data"

def velitel_odbornosti_data_path() -> Path:
    return Path.cwd() / "data" / "velitel_odbornosti_data.json"

def zadani_folder_path() -> Path:
    return Path.cwd() / "data" / "zadani"

def default_profilovka_path() -> Path:
    return Path.cwd() / "data" / "default_profilovka.png"

def poznamky_path() -> Path:
    return Path.cwd() / "data" / "poznamky.json"

def pohovory_path() -> Path:
    return Path.cwd() / "data" / "pohovory.json"

def prohlaseni_path() -> Path:
    return Path.cwd() / "data" / "prohlaseni_rodicu.docx"

def exporty_path() -> Path:
    return Path.cwd() / "exporty"

def env_path() -> Path:
    return Path.cwd() / ".env"

def odkazy_path() -> Path:
    return Path.cwd() / "data" / "odkazy.json"

def prubeh_rocniku_path() -> Path:
    return Path.cwd() / "data" / "prubeh_rocniku.json"

def info_path() -> Path:
    return Path.cwd() / "data" / "info.json"

def dostupne_progressy_path() -> Path:
    return Path.cwd() / "data" / "dostupne_progressy.json"

def dostupne_role_path() -> Path:
    return Path.cwd() / "data" / "dostupne_role.json"

