from flask import Flask, escape, request, render_template, jsonify
import json

from filmweb_integrator.fwimdbmerge.filmweb import Filmweb
from filmweb_integrator.fwimdbmerge.imdb import Imdb

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

from pandas.io.json import json_normalize

import pandas as pd
import numpy as np

@app.before_first_request
def initialize():
    # global merger
    # merger = Merger()
    print("Called only once, when the first request comes in")


@app.route('/')
@app.route('/ping')
def ping():
    # age = request.args['age']
    # print(age)
    # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'shovon.jpg')
    return f'Hello world!'


@app.route('/render', methods=['GET', 'POST'])
def render():
    keys = list(request.form.keys())
    # print(keys)
    if 'dane' in keys:
        dane_string = request.form['dane']
        dane = json.loads(dane_string)
        df = json_normalize(dane)

        # df = pd.read_csv("data_static/filmweb_example.csv")
        # df =  df.drop(['Unnamed: 0'], axis=1)
        df.columns = ['ID', 'Tytuł polski', 'Tytuł oryginalny', 'Rok produkcji',
                       'Ulubione', 'Ocena', 'Komentarz', 'Kraj produkcji', 'Gatunek', 'Data']
        # df.to_csv('filmweb_example.csv', index=False)#

        dfi = Filmweb(df).get_dataframe(True)
        dfi = Imdb().merge(dfi)

        dane_gatunki = dfi.loc[:,'akcja':'western'].sum().to_dict()

        return render_template("index.html",
                                dane=dane,
                               flow=dfi.fillna('').to_dict(),
                               radar=get_radar_data(dfi),
                               dane_gatunki = dane_gatunki)
        # return render_template("index.html", dane=dane)
    return 'BRAK DANYCH FILMÓW'


def get_radar_data(df):
    radar = pd.DataFrame(np.zeros((10,2)), index=range(1, 11), columns=['fw', 'imdb'])
    radar.fw = df.groupby('Ocena').size().astype(int)
    radar.imdb = df.groupby('averageRating_int').size().astype(int)
    return radar.fillna(0).to_dict()