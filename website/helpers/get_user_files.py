from website.paths.paths import user_data_folder_path
from flask import send_file
import json

def get_motivak_by_id(id: int, style: str):
    """
    style = file or name
    """
    motivak_path = user_data_folder_path() / str(id)
    for file in motivak_path.iterdir():
        if file.stem == "motivak":
            if style == "file":
                return send_file(file)
            else:
                return file.name
    else:
        return json.dumps(None)


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