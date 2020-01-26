import sys
sys.path.append("../../")
import cornac
from src.algorithms.reco_utils.recommender.cornac.cornac_utils import predict_ranking
from src.constants import *


class BPR(object):
    def __init__(self):
        self.model = None
        self.available_data = None

    def prepare_model(self, available_data):
        self.available_data = available_data
        train_set = cornac.data.Dataset.from_uir(available_data.itertuples(index=False), seed=BPR_SEED)
        self.model = cornac.models.BPR(
            k=BPR_LATENT_VECTOR_SIZE,
            max_iter=BPR_EPOCHS_NUM,
            learning_rate=BPR_LEARNING_RATE,
            lambda_reg=BPR_REGULARIZATION,
            verbose=True,
            seed=BPR_SEED
        )
        self.model.fit(train_set)

        return self.available_data, self.model

    def recommend(self, saved_model, user_id, top_k=10):
        self.available_data, self.model = saved_model
        if user_id not in self.available_data[COL_USER].unique():
            raise KeyError

        user_data = self.available_data[self.available_data[COL_USER] == user_id]
        predictions_for_user = predict_ranking(
            self.model,
            user_data,
            user_id,
            usercol=COL_USER,
            itemcol=COL_ITEM,
            predcol=COL_PREDICTION,
            remove_seen=True
        )
        top_k = predictions_for_user.nlargest(top_k, COL_PREDICTION)

        return top_k[COL_ITEM].to_list()