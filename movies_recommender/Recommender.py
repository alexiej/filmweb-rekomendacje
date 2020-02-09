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
import pickle
import math
import random

RECOMMENDER_PATH = Path(os.getcwd())/'movies_recommender'/'models'

def load_recommender(name='SVDpp.pkl'):
    import pickle
    import os
    reccommender = pickle.load(open(RECOMMENDER_PATH/name,mode="rb"))
    print('load recommender: ', name)
    return reccommender

class Recommender(object):
    def __init__(self, movies):
        self.movies = movies 
        # recommendation_dataset.movies
        # self.recommendation_dataset = recommendation_dataset

    def get_recommendation(self, watched: dict, k=20):
        raise NotImplementedError
    
    def get_similar_user_ids(self, watched, k=20, random_choice=2.0):
        full_dataset = self.algorithm.trainset
        # min_user_similar = 20 if len(watched) > 200 else 0.2*len(watched)

        # u_sqrt = math.sqrt(sum([i*i for  i in watched.values()]))
        # https://en.wikipedia.org/wiki/Cosine_similarity
        # If user has only 1 movie watched  as we are his similarity will be 1.0 if he get the same rating as us
        cosine_similarity = defaultdict(lambda: (0, 0, 0, 0))
        for index,rating in watched.items():
            for user_id, user_rating in full_dataset.ir[index]:
                cosine_similarity[user_id] = (
                                              cosine_similarity[user_id][0] + rating*user_rating,
                                              cosine_similarity[user_id][1] + user_rating*user_rating,
                                              cosine_similarity[user_id][2] + rating*rating,
                                              cosine_similarity[user_id][3] + 1,
                                              )

        similarity = {
            index: ( val0/(math.sqrt(val1)*math.sqrt(val2)) ) * (length/len(watched))
        for index, (val0, val1,val2, length) in cosine_similarity.items() 
        }
        similar_users = dict(
            random.sample(heapq.nlargest(int(k*random_choice), 
                    similarity.items(), key=itemgetter(1)),k)
            )
        return similar_users


    def evaluate(self, recommendation_dataset, test_size=.25, anti_test=True):
        recommendation_dataset.build_train_test(test_size=test_size)
        get_evaluation(self, recommendation_dataset=recommendation_dataset, verbose=True,anti_test=anti_test)

    def fit(self, dataset):
        raise NotImplementedError

    def test(self, test_set):
        raise NotImplementedError

    def save(self):
        name = type(self).__name__ + ".pkl"
        with open(RECOMMENDER_PATH/name,mode="wb") as f:
            pickle.dump(self,f)
            print("Module: ", self.__module__, " saved at: ", RECOMMENDER_PATH/name)


def get_moviescore_df(merger, movies, file):
    path = Path(os.getcwd()) / f'data_static/example_{file}_01_json.json'
    filmweb_df, df = merger.get_data(get_json_df(open(path, "r",encoding="utf-8").read()))
    moviescore_df = movies.merge_imdb_movielens(df)
    return moviescore_df


def get_watched(moviescore_df):
    return {str(v.movieId): v.OcenaImdb for v in moviescore_df.itertuples()} 

def test_recommendation(recommender,
                        recommendation_dataset, 
                        example_items=None, anti_test=True):
    if example_items is None:
        example_items = ['arek', 'mateusz']
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 500)

    recommender.evaluate(recommendation_dataset, test_size=.25, anti_test=anti_test)

    import time
    zero_time = time.time()
    start_time = time.time()
    recommender.fit(recommendation_dataset.full_dataset)
    print("--- FIT %s seconds ---" % (time.time() - start_time))

    k = 10
    merger = Merger(filmweb=Filmweb(), imdb=recommender.movies.imdb)

    # Test recommendation for the user
    for i in example_items:
        watched = get_watched(get_moviescore_df(merger, recommender.movies,i))

        start_time = time.time()

        print(f'========================================================\n')
        print(f'Recommendation from {type(recommender).__name__} "{i}":')
        print(recommender.get_recommendation(watched=watched, k=k))
        print("--- %s seconds ---" % (time.time() - start_time))
        print(f'========================================================')

    recommender.save()
    print("--- Total calculation time: %s seconds ---" % (time.time() - zero_time) )
