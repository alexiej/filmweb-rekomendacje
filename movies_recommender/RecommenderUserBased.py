import heapq
from collections import defaultdict
from operator import itemgetter
# python -m movies_recommender.RecommenderUserBased
from surprise.prediction_algorithms.matrix_factorization import SVD

from movies_analyzer.Movies import Movies
from movies_analyzer.RecommendationDataset import RecommendationDataSet

from movies_recommender.Recommender import Recommender, test_recommendation
from surprise import KNNBasic


class RecommenderUserBased(Recommender):
    def __init__(self, recommendation_dataset):
        super(RecommenderUserBased, self).__init__(recommendation_dataset, algorithm=SVD())

    def get_recommendation(self, moviescore_df, columns, k=20, name='cosine', k_inner_item=100):
        similar_users = self.get_similar_users_raw(moviescore_df, columns, k=k)
        full_dataset = self.algorithm.trainset

        # watched movies
        watched = {full_dataset.to_inner_iid(str(i)): 1 for i in moviescore_df[columns[0]].values}

        # Calculate for all similar user, predictions
        test_items = self.algorithm.test(
            [
                (full_dataset.to_inner_uid(str(user_id)), i, 3.5)
                for user_id in similar_users.keys()
                for i in range(0, full_dataset.n_items)
                if i not in watched
            ])

        # Get the stuff they rated, and add up ratings for each item, weighted by user similarity
        candidates = defaultdict(float)
        for p in test_items:
            candidates[p.iid] += p.est * similar_users[int(full_dataset.to_raw_uid(p.uid))]

        return self.movies.get_movie_by_movie_ids(
            [full_dataset.to_raw_iid(c[0])
             for c in sorted(candidates.items(), key=itemgetter(1), reverse=True)][:k])

    def get_similar_users_raw(self, moviescore_df, columns, k=20, name='cosine'):
        inner_user_id, inner_nearest_ids, sims_matrix, dataset_full = self.get_similar_users(moviescore_df,
                                                                                             columns,
                                                                                             k=k, name=name)
        return {dataset_full.to_raw_uid(i): sims_matrix[inner_user_id][i] for i in inner_nearest_ids}

    def get_similar_users(self, moviescore_df, columns, k=20, name='cosine'):
        """
            using cosine similarity find similar users, based on the current one.
        :param
            moviescore_df: converted movielens dataframe with movies
            columns: Tuple(str,str) - First column of MovieID, second of Imdb Score (1,5)
        :return: inner_user_id, inner_nearest_id, model.sim, dataset_full
        """
        sim_options = {'name': name,
                       'user_based': True}

        model = KNNBasic(sim_options=sim_options)
        new_user_id, dataset = self.recommendation_dataset.get_dataset_with_extended_user(
            moviescore_df, columns)

        dataset_full = dataset.build_full_trainset()
        model.fit(dataset_full)
        inner_user_id = dataset_full.to_inner_uid(new_user_id)
        inner_nearest_id = model.get_neighbors(inner_user_id, k=k)

        return inner_user_id, inner_nearest_id, model.sim, dataset_full

    def process(self, movielens_df, i):
        k = 10
        print(f'========================================================\n'
              f'Recommendation from UserBased for "{i}":')
        print(self.get_recommendation(
            moviescore_df=movielens_df[['movieId', 'OcenaImdb']],
            columns=['movieId', 'OcenaImdb'], k=k))
        print(f'========================================================')


if __name__ == '__main__':
    movies = Movies()
    recommendation_dataset = RecommendationDataSet(movies=movies)
    recommender = RecommenderUserBased(recommendation_dataset)

    test_recommendation(recommender=recommender, example_items=['arek'])
