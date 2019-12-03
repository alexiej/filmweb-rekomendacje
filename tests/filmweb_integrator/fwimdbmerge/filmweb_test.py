import unittest
from pathlib import Path

import pandas as pd

from filmweb_integrator.fwimdbmerge.filmweb import Filmweb

DATA_STATIC = str(Path(__file__).parent.parent.parent.parent.absolute()) + '/data_static'


class TestFilmweb(unittest.TestCase):

    def setUp(self):
        self.sut = Filmweb()

    def test_get_dataframe_should_return_simple_dataframe(self):
        # given
        df = pd.read_csv(DATA_STATIC + '/filmweb_example.csv')

        # when
        result = self.sut.get_dataframe(df, extended=False, use_saved_scraped=True)

        # then
        self.assertEqual(9, len(result.columns))

    def test_get_dataframe_should_return_extended_dataframe(self):
        # given
        df = pd.read_csv(DATA_STATIC + '/filmweb_example.csv')

        # when
        result = self.sut.get_dataframe(df, extended=True, use_saved_scraped=True)

        # then
        self.assertEqual(58, len(result.columns))
