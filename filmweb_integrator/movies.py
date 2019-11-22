#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from pathlib import Path
from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
from filmweb_integrator.fwimdbmerge.imdb import Imdb

DATA_STATIC = str(Path(__file__).parent.parent.absolute()) + '/data_static'

df = pd.read_csv(DATA_STATIC + '/filmweb_example.csv')
df.columns = ['ID', 'Tytuł polski', 'Tytuł oryginalny', 'Rok produkcji',
              'Ulubione', 'Ocena', 'Komentarz', 'Kraj produkcji', 'Gatunek', 'Data']

df = Filmweb(df).get_dataframe(True)
df.to_csv(DATA_STATIC + '/filmweb_example_after.csv')
df = Imdb().merge(df)
df.to_csv(DATA_STATIC + '/filmweb_example_final.csv')

print(df.head())
## merger.imdb.merge(dff)
# # df['Gatunek']
# #df = merger.process(df)
# # df[df['Gatunek'].isna()]
# dff['Gatunek'].isna()

# dff.apply(lambda x: merger.imdb.change_type(x['Gatunek']), axis=1)
# dff.apply(lambda x: merger.imdb.change_type(x['Gatunek']), axis=1)
