from flask import Flask, request, render_template, redirect, url_for
from game import *


app = Flask(__name__)
id_attrib_dict, tfidf, tfs, id_to_row, title_to_id = init_game()

class Path:
    def __init__(self, s, e):
        self.start = s
        self.end = e


@app.route('/<string:start_title>_to_<string:end_title>')
def search(start_title, end_title):
    start_id = title_to_id[start_title]
    end_id = title_to_id[end_title]
    lineage = priority_beam_search(start_id, end_id, 10, dummy_sim)
    return render_template('search.html',
                            start=start_title, end=end_title, lineage=lineage)


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
        return redirect(url_for('search', start_title=start, end_title=end))
        #return render_template('search.html', start=start, end=end)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
