import data_collecting
import plots
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

COMPANY = []

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    """На главной странице необходимо ввести имя компании"""
    html = render_template('index.html')

    return html


@app.route('/find_data', methods=['POST'])
def find_data():
    global COMPANY

    try:
        COMPANY = request.form['company'].upper().split()
        print(COMPANY)
    except Exception:
        return redirect('/index')

    if len(COMPANY) == 2:
        return redirect('/twin')
    if len(COMPANY) == 1:
        return redirect('/single')
    elif len(COMPANY) > 2:
        return redirect('/error')


@app.route('/twin')
def twin():
    """Отрисовка графика дл двух компаний"""
    global COMPANY

    twin_graph = 'twin_graph'

    collector = data_collecting.DataCollector()
    plot = plots.Plot()
    tables = []

    for company in COMPANY:
        try:
            collector.pull_data(company)
        except Exception:
            return redirect('/error')

        tables.append(collector.frame)

    path = plot.twin_table_plot(tables, COMPANY, twin_graph)

    html = render_template('graph.html', company=' '.join(COMPANY), img_path='static/{}'.format(path))

    return html


@app.route('/error')
def error():
    html = render_template('error.html')

    return html


@app.route('/single')
def single():
    """Отрисовка графика для одной компании"""
    global COMPANY

    prices = data_collecting.DataCollector()

    try:
        prices.pull_data(COMPANY[0])
    except Exception:
        return redirect('/error')

    plot = plots.Plot()
    try:
        path = plot.table_to_plot(prices.frame, COMPANY)
    except Exception:
        return redirect('/error')

    html = render_template('graph.html', company=COMPANY[0], img_path='static/{}'.format(path))

    return html


@app.after_request
def add_header(r):
    """ Отмена кэшировани картинок"""
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(debug=True)
