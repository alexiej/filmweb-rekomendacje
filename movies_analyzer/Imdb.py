#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from filmweb_integrator.fwimdbmerge.utils import to_list
from pathlib import Path
import pyarrow.parquet as pq
import pyarrow as pa
from imdb import IMDb as ImdbServer
import urllib.request 
import pickle
import os.path

ROOT = str(Path(__file__).parent.parent.absolute())
# import os; ROOT = os.getcwd()
IMDB_TITLE_GZIP = 'https://datasets.imdbws.com/title.basics.tsv.gz'
IMDB_RATING_GZIP = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
IMDB_ACTORS_GZIP = 'https://datasets.imdbws.com/title.principals.tsv.gz'
IMDB_ACTORS_NAMES_GZIP = 'https://datasets.imdbws.com/name.basics.tsv.gz'

IMDB_COVERS_CSV = ROOT + '/data_static/movie_covers.csv'
IMDB_MOVIES_PARQUET = ROOT + '/data/imdb_movies.parquet.gzip'
IMDB_COVERS_PARQUET = ROOT + '/data/imdb_covers.parquet.gzip'
IMDB_ACTORS_PARQUET = ROOT + '/data/imdb_actors.parquet.gzip'


IMAGE_FOLDER = 'data/images'
DATA_FOLDER = 'data/movies'
# ecommendation_dataset.
try:
    os.mkdir(IMAGE_FOLDER)
except:
    print(IMAGE_FOLDER + ': folder exist')

try:
    os.mkdir(DATA_FOLDER)
except:
    print(DATA_FOLDER + ': folder exist')

ia = ImdbServer()


def get_imdb_movie(tmbdid: str):
    """
        return a tuple with the movie and id, and image if it's exist.
        otherwirse try to load a movie and save it

        image_file, pickle_file, movie
    """
    tmbdid = str(tmbdid).replace('tt','')

    image_file = IMAGE_FOLDER + "/"+ str(tmbdid) + '.jpg'
    pickle_file = DATA_FOLDER+"/"+tmbdid+".pkl"

    if os.path.isfile(pickle_file):
        movie = pickle.load(open(pickle_file,"rb"))
        return   tmbdid if os.path.isfile(image_file) else 'no-cover' , movie

    movie = ia.get_movie(tmbdid)
    if 'cover url' in movie:
        urllib.request.urlretrieve(movie['cover url'], image_file)
    else:
        tmbdid = 'no-cover'

    with open(pickle_file,"wb") as f:
        pickle.dump(movie,f)
    return tmbdid, movie

class Imdb(object):
    def __init__(self):
        self.imdb = pd.read_parquet(IMDB_MOVIES_PARQUET, engine='pyarrow')
        self.imdb_actors = pd.read_parquet(IMDB_ACTORS_PARQUET, engine='pyarrow')

    @staticmethod
    def prepare():
        print("Download titles....")
        imdb_title = pd.read_csv(IMDB_TITLE_GZIP, sep='\t', dtype='str', index_col='tconst', engine='c')
        imdb_title = imdb_title[imdb_title['titleType']=='movie']
        imdb_title = imdb_title.dropna(subset=['startYear', 'originalTitle'])

        print("Download ratings....")
        table = pa.Table.from_pandas(pd.merge(
            imdb_title,
            pd.read_csv(IMDB_RATING_GZIP, sep='\t', dtype='str', index_col='tconst', engine='c'),
            how='left',
            left_index=True,
            right_index=True, sort=False), preserve_index=True)
        pq.write_table(table, IMDB_MOVIES_PARQUET, compression='gzip')

        print("Download actors....")
        imdb_actors = pd.read_csv(IMDB_ACTORS_GZIP, sep='\t', dtype='str', index_col='tconst', engine='c')
        imdb_actors = imdb_actors[(imdb_actors["ordering"] == '1') & (
                    (imdb_actors["category"] == 'actor') | (imdb_actors["category"] == 'actress'))]
        imdb_actors_names = pd.read_csv(IMDB_ACTORS_NAMES_GZIP, sep='\t', dtype='str', index_col='nconst', engine='c')
        imdb_actors_with_names = imdb_actors.merge(imdb_actors_names, right_index=True, left_on="nconst")
        imdb_actors_with_names = imdb_actors_with_names[["primaryName", "characters"]]
        pa_actors = pa.Table.from_pandas(imdb_actors_with_names)
        pq.write_table(pa_actors, IMDB_ACTORS_PARQUET, compression='gzip')

        print("Download covers....")
        table = pa.Table.from_pandas(pd.read_csv(IMDB_COVERS_CSV), preserve_index=False)
        pq.write_table(table, IMDB_COVERS_PARQUET, compression='gzip')

    @staticmethod
    def get_similarity(row):
        text_list_eng = to_list(row['genre_eng'])
        text_list_genres = to_list(row['genres'])
        # product of those lists
        commons = set(text_list_eng) & set(text_list_genres)
        return len(commons)

    @staticmethod
    def change_type(t):
        match = {
            'akcja': 'action',
            'dramat': 'drama',
            'animowany': 'cartoon',
            'romans': 'romance',
            'drogi': 'road',
            'biograficzny': 'biographic',
            'romantyczny': 'romantic',
            'wojenny': 'war',
            'katastroficzny': 'disaster',
            'kryminał': 'crime',
            'komedia': 'comedy',
            'dokumentalny': 'documentary',
            'pełnometrażowy': 'full-length',
            'krótkometrażowy': 'short',
            'niemy': 'silent',
            'historyczny': 'historical',
            'edukacyjny': 'educational',
            'kostiumowy': 'costume',
            'obyczajowy': 'drama'
        }
        arr = [match[s.lower()] if s.lower() in match else s.lower() for s in to_list(t)]
        return ", ".join(arr)

    def merge(self, df):
        df['originalTitle'] = df['Tytuł oryginalny']
        df['startYear'] = df['Rok produkcji'].fillna('0').astype(str).astype(int).astype(str)
        df['originalTitle'] = df['originalTitle'].fillna(df['Tytuł polski'])
        df['Gatunek'] = df['Gatunek'].fillna('')

        df['genre_eng'] = df['Gatunek'].map(lambda x: self.change_type(x))

        merged = pd.merge(
            self.imdb.reset_index(),
            df,
            how='inner',
            on=['startYear', 'originalTitle'])

        merged = self.filter_duplicates(merged)
        merged['averageRating'] = merged['averageRating'].fillna(value=0).astype(float)
        merged['diff'] = (merged['Ocena'] - merged['averageRating'])
        merged['averageRating_int'] = merged['averageRating'].round().astype(int)
        merged.set_index('tconst', inplace=True)
        return merged

    def filter_duplicates(self, df):
        df['similarity'] = df.apply(self.get_similarity, axis=1)
        top1 = df.groupby(['ID']).apply(lambda x: x.sort_values(["similarity"], ascending = False)).reset_index(drop=True)
        return top1.groupby('ID').head(1).copy()
