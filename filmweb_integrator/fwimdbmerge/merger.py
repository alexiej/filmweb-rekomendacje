#!/usr/bin/env python
# coding: utf-8

from injectable import autowired
from pandas.io.json import json_normalize

from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
from movies_analyzer.Imdb import Imdb
import json
import pandas as pd

def get_json_df(json_text):
    return json_normalize(json.loads(json_text))


def get_json_list_df(json_text):
    return pd.DataFrame(json.loads(json_text))


class Merger(object):
    @autowired
    def __init__(self, *, filmweb: Filmweb, imdb: Imdb):
        self.filmweb = filmweb
        self.imdb = imdb

    def get_data(self, df):
        filmweb_df = self.filmweb.get_dataframe(df, False)
        return filmweb_df, self.imdb.merge(filmweb_df)
