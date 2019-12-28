#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from filmweb_integrator.fwapi.film import Film
from .utils import to_list
from pathlib import Path
from datetime import datetime

FILMWEB_DATA_MAPPING = {'id':'ID', 'tytułpolski':'Tytuł polski', 'tytułoryginalny':'Tytuł oryginalny',
                        'rokprodukcji':'Rok produkcji', 'ulubione':'Ulubione', 'ocena':'Ocena',
                        'komentarz': 'Komentarz', 'krajprodukcji':'Kraj produkcji', 'gatunek':'Gatunek', 'data':'Data'}

ROOT = str(Path(__file__).parent.parent.parent.absolute().resolve())


class Filmweb(object):

    def get_dataframe(self, df, extended=False, use_saved_scraped=True):
        df = df.rename(columns=FILMWEB_DATA_MAPPING)
        df = df.drop(columns=['Komentarz'])
        df = df[df.Ocena != 'brak oceny']
        df.fillna('', inplace=True)

        df['Ulubione'] = self._label_encode(df.Ulubione.fillna(''))
        df['Ocena'] = df.Ocena.astype(int)
        df['OcenaImdb'] = df.Ocena.astype(float)/2

        # df['DataRaw'] = df['Data']
        # df['Data'] = pd.to_datetime(df['Data'])

        df = df.reset_index(drop=True)

        if extended:
            return self._with_analytics(df, use_saved_scraped)

        return df

    def _with_analytics(self, df, use_saved_scraped):
        df = pd.concat([
            df,
            self._dummies(df['Gatunek'].fillna('')),
            self._dummies(df['Kraj produkcji'].fillna('')),
            self._get_scrapped(df, use_saved_scraped)], axis=1)

        df['group'] = self._make_groups(df)
        df['budget'] = self._fill_mean(df, 'budget')
        df['boxoffice'] = self._fill_mean(df, 'boxoffice')

        return df.drop(columns=['group'])

    def _get_scrapped(self, df, use_saved_scraped):
        if not use_saved_scraped:
            # warning - takes long time (a lot filmweb api calls)
            new_columns = ['budget', 'boxoffice', 'topics_count']

            scrapped = pd.DataFrame(columns=new_columns)
            scrapped[new_columns] = df.apply(lambda x: self._movie_info(int(x.ID)), axis=1, result_type='expand')
            scrapped[new_columns] = scrapped[new_columns].apply(lambda x: x.fillna(x.mean()), axis=0).astype(int)
            return scrapped
        else:
            return pd.read_csv(ROOT + '/data_static/oceny_scraped.csv')

    @staticmethod
    def _dummies(series):
        data = pd.get_dummies(series.apply(to_list).apply(pd.Series).stack()).sum(level=0)
        return data

    @staticmethod
    def _label_encode(series):
        encoder = LabelEncoder()
        encoder.fit(series)
        return encoder.transform(series)

    @staticmethod
    def _movie_info(id):
        try:
            film = Film.get_by_id(id)
            film.populate()
            return film.budget, film.boxoffice, film.topics_count
        except Exception:
            return None, None, None

    @staticmethod
    def _make_groups(df):
        minidf = df.drop(
            columns=['budget', 'boxoffice', 'ID', 'Gatunek', 'Kraj produkcji', 'Tytuł polski', 'Tytuł oryginalny', 'Data',
                     'Ulubione', 'Rok produkcji'])
        minidf = minidf.fillna(0)
        kmeans = KMeans(n_jobs=-1, n_clusters=5)
        kmeans.fit(minidf)
        return kmeans.predict(minidf)

    @staticmethod
    def _fill_mean(df, column):
        return df.groupby('group')[column].apply(lambda x: x.fillna(x.mean())).astype(int)
