import datetime
from website.paths import app_logs_file_path, admin_logs_file_path
from flask_login import current_user

def log(data: str) -> None:
    with open(app_logs_file_path(), "a") as file:
        file.write(str(datetime.datetime.now()) + ":  " + data + "\n")

def get_logs() -> str:
    with open(app_logs_file_path()) as file:
        return file.read()

def delete_logs() -> str:
    with open(app_logs_file_path(), "w") as file:
        file.write("")


def alog(data: str) -> None:
    with open(admin_logs_file_path(), "a") as file:
        file.write(str(datetime.datetime.now()) + ", " + str(current_user.email) + ": "+ data + "\n")

def get_alogs() -> str:
    with open(admin_logs_file_path()) as file:
        return file.read()

def delete_alogs() -> str:
    with open(admin_logs_file_path(), "w") as file:
        file.write("")