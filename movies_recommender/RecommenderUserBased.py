import heapq
from collections import defaultdict
from operator import itemgetter
from movies_analyzer.Movies import Movies
from movies_analyzer.RecommendationDataset import RecommendationDataSet
from movies_recommender.Recommender import Recommender
from surprise import KNNBasic

class RecommenderUserBased(Recommender):
    def __init__(self, movies, similarity = 'cosine'):
        super(RecommenderUserBased, self).__init__(movies)
        sim_options = {'name': similarity,
                       'user_based': True
                       }
        self.algorithm = KNNBasic(sim_options=sim_options)

    def fit(self, dataset):
        return self.algorithm.fit(dataset)

    def test(self, test_set):
        return self.algorithm.test(test_set)

    def get_recommendation(self, watched, k=20,  k_inner_item=200):
        full_dataset = self.algorithm.trainset

        # watched movies
        watched = {full_dataset.to_inner_iid(key): value for key,value in watched.items()}

        # get similar users
        similar_users = self.get_similar_user_ids(watched, k=k_inner_item)

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
    from movies_recommender.Recommender import test_recommendation
    from movies_recommender.RecommenderUserBased import RecommenderUserBased
    from movies_analyzer.RecommendationDataset import RecommendationDataSet
    from movies_analyzer.Movies import Movies

    movies = Movies()
    recommendation_dataset = RecommendationDataSet(movies=movies)
    recommender = RecommenderUserBased(movies)

    assert recommender.__module__[:len('movies_recommender.')] == 'movies_recommender.'
    test_recommendation(recommender, recommendation_dataset, 
                        example_items=['arek','mateusz'], anti_test=False)

    """ For test only
    %load_ext autoreload
    %autoreload 2
    
    from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
    from filmweb_integrator.fwimdbmerge.merger import Merger, get_json_df
    from movies_recommender.Recommender import get_moviescore_df, get_watched

    recommender.fit(recommendation_dataset.full_dataset)
    self = recommender

    # get recommendation for one user
    merger = Merger(filmweb=Filmweb(), imdb=movies.imdb)
    watched = get_watched(get_moviescore_df(merger, recommender.movies,'arek'))
    k = 20
    k_inner_item = 20

    self.get_recommendation(watched)
    """
