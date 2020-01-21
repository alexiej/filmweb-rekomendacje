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

    def train(self):
        self.algorithm.fit(self.recommendation_dataset.full_dataset)

    def get_recommendation_by_similar_user(self,
                                           moviescore_df, columns, k=20, k_similar_user=100):
        similar_users = self.get_similar_users_raw(moviescore_df, columns, k=k_similar_user)
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

    def get_similar_item_movies(self, moviescore_df, columns, k=20, name='cosine', k_inner_item=100):
        similar_items = self.get_similar_item_movie_ids(moviescore_df, columns,
                                                        k=k, name=name,
                                                        k_inner_item=k_inner_item)
        return self.movies.get_movie_by_movie_ids([c[0] for c in similar_items])

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

    def get_similar_user_movies(self,
                                moviescore_df, columns,
                                k=20, name='cosine', k_similar_user=20):
        """
            Return similar user movies dataframe
        :param
        """
        similar_movie_ids = self.get_similar_user_movie_ids(
            moviescore_df, columns, k=k, name=name, k_similar_user=k_similar_user)

        return self.movies.get_movie_by_movie_ids([c[0] for c in similar_movie_ids])

    def get_similar_user_movie_ids(self,
                                   moviescore_df, columns,
                                   k=20, name='cosine', k_similar_user=100):
        """
            Get similar movies based on cosine similarity for selected movies in the moviescore_df
        :param
        """
        inner_user_id, inner_user_ids, sim_matrix, dataset_full = self.get_similar_users(moviescore_df, columns,
                                                                                         k=k_similar_user, name=name)

        # Get the stuff they rated, and add up ratings for each item, weighted by user similarity
        candidates = defaultdict(float)
        for inner_id in inner_user_ids:
            user_similarity_score = sim_matrix[inner_user_id][inner_id]
            ratings = dataset_full.ur[inner_id]
            for rating in ratings:
                candidates[rating[0]] += (rating[1] / 5.0) * user_similarity_score

        # Build a dictionary of stuff the user has already seen
        watched = {}
        for itemID, rating in dataset_full.ur[inner_user_id]:
            watched[itemID] = 1

        # Get top-rated items from similar users:
        return [(dataset_full.to_raw_iid(c[0]), c[1]) for c in
                sorted(candidates.items(), key=itemgetter(1), reverse=True) if c[0] not in watched][:k]

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

        k = 10
        moviescore_df = movielens_df[['movieId', 'OcenaImdb']]

        # print(f'========================================================\n'
        #       f'Recommendation from UserBased for "{i}":')
        # print(recommender.get_similar_user_movies(
        #     moviescore_df=moviescore_df,
        #     columns=['movieId', 'OcenaImdb'], k=k))
        # print(f'========================================================')

        # print(f'Recommendation from ItemBased for "{i}":')
        # print(recommender.get_similar_item_movies(
        #     moviescore_df=movielens_df,
        #     columns=['movieId', 'OcenaImdb'], k=k))
        # print(f'========================================================')

        recommender.train()
        print(f'Recommendation from SVD by similar Users "{i}":')
        print(recommender.get_recommendation_by_similar_user(
            moviescore_df=movielens_df,
            columns=['movieId', 'OcenaImdb'], k=k))

        print(f'Recommendation from SVD "{i}":')
        print(recommender.get_recommendation(
            moviescore_df=movielens_df,
            columns=['movieId', 'OcenaImdb'], k=k))