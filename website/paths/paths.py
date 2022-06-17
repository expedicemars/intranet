from pathlib import Path

def user_database_path() -> Path:
    return Path.cwd() / "website" / "database.db"

def known_bugs_path() -> Path:
    return Path.cwd() / "data" / "known_bugs.json"

def log_file_path() -> Path:
    return Path.cwd() / "data" / "logs.txt"

def terminy_path() -> Path:
    return Path.cwd() / "data" / "terminy.json"