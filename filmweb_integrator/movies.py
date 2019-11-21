#!/usr/bin/env python
# coding: utf-8

from filmweb_integrator.fwimdbmerge import Merger
import pandas as pd
import filmweb_integrator.fwimdbmerge.filmweb as f

merger = Merger()

df = pd.read_csv('./data_static/filmweb_example.csv')
df.columns = ['ID', 'Tytuł polski', 'Tytuł oryginalny', 'Rok produkcji',
              'Ulubione', 'Ocena', 'Komentarz', 'Kraj produkcji', 'Gatunek', 'Data']


fw = f.Filmweb(df)
df = fw.get_dataframe(True)
df.to_csv('./data_static/filmweb_example_after.csv')

merger.imdb.merge(df)
## merger.imdb.merge(dff)
# # df['Gatunek']
# #df = merger.process(df)
# # df[df['Gatunek'].isna()]
# dff['Gatunek'].isna()

# dff.apply(lambda x: merger.imdb.change_type(x['Gatunek']), axis=1)
# dff.apply(lambda x: merger.imdb.change_type(x['Gatunek']), axis=1)
