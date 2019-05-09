# -*- coding: utf-8 -*-
from flask import render_template
from flask import request
from flask import redirect
import pymysql
from app import app


@app.route('/')							# определяем основной путь
@app.route('/index')
def index():							# и соответствующий ему обработчик запросов
    return render_template('index.html')

@app.route('/wrong_add')
def wrong_add():
	return render_template('wrong_add.html')

@app.route('/add_deadline',methods=['POST'])
def add_deadline():
	global _title, _details, _date, _time
	_title = request.form['title']
	_details = request.form['details']
	_date = request.form['date']
	_time = request.form['time']

	if _title and _date and _time:
		if _details:
			return redirect('/index')
			# тут добавляем в бд все поданные на ввод значения
		else:
			return redirect('/index')
			# тут добавляем в бд все поданные на ввод значения, но вместо details -- NULL
	else:
		return redirect('wrong_add')
		# по факту, при неверном заполнении либо должно выскочить окошко с оповещением, либо ничего не должно произойти
