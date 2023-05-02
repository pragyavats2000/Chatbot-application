import sqlite3
from bot import pairs

conn = sqlite3.connect('restaurant.db')
c = conn.cursor()



conn.execute('''
    CREATE TABLE IF NOT EXISTS pairs (
        id INTEGER PRIMARY KEY,
        pattern TEXT,
        response TEXT
    );
''')

for pair in pairs:
    pattern, response = pair
    conn.execute('INSERT INTO pairs (pattern, response) VALUES (?, ?)', (str(pattern), str(response)))


# Commit the changes and close the connection
conn.commit()
conn.close()