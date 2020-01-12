import sys
sys.path.append("../../")
from src.algorithms.reco_utils.recommender.sar.sar_singlenode import SARSingleNode
from src.algorithms.reco_utils.evaluation.python_evaluation import map_at_k, ndcg_at_k, precision_at_k, recall_at_k, mrr_at_k
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


# moje wyliczanie metryk, wyliczanie dla pojedynczych usero i dodanie i podzielenie

# sum_recall = 0
    # sum_precision = 0
    # for user_id in test[COL_USER].unique():
    #     user_test_set = test[test[COL_USER] == user_id]  # ewentualnie brac 10 rekordow na test
    #
    #     top_k = model.recommend_k_items(user_test_set, remove_seen=True)
    #     eval_precision = precision_at_k(
    #         user_test_set,
    #         top_k,
    #         col_user=COL_USER,
    #         col_item=COL_ITEM,
    #         col_rating=COL_RATING,
    #         col_prediction=COL_PREDICTION,
    #         relevancy_method='top_k',
    #         k=10
    #     )
    #     eval_recall = recall_at_k(
    #         user_test_set,
    #         top_k,
    #         col_user=COL_USER,
    #         col_item=COL_ITEM,
    #         col_rating=COL_RATING,
    #         col_prediction=COL_PREDICTION,
    #         relevancy_method='top_k',
    #         k=10
    #     )
    #
    #     # print("USER ID: ", user_id)
    #     # print("test: ", list(user_test_set["PathId"]))
    #     # print("top_k: ", list(top_k["PathId"]))
    #     # print("Recall: " + str(eval_recall))
    #     # print("Precision: " + str(eval_precision))
    #     sum_recall += eval_recall
    #     sum_precision += eval_precision
    #
    # # print("Average recall: ", sum_recall/test[COL_USER].nunique())
    # # print("Average precision: ", sum_precision/test[COL_USER].nunique())
    #
    # return {"Recall": str(sum_recall/test[COL_USER].nunique()), "Precision": str(sum_precision/test[COL_USER].nunique())}