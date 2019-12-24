#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

from filmweb_integrator.fwimdbmerge.utils import to_list


def records_data(df):
    return sort_by_date(df, False).to_dict(orient='records')


def flow_chart_data(df):
    return sort_by_date(df).to_dict()


def pie_chart_data(df):
    genres_series = df['Gatunek'].apply(to_list)
    genres_list = pd.Series(sum([item for item in genres_series], []))
    return genres_list.value_counts().to_dict()


def radar_chart_data(df):
    radar = pd.DataFrame(np.zeros((10, 2)), index=range(1, 11), columns=['fw', 'imdb'])
    radar.fw = df.groupby('Ocena').size().astype(int)
    radar.imdb = df.groupby('averageRating_int').size().astype(int)
    return radar.fillna(0).to_dict()


def sort_by_date(df, ascending=True):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.sort_values(by=['Data'], ascending=ascending)
    df['Data'] = df['Data'].dt.strftime('%Y-%m-%d')
    return df.reset_index()