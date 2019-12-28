from pathlib import Path
from movies_analyzer.Imdb import Imdb
import pandas as pd
from surprise import Dataset, KNNBasic
from surprise import Reader

SMALL_MOVIELENS = 'data/ml-latest-small/'

RATINGS = 'ratings.csv'
LINKS = 'links.csv'
MOVIES = 'movies.csv'


class Movies(object):
    def __init__(self, movielens_path=SMALL_MOVIELENS):
        self.imdb = Imdb()
        self.movielens_path = Path(movielens_path)

        links = pd.read_csv(self.movielens_path/LINKS, dtype=str)
        links['imdbId'] = 'tt' + links['imdbId'].astype(str)
        links['link'] = 'https://www.imdb.com/title/' + links['imdbId'] + '/'

        movies = pd.read_csv(self.movielens_path/LINKS, dtype=str,
                             names=['movieId', 'ml_title', 'ml_genres'])

        data = pd.merge(
            links,
            movies,
            how='left',
            left_on='movieId',
            right_on='movieId', sort=False)

        data['movieId'] = data['movieId'].astype(int)

        data.set_index('imdbId', inplace=True)

        self.data = pd.merge(
            self.imdb.imdb,
            data,
            how='inner',
            left_index=True,
            right_index=True, sort=False)

    def merge_imdb_movielens(self, merge_df):
        return pd.merge(self.data,
                        merge_df[[c for c in merge_df.columns if c not in self.data.columns]],
                        how='inner',
                        left_index=True, right_index=True)

    def get_movie(self, imdb_id):
        return self.data.loc[imdb_id]

    def get_movie_by_movie_id(self, movie_id):
        return self.data[self.data['movieId'] == movie_id].iloc[0]

    def get_movie_by_movie_ids(self, movie_ids):
        return self.data[self.data['movieId'].isin(movie_ids)]

    def to_imdb_id(self, movie_id: int):
        return self.get_movie_by_movie_id(movie_id).name

    def to_movie_id(self, imdb_id: str):
        return int(self.data.loc[imdb_id]['movieId'])
