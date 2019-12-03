#!/usr/bin/env python
# coding: utf-8

from injectable import autowired
from pandas.io.json import json_normalize

from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
from filmweb_integrator.fwimdbmerge.imdb import Imdb


class Merger(object):

    @autowired
    def __init__(self, *, filmweb: Filmweb, imdb: Imdb):
        self.filmweb = filmweb
        self.imdb = imdb

    def get_data(self, json):
        df = json_normalize(json)
        df = self.filmweb.get_dataframe(df, False)
        return self.imdb.merge(df)
