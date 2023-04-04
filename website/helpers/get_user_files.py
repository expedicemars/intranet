from website.paths import user_data_folder_path, default_profilovka_path
from flask import send_file
import json


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
        return json.dumps(None)
    else:
        return json.dumps(result)

def get_profilovka_by_id(id):
    path = user_data_folder_path() / str(id)
    for file in path.iterdir():
        if file.stem == "profilovka":
            profilovka_path = path / file.name
            return send_file(profilovka_path)
    else:
        return send_file(default_profilovka_path())