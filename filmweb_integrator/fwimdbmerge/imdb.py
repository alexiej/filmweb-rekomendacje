#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from .utils import to_list
from pathlib import Path

ROOT = str(Path(__file__).parent.parent.parent.absolute())
IMDB_MOVIES_PICLE = ROOT + '/data/imdb_movies.pkl'
IMDB_COVERS_PICLE = ROOT + '/data/imdb_covers.pkl'
IMDB_TITLE_GZIP = 'https://datasets.imdbws.com/title.basics.tsv.gz'
IMDB_RATING_GZIP = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
IMDB_COVERS_CSV = ROOT + '/data_static/movie_covers.csv'


class Imdb(object):

    def __init__(self):
        self.imdb = pd.read_pickle(IMDB_MOVIES_PICLE)

    @staticmethod
    def prepare():
        imdb_title = pd.read_csv(IMDB_TITLE_GZIP, sep='\t', dtype='str', index_col='tconst', engine='c')
        imdb_title = imdb_title[imdb_title['titleType']=='movie']
        imdb_title = imdb_title.dropna(subset=['startYear', 'originalTitle'])

        pd.merge(
            imdb_title,
            pd.read_csv(IMDB_RATING_GZIP, sep='\t', dtype='str', index_col='tconst', engine='c'),
            how='left',
            left_index=True,
            right_index=True).to_pickle(IMDB_MOVIES_PICLE)
        pd.read_csv(IMDB_COVERS_CSV).to_pickle(IMDB_COVERS_PICLE)

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
            df,
            self.imdb,
            how='inner',
            on=['startYear','originalTitle'])

        merged = self.filter_duplicates(merged)
        merged['averageRating'] = merged['averageRating'].fillna(value=0).astype(float)
        merged['diff'] = (merged['Ocena'] - merged['averageRating'])
        merged['averageRating_int'] = merged['averageRating'].round().astype(int)

        return merged

    def filter_duplicates(self, df):
        df['similarity'] = df.apply(self.get_similarity, axis=1)
        top1 = df.groupby(['ID']).apply(lambda x: x.sort_values(["similarity"], ascending = False)).reset_index(drop=True)
        return top1.groupby('ID').head(1).copy()
