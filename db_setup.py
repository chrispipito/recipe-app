import sqlite3

connection = sqlite3.connect('recipes.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL
)
''')

connection.commit()
connection.close()

