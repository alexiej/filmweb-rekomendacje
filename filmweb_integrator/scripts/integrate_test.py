#!/usr/bin/env python
# coding: utf-8
# RUN SCRIPT: python -m filmweb_integrator.scripts.integrate_test

import pickle
import os
from pathlib import Path
import pandas as pd

from filmweb_integrator.fwimdbmerge.merger import Merger, get_json_df
from filmweb_integrator.fwimdbmerge.utils import get_logger

DATA_STATIC = Path(os.getcwd()) / 'data_static'
FILMWEB_EXAMPLE_CSV = DATA_STATIC / './example_test_01_json.csv'
FILMWEB_EXAMPLE_JSON = DATA_STATIC / './example_test_01_json.json'
FILMWEB_EXAMPLE_FILMWEB = DATA_STATIC / './example_test_02_filmweb.csv'
FILMWEB_EXAMPLE_MERGE = DATA_STATIC / './example_test_03_merge.csv'

logger = get_logger()

logger.warning(f"Load csv file:  {DATA_STATIC}/{FILMWEB_EXAMPLE_CSV}")
df = pd.read_csv(FILMWEB_EXAMPLE_CSV)

logger.warning("Write to json")
with open(FILMWEB_EXAMPLE_JSON, "w") as file_wr:
    df.to_json(file_wr, orient='records')

logger.warning("Start merging")
filmweb_df, df = Merger().get_data(df)

logger.warning("Save final.csv")
filmweb_df.to_csv(FILMWEB_EXAMPLE_FILMWEB, index=False)
df.to_csv(FILMWEB_EXAMPLE_MERGE, index=False)

logger.warning("Print data")
print(df.head())
