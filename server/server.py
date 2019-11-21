from flask import Flask, escape, request, render_template, jsonify
import json

app = Flask(__name__, template_folder='templates')

from filmweb_integrator.fwimdbmerge import Merger
from pandas.io.json import json_normalize

merger = Merger()
import pandas as pd


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
    print(keys)
    if 'dane' in keys:
        dane_string = request.form['dane']
        # print('Dane length: ', dane)
        dane = json.loads(dane_string)
        df = json_normalize(dane)
        # df = pd.read_csv("filmweb_example.csv", index=False)
        # df =  df.drop(['Unnamed: 0'], axis=1)
        df.columns = ['ID', 'Tytuł polski', 'Tytuł oryginalny', 'Rok produkcji',
                      'Ulubione', 'Ocena', 'Komentarz', 'Kraj produkcji', 'Gatunek', 'Data']
        # df.to_csv('filmweb_example.csv', index=False)#
        dfi = merger.process(df)

        dane_gatunki = dfi[['akcja', 'animacja',
       'anime', 'biograficzny', 'czarnakomedia', 'dladzieci', 'dokumentalny',
       'dramat', 'dramatobyczajowy', 'familijny', 'fantasy', 'gangsterski',
       'horror', 'komedia', 'komediakryminalna', 'komediarom.', 'kostiumowy',
       'kryminał', 'melodramat', 'musical', 'muzyczny', 'obyczajowy',
       'przygodowy', 'romans', 'sci-fi', 'sensacyjny', 'szpiegowski',
       'thriller', 'western']].sum().to_dict()


        # print(dfi.columns)
        # print(dfi.iloc[0])
        return render_template("index.html", dane=dfi.to_dict(orient='records'),
                               dane_gatunki = dane_gatunki)
        # return render_template("index.html", dane=dane)
    return 'BRAK DANYCH FILMÓW'
