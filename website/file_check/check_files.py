import json
import website.paths.paths as p
from website.json_handlers.logs_handling import log


def check_known_bugs_file() -> None:
    bugs_path = p.known_bugs_path()
    if bugs_path.exists():
        log("Known bugs file already exists.")
    else:
        bugs_path.touch()
        with open(bugs_path, "w") as file:
            file.write(json.dumps([]))
        log("creating Known bugs file at " + str(bugs_path))
        

def check_logs_file() -> None:
    logs_path = p.log_file_path()
    if logs_path.exists():
        log("(this) log file already exists")
    else:
        logs_path.touch()
        log("creating (this) log file at  " + str(logs_path))

