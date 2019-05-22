import data_collecting
import plots
import errors
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from urllib.parse import urlencode
from urllib.parse import urljoin

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    """На главной странице необходимо ввести имя компании"""
    html = render_template('index.html')

    return html


@app.route('/find_data', methods=['POST'])
def find_data():
    company = []

    try:
        company = request.form['company'].upper().split()
        print(company)
    except Exception:
        return redirect('/index')

    if len(company) == 2:
        query = {'first': company[0], 'second': company[1]}
        return redirect('/twin/?' + urlencode(query))
    if len(company) == 1:
        query = {'company': company[0]}
        return redirect('/single/?' + urlencode(query))
    elif len(company) > 2:
        return errors.error_redirect(1)


@app.route('/twin/')
def twin():
    """Отрисовка графика дл двух компаний"""
    companies = list()
    companies.append(request.args.get('first'))
    companies.append(request.args.get('second'))

    twin_graph = 'twin_graph'

    print(companies)

    collector = data_collecting.DataCollector()
    plot = plots.Plot()
    tables = []

    for company in companies:
        try:
            collector.pull_data(company)
        except Exception:
            return errors.error_redirect(2)

        tables.append(collector.frame)

    path = urljoin('/static/', plot.twin_table_plot(tables, companies, twin_graph))

    html = render_template('graph.html', company=' '.join(companies), img_path=path)

    return html


@app.route('/error/')
def error():
    error_type = request.args.get('type')

    if error_type == '2':
        message = 'You have inserted the wrong company name('
    elif error_type == '3':
        message = 'Unable to draw a plot('
    elif error_type == '1':
        message = 'You have inserted too much companies'
    else:
        message = 'Unknown error!'

    html = render_template('error.html', message=message)

    return html


@app.route('/single/')
def single():
    """Отрисовка графика для одной компании"""
    company = request.args.get('company')

    prices = data_collecting.DataCollector()

    print(company)

    try:
        prices.pull_data(company)
    except Exception:
        return errors.error_redirect(2)

    plot = plots.Plot()

    try:
        path = urljoin('/static/', plot.table_to_plot(prices.frame, company))
    except Exception:
        return errors.error_redirect(3)

    html = render_template('graph.html', company=company, img_path=path)

    return html


@app.after_request
def add_header(r):
    """Отмена кэшировани картинок"""
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(debug=True)
