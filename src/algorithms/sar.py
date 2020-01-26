import sys
sys.path.append("../../")
from src.algorithms.reco_utils.recommender.sar.sar_singlenode import SARSingleNode
from src.constants import *


class SAR(object):
    def __init__(self):
        self.model = None
        self.available_data = None

    def prepare_model(self, available_data):
        self.available_data = available_data
        self.model = SARSingleNode(
            similarity_type="jaccard",
            time_decay_coefficient=30,
            time_now=None,
            timedecay_formula=True,
            col_user=COL_USER,
            col_item=COL_ITEM,
            col_rating=COL_RATING,
            col_prediction=COL_PREDICTION,
            col_timestamp=COL_TIMESTAMP
        )
        self.model.fit(available_data)

        return self.available_data, self.model

    def recommend(self, saved_model, user_id, top_k=10):
        self.available_data, self.model = saved_model
        if user_id not in self.available_data[COL_USER].unique():
            raise KeyError

        user_data = self.available_data[self.available_data[COL_USER] == user_id]
        top_k = self.model.recommend_k_items(user_data, top_k=top_k, remove_seen=True)

        return top_k[COL_ITEM].to_list()
