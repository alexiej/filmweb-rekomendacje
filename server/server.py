#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, render_template
import json

from filmweb_integrator.fwimdbmerge.merger import Merger
from movies_analyzer.data_provider import flow_chart_data, pie_chart_data, radar_chart_data

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')


@app.before_first_request
def initialize():
    print("Called only once, when the first request comes in")


@app.route('/')
@app.route('/ping')
def ping():
    return 'Hello world!'


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

        df = Merger(dane).get_data()

        return render_template("index.html",
                                dane=dane,
                               flow=dfi.fillna('').to_dict(),
                               radar=get_radar_data(dfi),
                               dane_gatunki = dane_gatunki)
        # return render_template("index.html", dane=dane)
    return 'BRAK DANYCH FILMÓW'
