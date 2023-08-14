from website.paths import velitel_odbornosti_data_path
import json

def zapsat_kontakt(odbornost, data) -> None:
    with open(velitel_odbornosti_data_path()) as file:
        file = json.load(file)
    file[odbornost] = data
    with open(velitel_odbornosti_data_path(), "w") as f:
        f.write(json.dumps(file, indent=4))
    