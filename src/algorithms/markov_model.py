import sys
sys.path.append("../")
from src.constants import *


class MarkovModel(object):
    def __init__(self):
        self.sequence = None
        self.available_data = None

    def prepare_model(self, available_data):
        self.available_data = available_data.groupby(COL_USER)[COL_ITEM].apply(list).to_dict()
        self.sequence = dict()  # sciezka: {sciezka po niej: liczba takich wystapien, inna sciezka po niej: liczba wystapien}

        for user_id, one_user_seq in self.available_data.items():
            for i in range(len(one_user_seq) - 1):
                path = one_user_seq[i]
                if path not in self.sequence:
                    self.sequence[path] = dict()
                    self.sequence[path][one_user_seq[i + 1]] = 1
                else:
                    if one_user_seq[i + 1] not in self.sequence[path]:
                        self.sequence[path][one_user_seq[i + 1]] = 1
                    else:
                        self.sequence[path][one_user_seq[i + 1]] += 1

        return self.available_data, self.sequence

    def recommend(self, saved_model, user_id, top_k=10):
        self.available_data, self.sequence = saved_model

        user_seq = self.available_data[user_id]
        last_item = user_seq[-1]

        following_paths = self.sequence[last_item]  # slownik ze wszystkimi sciezkami ktore wystepowaly po niej wraz z liczbami takich zajsc

        ranking_list = [item_occurences[0] for item_occurences in
                        sorted(following_paths.items(), key=lambda item: item[1], reverse=True)]

        list_without_passed = [item for item in ranking_list if item not in user_seq]

        items_num = min(top_k, len(list_without_passed))
        return list_without_passed[:items_num]
