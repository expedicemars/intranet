from pathlib import Path

def user_database_path() -> Path:
    return Path.cwd() / "website" / "database.db"

def known_bugs_path() -> Path:
    return Path.cwd() / "data" / "known_bugs.json"

def app_logs_file_path() -> Path:
    return Path.cwd() / "data" / "app_logs.txt"

def admin_logs_file_path() -> Path:
    return Path.cwd() / "data" / "admin_logs.txt"

def terminy_path() -> Path:
    return Path.cwd() / "data" / "terminy.json"

def faze_path() -> Path:
    return Path.cwd() / "data" /  "faze.json"

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