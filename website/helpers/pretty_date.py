from datetime import datetime, date, timedelta

def pretty_date(datum) -> str:
    """
    Udělá datum ve formátu 21. 4. 2001
    None -> None
    """
    if datum:
        if isinstance(datum, str):
            dt = date.fromisoformat(datum)
        else:
            dt = datum
        return f"{dt.day}. {dt.month}. {dt.year}"
    else:
        return None
    

def pretty_datetime(isoformat) -> str:
    """
    Udělá datum ve formátu 21. 4. 2001 7:40
    None -> None
    """
    if isoformat:
        if isinstance(isoformat, str):
            dt = datetime.fromisoformat(isoformat)
        else:
            dt = isoformat
   
        minutes = str(dt.minute)
        if len(minutes) == 1:
            minutes = "0" + minutes
        result = f"{dt.day}. {dt.month}. {dt.year}, {dt.hour}:{minutes}"
        return result
    else:
        return None
