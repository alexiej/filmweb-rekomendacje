from collections import defaultdict
from operator import itemgetter
# python -m movies_recommender.RecommenderSVD
import heapq
from movies_analyzer.Movies import Movies
from movies_analyzer.RecommendationDataset import RecommendationDataSet
from movies_recommender.Evaluator import get_evaluation

from movies_recommender.Recommender import Recommender, test_recommendation
from surprise import SVDpp, KNNBasic
from movies_recommender.utils import get_top_n


class RecommenderSVDppSimilarUsers(Recommender):
    """ 
        Instead of building new dataset when the new user is in, we get similar users,
        and based on that try to get similar movies
    """
    def __init__(self, recommendation_dataset):
        super(RecommenderSVDppSimilarUsers, self).__init__(recommendation_dataset)
        self.algorithm = SVDpp()

    def fit(self, dataset):
        return self.algorithm.fit(dataset)

    def test(self, test_set):
        return self.algorithm.test(test_set)

    def get_recommendation(self,
                           moviescore_df, columns, k=20, k_inner_item=5):
        # get dataset 
        full_dataset = self.algorithm.trainset
        similar_users = self.recommendation_dataset.get_similar_user_ids(moviescore_df, columns, k=k_inner_item)

        # watched movies
        watched = {full_dataset.to_inner_iid(str(int(i[0]))): i[1] for i in moviescore_df[columns].values}

        # Calculate for all similar user, predictions
        candidates = defaultdict(float)
        for inner_move_id in range(0, full_dataset.n_items):
            if inner_move_id not in watched:
                movie_id = full_dataset.to_raw_iid(inner_move_id)
                for inner_user_id, similarity in  similar_users.items():
                    prediction = self.algorithm.predict(
                            full_dataset.to_raw_uid(inner_user_id), 
                            movie_id)
                    candidates[movie_id] +=  similarity*prediction.est

        return self.movies.get_movie_by_movie_ids(heapq.nlargest(k, candidates, key = candidates.get))


if __name__ == '__main__':
    recommendation_dataset = RecommendationDataSet(movies=Movies())
    from movies_recommender.RecommenderSVDppSimilarUsers import RecommenderSVDppSimilarUsers
    recommender = RecommenderSVDppSimilarUsers(recommendation_dataset)
    test_recommendation(recommender=recommender, example_items=['arek','mateusz'], anti_test=True)

    """ For test only
    %load_ext autoreload
    %autoreload 2
    
    from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
    from filmweb_integrator.fwimdbmerge.merger import Merger, get_json_df
    from movies_recommender.Recommender import get_moviescore_df

    recommendation_dataset = RecommendationDataSet(movies=Movies())
    recommender = RecommenderSVDppSimilarUsers(recommendation_dataset)
    recommender.fit(recommender.recommendation_dataset.full_dataset)

    merger = Merger(filmweb=Filmweb(), imdb=recommender.movies.imdb)
    moviescore_df = get_moviescore_df(merger, recommender.movies,'arek')
    k = 20
    k_inner_item = 20
    columns=['movieId', 'OcenaImdb']

    self = recommender
    self.get_recommendation(moviescore_df,columns)
    """