import numpy as np
import scipy.sparse as ssp
import math
from src.constants import *


def get_sparse_vector(ids, length, values=None):
    n = len(ids)
    if values is None:
        return ssp.coo_matrix((np.ones(n), (ids, np.zeros(n))), (length, 1)).tocsc()
    else:
        return ssp.coo_matrix((values, (ids, np.zeros(n))), (length, 1)).tocsc()


class UserKNN(object):
    def __init__(self):
        self.neighborhood_size = None
        self.path_id_map = None
        self.id_path_map = None
        self.binary_user_item = None
        self.n_items = None
        self.n_users = None
        self.dataset = None

    def prepare_model(self, dataset):
        self.neighborhood_size = int(math.sqrt(dataset[COL_USER].nunique()))
        self.path_id_map = dict(zip(dataset[COL_ITEM].unique(), range(dataset[COL_ITEM].nunique())))
        self.id_path_map = {value: key for key, value in self.path_id_map.items()}
        dataset[COL_ITEM] = dataset[COL_ITEM].map(self.path_id_map)
        self.dataset = dataset

        self.binary_user_item = ssp.coo_matrix((dataset[COL_RATING], (dataset[COL_USER], dataset[COL_ITEM]))).tocsr()

        self.n_items = self.binary_user_item.shape[1]
        self.n_users = self.binary_user_item.shape[0]

        return self.neighborhood_size, self.path_id_map, self.id_path_map, self.binary_user_item, \
               self.n_items, self.n_users, self.dataset

    def _items_count_per_user(self):
        if not hasattr(self, '__items_count_per_user'):
            self.__items_count_per_user = np.asarray(self.binary_user_item.sum(axis=1)).ravel()
        return self.__items_count_per_user

    def similarity_with_users(self, sequence):
        sparse_sequence = get_sparse_vector(sequence, self.n_items)
        overlap = self.binary_user_item.dot(sparse_sequence).toarray().ravel()
        overlap[overlap != 0] /= np.sqrt(self._items_count_per_user()[overlap != 0])
        return overlap

    def similarity_jaccard(self, sequence):
        """
        |A n B| / |A u B|
        A u B = A + B - A n B
        """
        sparse_sequence = get_sparse_vector(sequence, self.n_items)
        overlap = self.binary_user_item.dot(sparse_sequence).toarray().ravel()
        overlap[overlap != 0] /= (len(sequence) + self._items_count_per_user()[overlap != 0] - overlap[overlap != 0])
        return overlap

    def recommend(self, saved_model, user_id, top_k=10):
        self.neighborhood_size, self.path_id_map, self.id_path_map, self.binary_user_item, self.n_items, self.n_users, self.dataset = saved_model
        if user_id not in self.dataset[COL_USER].unique():
            raise KeyError

        user_seq = self.dataset[self.dataset[COL_USER] == user_id][COL_ITEM].tolist()

        sim_with_users = self.similarity_with_users(user_seq)

        users_ranking = (-sim_with_users).argsort()
        nearest_neighbors = users_ranking[:self.neighborhood_size]

        sim_with_users = get_sparse_vector(nearest_neighbors, self.n_users, values=sim_with_users[nearest_neighbors])
        sim_with_items = self.binary_user_item.T.dot(sim_with_users).toarray().ravel()

        ranking_list = (-sim_with_items).argsort()
        list_without_passed = [item for item in ranking_list if item not in user_seq]

        items_num = min(top_k, len(list_without_passed))
        list_without_passed = list_without_passed[:items_num]
        return [self.id_path_map[id] for id in list_without_passed]
