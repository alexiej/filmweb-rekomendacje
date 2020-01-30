import heapq
from collections import defaultdict
from operator import itemgetter

from surprise import KNNBasic
from movies_recommender.Evaluator import get_evaluation
from movies_analyzer.RecommendationDataset import RecommendationDataSet
import pandas as pd
import os
from pathlib import Path
from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
from filmweb_integrator.fwimdbmerge.merger import Merger, get_json_df
from movies_analyzer.Movies import Movies, SMALL_MOVIELENS

class Recommender(object):
    def __init__(self, recommendation_dataset: RecommendationDataSet):
        self.movies = recommendation_dataset.movies
        self.recommendation_dataset = recommendation_dataset

    def get_recommendation(self, moviescore_df, columns, k=20):
        raise NotImplementedError

    def evaluate(self, test_size=.25, anti_test=True):
        self.recommendation_dataset.build_train_test(test_size=test_size)
        get_evaluation(self,verbose=True,anti_test=anti_test)

    def fit(self, dataset):
        raise NotImplementedError

    def test(self, test_set):
        raise NotImplementedError


def get_moviescore_df(merger, movies, file):
    path = Path(os.getcwd()) / f'data_static/example_{file}_01_json.json'
    filmweb_df, df = merger.get_data(get_json_df(open(path, "r",encoding="utf-8").read()))
    return movies.merge_imdb_movielens(df)


def test_recommendation(recommender: Recommender, example_items=None, anti_test=True):
    if example_items is None:
        example_items = ['arek', 'mateusz']
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 500)

    recommender.evaluate(test_size=.25, anti_test=anti_test)

    import time
    start_time = time.time()
    recommender.fit(recommender.recommendation_dataset.full_dataset)
    print("--- FIT %s seconds ---" % (time.time() - start_time))

    k = 10
    merger = Merger(filmweb=Filmweb(), imdb=recommender.movies.imdb)

    # Test recommendation for the user
    for i in example_items:
        moviescore_df = get_moviescore_df(merger, recommender.movies,i)
        start_time = time.time()

        print(f'========================================================\n')
        print(f'Recommendation from {type(recommender).__name__} "{i}":')
        print(recommender.get_recommendation(
            moviescore_df=moviescore_df,
            columns=['movieId', 'OcenaImdb'], k=k))
        print("--- %s seconds ---" % (time.time() - start_time))
        print(f'========================================================')

