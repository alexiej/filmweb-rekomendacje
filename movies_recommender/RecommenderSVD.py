from collections import defaultdict
from operator import itemgetter
# python -m movies_recommender.RecommenderSVD

from movies_analyzer.Movies import Movies
from movies_analyzer.RecommendationDataset import RecommendationDataSet
from movies_recommender.Evaluator import get_evaluation

from movies_recommender.Recommender import Recommender, test_recommendation
from surprise import SVD, KNNBasic

from movies_recommender.utils import get_top_n


class RecommenderSVD(Recommender):
    def __init__(self, recommendation_dataset):
        super(RecommenderSVD, self).__init__(recommendation_dataset)
        self.algorithm = SVD()

    def fit(self, dataset):
        return self.algorithm.fit(dataset)

    def test(self, test_set):
        return self.algorithm.test(test_set)

    def get_recommendation(self,
                           moviescore_df, columns, k=20):
        # get dataset 
        new_user_id, dataset = self.recommendation_dataset.get_dataset_with_extended_user(moviescore_df, columns)
        full_dataset = dataset.build_full_trainset()
        inner_user_id = full_dataset.to_inner_uid(new_user_id)

        # after new dataset we need again train our model with the new user for the whole 
        # dataset with the new user.
        self.algorithm.fit(full_dataset)

        # watched movies
        watched = {full_dataset.to_inner_iid(int(i[0])): i[1] for i in moviescore_df[columns].values}

        # Calculate for all similar user, predictions
        test_items = [
            self.algorithm.predict(new_user_id, full_dataset.to_raw_iid(i))
            for i in range(0, full_dataset.n_items)
            if i not in watched
        ]

        topn_items = [i[0] for i in get_top_n(test_items, n=k, minimum_rating=1.0)[new_user_id]]
        return self.movies.get_movie_by_movie_ids(topn_items)


if __name__ == '__main__':
    recommendation_dataset = RecommendationDataSet(movies=Movies())
    from movies_recommender.RecommenderSVD import RecommenderSVD
    recommender = RecommenderSVD(recommendation_dataset)
    assert recommender.__module__[:len('movies_recommender.')] == 'movies_recommender.'

    test_recommendation(recommender=recommender, example_items=['arek','mateusz'], anti_test=True)


    """ For test only
    %load_ext autoreload
    %autoreload 2
    
    from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
    from filmweb_integrator.fwimdbmerge.merger import Merger, get_json_df
    from movies_recommender.Recommender import get_moviescore_df

    recommendation_dataset = RecommendationDataSet(movies=Movies())
    recommender = RecommenderSVD(recommendation_dataset)
    recommender.fit(recommender.recommendation_dataset.full_dataset)
    self = recommender

    # get recommendation for one user
    merger = Merger(filmweb=Filmweb(), imdb=recommender.movies.imdb)
    moviescore_df = get_moviescore_df(merger, recommender.movies,'arek')
    k = 20
    k_inner_item = 20
    columns=['movieId', 'OcenaImdb']


    self.get_recommendation(moviescore_df,columns)
    """
