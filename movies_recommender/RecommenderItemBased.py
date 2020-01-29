import heapq
from collections import defaultdict
from operator import itemgetter
# python -m movies_recommender.RecommenderItemBased
from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise.prediction_algorithms.predictions import Prediction

from movies_analyzer.Movies import Movies
from movies_recommender.Evaluator import get_evaluation
from movies_analyzer.RecommendationDataset import RecommendationDataSet

from movies_recommender.Recommender import Recommender, test_recommendation
from surprise import KNNBasic


class RecommenderItemBased(Recommender):
    def __init__(self, recommendation_dataset: RecommendationDataSet, similarity='cosine'):
        super(RecommenderItemBased, self).__init__(recommendation_dataset)
        sim_options = {'name': similarity,
                       'user_based': False
                       }
        self.algorithm = KNNBasic(sim_options=sim_options)

    def get_recommendation(self, moviescore_df, columns, k=20, k_inner_item=100):
        similar_items = self.get_similar_movie_ids(moviescore_df, columns,
                                                        k=k, name=name,
                                                        k_inner_item=k_inner_item)
        return self.movies.get_movie_by_movie_ids(similar_items)

    def fit(self, dataset):
        self.algorithm.fit(dataset)

    def test(self, test_set):
        self.algorithm.test(test_set)

    def get_similar_movie_ids(self, moviescore_df, columns, k=20,  k_inner_item=100):
        """
            Based on similar item movies, find nearest movies to the watched
            :param
        """
        # Build a dictionary of stuff the user has already seen
        watched = { self.algorithm.trainset.to_inner_iid(str(row.movieId)): row.OcenaImdb 
                    for row in  moviescore_df[['movieId','OcenaImdb']].itertuples()}

        # Get most liked movies
        # inner_item_ratings = full_dataset.ur[inner_user_id]
        most_liked = heapq.nlargest(k_inner_item, watched, key = watched.get) #['Ocena','OcenaImdb','averageRating'])[['movieId','OcenaImdb']]
        
        # Get the stuff they rated, and add up ratings for each item, weighted by user similarity
        candidates = defaultdict(float)
        for most_liked_inner_id in most_liked:
            rating = watched[most_liked_inner_id]
            similarity_row = self.algorithm.sim[most_liked_inner_id]

            for inner_id, score in enumerate(similarity_row[:15]):
                if inner_id!=most_liked_inner_id:
                    candidates[inner_id] += score * (rating / 5.0)

        # return top-n movies
        return heapq.nlargest(k, candidates, key = candidates.get)


if __name__ == '__main__':
    recommendation_dataset = RecommendationDataSet(movies=Movies())
    recommender = RecommenderItemBased(recommendation_dataset)

    test_recommendation(recommender=recommender, example_items=['arek'])
