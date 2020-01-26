import argparse
import sys
import pandas as pd
import pickle
from os import listdir
from os.path import isfile, join
from mapper import map_to_algorithm
from constants import *

ALL_DATA_SETS_SYMBOL = '*'


def get_algorithms():
    algorithms = [f for f in listdir("algorithms") if isfile(join("algorithms", f))]
    algorithms = [f[:-len(".py")] for f in algorithms if f.endswith(".py")]
    return algorithms


def get_data_sets():
    data_sets = [f for f in listdir("data_sets") if isfile(join("data_sets", f))]
    data_sets = [f[:-len(".txt")] for f in data_sets if f.endswith(".txt")]
    return data_sets


def parse_arguments():
    algorithms = get_algorithms()
    data_sets = get_data_sets()
    data_sets.append(ALL_DATA_SETS_SYMBOL)  # option to pick all data sets

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
        help="dataset to build model for, you can use * to build models for every data set. "
             "Symbol needs to be escaped or taken in quotes because its bash special char!",
        metavar='DATA_SET/\'*\' for all files',
        required=True,
        choices=data_sets
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    algorithm_name = args.algorithm

    if args.data_set == ALL_DATA_SETS_SYMBOL:
        data_sets = get_data_sets()
    else:
        data_sets = [args.data_set]

    for data_set in data_sets:
        print("BUILDING MODEL FOR PARAMETERS:")
        print("--algorithm " + algorithm_name)
        print("--data_set " + data_set)

        path = f"data_sets/{data_set}.txt"
        data = pd.read_csv(path, sep=";", names=[COL_USER, COL_ITEM, COL_RATING, COL_TIMESTAMP])
        data.sort_values(COL_TIMESTAMP, inplace=True)
        algorithm = map_to_algorithm(algorithm_name)
        model_to_save = algorithm.prepare_model(data)
        file = open(f'models/{algorithm_name}_{data_set}.pkl', 'wb+')
        pickle.dump(model_to_save, file)
        file.close()

        print("MODEL HAS BEEN BUILD\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
