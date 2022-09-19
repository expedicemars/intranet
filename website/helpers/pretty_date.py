from datetime import datetime

def pretty_date(datetime: datetime) -> str:
    """
    Udělá datum ve formátu 21. 4. 2001 7:40
    
    """
    minutes = str(datetime.minute)
    if len(minutes) == 1:
        minutes = "0" + minutes
    result = f"{datetime.day}. {datetime.month}. {datetime.year}, {datetime.hour}:{minutes}"
    return result

