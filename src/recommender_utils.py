import pickle
import pandas as pd
import os
import sys
from results.models import RecommendationElement
from histories.models import HistoryElement
from src.constants import *
from os import listdir
from os.path import isfile, join, dirname
from src.algorithms import reco_utils
from .mapper import map_to_algorithm
sys.modules['reco_utils'] = reco_utils


def recommend(algorithm_name, data_set, user_id, top_k):
    algorithm = map_to_algorithm(algorithm_name)

    file = open(f'{os.path.dirname(os.path.abspath(__file__))}/models/{algorithm_name}_{data_set}.pkl', 'rb')
    saved_model = pickle.load(file)
    file.close()

    recommendations = algorithm.recommend(saved_model, user_id, top_k=top_k)
    recommendation_objects = [RecommendationElement(index+1, *(eval(recommendation)))
                              for index, recommendation in enumerate(recommendations)]

    return recommendation_objects


def get_data_set_info(data_set, number_of_ids):
    data = pd.read_csv(f"{os.path.dirname(os.path.abspath(__file__))}/data_sets/{data_set}.txt", sep=";", names=[COL_USER, COL_ITEM, COL_RATING, COL_TIMESTAMP])
    data_set_info = dict()
    data_set_info['users_num'] = data[COL_USER].nunique()
    data_set_info['items_num'] = data[COL_ITEM].nunique()
    data_set_info['users_id_sample'] = list(data[COL_USER].unique())[:number_of_ids]
    data_set_info['density'] = (len(data.index) / (data_set_info['users_num'] * data_set_info['items_num'])) * 100
    data_set_info['density'] = round(data_set_info['density'], 2)
    return data_set_info


def user_history(data_set, user_id):
    data = pd.read_csv(f"{os.path.dirname(os.path.abspath(__file__))}/data_sets/{data_set}.txt", sep=";", names=[COL_USER, COL_ITEM, COL_RATING, COL_TIMESTAMP])
    history_df = data[data[COL_USER] == user_id][[COL_ITEM, COL_TIMESTAMP]]
    history_df.sort_values(COL_TIMESTAMP, inplace=True, ascending=False)
    history_item_timestamp_list = list(history_df.itertuples(index=False, name=None))
    history_objects = [HistoryElement(timestamp, *(eval(history_item)))
                       for history_item, timestamp in history_item_timestamp_list]

    return history_objects


def get_algorithms_names():
    algorithms = [f for f in listdir(join(dirname(__file__), 'algorithms'))
                  if isfile(join(join(dirname(__file__), 'algorithms'), f))]
    algorithms = [f[:-len(".py")] for f in algorithms if f.endswith(".py")]
    return algorithms


def get_data_sets_names():
    data_sets = [f for f in listdir(join(dirname(__file__), 'data_sets'))
                 if isfile(join(join(dirname(__file__), 'data_sets'), f))]
    data_sets = [f[:-len(".txt")] for f in data_sets if f.endswith(".txt")]
    return data_sets


# if __name__ == '__main__':
#     # print(recommend("sar", "u100_p110", 10))
#     print(user_history("u100_p110", 10))
#     print(users_id_list("u100_p110"))