import sqlite3

conn = sqlite3.connect('recipes.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE recipes
             (id INTEGER PRIMARY KEY, name TEXT, ingredients TEXT, instructions TEXT)''')

# Commit the changes and close the connection
conn.commit()
conn.close()
