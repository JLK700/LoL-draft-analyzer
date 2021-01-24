import pickle
from enum import Enum

with open("train.pkl", "rb") as file:
    train = pickle.load(file)

with open("valid.pkl", "rb") as file:
    valid = pickle.load(file)

with open("test.pkl", "rb") as file:
    test = pickle.load(file)


class LabelType(Enum):
    WIN = 0
    FIRST_BLOOD = 1
    FIRST_DRAGON = 2
    FIRST_TOWER = 3
    FIRST_HERALD = 4
    GAME_TIME = 5


def make_x_and_y(x):
    df = x.copy()

    for i in df.index:
        df.at[i, 'Winner'] = 1 if df.at[i, 'Winner'] == 'Win' else 0

    labels = {'Win': df.Winner.to_numpy(dtype='int64'),
              'FirstBlood': df.FirstBlood.to_numpy(dtype='int64'),
              'FirstDragon': df.FirstDragon.to_numpy(dtype='int64'),
              'FirstHerald': df.FirstHerald.to_numpy(dtype='int64'),
              'FirstTower': df.FirstTower.to_numpy(dtype='int64'),
              'GameDuration': df.GameDuration.to_numpy(dtype='int64')}

    return df, labels


def filter_row(row):
    row = row.value_counts()
    try:
        return (row['DUO_SUPPORT'] == 2) & (row['MIDDLE'] == 2) & (row['TOP'] == 2) & (row['JUNGLE'] == 2) & (
                row['DUO_CARRY'] == 2)
    except KeyError:
        return False


def delete_faulty_matches(x):
    df = x.copy()
    df = df[df.apply(filter_row, axis=1)]
    return df


train = delete_faulty_matches(train)
valid = delete_faulty_matches(valid)
test = delete_faulty_matches(test)

x_train, y_train = make_x_and_y(train)
x_valid, y_valid = make_x_and_y(valid)
x_test, y_test = make_x_and_y(test)

with open("x_train.pkl", "wb") as pickle_file:
    pickle.dump(x_train, pickle_file)

with open("x_valid.pkl", "wb") as pickle_file:
    pickle.dump(x_valid, pickle_file)

with open("x_test.pkl", "wb") as pickle_file:
    pickle.dump(x_test, pickle_file)

with open("y_train.pkl", "wb") as pickle_file:
    pickle.dump(y_train, pickle_file)

with open("y_valid.pkl", "wb") as pickle_file:
    pickle.dump(y_valid, pickle_file)

with open("y_test.pkl", "wb") as pickle_file:
    pickle.dump(y_test, pickle_file)
