import json
from website.paths import dostupne_progressy_path, dostupne_role_path

def get_dostupne_progressy() -> list:
    with open(dostupne_progressy_path()) as file:
        return json.load(file)
    
def get_dostupne_role() -> list:
    with open(dostupne_role_path()) as file:
        return json.load(file)