import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
import numpy as np
from enum import Enum
from timeit import default_timer as timer
from collections import OrderedDict


class ExtraInputType(Enum):
    WIN = 0
    FIRST_BLOOD = 1
    FIRST_DRAGON = 2
    FIRST_TOWER = 3
    FIRST_HERALD = 4
    GAME_TIME = 5


def augment_y(y):
    first = y.copy()
    second = 1 - y.copy()
    return np.concatenate((first, second), axis=0)


def mask(df, pos, team):
    if team == 'Blue':
        ids = [0, 1, 2, 3, 4]
    if team == 'Red':
        ids = [5, 6, 7, 8, 9]

    for i in ids:
        if pos in ['Top', 'Jungle']:
            df[f'p{i}{pos}'] = (df[f'Participant{i}Lane'] == pos.upper()).astype(int)
        elif pos == 'Mid':
            df[f'p{i}{pos}'] = (df[f'Participant{i}Lane'] == "MIDDLE").astype(int)
        elif pos == 'Supp':
            df[f'p{i}{pos}'] = (df[f'Participant{i}Role'] == "DUO_SUPPORT").astype(int)
        else:
            df[f'p{i}{pos}'] = (df[f'Participant{i}Role'] == "DUO_CARRY").astype(int)

    df[f'{team}{pos}'] = (df[f'p{ids[0]}{pos}'] * df[f'Participant{ids[0]}Champion'] +
                          df[f'p{ids[1]}{pos}'] * df[f'Participant{ids[1]}Champion'] +
                          df[f'p{ids[2]}{pos}'] * df[f'Participant{ids[2]}Champion'] +
                          df[f'p{ids[3]}{pos}'] * df[f'Participant{ids[3]}Champion'] +
                          df[f'p{ids[4]}{pos}'] * df[f'Participant{ids[4]}Champion'])
    for i in ids:
        df = df.drop(columns=f'p{i}{pos}')

    return df


class RoleLineMergeTransformer(BaseEstimator, TransformerMixin):
    """
        Transformer 1
        Transform champion, role, line into one column
    """

    def __init__(self):
        print('init called')

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):
        df = X.copy()

        for team in ['Red', 'Blue']:
            for pos in ['Top', 'Jungle', 'Mid', 'Bot', 'Supp']:
                df = mask(df, pos, team)

        df.drop(df.loc[:, 'Participant0Champion': 'Participant9Lane'], axis=1, inplace=True)
        return df


class DropUselessColumnsTransformer(BaseEstimator, TransformerMixin):
    """
        Transformer 2
        Dropping useless columns
    """

    def __init__(self, *, extra_input=None):
        if extra_input is None:
            extra_input = []
        self.extra_input = extra_input
        print('init called')

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):
        df = X.copy()

        # Obligatory drop columns
        df = df.drop('GameId', axis=1)
        df = df.drop('Platform', axis=1)

        # Optional drop columns
        if ExtraInputType.WIN not in self.extra_input:
            df = df.drop('Winner', axis=1)
        if ExtraInputType.FIRST_BLOOD not in self.extra_input:
            df = df.drop('FirstBlood', axis=1)
        if ExtraInputType.FIRST_DRAGON not in self.extra_input:
            df = df.drop('FirstDragon', axis=1)
        if ExtraInputType.FIRST_HERALD not in self.extra_input:
            df = df.drop('FirstHerald', axis=1)
        if ExtraInputType.FIRST_TOWER not in self.extra_input:
            df = df.drop('FirstTower', axis=1)
        if ExtraInputType.GAME_TIME not in self.extra_input:
            df = df.drop('GameDuration', axis=1)

        return df


class MakeVectorTransformer(BaseEstimator, TransformerMixin):
    """
        Transformer 3
        Creating final model vector
    """

    def __init__(self, top_n=25, augmented=False):
        self.top_n = top_n
        self.augmented = augmented
        print('init called')

    def fit(self, X, y=None, **fit_params):
        x = X.copy()

        # if dla -1

        self.top_n_champions_ = OrderedDict({
            'Bot': x.groupby(['BlueBot'])['BlueBot'].count().sort_values(ascending=False).head(
                self.top_n).index,
            'Jungle': x.groupby(['BlueJungle'])['BlueJungle'].count().sort_values(
                ascending=False).head(self.top_n).index,
            'Mid': x.groupby(['BlueMid'])['BlueMid'].count().sort_values(ascending=False).head(
                self.top_n).index,
            'Supp': x.groupby(['BlueSupp'])['BlueSupp'].count().sort_values(
                ascending=False).head(
                self.top_n).index,
            'Top': x.groupby(['BlueTop'])['BlueTop'].count().sort_values(ascending=False).head(
                self.top_n).index
        })

        return self

    def transform(self, X, y=None):

        x = X.copy()

        for team in ['Red', 'Blue']:
            for pos in self.top_n_champions_:
                for champion_id in self.top_n_champions_[pos]:
                    x[f'{team}{pos}_{champion_id}'] = (x[f'{team}{pos}'] == champion_id).astype(int)
                x[f'{team}{pos}_-1'] = 1 - (x[f'{team}{pos}'].isin(self.top_n_champions_[pos])).astype(int)
                x = x.drop(columns=[f'{team}{pos}'])

        if self.augmented:
            red = x.loc[:, 'RedBot_145': 'RedTop_-1']
            blue = x.loc[:, 'BlueBot_145': 'BlueTop_-1']

            a = pd.concat([blue, red], axis=1)
            a.columns = x.columns

            x = pd.concat([x, a], axis=0)

        return x.to_numpy(dtype='float32')


class AddPairFeaturesTransformer(BaseEstimator, TransformerMixin):
    """
        Transformer 4
        Add Pair Features
        Not ready yet
    """

    def __init__(self, top_n=25, pair=None):
        if pair is None:
            pair = ()
        self.top_n = top_n + 1
        self.pair = pair
        print('init called')

    def fit(self, X, y=None, **fit_params):
        return self

    def mult(self, x, y):
        x = x[1:]
        x = x.values
        y = y.values

        x = pd.DataFrame(x)
        y = pd.DataFrame(y)

        return x.dot(y.T).melt().value.to_numpy().astype(float)

    def transform(self, X, y=None):
        df = X.copy()
        print(df)
        if self.pair:
            start = timer()

            first = df.iloc[:, self.pair[0] * self.top_n: (self.pair[0] + 1) * self.top_n]
            second = df.iloc[:, self.pair[1] * self.top_n: (self.pair[1] + 1) * self.top_n]

            first = first.reset_index()
            result = [self.mult(first.iloc[i], second.iloc[i]) for i, row in first.iterrows()]

            result = pd.DataFrame(result)
            print(result)

            result = result.reset_index()
            result = result.iloc[:, 1:]

            df = df.reset_index()
            df = df.iloc[:, 1:]

            df = pd.concat([df, result], axis=1)
            print(df)

            end = timer()
            print(end - start)

        return df.to_numpy(dtype='float32')

