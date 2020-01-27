import heapq
from collections import defaultdict
from operator import itemgetter

from surprise import KNNBasic
from movies_recommender.Evaluator import get_evaluation
from movies_analyzer.RecommendationDataset import RecommendationDataSet
import pandas as pd
import os
from pathlib import Path


class Recommender(object):
    def __init__(self, recommendation_dataset: RecommendationDataSet, algorithm):
        self.movies = recommendation_dataset.movies
        self.algorithm = algorithm
        self.recommendation_dataset = recommendation_dataset

    def get_recommendation(self, moviescore_df, columns, k=20):
        raise NotImplementedError

    def evaluate(self, test_size=.25):
        self.recommendation_dataset.build_train_test(test_size=.25)
        self.algorithm.fit(self.recommendation_dataset.train_set)
        get_evaluation(self)

    def process(self, movielens_df, i):
        raise NotImplementedError


def get_example_df(file):
    return pd.read_csv(Path(os.getcwd()) / f'data_static/example_{file}_03_merge.csv').set_index('tconst')


def test_recommendation(recommender: Recommender, example_items=None):
    if example_items is None:
        example_items = ['arek', 'mateusz']

    recommender.evaluate(test_size=.25)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 500)

    # Test recommendation for the user
    for i in example_items:
        movielens_df = recommender.movies.merge_imdb_movielens(get_example_df(i))
        recommender.process(movielens_df, i)
