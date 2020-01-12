import pandas as pd
from src.constants import *


def split_data(data, train_split, test_split):

    def split(df, test_part):
        test = pd.DataFrame()
        for uid in df[COL_USER].unique():
            one_user = df[df[COL_USER] == uid]
            t = int(round(test_part * len(one_user)))

            test_one_user = one_user.tail(t)
            test = test.append(test_one_user)
            df = df.drop(test_one_user.index)
        return df, test

    train_set, test_set = split(data, test_split)
    return train_set, test_set
