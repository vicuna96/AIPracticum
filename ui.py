from flask import Flask, request, render_template, redirect, url_for
import os
from game import *

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')


app = Flask(__name__)

class Path:
    def __init__(self, s, e):
        self.start = s
        self.end = e


@app.route('/<string:start_title>_to_<string:end_title>', methods = ['POST', 'GET'])
def search(start_title, end_title):
    if request.method == 'GET':
        try:
            start_id = title_to_id[start_title]
            end_id = title_to_id[end_title]
        except:
            start_id = random_id_generator(id_attrib_dict)
            end_id = random_id_generator(id_attrib_dict)
        lineage = priority_beam_search(start_id, end_id, 10, dummy_sim)
        return render_template('search.html',
                                start=start_title, end=end_title, lineage=lineage)
    if request.method == 'POST':
        return redirect(url_for('add'))


@app.route('/', methods = ["POST", "GET"])
def add():
    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        result = request.form #dictionary
        for key, value in result.items():
            if key == 'start':
                start = value
            if key == 'end':
                end = value
        if start == "":
            start = "Wikipedia"
        if end == "":
            end = "Game"
        return redirect(url_for('search', start_title=start, end_title=end))

# Code below taken from http://flask.pocoo.org/snippets/40/
# Necessary since css file was not updating properly
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
# Code above taken from http://flask.pocoo.org/snippets/40/

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
