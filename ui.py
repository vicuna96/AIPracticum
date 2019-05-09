from flask import Flask, request, render_template
app = Flask(__name__)

class Path:
    def __init__(self, s, e):
        self.start = s
        self.end = e


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
        return (start, end)

@app.route('/<string:start_title>_to_<string:end_title>')
def search(start_title, end_title):
    return render_template('search.html', start=start_title, end=end_title)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
