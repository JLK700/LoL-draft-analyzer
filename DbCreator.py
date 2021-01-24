import sqlite3


conn = sqlite3.connect('lol.db')
cursor = conn.cursor()

# cursor.execute("""CREATE TABLE PLAYERS(
#                 Name TEXT,
#                 Region TEXT
#                 )""")

cursor.execute("""CREATE TABLE GAMES(
                GameId INTEGER,
                Platform TEXT,
                GameDuration INTEGER,
                Winner TEXT,
                FirstBlood TEXT,
                FirstTower TEXT,
                FirstDragon TEXT,
                FirstHerald TEXT,
                Participant0Champion INTEGER,
                Participant0Role TEXT,
                Participant0Lane TEXT,
                Participant1Champion INTEGER,
                Participant1Role TEXT,
                Participant1Lane TEXT,
                Participant2Champion INTEGER,
                Participant2Role TEXT,
                Participant2Lane TEXT,
                Participant3Champion INTEGER,
                Participant3Role TEXT,
                Participant3Lane TEXT,
                Participant4Champion INTEGER,
                Participant4Role TEXT,
                Participant4Lane TEXT,
                Participant5Champion INTEGER,
                Participant5Role TEXT,
                Participant5Lane TEXT,
                Participant6Champion INTEGER,
                Participant6Role TEXT,
                Participant6Lane TEXT,
                Participant7Champion INTEGER,
                Participant7Role TEXT,
                Participant7Lane TEXT,
                Participant8Champion INTEGER,
                Participant8Role TEXT,
                Participant8Lane TEXT,
                Participant9Champion INTEGER,
                Participant9Role TEXT,
                Participant9Lane TEXT
                )""")

conn.commit()
conn.close()
