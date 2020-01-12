import sys
sys.path.append("../")
from src.algorithms.markov_model import MarkovModel
from src.algorithms.most_popular import MostPopular
from src.algorithms.user_knn import UserKNN
from src.algorithms.sar import SAR


def map_to_algorithm(name):
    if name == "markov_model":
        algorithm = MarkovModel()
    elif name == "most_popular":
        algorithm = MostPopular()
    elif name == "user_knn":
        algorithm = UserKNN()
    elif name == "sar":
        algorithm = SAR()
    else:
        raise NotImplementedError(f"Algorithm with name: '{name}' not implemented "
                                  f"or not added to mapper.map_to_algorithm function")
    return algorithm
