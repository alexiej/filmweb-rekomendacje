import heapq
from collections import defaultdict
from operator import itemgetter
# python -m movies_recommender.RecommenderItemBased
from movies_analyzer.Movies import Movies
from movies_analyzer.RecommendationDataset import RecommendationDataSet
from movies_recommender.Recommender import Recommender
from surprise import KNNBasic


class RecommenderItemBased(Recommender):
    def __init__(self, recommendation_dataset: RecommendationDataSet, similarity='cosine'):
        super(RecommenderItemBased, self).__init__(recommendation_dataset.movies)
        self.recommendation_dataset = recommendation_dataset
        sim_options = {'name': similarity,
                       'user_based': False
                       }
        self.algorithm = KNNBasic(sim_options=sim_options)

    def get_recommendation(self, watched,  k=20, k_inner_item=100):
        similar_items = self.get_similar_movie_ids(watched, k=k, k_inner_item=k_inner_item)
        return self.movies.get_movie_by_movie_ids(similar_items)

    def fit(self, dataset):
        return self.algorithm.fit(dataset)

    def test(self, test_set):
        return self.algorithm.test(test_set)

    def get_similar_movie_ids(self, watched, k=20,  k_inner_item=100):
        """
            Based on similar item movies, find nearest movies to the watched
            :param
        """
        full_dataset = self.algorithm.trainset

        # watched movies
        watched = {full_dataset.to_inner_iid(key): value for key,value in watched.items()}

        # Get most liked movies
        # inner_item_ratings = full_dataset.ur[inner_user_id]
        most_liked = heapq.nlargest(k_inner_item, watched, key = watched.get) #['Ocena','OcenaImdb','averageRating'])[['movieId','OcenaImdb']]
        
        # Get the stuff they rated, and add up ratings for each item, weighted by user similarity
        candidates = defaultdict(float)
        for most_liked_inner_id in most_liked:
            rating = watched[most_liked_inner_id]
            similarity_row = self.algorithm.sim[most_liked_inner_id]

            for inner_id, score in enumerate(similarity_row):
                if inner_id!=most_liked_inner_id:
                    candidates[inner_id] += score * (rating / 5.0)

        # return top-n movies
        similar_items = [full_dataset.to_raw_iid(i) for i in heapq.nlargest(k, candidates, key = candidates.get)]
        return similar_items

if __name__ == '__main__':
    from movies_recommender.Recommender import test_recommendation
    from movies_recommender.RecommenderItemBased import RecommenderItemBased
    from movies_analyzer.RecommendationDataset import RecommendationDataSet
    from movies_analyzer.Movies import Movies

    movies = Movies()
    recommendation_dataset = RecommendationDataSet(movies=movies)
    recommender = RecommenderItemBased(recommendation_dataset)

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

    self.get_recommendation(watched, k=20)
    """