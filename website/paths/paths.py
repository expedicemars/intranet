from pathlib import Path

def user_database_path() -> Path:
    return Path.cwd() / "website" / "database.db"

def known_bugs_path() -> Path:
    return Path.cwd() / "data" / "known_bugs.json"

def log_file_path() -> Path:
    return Path.cwd() / "data" / "logs.txt"

def terminy_path() -> Path:
    return Path.cwd() / "data" / "terminy.json"

def faze_path() -> Path:
    return Path.cwd() / "data" /  "faze.json"

def mailing_list_path() -> Path:
    return Path.cwd() / "data"  / "mailing_list.json"

def user_data_folder_path() -> Path:
    return Path.cwd() / "user_data"