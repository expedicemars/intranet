"""
zdroj: https://pythontic.com/database/sqlite/alter%20table
Přidání atributu role každýmu userovi:

takhle nejak se to dela


potom jsem musel vlezt do usera a nastavit, ze ma tohle pole

stejne jsem pak smazal databazi, protoze user mel jeste pocet_odhadu a column nejde smazat
"""

import sqlite3
from website.paths.paths import user_database_path
connection = sqlite3.connect(user_database_path())
cursor = connection.cursor()
print(cursor)
addColumn = "ALTER TABLE user ADD COLUMN role text"
cursor.execute(addColumn)