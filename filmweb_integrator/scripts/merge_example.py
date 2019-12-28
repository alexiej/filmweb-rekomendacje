#!/usr/bin/env python
# coding: utf-8
# RUN SCRIPT: python -m filmweb_integrator.scripts.merge_example
"""
 CONVERTS EXAMPLES of files .csv file into 3 different.
"""

import os
from pathlib import Path
import pandas as pd

from filmweb_integrator.fwimdbmerge.merger import Merger, get_json_df
from filmweb_integrator.fwimdbmerge.utils import get_logger
from movies_analyzer.Movies import Movies

DATA_STATIC = Path(os.getcwd()) / 'data_static'
EXAMPLE = 'arek'
EXAMPLE_USE_JSON = True

FILMWEB_EXAMPLE_CSV = DATA_STATIC / f'./example_{EXAMPLE}_01_json.csv'
FILMWEB_EXAMPLE_JSON = DATA_STATIC / f'./example_{EXAMPLE}_01_json.json'
FILMWEB_EXAMPLE_FILMWEB = DATA_STATIC / f'./example_{EXAMPLE}_02_filmweb.csv'
FILMWEB_EXAMPLE_MERGE = DATA_STATIC / f'./example_{EXAMPLE}_03_merge.csv'
FILMWEB_EXAMPLE_MOVIELENS = DATA_STATIC / f'./example_{EXAMPLE}_04_movielens.csv'

logger = get_logger()


if EXAMPLE_USE_JSON:
    logger.warning(f"Load json file:  {DATA_STATIC}/{FILMWEB_EXAMPLE_CSV}")
    df = get_json_df(open(FILMWEB_EXAMPLE_JSON,"r").read())

    logger.warning(f"Write to csv ({len(df)})")
    df.to_csv(FILMWEB_EXAMPLE_CSV)
else:
    logger.warning(f"Load csv file:  {DATA_STATIC}/{FILMWEB_EXAMPLE_CSV}")
    df = pd.read_csv(FILMWEB_EXAMPLE_CSV)

    logger.warning(f"Write to json ({len(df)})")
    with open(FILMWEB_EXAMPLE_JSON, "w") as file_wr:
        df.to_json(file_wr, orient='records')


logger.warning("Start merging")
movies = Movies()
merger = Merger(imdb=movies.imdb)
filmweb_df, merge_df = merger.get_data(df)

logger.warning(f"Save merge.csv Filmweb({len(filmweb_df)}) -> IMDB({len(merge_df)})")
filmweb_df.to_csv(FILMWEB_EXAMPLE_FILMWEB, index=False)
merge_df.to_csv(FILMWEB_EXAMPLE_MERGE, index=True)

movielens_df = movies.merge_imdb_movielens(merge_df)
logger.warning(f"Save movielens merge IMDB({len(merge_df)}) -> MOVIELENS({len(movielens_df)})")
movielens_df.to_csv(FILMWEB_EXAMPLE_MOVIELENS, index=True)

logger.warning(f"Print data ({len(movielens_df)})")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
print(movielens_df.head())
