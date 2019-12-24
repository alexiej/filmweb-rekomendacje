import unittest
from pathlib import Path
import json
import pandas as pd

from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
from pandas.io.json import json_normalize

DATA_STATIC = str(Path(__file__).parent.parent.parent.parent.absolute()) + '/data_static'
FILMWEB_EXAMPLE_JSON = DATA_STATIC + '/example_test_01_json.json'
FILMWEB_EXAMPLE_CSV = DATA_STATIC + '/example_test_01_json.csv'
FILMWEB_EXAMPLE_FILMWEB = DATA_STATIC + '/example_test_01_json.json'



"""
self = TestFilmweb()
self.setUp()
"""
class TestFilmweb(unittest.TestCase):

    def setUp(self):
        self.sut = Filmweb()

    def test_get_json_shuold_return_dataframe(self):
        json_text = open(FILMWEB_EXAMPLE_JSON).read()
        df = json_normalize(json.loads(json_text))
        self.assertEqual(46, len(df))

    def test_get_dataframe_should_return_simple_dataframe(self):
        # given
        df = pd.read_csv(FILMWEB_EXAMPLE_CSV)

        # when
        result = self.sut.get_dataframe(df, extended=False, use_saved_scraped=True)

        # then
        self.assertEqual(9, len(result.columns))

    def test_get_dataframe_should_return_extended_dataframe(self):
        # given
        df = pd.read_csv(FILMWEB_EXAMPLE_CSV)

        # when
        result = self.sut.get_dataframe(df, extended=True, use_saved_scraped=True)

        # then
        self.assertEqual(58, len(result.columns))
