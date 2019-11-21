#!/usr/bin/env python
# coding: utf-8

from .filmweb import Filmweb
from .imdb import Imdb


class Merger(object):
    def __init__(self):
        self.imdb = Imdb()

    def process(self, df, use_saved_scraped = True):
        fw = Filmweb(df)
        df = fw.get_dataframe(use_saved_scraped)
        df = self.imdb.merge(df)
        return df
