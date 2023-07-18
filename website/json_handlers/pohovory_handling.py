from website.paths import pohovory_path
from datetime import datetime, timedelta
import json
from typing import List


def pridat_pohovory(start_datetime:  datetime, end_datetime: datetime) ->  None:
    """
    struktura: [
        {
            "iso": 02010900T7:20,
            "user": null
        },
        {
            "iso": lksldkfslf,
            "user":1
        }
    ]
    """
    nove_terminy: List[datetime] = []
    nove_terminy.append(start_datetime)
    dt = timedelta(minutes=10)
    while nove_terminy[-1] < end_datetime:
        nove_terminy.append(nove_terminy[-1] + dt)
    
    with open(pohovory_path()) as file:
        file = json.load(file)
    
    nove_terminy = [t.isoformat() for t in nove_terminy]
    stare_terminy = [t["iso"] for t in file]
    for t in nove_terminy:
        if t in stare_terminy:
            pass
        else:
            file.append({
                "iso": t,
                "user": None
            })
    def key_func(zaznam):
        return datetime.fromisoformat(zaznam["iso"])
    file.sort(key = key_func)
    with open(pohovory_path(),"w") as new:
        new.write(json.dumps(file, indent=4))

def smazat_termin(datetime: datetime) -> bool:
    datetime = datetime.isoformat()
    with open(pohovory_path()) as file:
        file = json.load(file)
    for f in file:
        if f["iso"] == datetime:
            if f["user"] is None:
                file.remove(f)
                with open(pohovory_path(),"w") as new:
                    new.write(json.dumps(file, indent=4))
                return True
            else:
                return False
            
                

def get_pohovory() -> List[dict]:
    with open(pohovory_path()) as file:
        file = json.load(file)
    return file

def zapsat_na_pohovor(isoformat: datetime, id: int) -> bool:
    with open(pohovory_path()) as file:
        file = json.load(file)
    #zda je zvoleny furt volny
    volny = False
    for f in file:
        if f["iso"] == isoformat.isoformat() and f["user"] is None:
            volny = True
    if volny:
        #smazu stary
        for f in file:
            if f["user"] == id:
                f["user"] = None
        #zapisu novy
        for f in file:
            if f["iso"] == isoformat.isoformat():
                f["user"] = id
                break
        with open(pohovory_path(),"w") as new:
            new.write(json.dumps(file, indent=4))
        return volny
    else:
        return volny

def get_neobsazene_pohovory() -> list:
    with open(pohovory_path()) as file:
        file = json.load(file)
    result = []
    for f in file:
        if f["user"]:
            pass
        else:
            result.append(f)
    return result