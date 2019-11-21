#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from .utils import to_list


class Imdb(object):
    def __init__(self):
        # imdb_title = pd.read_csv('https://datasets.imdbws.com/title.basics.tsv.gz', compression='gzip', sep='\t')
        # imdb_rating = pd.read_csv('https://datasets.imdbws.com/title.ratings.tsv.gz', compression='gzip', sep='\t')
        print("Init Imdb database")

        imdb_title = pd.read_csv('data/title.basics.tsv', sep='\t')
        imdb_rating = pd.read_csv('data/title.ratings.tsv', sep='\t')
        imdb_covers = pd.read_csv('data_static/movie_covers.csv')
        imdb = pd.merge(imdb_title, imdb_rating, how='left', on='tconst')
        imdb = imdb.dropna(subset=['startYear', 'originalTitle'])
        imdb = imdb[imdb['titleType']=='movie']

        # imdb_covers['tconst'] = 'tt' + imdb_covers['imdbId'].astype(str)
        # imdb = pd.merge(imdb, imdb_covers, how='left', on='tconst')

        self.imdb = imdb
        print(f"End init ({len(self.imdb)} movies)")

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
        df['startYear'] = df['Rok produkcji'].astype(str)
        df['originalTitle'] = df['originalTitle'].fillna(df['Tytuł polski'])

        df['Gatunek'] = df['Gatunek'].fillna('')
        df['startYear'] = df['startYear'].astype(float).fillna(0).astype(int).astype(str)

        df['genre_eng'] = df.apply(lambda x: self.change_type(x['Gatunek']), axis=1)

        merged = pd.merge(
            df,
            self.imdb,
            how='inner',
            on=['startYear','originalTitle'])

        merged['similarity'] = merged.apply(self.get_similarity, axis=1)

        top1 = merged.groupby(['ID']).apply(lambda x: x.sort_values(["similarity"], ascending = False)).reset_index(drop=True)
        merged = top1.groupby('ID').head(1).copy()

        merged[['averageRating']] = merged[['averageRating']].fillna(value=0)
        merged[['averageRating_int']]  = merged[['averageRating']].round().astype(int)

        return merged
