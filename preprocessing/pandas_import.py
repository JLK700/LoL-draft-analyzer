import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
import pickle

conn = sqlite3.connect('lol.db')
cursor = conn.cursor()

cursor.execute("""SELECT * FROM GAMES""")
data = cursor.fetchall()

panda = pd.DataFrame(data, columns=['GameId', 'Platform', 'GameDuration', 'Winner', 'FirstBlood', 'FirstTower', 'FirstDragon', 'FirstHerald', 'Participant0Champion', 'Participant0Role', 'Participant0Lane', 'Participant1Champion', 'Participant1Role', 'Participant1Lane', 'Participant2Champion', 'Participant2Role', 'Participant2Lane', 'Participant3Champion', 'Participant3Role', 'Participant3Lane', 'Participant4Champion', 'Participant4Role', 'Participant4Lane', 'Participant5Champion', 'Participant5Role', 'Participant5Lane', 'Participant6Champion', 'Participant6Role', 'Participant6Lane', 'Participant7Champion', 'Participant7Role', 'Participant7Lane', 'Participant8Champion', 'Participant8Role', 'Participant8Lane', 'Participant9Champion', 'Participant9Role', 'Participant9Lane'])
panda = panda.drop_duplicates()
print(panda['GameId'].value_counts(ascending=True))

train, test = train_test_split(panda, test_size=0.2, shuffle=True)
valid, test = train_test_split(test, test_size=0.5, shuffle=True)

with open("train.pkl", "wb") as pickle_file:
    pickle.dump(train, pickle_file)

with open("valid.pkl", "wb") as pickle_file:
    pickle.dump(valid, pickle_file)

with open("test.pkl", "wb") as pickle_file:
    pickle.dump(test, pickle_file)

conn.commit()
conn.close()



