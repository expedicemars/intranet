from website.paths import user_data_folder_path, default_profilovka_path
from flask import send_file
import json
import re


def get_prace_filenames(id):
    """
    vrací jsony
    """
    result = []
    p = user_data_folder_path() / str(id) / "prace"
    for file in p.iterdir():
        if file.name == ".DS_Store":
            continue
        result.append(file.name)
    if len(result) == 0:
        return json.dumps(None) # vrací prostý null
    else:
        return json.dumps(result)

def get_shrnuti_filename(id):
    p = user_data_folder_path() / str(id)
    filename = None
    for file in p.iterdir():
        if re.match("shrnuti_", file.name):
            filename = file.name
            break
    return {"filename": filename} 


def get_profilovka_by_id(id):
    path = user_data_folder_path() / str(id)
    for file in path.iterdir():
        if file.stem == "profilovka":
            return send_file(file)
    else:
        return send_file(default_profilovka_path())