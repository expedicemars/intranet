from datetime import datetime

def pretty_date(isoformat: str) -> str:
    """
    Udělá datum ve formátu 21. 4. 2001 7:40
    None -> None
    """
    if isoformat:
        dt = datetime.fromisoformat(isoformat)
        minutes = str(dt.minute)
        if len(minutes) == 1:
            minutes = "0" + minutes
        result = f"{dt.day}. {dt.month}. {dt.year}, {dt.hour}:{minutes}"
        return result
    else:
        return None
