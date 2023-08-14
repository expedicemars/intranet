import os

def check_size(files:list , size_bytes: int):
    """Vrátí buď files, pokud je jejich souhrnná velikost OK, nebo False.

    Args:
        files (list): list souborů
        
        size_bytes (int): číslo (třeba 5*1024*1024)
    """
    celkova_velikost = 0
    for file in files:
        celkova_velikost += file.seek(0, os.SEEK_END)
        file.seek(0,os.SEEK_SET)
    if celkova_velikost > size_bytes:
        return False
    else:
        return files