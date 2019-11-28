#!/usr/bin/env python
# coding: utf-8

import pickle

from pathlib import Path
from filmweb_integrator.fwimdbmerge.merger import Merger
from filmweb_integrator.fwimdbmerge.utils import get_logger

DATA_STATIC = str(Path(__file__).parent.parent.absolute()) + '/data_static'

logger = get_logger()

logger.warning("Start import csv")
dane = pickle.load(open(DATA_STATIC + '/filmweb_example.pkl', 'rb'))
logger.warning("Start merging")
df = Merger().get_data(dane)
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
