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
    def __init__(self, recommendation_dataset: RecommendationDataSet):
        self.movies = recommendation_dataset.movies
        self.recommendation_dataset = recommendation_dataset

    def get_recommendation(self, moviescore_df, columns, k=20):
        raise NotImplementedError

    def evaluate(self, test_size=.25):
        self.recommendation_dataset.build_train_test(test_size=test_size)
        self.fit(self.recommendation_dataset.train_set)
        get_evaluation(self)

    def fit(self, dataset):
        raise NotImplementedError

    def test(self, test_set):
        raise NotImplementedError


def get_example_df(file):
    return pd.read_csv(Path(os.getcwd()) / f'data_static/example_{file}_03_merge.csv').set_index('tconst')


def test_recommendation(recommender: Recommender, example_items=None):
    if example_items is None:
        example_items = ['arek', 'mateusz']

    recommender.evaluate(test_size=.25)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 500)

    import time
    start_time = time.time()
    recommender.fit(recommender.recommendation_dataset.full_dataset)
    print("--- FIT %s seconds ---" % (time.time() - start_time))

    k = 10

    # Test recommendation for the user
    for i in example_items:
        movielens_df = recommender.movies.merge_imdb_movielens(get_example_df(i))

        start_time = time.time()
        # recommender.process(movielens_df, i)
        # print(f'Recommendation from SVD by similar Users "{i}":')
        # print(self.get_recommendation_by_similar_user(
        #     moviescore_df=movielens_df,
        #     columns=['movieId', 'OcenaImdb'], k=k))

        print(f'========================================================\n')
        print(f'Recommendation from {recommender.__class__} "{i}":')
        print(recommender.get_recommendation(
            moviescore_df=movielens_df,
            columns=['movieId', 'OcenaImdb'], k=k))
        print("--- %s seconds ---" % (time.time() - start_time))
        print(f'========================================================')

