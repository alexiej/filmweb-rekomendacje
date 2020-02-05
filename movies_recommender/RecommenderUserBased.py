import heapq
from collections import defaultdict
from operator import itemgetter
from surprise.prediction_algorithms.matrix_factorization import SVD

from movies_analyzer.Movies import Movies
from movies_analyzer.RecommendationDataset import RecommendationDataSet

from movies_recommender.Recommender import Recommender, test_recommendation
from surprise import KNNBasic

class RecommenderUserBased(Recommender):
    def __init__(self, recommendation_dataset, similarity = 'cosine'):
        super(RecommenderUserBased, self).__init__(recommendation_dataset)
        sim_options = {'name': similarity,
                       'user_based': True
                       }
        self.algorithm = KNNBasic(sim_options=sim_options)

    def fit(self, dataset):
        return self.algorithm.fit(dataset)

    def test(self, test_set):
        return self.algorithm.test(test_set)

    def get_recommendation(self, moviescore_df, columns, k=20,  k_inner_item=200):
        similar_users = self.recommendation_dataset.get_similar_user_ids(moviescore_df, columns, k=k_inner_item)
        full_dataset = self.algorithm.trainset

        # watched movies
        watched = {full_dataset.to_inner_iid(str(int(i[0]))): i[1] for i in moviescore_df[columns].values}

        # get most similar items, based on cosine similarity and most similar users
        candidates = defaultdict(float)
        for user_id, similarity in similar_users.items():
            for inner_movie_id, rate in full_dataset.ur[user_id]:
                if inner_movie_id not in watched:
                    candidates[inner_movie_id] += similarity * rate

        # return top-n movies
        movie_ids = [
                full_dataset.to_raw_iid(i) 
                for i in heapq.nlargest(k, candidates, key = candidates.get)]

        return self.movies.get_movie_by_movie_ids(movie_ids)
        

if __name__ == '__main__':
    recommendation_dataset = RecommendationDataSet(movies=Movies())
    # Require for working saving pickle to load not from module 
    # AttributeError: Can't get attribute 'RecommenderUserBased' on <module '__main__' from 'server.py'>`
    from movies_recommender.RecommenderUserBased import RecommenderUserBased
    recommender = RecommenderUserBased(recommendation_dataset)
    test_recommendation(recommender=recommender, example_items=['arek','mateusz'], anti_test=True)

    """ For test only
    %load_ext autoreload
    %autoreload 2
    
    from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
    from filmweb_integrator.fwimdbmerge.merger import Merger, get_json_df
    from movies_recommender.Recommender import get_moviescore_df

    recommendation_dataset = RecommendationDataSet(movies=Movies())
    recommender = RecommenderUserBased(recommendation_dataset)
    recommender.fit(recommender.recommendation_dataset.full_dataset)

    merger = Merger(filmweb=Filmweb(), imdb=recommender.movies.imdb)
    moviescore_df = get_moviescore_df(merger, recommender.movies,'arek')
    k = 20
    k_inner_item = 20
    columns=['movieId', 'OcenaImdb']

    self = recommender
    self.get_recommendation(moviescore_df,columns)
    """

