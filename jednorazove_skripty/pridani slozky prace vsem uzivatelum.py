"""
26. 8. mi doslo, ze vsichni useri musej mit slozku na praci
"""

import pathlib

user_data_folder_path = pathlib.Path.cwd().parent / "user_data"

for user in user_data_folder_path.iterdir():
    if user.name == ".DS_Store":
        continue
    prace_path = user / "prace"
    prace_path.mkdir()