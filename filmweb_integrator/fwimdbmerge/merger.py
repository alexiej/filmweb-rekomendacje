#!/usr/bin/env python
# coding: utf-8

from pandas.io.json import json_normalize

from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
from filmweb_integrator.fwimdbmerge.imdb import Imdb


class Merger(object):

    def __init__(self, json):
        self.df = json_normalize(json)

    def get_data(self):
        df = Filmweb(self.df).get_dataframe(True)
        return Imdb().merge(df)
