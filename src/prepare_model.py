import argparse
import sys
import pandas as pd
import pickle
from os import listdir
from os.path import isfile, join
from mapper import map_to_algorithm
from constants import *


def parse_arguments():
    algorithms = [f for f in listdir("algorithms") if isfile(join("algorithms", f))]
    algorithms = [f[:-len(".py")] for f in algorithms if f.endswith(".py")]

    data_sets = [f for f in listdir("data_sets") if isfile(join("data_sets", f))]
    data_sets = [f[:-len(".txt")] for f in data_sets if f.endswith(".txt")]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--algorithm",
        help="algorithm to build model for",
        metavar='ALGORITHM',
        required=True,
        choices=algorithms
    )
    parser.add_argument(
        "-d", "--data_set",
        help="dataset to build model for",
        metavar='DATA_SET',
        required=True,
        choices=data_sets
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    print("BUILDING MODEL FOR PARAMETERS:")
    print("--algorithm " + args.algorithm)
    print("--data_set " + args.data_set)

    algorithm_name = args.algorithm
    path = f"data_sets/{args.data_set}.txt"

    data = pd.read_csv(path, sep=";", names=[COL_USER, COL_ITEM, COL_RATING, COL_TIMESTAMP])
    data.sort_values(COL_TIMESTAMP, inplace=True)
    algorithm = map_to_algorithm(algorithm_name)
    model_to_save = algorithm.prepare_model(data)

    file = open(f'models/{algorithm_name}_{args.data_set}.pkl', 'wb+')
    pickle.dump(model_to_save, file)
    file.close()

    print("MODEL HAS BEEN BUILD")
    return 0


if __name__ == '__main__':
    sys.exit(main())
