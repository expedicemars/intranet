from website.paths.paths import pohovory_path
from datetime import datetime, timedelta
import json
from typing import List


def pridat_pohovory(start_datetime:  datetime, end_datetime: datetime) ->  None:
    terminy: List[datetime] = []
    terminy.append(start_datetime)
    dt = timedelta(minutes=20)
    while terminy[-1] < end_datetime:
        terminy.append(terminy[-1] + dt)
    with open(pohovory_path()) as file:
        file = json.load(file)
    terminy = [t.isoformat() for t in terminy]
    for t in terminy:
        if t in file:
            pass
        else:
            file.append(t)
    file.sort()
    with open(pohovory_path(),"w") as new:
        new.write(json.dumps(file, indent=4))

def smazat_termin(datetime: datetime) -> None:
    datetime = datetime.isoformat()
    with open(pohovory_path()) as file:
        file = json.load(file)
    if datetime in file:
        file.remove(datetime)
        with open(pohovory_path(),"w") as new:
            new.write(json.dumps(file, indent=4))

def get_pohovory() -> List[datetime]:
    with open(pohovory_path()) as file:
        file = json.load(file)
    file = [datetime.fromisoformat(d) for d in file]
    return file