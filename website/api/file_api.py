from flask import Blueprint, send_file
import json
from website.helpers.require_role_decorator import require_role_on_current_user
from website.paths.paths import user_data_folder_path, zadani_folder_path, prohlaseni_path, exporty_path



file_api = Blueprint("file_api", __name__)

@file_api.route("/prohlaseni_rodicu")
@require_role_on_current_user(["user","admin"])
def prohlaseni_rodicu():
    return send_file(prohlaseni_path())

