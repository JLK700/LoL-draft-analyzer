import sqlite3

conn = sqlite3.connect('lol.db')
cursor = conn.cursor()

cursor.execute("""SELECT Count(DISTINCT(GameId)) FROM GAMES""")

# cursor.execute("""SELECT rowid, * FROM GAMES""")
x = cursor.fetchall()

print(x)


conn.commit()
conn.close()
