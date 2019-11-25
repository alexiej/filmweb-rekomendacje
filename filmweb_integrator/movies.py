#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from pathlib import Path

from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
from filmweb_integrator.fwimdbmerge.imdb import Imdb
from filmweb_integrator.fwimdbmerge.utils import get_logger

DATA_STATIC = str(Path(__file__).parent.parent.absolute()) + '/data_static'

logger = get_logger()

logger.warning("Start import csv")
df = pd.read_csv(DATA_STATIC + '/oceny.csv')
df.columns = ['ID', 'Tytuł polski', 'Tytuł oryginalny', 'Rok produkcji',
              'Ulubione', 'Ocena', 'Komentarz', 'Kraj produkcji', 'Gatunek', 'Data']

logger.warning("Start getting dataframe")
df = Filmweb(df).get_dataframe(True)
logger.warning("Save after.csv")
df.to_csv(DATA_STATIC + '/filmweb_example_after.csv')
logger.warning("Start imdb")
imdb = Imdb()
logger.warning("Start imdb merge")
df = imdb.merge(df)
logger.warning("Save final.csv")
df.to_csv(DATA_STATIC + '/filmweb_example_final.csv')
logger.warning("Print data")

print(df.head())
## merger.imdb.merge(dff)
# # df['Gatunek']
# #df = merger.process(df)
# # df[df['Gatunek'].isna()]
# dff['Gatunek'].isna()

# dff.apply(lambda x: merger.imdb.change_type(x['Gatunek']), axis=1)
# dff.apply(lambda x: merger.imdb.change_type(x['Gatunek']), axis=1)
