from collections import defaultdict
from operator import itemgetter
# python -m movies_recommender.RecommenderSVD

from movies_analyzer.Movies import Movies
from movies_analyzer.RecommendationDataset import RecommendationDataSet
from movies_recommender.Evaluator import get_evaluation

from movies_recommender.Recommender import Recommender, test_recommendation
from surprise import SVD

from movies_recommender.utils import get_top_n


class RecommenderSVD(Recommender):
    def __init__(self, recommendation_dataset):
        super(RecommenderSVD, self).__init__(recommendation_dataset, algorithm=SVD())

    def get_recommendation(self,
                           moviescore_df, columns, k=20):
        new_user_id, dataset = self.recommendation_dataset.get_dataset_with_extended_user(moviescore_df, columns)
        full_dataset = dataset.build_full_trainset()
        inner_user_id = full_dataset.to_inner_uid(new_user_id)

        # watched movies
        watched = {full_dataset.to_inner_iid(i): 1 for i in moviescore_df[columns[0]].values}

        # Calculate for all similar user, predictions
        test_items = self.algorithm.test([
            (inner_user_id, i, 3.5)
            for i in range(0, full_dataset.n_items)
            if i not in watched
        ])

        topn_items = [full_dataset.to_raw_iid(i[0]) for i in get_top_n(test_items, n=k, minimum_rating=1.0)[inner_user_id]]
        return self.movies.get_movie_by_movie_ids(topn_items)


if __name__ == '__main__':
    movies = Movies()
    recommendation_dataset = RecommendationDataSet(movies=movies)
    recommender = RecommenderSVD(recommendation_dataset)

    test_recommendation(recommender=recommender, example_items=['arek'])
