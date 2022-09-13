import datetime
from website.paths.paths import app_logs_file_path

def log(data: str) -> None:
    with open(app_logs_file_path(), "a") as file:
        file.write(str(datetime.datetime.utcnow()) + ":  " + data + "\n")

def get_logs() -> str:
    with open(app_logs_file_path()) as file:
        return file.read()

def delete_logs() -> str:
    with open(app_logs_file_path(), "w") as file:
        file.write("")

