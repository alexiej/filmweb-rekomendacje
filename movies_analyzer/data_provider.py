#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np


def records_data(df):
    return df.fillna('').to_dict(orient='records')


def flow_chart_data(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.fillna('').sort_values(by=['Data'])
    df['Data'] = df['Data'].dt.strftime('%Y-%m-%d')
    return df.reset_index().to_dict()


def pie_chart_data(df):
    return df.loc[:,'akcja':'western'].sum().to_dict()


def radar_chart_data(df):
    radar = pd.DataFrame(np.zeros((10,2)), index=range(1, 11), columns=['fw', 'imdb'])
    radar.fw = df.groupby('Ocena').size().astype(int)
    radar.imdb = df.groupby('averageRating_int').size().astype(int)
    return radar.fillna(0).to_dict()
