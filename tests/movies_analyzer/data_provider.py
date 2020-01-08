import unittest
from pathlib import Path
import json
import pandas as pd
import numpy as np
# from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
# from pandas.io.json import json_normalize
from movies_analyzer.data_provider import gatunki_rozszerz_dataframe,map_data, records_data,pie_chart_data,histogram_data
from filmweb_integrator.fwimdbmerge.utils import read_file
DATA_STATIC = str(Path(__file__).parent.parent.parent.absolute()) + '/data_static'
FILMWEB_EXAMPLE_MERGE_TEST = DATA_STATIC + '/example_test_03_merge.csv'
FILMWEB_EXAMPLE_MERGE_AREK = DATA_STATIC + '/example_arek_03_merge.csv'


FILMWEB_EXAMPLE_JSON_AREK = DATA_STATIC + '/example_arek_01_json.json'

from filmweb_integrator.fwimdbmerge.merger import Merger, get_json_df


def get_json_merge_df(filename):
    # filename = FILMWEB_EXAMPLE_JSON_AREK
    merger = Merger()
    json_text = read_file(filename)
    filmweb_df, df = merger.get_data(df=get_json_df(json_text))
    return filmweb_df, df


"""
self = TestDataProvider()
self.setUp()
"""
class TestDataProvider(unittest.TestCase):
    def setUp(self):
        pass
        # self.sut = Filmweb()

    def test_records_data(self):
        # given
        df = pd.read_csv(FILMWEB_EXAMPLE_MERGE_TEST)

        # when
        result = records_data(df)

        # then
        self.assertEqual(29, len(result))
        self.assertEqual(list, type(result))
        self.assertEqual(dict, type(result[0]))
        
        columns = [ 'tconst', 
        'Tytuł polski', 
        'Tytuł oryginalny',
         'Rok produkcji', 
         'Ulubione', 
         'Ocena', 
         'Kraj produkcji', 
         'Gatunek', 
         'Data', 
         'originalTitle', 
         'startYear', 
         'genre_eng', 
         'titleType', 
         'primaryTitle', 
         'isAdult',
          'endYear', 
          'runtimeMinutes', 
          'genres', 
          'averageRating',
           'numVotes', 
           'similarity', 
           'diff', 
           'averageRating_int']

        # columns in result[0].keys()
        for c in columns:
            self.assertIn(c,result[0].keys())


    def test_pie_chart_data(self):
        # given
        df = pd.read_csv(FILMWEB_EXAMPLE_MERGE_TEST)

        # when
        result = pie_chart_data(df, topn=5)

        self.assertEqual(list(result.keys()),['ilosc','srednia'])
        self.assertEqual(len(result['ilosc']), 5)
        self.assertEqual(result['ilosc']['Sci-Fi'], 6)
        self.assertEqual(result['srednia']['Sci-Fi'], 8.0)
        

    def test_histogram_data(self):
        # given
        df = pd.read_csv(FILMWEB_EXAMPLE_MERGE_TEST)

        # when
        result = histogram_data(df)

        self.assertEqual(list(result.keys()),list(range(1,11)))
        self.assertEqual(result[5],3)


    def test_gatunki_historia(self):
        # given
        filmweb_df, df = get_json_merge_df(FILMWEB_EXAMPLE_JSON_AREK)

        # when
        pie_chart = pie_chart_data(df, topn=5)

        df_gatunki = gatunki_rozszerz_dataframe(df)
        gatunki = list(pie_chart['ilosc'].keys())

        lata_srednia,lata_ilosc, lata = year_gatunek_data(df_gatunki,gatunki)

        self.assertEqual(type(lata_srednia), list)
        self.assertEqual(type(lata_srednia[0]), dict)
        self.assertTrue(
            np.isin(list(lata_srednia[0].keys()),["name", "data"]).all()
        )

    def test_map(self):
        # given
        filmweb_df, df = get_json_merge_df(FILMWEB_EXAMPLE_JSON_AREK)

        df_mapa = map_data(df)
        self.assertEqual(type(df_mapa), dict)
        first_element = df_mapa[list(df_mapa.keys())[0]];
        self.assertEqual(type(first_element), dict)
        self.assertTrue(
            np.isin(list(first_element.keys()),["ocena", "ilosc"]).all()
        )
        self.assertTrue(
            "USA" in df_mapa.keys()
        )

