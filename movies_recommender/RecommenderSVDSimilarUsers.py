from collections import defaultdict
import heapq
from movies_analyzer.Movies import Movies
from movies_analyzer.RecommendationDataset import RecommendationDataSet
from movies_recommender.Recommender import Recommender
from surprise import SVD

class RecommenderSVDSimilarUsers(Recommender):
    """ 
        Instead of building new dataset when the new user is in, we get similar users,
        and based on that try to get similar movies
    """
    def __init__(self, movies):
        super(RecommenderSVDSimilarUsers, self).__init__(movies)
        self.algorithm = SVD()

    def fit(self, dataset):
        return self.algorithm.fit(dataset)

    def test(self, test_set):
        return self.algorithm.test(test_set)

    def get_recommendation(self, watched,  k=20, k_inner_item=5):
        # get dataset 
        full_dataset = self.algorithm.trainset

        # watched movies
        watched = {full_dataset.to_inner_iid(key): value for key,value in watched.items()}

        # get similar users
        similar_users = self.get_similar_user_ids(watched, k=k_inner_item)

        # Calculate for all similar user, predictions
        candidates = defaultdict(float)
        for inner_move_id in range(0, full_dataset.n_items):
            if inner_move_id not in watched:
                movie_id = full_dataset.to_raw_iid(inner_move_id)
                for inner_user_id, similarity in  similar_users.items():
                    prediction = self.algorithm.estimate(inner_user_id,inner_move_id)
                    candidates[movie_id] +=  similarity*prediction

        # heapq.nlargest(k, candidates.items(), key=itemgetter(1))
        return self.movies.get_movie_by_movie_ids(heapq.nlargest(k, candidates, key = candidates.get))


if __name__ == '__main__':
    from movies_recommender.RecommenderSVDSimilarUsers import RecommenderSVDSimilarUsers
    from movies_recommender.Recommender import test_recommendation
    from movies_analyzer.RecommendationDataset import RecommendationDataSet
    from movies_analyzer.Movies import Movies

    movies = Movies()
    recommendation_dataset = RecommendationDataSet(movies=movies)
    recommender = RecommenderSVDSimilarUsers(movies)

    assert recommender.__module__[:len('movies_recommender.')] == 'movies_recommender.'
    test_recommendation(recommender, recommendation_dataset, 
                        example_items=['arek','mateusz'], anti_test=True)

    """ For test only
    %load_ext autoreload
    %autoreload 2
    
    from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
    from filmweb_integrator.fwimdbmerge.merger import Merger, get_json_df
    from movies_recommender.Recommender import get_moviescore_df, get_watched
    from movies_recommender.utils import getsize

    recommender.fit(recommendation_dataset.full_dataset)
    self = recommender

    # get recommendation for one user
    merger = Merger(filmweb=Filmweb(), imdb=movies.imdb)
    watched = get_watched(get_moviescore_df(merger, recommender.movies,'arek'))
    k = 20
    k_inner_item = 20

    self.get_recommendation(watched)
    """