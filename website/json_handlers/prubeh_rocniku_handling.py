from website.paths.paths import prubeh_rocniku_path
import json

def set_nove_datum_konce_registrace(datum: str) -> None:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    f["datum_konce_registrace"] = datum
    with open(prubeh_rocniku_path(), "w") as file:
        file.write(json.dumps(f, indent=4))

def get_datum_konce_registrace() -> str:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    return f["datum_konce_registrace"]

def toggle_registrace() -> None:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    f["otevrena_registrace"] = False if f["otevrena_registrace"] else True
    with open(prubeh_rocniku_path(), "w") as file:
        file.write(json.dumps(f, indent=4))

def get_registrace_otevrena() -> bool:
    with open(prubeh_rocniku_path()) as file:
        f = json.load(file)
    return f["otevrena_registrace"]