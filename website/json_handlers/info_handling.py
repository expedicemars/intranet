from website.paths import info_path
import json


def ulozit_info(form_dict) -> None:
    with open(info_path()) as file:
        f = json.load(file)
    
    for zaznam in f:
        zaznam["content"] = form_dict[zaznam["nadpis"]]
    
    with open(info_path(), "w") as file:
        file.write(json.dumps(f, indent=4))
        

def get_vsechny_informace() -> dict:
    with open(info_path()) as file:
        return json.load(file)