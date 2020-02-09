from collections import defaultdict
from operator import itemgetter
# python -m movies_recommender.RecommenderSVDpp

from movies_analyzer.Movies import Movies
from movies_analyzer.RecommendationDataset import RecommendationDataSet
from movies_recommender.Recommender import Recommender
from surprise import SVDpp, KNNBasic

from movies_recommender.utils import get_top_n


class RecommenderSVDpp(Recommender):
    def __init__(self, recommendation_dataset: RecommendationDataSet):
        super(RecommenderSVDpp, self).__init__(recommendation_dataset.movies)
        self.algorithm = SVDpp()
        self.recommendation_dataset = recommendation_dataset

    def fit(self, dataset):
        return self.algorithm.fit(dataset)

    def test(self, test_set):
        return self.algorithm.test(test_set)

    def get_recommendation(self, watched, k=20):
        # get dataset 
        new_user_id, full_dataset = self.recommendation_dataset.get_dataset_with_extended_user(watched)
        inner_user_id = full_dataset.to_inner_uid(new_user_id)

        # after new dataset we need again train our model with the new user for the whole 
        # dataset with the new user.
        self.algorithm.fit(full_dataset)

        # watched movies
        watched = {full_dataset.to_inner_iid(key): value for key,value in watched.items()}

        # Calculate for all similar user, predictions
        test_items = [
            self.algorithm.predict(new_user_id, full_dataset.to_raw_iid(i))
            for i in range(0, full_dataset.n_items)
            if i not in watched
        ]

        topn_items = [i[0] for i in get_top_n(test_items, n=k, minimum_rating=1.0)[new_user_id]]
        return self.movies.get_movie_by_movie_ids(topn_items)


if __name__ == '__main__':
    from movies_recommender.Recommender import test_recommendation
    from movies_recommender.RecommenderSVDpp import RecommenderSVDpp
    from movies_analyzer.RecommendationDataset import RecommendationDataSet
    from movies_analyzer.Movies import Movies

    movies = Movies()
    recommendation_dataset = RecommendationDataSet(movies=movies)
    recommender = RecommenderSVDpp(recommendation_dataset)

    assert recommender.__module__[:len('movies_recommender.')] == 'movies_recommender.'
    test_recommendation(recommender, recommendation_dataset, 
                        example_items=['arek','mateusz'], anti_test=True)

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
