from website.paths.paths import user_data_folder_path
from flask import send_file

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
        return None