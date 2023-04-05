from website.paths import motivacni_formular_otazky_path
import json

def get_motivacni_formular_otazky() -> dict:
    with open(motivacni_formular_otazky_path()) as file:
        return json.load(file)