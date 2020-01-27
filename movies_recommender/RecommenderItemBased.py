import heapq
from collections import defaultdict
from operator import itemgetter
# python -m movies_recommender.RecommenderItemBased
from surprise.prediction_algorithms.matrix_factorization import SVD

from movies_analyzer.Movies import Movies
from movies_recommender.Evaluator import get_evaluation
from movies_analyzer.RecommendationDataset import RecommendationDataSet

from movies_recommender.Recommender import Recommender, test_recommendation
from surprise import KNNBasic


class RecommenderItemBased(Recommender):
    def __init__(self, recommendation_dataset):
        super(RecommenderItemBased, self).__init__(recommendation_dataset)
        self.algorithm = SVD()

    def get_recommendation(self, moviescore_df, columns, k=20, name='cosine', k_inner_item=100):
        similar_items = self.get_similar_item_movie_ids(moviescore_df, columns,
                                                        k=k, name=name,
                                                        k_inner_item=k_inner_item)
        return self.movies.get_movie_by_movie_ids([c[0] for c in similar_items])

    def evaluate(self, test_size=.25):
        print("TODO: For evaluate(): test() not yet implemented")
        pass

    def fit(self, dataset):
        print("No fit required")

    def test(self, test_set):
        # TODO: Evaluate for ItemBase
        print("TODO: Not yet implemented")

    def get_similar_item_movie_ids(self, moviescore_df, columns, k=20, name='cosine', k_inner_item=100):
        """
            Based on similar item movies, find nearest movies to the watched
            :param
        """
        sim_options = {'name': name,
                       'user_based': False
                       }
        model = KNNBasic(sim_options=sim_options)
        new_user_id, dataset = self.recommendation_dataset.get_dataset_with_extended_user(
            moviescore_df,
            columns)
        dataset_full = dataset.build_full_trainset()
        model.fit(dataset_full)

        inner_user_id = dataset_full.to_inner_uid(new_user_id)

        # Get most liked by movies
        inner_item_ratings = dataset_full.ur[inner_user_id]
        inner_item_most_liked = heapq.nlargest(k_inner_item, inner_item_ratings, key=lambda t: t[1])

        # Get the stuff they rated, and add up ratings for each item, weighted by user similarity
        candidates = defaultdict(float)
        for item_id, rating in inner_item_most_liked:
            similarity_row = model.sim[item_id]
            for inner_id, score in enumerate(similarity_row):
                candidates[inner_id] += score * (rating / 5.0)

        # Build a dictionary of stuff the user has already seen
        watched = {}
        for inner_item_id, _ in dataset_full.ur[inner_user_id]:
            watched[inner_item_id] = 1

        return [(dataset_full.to_raw_iid(c[0]), c[1])
                for c in sorted(candidates.items(), key=itemgetter(1), reverse=True)
                if c[0] not in watched][:k]


if __name__ == '__main__':
    movies = Movies()
    recommendation_dataset = RecommendationDataSet(movies=movies)
    recommender = RecommenderItemBased(recommendation_dataset)

    test_recommendation(recommender=recommender, example_items=['arek'])
