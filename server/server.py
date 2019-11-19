from flask import Flask, escape, request, render_template, jsonify
import json
app = Flask(__name__, template_folder='templates')


# @app.route('/')
# def hello():
#     name = request.args.get("name", "World")
#     c


# PEOPLE_FOLDER = os.path.join('static', 'people_photo')

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


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
        return render_template("index.html", dane = dane)
    return 'BRAK DANYCH FILMÓW'