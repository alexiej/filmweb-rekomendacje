#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

from filmweb_integrator.fwimdbmerge.utils import to_list


def records_data(df):
    return sort_by_date(df, False).to_dict(orient='records')


def flow_chart_data(df):
    return sort_by_date(df).to_dict()


def pie_chart_data(df, topn=5):
    gatunki = {}
    # df["Rok"] = df["Data"].str[:4].astype(int)
    # rok_min = df["Rok"].min()
    # rok_max = df["Rok"].max()

    # we go through all rows, and all movie categories in the row
    for i,row in df.iterrows():
        for gatunek in to_list(row["Gatunek"]):
            if gatunek not in gatunki:
                gatunki[gatunek] =  {
                    'gatunek': gatunek,
                    'ilosc': 0,
                    'srednia': 0
                }
            gatunki[gatunek]['ilosc'] += 1
            gatunki[gatunek]['srednia'] +=row["Ocena"]
  
    dane = pd.DataFrame(gatunki.values())
    dane.set_index('gatunek',inplace=True)
    dane['srednia'] = dane['srednia']/dane['ilosc']

    return  dane.sort_values(by=['ilosc'],ascending=False).iloc[:topn].to_dict()


def histogram_data(df):
    oceny = df.groupby('Ocena').size().astype(int)
    return {o: ( oceny.loc[o] 
                if o in oceny else 0.0) 
                for o in range(1,11)}


def gatunki_rozszerz_dataframe(df):
    # df cotain 'tconst' index
    data =  df.copy().reset_index(drop=False)
    if "index" in data.columns:
        data.drop("index",axis=1,inplace=True)
    data["Gatunek"] = data["Gatunek"].apply(to_list)
    data = data.loc[np.repeat(
       data.index.values, 
       data["Gatunek"].apply(len))].reset_index(drop=False)
    data["subindex"] = data.groupby("index").cumcount()
    data["Gatunek"] = data.apply(lambda row: [row["Gatunek"][row["subindex"]]],axis=1, result_type="expand")
    return data



def krajkod_rozszerz_dataframe(df):
    # df cotain 'tconst' index
    data =  df.copy().reset_index(drop=False)
    if "index" in data.columns:
        data.drop("index",axis=1,inplace=True)
    data = data.loc[np.repeat(
       data.index.values, 
       data["KrajKod"].apply(len))].reset_index(drop=False)
    data["subindex"] = data.groupby("index").cumcount()
    data["KrajKod"] = data.apply(lambda row: [row["KrajKod"][row["subindex"]]],axis=1, result_type="expand")
    return data


def year_gatunek_data(df_gatunki, gatunki=[]):
    rok_min = df_gatunki["Rok"].min()
    rok_max = df_gatunki["Rok"].max()
    lata = [i for i in range(rok_min,rok_max+1)]
    lata_srednia = [ 
        {
            'name': g,
            'data': [ 
                0 if not np.any((df_gatunki["Rok"]==i) & (df_gatunki["Gatunek"]==g)) else
                df_gatunki[(df_gatunki["Rok"]==i) & (df_gatunki["Gatunek"]==g)]["Ocena"].mean().round(2) for i in lata]
        } for g in gatunki
    ]
    lata_ilosc = {
        g: {
            i:  0 if not np.any((df_gatunki["Rok"]==i) & (df_gatunki["Gatunek"]==g)) else
                len(df_gatunki[(df_gatunki["Rok"]==i) & (df_gatunki["Gatunek"]==g)]) for i in lata
        } for g in gatunki
    }
    return lata_srednia, lata_ilosc, lata

def radar_chart_data(df):
    radar = pd.DataFrame(np.zeros((10, 2)), index=range(1, 11), columns=['fw', 'imdb'])
    radar.fw = df.groupby('Ocena').size().astype(int)
    radar.imdb = df.groupby('averageRating_int').size().astype(int)
    return radar.fillna(0).to_dict()

from sklearn.preprocessing import minmax_scale


def map_data(df):
    df_krajkod = krajkod_rozszerz_dataframe(df)
    df_krajkod =  df_krajkod.groupby("KrajKod").agg({
        "Ocena": "mean",
        "tconst": "count"
    }).rename(columns={"Ocena": "ocena", "tconst": "ilosc"})
    df_krajkod["procent"] = df_krajkod["ilosc"]/sum(df_krajkod["ilosc"])
    # Logarytm powoduje ze duze wartosci takie jak USA sa zmniejszane aby podczas skalowania nie bylo za duzego odstepu miedzy wartosciami
    df_krajkod["fillKey"] = np.array(np.round(minmax_scale(np.log(df_krajkod["procent"]))*10))

    df_krajkod["fillKey"] = "N" + df_krajkod["fillKey"].astype(int).apply(str)
    
    # pd.cut(df_krajkod["procent"], bins=[0,0.1,0.2,0.3])

    return df_krajkod.to_dict(orient="index")
    

def sort_by_date(df, ascending=True):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.sort_values(by=['Data'], ascending=ascending)
    df['Data'] = df['Data'].dt.strftime('%Y-%m-%d')
    return df.reset_index()