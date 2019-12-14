#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, render_template
import json

from filmweb_integrator.fwimdbmerge.merger import Merger
from movies_analyzer.data_provider import records_data, flow_chart_data, pie_chart_data, radar_chart_data, dashboard

app = Flask(__name__, template_folder='templates')


@app.before_first_request
def initialize():
    print("Called only once, when the first request comes in")


@app.route('/')
@app.route('/ping')
def ping():
    return 'Hello world!'
    


@app.route('/render', methods=['GET', 'POST'])
def render():
    if 'dane' in request.form:
        dane = json.loads(request.form['dane'])
        df = Merger(dane).get_data()

        return render_template("index.html",
                               dane = dane,
                               flow = flow_chart_data(df),
                               radar = radar_chart_data(df),
                               pie = pie_chart_data(df),
                               dsh = dashboard(df))
    return 'BRAK DANYCH FILMÓW'