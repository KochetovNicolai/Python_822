# -*- coding: utf-8 -*-
from flask import render_template
from flask import request
from flask import redirect
from app import app
from app.dl_db import Deadline
from app.form import DeadlineForm
# from django-core import template  # всякие стандартные импорты
# register=template.Library()


@app.route('/')							# определяем основной путь
@app.route('/index')
def index():							# и соответствующий ему обработчик запросов
    return render_template('index.html')


@app.route('/wrong_add')
def wrong_add():
    return render_template('wrong_add.html')


@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    # form = DeadlineForm()
    return render_template('add_form.html')


@app.route('/add_deadline', methods=['POST'])
def add_deadline():
    global _title, _details, _date, _time
    _title = request.form['title']
    _details = request.form['details']
    _date = request.form['date']
    _time = request.form['time']

    if _title and _date and _time:
        if _details:
            # new_deadline = Deadline(_title, _details, _date, _time)
            new_deadline = Deadline(_title, _details)
            Deadline.save_deadline(new_deadline)
            return render_template('index.html')
            # тут добавляем в бд все поданные на ввод значения
        else:
            # new_deadline = Deadline(_title, 'NULL', _date, _time)
            new_deadline = Deadline(_title, 'NULL')
            Deadline.save_deadline(new_deadline)
            return render_template('index.html')
            # тут добавляем в бд все поданные на ввод значения, но вместо details -- NULL
    else:
        return redirect('wrong_add')
        # переход на страницу с оповещением о некорректности ввода


@app.route('/show_new')
def show_new():
    list_of_deadlines = Deadline.get_deadlines()    # получаем лист наших дедлайнов (объектов типа Deadline)
    list_of = [1, 2, 3]
    return render_template('show_deadlines.html', cur_list=list_of)
