#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, render_template
from pathlib import Path
import pickle
import os

from filmweb_integrator.fwimdbmerge.utils import get_logger
from filmweb_integrator.fwimdbmerge.merger import Merger, get_json_df
from movies_analyzer.data_provider import records_data, flow_chart_data, pie_chart_data, radar_chart_data

ROOT = Path(os.getcwd()) / 'data_static'
JSON_EXAMPLE = ROOT/'example_last_01_json.json'
FILMWEB_EXAMPLE = ROOT/'example_last_02_filmweb.csv'
MERGE_EXAMPLE = ROOT/'example_last_03_merge.csv'

JSON_GET = JSON_EXAMPLE


def debug_dump(json_text, filmweb_df, df):
    if app.debug:
        with open(JSON_EXAMPLE, "w") as text_file:
            text_file.write(json_text)
        filmweb_df.to_csv(FILMWEB_EXAMPLE,index=False)
        df.to_csv(MERGE_EXAMPLE,index=False)


logger = get_logger()
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
    json_text = None
    if app.debug and request.method == 'GET':
        logger.warn(f"DEBUG MODE using file {JSON_GET}")
        json_text = open(JSON_GET, "r").read()

    else:
        if 'dane' in request.form:
            json_text = request.form['dane']

    if json_text is not None:
        filmweb_df, df = Merger().get_data(get_json_df(json_text))
        debug_dump(json_text, filmweb_df, df)

        return render_template("index.html",
                               dane=records_data(df),
                               flow=flow_chart_data(df),
                               radar=radar_chart_data(df),
                               pie=pie_chart_data(df))

    return 'BRAK DANYCH FILMÓW'
